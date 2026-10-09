"""tools.py - STUDENT IMPLEMENTS.  Source tools for the research agents.   Guide: GUIDE.md, part 1.

Rules for every tool:
  * runs on the HOST (not in the sandbox): API keys must never enter the sandbox;
  * returns a STRING (JSON text of compact records) and NEVER raises:
        "NO RESULTS"  when the source answers with nothing,
        "ERROR: ..."  when the source keeps failing after the retries (the agent then tries another source);
  * the docstring is the tool description the LLM reads: keep it precise (what it does, what it returns, when to use it).
Try your tools without any agent:   python tools.py
"""
import json  # noqa: F401
import os  # noqa: F401
import time  # noqa: F401
import random
import re
import threading
from html.parser import HTMLParser
from io import BytesIO
import xml.etree.ElementTree  # noqa: F401  (arXiv answers with Atom XML)

import httpx  # noqa: F401
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

# ---- constants (given) ----
ARXIV_URL = "https://export.arxiv.org/api/query"  # https only: http answers 301
HF_DAILY_URL = "https://huggingface.co/api/daily_papers"
HF_SEARCH_URL = "https://huggingface.co/api/papers/search"
EXA_URL = "https://mcp.exa.ai/mcp"


class RetryableError(Exception):
    """Given. Raise it inside a call to ask with_retry to wait and try again (retry_after in seconds, optional)."""

    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


# ---- TODO 1: retry helper ----
def with_retry(fn, *, attempts=5, base=1.0, cap=30.0):
    """Call fn(); when it raises RetryableError, wait and call it again.

    PSEUDO-CODE:
      for attempt in 0 .. attempts-1:
          try: return fn()
          except RetryableError as e:
              if this was the last attempt: raise
              delay = e.retry_after if the server told us, else exponential backoff base * 2**attempt
              cap the delay at `cap` seconds; add random jitter to the exponential case
              sleep(delay)
    Use it to wrap EVERY network call below. Also treat these as retryable: HTTP 429/500/502/503/504,
    httpx.TransportError (timeouts, connection resets). Read the Retry-After header when present.
    """
    if attempts < 1:
        raise ValueError("attempts must be at least one")
    for attempt in range(attempts):
        try:
            return fn()
        except RetryableError as exc:
            if attempt == attempts - 1:
                raise
            if exc.retry_after is not None:
                delay = min(cap, max(0.0, float(exc.retry_after)))
            else:
                delay = min(cap, base * 2 ** attempt + random.uniform(0, base))
            time.sleep(delay)


def _request(method, url, **kwargs):
    """A single attempt; callers wrap it in with_retry, including rate-limit metadata."""
    try:
        response = httpx.request(method, url, timeout=45, follow_redirects=True, **kwargs)
    except httpx.TransportError as exc:
        raise RetryableError(str(exc)) from exc
    if response.status_code in {429, 500, 502, 503, 504}:
        header = response.headers.get("Retry-After")
        try:
            delay = float(header) if header is not None else None
        except ValueError:
            delay = None
        raise RetryableError(f"HTTP {response.status_code}", delay)
    response.raise_for_status()
    return response


def _error(exc):
    message = str(exc)
    key = os.getenv("EXA_API_KEY", "")
    if key:
        message = message.replace(key, "[REDACTED]")
    message = re.sub(r"(?i)(exaApiKey=)[^&\s\"']+", r"\1[REDACTED]", message)
    return f"ERROR: {type(exc).__name__}: {message[:500]}"


def _text(value):
    return " ".join(str(value or "").split())


def _json(records):
    return json.dumps(records, ensure_ascii=False) if records else "NO RESULTS"


_arxiv_lock = threading.Lock()
_arxiv_last_call = 0.0


def _arxiv_request(params):
    global _arxiv_last_call
    with _arxiv_lock:
        delay = 3.0 - (time.monotonic() - _arxiv_last_call)
        if delay > 0:
            time.sleep(delay)
        _arxiv_last_call = time.monotonic()
    return _request("GET", ARXIV_URL, params=params)


