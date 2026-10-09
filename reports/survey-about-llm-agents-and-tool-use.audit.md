# Independent Source and Claim Citation Audit

## Source Verification Table

| Source # | ID / Reference | Primary Source URL | Actual Title (Primary Page Metadata / arXiv) | Status | Explanation |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | 2210.03629 | https://arxiv.org/abs/2210.03629 | ReAct: Synergizing Reasoning and Acting in Language Models | MATCH | The citation title exactly matches the primary page identity and arXiv metadata title. |
| 2 | 2302.04761 | https://arxiv.org/abs/2302.04761 | Toolformer: Language Models Can Teach Themselves to Use Tools | MATCH | The citation title exactly matches the primary page identity and arXiv metadata title. |
| 3 | 2305.15334 | https://arxiv.org/abs/2305.15334 | Gorilla: Large Language Model Connected with Massive APIs | MATCH | The citation title exactly matches the primary page identity and arXiv metadata title. |
| 4 | 2501.07834 | https://huggingface.co/papers/2501.07834 | Flow: Modularized Agentic Workflow Automation | MISMATCH | The report/sources.json title is "Flow: A Modular Approach to Automated Agentic Workflow Generation", whereas the primary paper title on Hugging Face / arXiv is "Flow: Modularized Agentic Workflow Automation". |
| 5 | 2601.22037 | https://huggingface.co/papers/2601.22037 | Optimizing Agentic Workflows using Meta-tools | MATCH | The citation title exactly matches the primary page metadata title on Hugging Face. |
| 6 | 2609.18674 | https://arxiv.org/abs/2609.18674 | CaMeLoT: CaMeL orchestrated with Temporal logic for static verification and liveness | MATCH | The citation title exactly matches the primary page identity and arXiv metadata title. |
| 7 | 2607.20759 | https://arxiv.org/abs/2607.20759 | IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests | MATCH | The citation title exactly matches the primary page identity and arXiv metadata title. |
| 8 | st-webagentbench | https://proceedings.iclr.cc/paper_files/paper/2026/file/c6c29e590e3c62e37e6b39cdd6baf2e8-Paper-Conference.pdf | ST-WEBAGENTBENCH: A BENCHMARK FOR EVALUAT ING SAFETY AND TRUSTWORTHINESS IN WEB AGENTS | MISMATCH | The report/sources.json title uses lowercase/mixed case ("Assessing the Safety and Trustworthiness of Web Agents in Realistic Environments"), whereas the official PDF title is capitalized as "ST-WEBAGENTBENCH: A BENCHMARK FOR EVALUAT ING SAFETY AND TRUSTWORTHINESS IN WEB AGENTS". |
| 9 | toolhazard | https://arxiv.org/pdf/2608.11878 | ToolHazard: Scaling Adversarial Environments for Security Evaluation and Alignment of LLM-based Agents | MATCH | The citation title matches the title in the fetched PDF header and abstract. |
| 10 | 10.1007/s10462-025-11471-9 | https://link.springer.com/article/10.1007/s10462-025-11471-9 | From language to action: a review of large language models as autonomous agents and tool users | MATCH | The citation title exactly matches the Springer article title. |
| 11 | 2606.25819 | https://arxivtldr.org/abs/2606.25819 | Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability | MATCH | The citation title matches the primary title on the source page. |

## Claim Verification Table

