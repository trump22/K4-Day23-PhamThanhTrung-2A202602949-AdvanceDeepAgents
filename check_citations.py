"""check_citations.py - STUDENT IMPLEMENTS `check`.   Runs INSIDE the sandbox (standard library only).

research.py uploads this file to the sandbox and the lead agent runs it with the `execute` tool:
    python3 /tmp/work/research/check_citations.py [report.md] [sources.json]
It must exit 0 and print "OK: ..." when the report is consistent, else print each problem and exit 1.
"""
import json
import re
import sys
from datetime import date

REPORT = "/tmp/work/report/report.md"
SOURCES = "/tmp/work/research/sources.json"


def check(report_text, sources):
    """Return a list of problem strings (empty list = OK).

    PSEUDO-CODE:
      problems = []
      if sources is empty: return ["no sources in sources.json"]
      for each source entry:
          n must be an int                       -> problem if not
          url must start with http:// or https://-> problem if not
          the same url must not appear twice     -> problem if duplicated
      split report_text at the heading "## References":
          body = text before it; if the heading is missing -> problem
      cited = set of numbers found as [n] in the BODY only (not in the reference list; use a regex)
      every number in `cited` must exist in sources -> problem "[n] cited but missing from sources.json"
      every source number must be in `cited`        -> problem "source [n] never cited"
      the lines of the References section that start with "[n]" (regex) are the reference lines:
          every source needs exactly ONE reference line (none missing, no number twice, no number that is not a source)
          each reference line holds exactly ONE http(s) URL and it must equal that source's url
          (a line bundling several sources under one number is a problem)
      return problems
    """
    problems = []
    if not isinstance(sources, list) or not sources:
        return ["no sources in sources.json (expected a nonempty list)"]
    numbers, urls = {}, set()
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            problems.append(f"source {i}: expected an object")
            continue
        n, url = source.get("n"), source.get("url")
        if type(n) is not int or n < 1:
            problems.append(f"source {i}: n must be a positive integer")
            continue
        if n in numbers:
            problems.append(f"duplicate source number [{n}]")
        numbers[n] = source
        if not isinstance(url, str) or not re.match(r"^https?://\S+$", url):
            problems.append(f"source [{n}]: invalid http(s) URL")
        elif url in urls:
            problems.append(f"duplicate source URL for [{n}]")
        else:
            urls.add(url)
        family = source.get("source")
        published = source.get("date", "")
        if published:
            try:
                parts = str(published).split("-")
                if len(parts) not in {1, 2, 3}:
                    raise ValueError("invalid precision")
                date(int(parts[0]), int(parts[1]) if len(parts) > 1 else 1,
                     int(parts[2]) if len(parts) > 2 else 1)
            except (ValueError, TypeError):
                problems.append(f"source [{n}]: invalid date; preserve known precision or leave unknown date empty, never invent 00")
        if family in {"arxiv", "hf-daily", "hf-search"}:
            prefix = "https://arxiv.org/abs/" if family == "arxiv" else "https://huggingface.co/papers/"
            if not isinstance(source.get("id"), str) or url != prefix + source["id"]:
                problems.append(f"source [{n}]: {family} URL must equal {prefix}<id>; id must be the exact paper identifier string, not a label or title")
            elif re.search(r"v\d+$", source["id"]):
                problems.append(f"source [{n}]: {family} identifier must be versionless, remove the vN suffix from both id and URL")
    # Fenced code and inline code are examples, not scholarly citations.
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", report_text)
    heading = re.search(r"(?m)^##\s+References\s*$", text)
    if heading is None:
        return problems + ["missing ## References heading"]
    body, references = text[:heading.start()], text[heading.end():]
    body = re.sub(r"`[^`\n]*`", "", body)
    cited = set()
    for match in re.finditer(r"\[(\d+(?:\s*[,\-–]\s*\d+)*)\](?!\s*\()", body):
        for part in match.group(1).split(","):
            ends = re.split(r"[-–]", part.strip())
            if len(ends) == 1:
                cited.add(int(ends[0]))
            else:
                low, high = map(int, ends)
                if high < low or high - low > 10000:
                    problems.append(f"invalid citation range {match.group(0)}")
                else:
                    cited.update(range(low, high + 1))
    for n in sorted(cited - numbers.keys()):
        problems.append(f"[{n}] cited but missing from sources.json")
    for n in sorted(numbers.keys() - cited):
        problems.append(f"source [{n}] never cited")
    reference_counts = {}
    for line in references.splitlines():
        match = re.match(r"^\s*\[(\d+)\]\s+(.+)$", line)
        if not match:
            continue
        n = int(match.group(1))
        reference_counts[n] = reference_counts.get(n, 0) + 1
        if n not in numbers:
            problems.append(f"reference [{n}] is not in sources.json")
            continue
        found = re.findall(r"https?://[^\s<>\)]+", match.group(2))
        if len(found) != 1:
            problems.append(f"reference [{n}] must contain exactly one URL")
        elif found[0].rstrip(".,;") != numbers[n].get("url"):
            problems.append(f"reference [{n}] URL differs from sources.json")
    for n in numbers:
        count = reference_counts.get(n, 0)
        if count != 1:
            problems.append(f"source [{n}] needs exactly one reference line (found {count})")
    return problems


def main(argv):
    report_path = argv[1] if len(argv) > 1 else REPORT
    sources_path = argv[2] if len(argv) > 2 else SOURCES
    try:
        with open(report_path, encoding="utf-8") as f:
            report = f.read()
        with open(sources_path, encoding="utf-8") as f:
            sources = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read inputs: {exc}")
        return 1
    problems = check(report, sources)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(sources)} sources, all citations resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