def _hf_record(item, prefer_ai=False):
    paper = item.get("paper") or {}
    if not paper.get("id"):
        return None
    id_ = re.sub(r"v\d+$", "", str(paper["id"]))
    summary = (paper.get("ai_summary") or item.get("ai_summary")) if prefer_ai else None
    return {"id": id_, "url": f"https://huggingface.co/papers/{id_}",
            "published": str(paper.get("publishedAt") or item.get("publishedAt") or "")[:10],
            "title": _text(paper.get("title") or item.get("title")),
            "summary": _text(summary or paper.get("summary") or item.get("summary"))[:600],
            "upvotes": paper.get("upvotes") or item.get("upvotes") or 0,
            "github": paper.get("githubRepo") or item.get("githubRepo") or "",
            "stars": paper.get("githubStars") or item.get("githubStars") or 0}


def _mcp(name, arguments):
    key = os.getenv("EXA_API_KEY", "").strip()
    def call():
        response = _request("POST", EXA_URL, params={"exaApiKey": key} if key else None,
                            headers={"Content-Type": "application/json",
                                     "Accept": "application/json, text/event-stream"},
                            json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                  "params": {"name": name, "arguments": arguments}})
        packets = []
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            for line in response.text.splitlines():
                if line.startswith("data:") and line[5:].strip() not in {"", "[DONE]"}:
                    packets.append(json.loads(line[5:].strip()))
        else:
            packets = [response.json()]
        for packet in packets:
            if "error" in packet:
                raise RuntimeError(str(packet["error"]))
            result = packet.get("result")
            if result is None:
                continue
            text = "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
            def limited(value, context=""):
                if isinstance(value, dict):
                    for k, v in value.items():
                        key_name = context + re.sub(r"[^a-z]", "", k.lower())
                        if "rate" in key_name and any(word in key_name for word in ("limit", "exceed")) and v is True:
                            return True
                        if limited(v, key_name):
                            return True
                elif isinstance(value, list):
                    return any(limited(v, context) for v in value)
                elif isinstance(value, str):
                    return value.lower() in {"rate_limited", "rate limit exceeded", "ratelimitexceeded"}
                return False
            rate_flag = limited(result.get("_meta", {}))
            text_rate = any(marker in text.lower() for marker in ("rate limit exceeded", "rate limited", "rate limit reached", "exceeded the free"))
            if rate_flag or text_rate:
                raise RetryableError("Exa MCP rate limit reached")
            if result.get("isError"):
                raise RuntimeError(text or "Exa tool error")
            return text.strip() or "NO RESULTS"
        raise RuntimeError("Exa MCP returned no result")
    return with_retry(call, attempts=6, base=2, cap=60)


# ---- TODO 2: arXiv ----
@tool
def arxiv_search(query: str, max_results: int = 10) -> str:
    """Search arXiv papers by keywords, newest first. Returns a JSON list of {id, url, published, title, summary}."""
    # PSEUDO-CODE:
    #   keep only word characters of `query` -> terms; no terms -> "NO RESULTS" (do not call the network)
    #   respect arXiv etiquette: at least 3 seconds between two arXiv calls (remember the time of the last call)
    #   GET ARXIV_URL params: search_query="all:t1 AND all:t2 ...", sortBy=submittedDate, sortOrder=descending,
    #       max_results=clamp(max_results, 1, 30)           (wrap in with_retry)
    #   parse the Atom XML: each <entry> -> {id (last part of <id> after /abs/), url, published[:10], title, summary}
    #       collapse whitespace/newlines in title and summary; cut summary to ~600 chars
    #   no entries -> "NO RESULTS"; else json.dumps(records, ensure_ascii=False)
    #   any exception -> "ERROR: <type>: <message>"
    try:
        terms = [t for t in re.findall(r"[^\W_]+(?:-[^\W_]+)*", query, re.UNICODE)
                 if t.upper() not in {"AND", "OR", "NOT", "ALL", "TI", "AU", "ABS"}]
        if not terms:
            return "NO RESULTS"
        params = {"search_query": " AND ".join("all:" + t for t in terms[:12]),
                  "sortBy": "submittedDate", "sortOrder": "descending",
                  "max_results": max(1, min(30, int(max_results))), "start": 0}
        response = with_retry(lambda: _arxiv_request(params), attempts=6, base=3, cap=60)
        root = xml.etree.ElementTree.fromstring(response.text)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        records = []
        for entry in root.findall("a:entry", ns):
            url = entry.findtext("a:id", "", ns)
            id_ = re.sub(r"v\d+$", "", url.split("/abs/")[-1])
            if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[A-Za-z.-]+/\d{7})", id_):
                continue
            records.append({"id": id_, "url": f"https://arxiv.org/abs/{id_}",
                            "published": entry.findtext("a:published", "", ns)[:10],
                            "title": _text(entry.findtext("a:title", "", ns)),
                            "summary": _text(entry.findtext("a:summary", "", ns))[:600]})
        return _json(records)
    except Exception as exc:
        return _error(exc)