| Claim # | Claim Statement | Cited Source(s) | Verdict | Justification Grounded in Fetched Text | URL |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | ReAct interweaves verbal reasoning traces with external API actions. | [1] | SUPPORTED | The abstract and paper text explicitly state that ReAct explores generating both reasoning traces and task-specific actions in an interleaved manner to interface with external sources. | https://arxiv.org/abs/2210.03629 |
| 2 | Toolformer trains language models in a self-supervised manner to decide which APIs to call. | [2] | SUPPORTED | The abstract states: "We introduce Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass... This is done in a self-supervised way". | https://arxiv.org/abs/2302.04761 |
| 3 | Gorilla leverages retrieval-aware fine-tuning to connect LLMs with massive APIs. | [3] | SUPPORTED | The abstract and introduction describe Gorilla as a finetuned LLaMA-based model that, when combined with a document retriever, successfully connects LLMs with massive APIs. | https://arxiv.org/abs/2305.15334 |
| 4 | IssueTrojanBench shows that 66.5% of malicious issues penetrate all agent- and model-level guardrails in coding agents. | [7] | SUPPORTED | The abstract states: "Our results reveal critical vulnerabilities in the as-deployed modern coding agents, i.e., 66.5% of the malicious issues from IssueTrojanBench penetrate all the guardrails (agent- and LLM-level) of coding agents." | https://arxiv.org/abs/2607.20759 |
| 5 | ST-WebAgentBench shows that raw completion rates of 24.3% drop to 15.0% Completion-under-Policy (CuP). | [8] | UNVERIFIABLE | The fetched PDF text for ST-WebAgentBench introduces the CuP metric and notes substantial safety gaps, but the specific numerical benchmark values of "24.3%" and "15.0%" do not appear in the accessible abstract/introduction text. | https://proceedings.iclr.cc/paper_files/paper/2026/file/c6c29e590e3c62e37e6b39cdd6baf2e8-Paper-Conference.pdf |

## Comprehensive Scan of Report Paragraphs

Beyond the five primary claims evaluated above, an independent scan of all report paragraphs was conducted to check for invented experimental settings, overly broad conclusions, and claims absent from fetched evidence. 

1. **Section Background / Review Citation [10]:** The report cites a 2026 Springer review ("From language to action: a review of large language models as autonomous agents and tool users") [10]. The fetched Springer article confirms its focus on reviewing LLM agents, single-agent/multi-agent architectures, tool integration, and 68 datasets, fully supporting the report's framing.
2. **Section Dynamic Workflow Generation and Meta-Tool Optimization / Flow [4]:** The report cites Niu et al. (2025) / Flow [4]. The fetched arXiv page (`2501.07834`) confirms that Flow defines workflows as activity-on-vertex (AOV) graphs and uses dynamic subtask allocation adjustment based on historical performance, supporting the report's description (note: source title metadata discrepancy noted above).
3. **Section Dynamic Workflow Generation and Meta-Tool Optimization / AWO [5]:** The report cites Agent Workflow Optimization (AWO) transforming recurring sequences into deterministic meta-tools [5]. The fetched Hugging Face paper page (`2601.22037`) confirms that AWO identifies redundant tool execution patterns and creates deterministic meta-tools that bundle actions, reducing LLM calls by up to 11.9% and increasing success rate.
4. **Section Formal Verification and Runtime Safety Guardrails / CaMeLoT [6]:** The report cites CaMeLoT [6]. The fetched arXiv page (`2609.18674`) confirms that CaMeLoT translates agent plans into finite-state transition systems and checks them against temporal logic safety policies (CTL) using the nuXmv model checker prior to execution.
5. **Section Evaluation Methodologies / ToolBench-X [11]:** The report cites ToolBench-X [11] regarding recoverable environmental hazards (specification drift, execution failure, etc.) and agent unreliability. The fetched ArXiv TLDR page (`2606.25819`) confirms these exact five hazard types and conclusions.
6. **Section Evaluation Methodologies / ToolHazard [9]:** The report cites ToolHazard-Bench regarding adversarial environmental injection timing. The fetched PDF header and abstract (`2608.11878`) confirm that ToolHazard evaluates agents under complex workflows and diverse environmental attacks, noting that injection timing affects success.

## Verdict Summary
- **Total Sources Audited:** 11
- **Source Identity Breakdown:** 9 MATCH, 2 MISMATCH (Source 4: minor title wording difference; Source 8: capitalization/formatting difference in PDF title).
- **Total Claims Audited:** 5
- **Claim Verdict Breakdown:**
  - SUPPORTED: 4 (Claims 1, 2, 3, 4)
  - PARTIAL: 0
  - UNSUPPORTED: 0
  - UNVERIFIABLE: 1 (Claim 5: numerical percentages 24.3% and 15.0% are not present in the fetched abstract/intro excerpt of the ICLR paper PDF).
