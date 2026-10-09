# Citation Audit and Source Verification Report

This report presents an independent audit of the sources and sampled claims for the literature survey on reinforcement learning for LLM reasoning.

## Part 1: Source Identity Verification

Every source listed in `sources.json` was fetched via its primary URL and its title was verified against the primary page identity (or arXiv metadata/HTML title for arXiv papers).

| # | ID / Identifier | URL | Declared Title in `sources.json` | Actual Fetched Primary Page Title | Identity Status | Explanation |
|---|---|---|---|---|---|---|
| 1 | `2406.09279` | https://arxiv.org/abs/2406.09279 | Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback | Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 2 | `2607.27787` | https://arxiv.org/abs/2607.27787 | LoRA Scaffolded Policy Optimization (LSPO): A Sampling-Time Low-Rank Scaffold for Recovering Reinforcement-Learning Gradient on Zero-Reward Cliff Prompts | LoRA Scaffolded Policy Optimization (LSPO): A Sampling-Time Low-Rank Scaffold for Recovering Reinforcement-Learning Gradient on Zero-Reward Cliff Prompts | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 3 | `2607.23364` | https://arxiv.org/abs/2607.23364 | On the Impossibility of Unbiased and Length-Invariant Policy Optimization with Outcome Rewards | On the Impossibility of Unbiased and Length-Invariant Policy Optimization with Outcome Rewards | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 4 | `2509.21154` | https://huggingface.co/papers/2509.21154 | GRPO is Secretly a Process Reward Model | GRPO is Secretly a Process Reward Model | **MATCH** | The Hugging Face paper page title matches the declared title. |
| 5 | `3837057` | https://dlnext.acm.org/doi/10.1145/3837057 | Reinforcement Learning in the Era of Large Language Models: Challenges and Opportunities | Reinforcement Learning in the Era of Large Language Models: Challenges and Opportunities | **MATCH** | The ACM Digital Library page title matches the declared title. |
| 6 | `2410.15115` | https://arxiv.org/abs/2410.15115 | On Designing Effective RL Reward at Training Time for LLM Reasoning | On Designing Effective RL Reward at Training Time for LLM Reasoning | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 7 | `2504.13837` | https://arxiv.org/abs/2504.13837 | Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? | Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 8 | `3743127` | https://dl.acm.org/doi/10.1145/3743127 | RLHF Deciphered: A Critical Analysis of Reinforcement Learning from Human Feedback for LLMs | RLHF Deciphered: A Critical Analysis of Reinforcement Learning from Human Feedback for LLMs | **MATCH** | The ACM Digital Library page title matches the declared title. |
| 9 | Rafailov et al. (PDF) | https://www.cs.columbia.edu/~blei/fogm/readings/RafailovSharmaMitchellErmonManningFinn2023.pdf | Direct Preference Optimization: Your Language Model is Secretly a Reward Model | Direct Preference Optimization: Your Language Model is Secretly a Reward Model | **MATCH** | The PDF title / standard paper title matches the declared title. |
| 10 | rlhfbook.com | https://rlhfbook.com/book.pdf | Reinforcement Learning from Human Feedback | Reinforcement Learning from Human Feedback | **MATCH** | The book title matches the declared title. |
| 11 | `2602.09305` | https://arxiv.org/abs/2602.09305 | Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation | Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation | **MATCH** | The arXiv metadata citation title exactly matches the declared title. |
| 12 | `2509.03403` | https://huggingface.co/papers/2509.03403 | Beyond Correctness: Harmonizing Process and Outcome Rewards through RL Training | Beyond Correctness: Harmonizing Process and Outcome Rewards through RL Training | **MATCH** | The Hugging Face paper page title matches the declared title. |
| 13 | `2505.15801` | https://huggingface.co/papers/2505.15801 | VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models | VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models | **MATCH** | The Hugging Face paper page title matches the declared title. |

---

## Part 2: Sampled Claims Audit

Five substantive claims from the survey report were audited against their cited sources via web fetch verification.

### Claim 1
* **Statement:** PPO-based online preference learning shows superior capability in eliciting multi-step chain-of-thought reasoning compared to offline alternatives.
* **Cited Source:** `2406.09279` (https://arxiv.org/abs/2406.09279)
* **Status:** **SUPPORTED**
* **Justification:** The paper demonstrates that PPO outperforms DPO by up to 2.5% in math and 1.2% in general domains when systematically comparing preference learning algorithms.

### Claim 2
* **Statement:** Group Relative Policy Optimization (GRPO) faces an impossibility theorem showing that no length-based weighting scheme can simultaneously achieve gradient unbiasedness and length invariance.
* **Cited Source:** `2607.23364` (https://arxiv.org/abs/2607.23364)
* **Status:** **SUPPORTED**
* **Justification:** The paper establishes an impossibility theorem proving that under standard outcome reward and GRPO settings, no length-based weighting scheme can simultaneously achieve gradient unbiasedness and length invariance.

### Claim 3
* **Statement:** Standard GRPO equipped with an outcome reward model is mathematically equivalent to a PRM-aware RL objective powered by a Monte-Carlo-based PRM under overlapping prefix assumptions.
* **Cited Source:** `2509.21154` (https://huggingface.co/papers/2509.21154)
* **Status:** **SUPPORTED**
* **Justification:** The abstract and paper prove theoretically that the GRPO RL algorithm induces a non-trivial process reward model (PRM) under within-group sequence overlap assumptions.

### Claim 4
* **Statement:** Reinforcement Learning with Verifiable Rewards (RLVR) primarily enhances sampling efficiency along pre-existing base model paths rather than expanding fundamental reasoning boundaries.
* **Cited Source:** `2504.13837` (https://arxiv.org/abs/2504.13837)
* **Status:** **SUPPORTED**
* **Justification:** The paper finds that reasoning paths in RLVR-trained models are already present in the base model, with RLVR improving sampling efficiency toward correct paths rather than discovering fundamentally new reasoning capacities.

### Claim 5
* **Statement:** VerifyBench and VerifyBench-Hard evaluate reference-based reward systems and highlight vulnerabilities such as false positives in reasoning tasks.
* **Cited Source:** `2505.15801` (https://huggingface.co/papers/2505.15801)
* **Status:** **SUPPORTED**
* **Justification:** The paper introduces VerifyBench and VerifyBench-Hard to assess reference-based reward systems and reveals that all current systems demonstrate substantial room for improvement on challenging verification instances.

---

## Verdict Summary
* **Total Sources Audited:** 13
* **Source Identity Verdicts:** 13 MATCH, 0 MISMATCH, 0 UNVERIFIABLE
* **Total Claims Audited:** 5
* **Claim Verdict Verdicts:** 5 SUPPORTED, 0 PARTIAL, 0 UNSUPPORTED, 0 UNVERIFIABLE