# ---- TODO 3: Hugging Face ----
@tool
def hf_daily_papers(limit: int = 30, date: str = "", keyword: str = "") -> str:
    """Hugging Face Daily Papers = what is trending in AI research. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars} sorted by upvotes. `date` is YYYY-MM-DD (empty = latest).
    `keyword` filters title/summary; there is no topic search on this endpoint (use hf_search_papers for a topic)."""
    # PSEUDO-CODE:
    #   GET HF_DAILY_URL params: limit (clamp 1..100) and date (only when given)      (with_retry)
    #   response = list of items {"paper": {id, title, summary, upvotes, githubRepo, githubStars, publishedAt}, ...}
    #   map every item to the record shape above (skip items without paper.id); url = https://huggingface.co/papers/<id>
    #   keyword -> keep records whose title+summary contains it (case-insensitive); sort by upvotes descending
    try:
        params = {"limit": max(1, min(100, int(limit)))}
        if date:
            params["date"] = date
        items = with_retry(lambda: _request("GET", HF_DAILY_URL, params=params)).json()
        records = [r for item in items if (r := _hf_record(item)) is not None]
        if keyword.strip():
            words = keyword.lower().split()
            records = [r for r in records if any(w in (r["title"] + " " + r["summary"]).lower() for w in words)]
        records.sort(key=lambda r: r["upvotes"], reverse=True)
        return _json(records)
    except Exception as exc:
        return _error(exc)


@tool
def hf_search_papers(query: str, limit: int = 10) -> str:
    """Search Hugging Face papers by topic. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars}."""
    # PSEUDO-CODE:
    #   GET HF_SEARCH_URL params: q=query, limit (clamp 1..50)                         (with_retry)
    #   same item shape as the daily endpoint; prefer paper["ai_summary"] over paper["summary"] when present
    try:
        if not query.strip():
            return "NO RESULTS"
        params = {"q": query, "limit": max(1, min(50, int(limit)))}
        items = with_retry(lambda: _request("GET", HF_SEARCH_URL, params=params)).json()
        return _json([r for item in items if (r := _hf_record(item, prefer_ai=True)) is not None])
    except Exception as exc:
        return _error(exc)


# ---- TODO 4: web search / fetch through the Exa MCP endpoint ----
def _primary_fetch(url):
    """Host-only fallback for an unavailable Exa fetch; returns actual primary text."""
    response = with_retry(lambda: _request("GET", url), attempts=3, cap=20)
    if "application/pdf" in response.headers.get("Content-Type", "") or response.content.startswith(b"%PDF"):
        from pypdf import PdfReader
        chunks = []
        for page in PdfReader(BytesIO(response.content)).pages:
            chunks.append(page.extract_text() or "")
            if sum(map(len, chunks)) >= 12000:
                break
        content = "\n".join(chunks)
    else:
        class VisibleText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.hidden = 0
                self.chunks = []
            def handle_starttag(self, tag, attrs):
                if tag in {"script", "style", "svg", "noscript"}:
                    self.hidden += 1
                elif tag in {"p", "h1", "h2", "h3", "div", "br", "li"} and not self.hidden:
                    self.chunks.append("\n")
            def handle_endtag(self, tag):
                if tag in {"script", "style", "svg", "noscript"}:
                    self.hidden = max(0, self.hidden - 1)
            def handle_data(self, data):
                if not self.hidden and data.strip():
                    self.chunks.append(data.strip() + " ")
        parser = VisibleText()
        response.encoding = "utf-8"
        parser.feed(response.text)
        content = "".join(parser.chunks)
    if not content.strip():
        return "NO RESULTS"
    return f"DIRECT PRIMARY PAGE FETCH (host fallback); URL: {response.url}\n" + content[:12000]

@tool
def web_search(query: str, objective: str = "", num_results: int = 5) -> str:
    """Search the web (Exa). Describe the ideal page in natural language. Returns clean text of the top results with URLs."""
    # PSEUDO-CODE:
    #   call the MCP tool "web_search_exa" with arguments {query, objective, numResults}
    #       (objective is REQUIRED by Exa: when empty, build one from the query)
    #   see GUIDE.md part 1.4 for how to call an MCP server over plain HTTP (JSON-RPC "tools/call") and read the answer
    #   read optional env EXA_API_KEY; when present it is sent to the Exa endpoint.
    #       (see GUIDE.md 1.4 for where it goes) => the key then appears in exception text: redact it before returning "ERROR: ..."
    #   WATCH OUT: read GUIDE.md 1.4 about how Exa signals "rate limited" on the free tier, and retry on it
    try:
        if not query.strip():
            return "NO RESULTS"
        if os.getenv("LAB_EXA_UNAVAILABLE", "").lower() in {"1", "true"} and not os.getenv("EXA_API_KEY", "").strip():
            return "ERROR: Exa search is marked unavailable after confirmed rate-limit failures. Use arxiv/Hugging Face discovery and web_fetch on their primary URLs; do not invent search results. Clear LAB_EXA_UNAVAILABLE or configure EXA_API_KEY to retry Exa."
        return _mcp("web_search_exa", {"query": query, "objective": objective or f"Find credible primary sources about {query}",
                                       "numResults": max(1, min(10, int(num_results)))})
    except Exception as exc:
        return _error(exc)


@tool
def web_fetch(url: str) -> str:
    """Read one page via Exa, with direct primary-page fallback when unavailable. Returns source URL and text, limited to 12000 characters."""
    # PSEUDO-CODE: MCP tool "web_fetch_exa" with arguments {"urls": [url]}; truncate the text to ~12000 chars
    try:
        if not re.match(r"^https?://", url):
            return "ERROR: ValueError: URL must use HTTP or HTTPS"
        identity = ""
        if re.match(r"^https://(?:www\.)?arxiv\.org/(?:abs|html)/", url):
            class Metadata(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.fields = {}
                def handle_starttag(self, tag, attrs):
                    fields = dict(attrs)
                    if tag == "meta" and fields.get("name", "").startswith("citation_"):
                        self.fields[fields["name"]] = fields.get("content", "")
            try:
                identity_url = re.sub(r"/html/", "/abs/", url)
                page = with_retry(lambda: _request("GET", identity_url), attempts=3)
                page.encoding = "utf-8"
                parser = Metadata()
                parser.feed(page.text)
                identity = "PRIMARY PAGE IDENTITY (direct HTML metadata): " + json.dumps(
                    {"requested_url": url, "resolved_url": str(page.url), **parser.fields}, ensure_ascii=False) + "\n"
            except Exception as exc:
                identity = "PRIMARY PAGE IDENTITY NOT VERIFIED: " + _error(exc) + "\n"
        if os.getenv("LAB_WEB_FETCH_DIRECT", "").lower() in {"1", "true"}:
            return identity + _primary_fetch(url)
        try:
            return identity + _mcp("web_fetch_exa", {"urls": [url]})[:12000]
        except Exception:
            return identity + _primary_fetch(url)
    except Exception as exc:
        return _error(exc)


# ---- TODO 5: registry (the researcher subagent gets exactly these) ----
SOURCE_TOOLS = [arxiv_search, hf_daily_papers, hf_search_papers, web_search, web_fetch]


if __name__ == "__main__":
    for name, fn, args in [
        ("arxiv_search", arxiv_search, {"query": "world model", "max_results": 3}),
        ("hf_daily_papers", hf_daily_papers, {"limit": 20}),
        ("hf_search_papers", hf_search_papers, {"query": "world model", "limit": 3}),
        ("web_search", web_search, {"query": "survey paper on world models", "num_results": 2}),
        ("web_fetch", web_fetch, {"url": "https://arxiv.org/abs/1803.10122"}),
    ]:
        try:
            print(f"== {name}\n{fn.invoke(args)[:400]}\n")
        except NotImplementedError as exc:
            print(f"== {name}: not implemented yet ({exc})\n")
