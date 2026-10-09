# Citation and Claim Audit

## Source Title–URL Audit

| n  | sources.json Title                                                                         | Actual Fetched Title                                                                                                          | URL                                                        | Match?      | Notes                                                                                                                            |
|----|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1  | Video Diffusion Models: A Survey                                                          | Video Diffusion Models: A Survey                                                                                             | https://huggingface.co/papers/2405.03150                  | MATCH       | Title matches exactly (HuggingFace mirror of arXiv).                                                                              |
| 2  | Controllable Video Generation: A Survey                                                   | Controllable Video Generation: A Survey                                                                                      | https://huggingface.co/papers/2507.16869                  | MATCH       | Title matches exactly (HuggingFace mirror of arXiv).                                                                              |
| 3  | Bridging Text and Video Generation: A Survey                                              | Bridging Text and Video Generation: A Survey                                                                                 | https://huggingface.co/papers/2510.04999                  | MATCH       | Title matches exactly (HuggingFace mirror of arXiv).                                                                              |
| 4  | Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities | Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities                              | https://huggingface.co/papers/2505.02567                  | MATCH       | Title matches exactly.                                                                                                            |
| 5  | Human Motion Video Generation: A Survey                                                   | Human Motion Video Generation: A Survey                                                                                      | https://huggingface.co/papers/2509.03883                  | MATCH       | Title matches exactly.                                                                                                            |
| 6  | FlowAct-R2: Beyond Talking Avatar via Streaming Multimodal References and Proactive Agent Planning | FlowAct-R2: Beyond Talking Avatar via Streaming Multimodal References and Proactive Agent Planning                           | https://arxiv.org/abs/2609.35728                         | MATCH       | Title matches exactly (arXiv page).                                                                                              |
| 10 | SpecFold: Folding Multi-Branch Redundancy for Faster Speculative Decoding in Diffusion Language Models | SpecFold: Folding Multi-Branch Redundancy for Faster Speculative Decoding in Diffusion Language Models                       | https://huggingface.co/papers/2610.04875                  | MATCH       | Title matches exactly.                                                                                                            |
| 12 | CLIP-CC-Bench: Evaluating Paragraph-Level Video Descriptions in Video-Language Models      | CLIP-CC-Bench: Evaluating Paragraph-Level Video Descriptions in Video-Language Models                                        | https://arxiv.org/abs/2608.04302                         | MATCH       | Title matches exactly.                                                                                                            |
| 13 | UniVBench: Towards Unified Evaluation for Video Foundation Models                         | UniVBench: Towards Unified Evaluation for Video Foundation Models                                                            | https://arxiv.org/abs/2602.21835                         | MATCH       | Title matches exactly.                                                                                                            |
| 14 | FIFA: Unified Faithfulness Evaluation Framework for Text-to-Video and Video-to-Text Generation | FIFA: Unified Faithfulness Evaluation Framework for Text-to-Video and Video-to-Text Generation                              | https://arxiv.org/abs/2507.06523                         | MATCH       | Title matches exactly.                                                                                                            |

## Claim Checks

**Claim 1.**
> "Video and multimodal generation has evolved from GANs and VAEs focusing on temporal consistency to unified diffusion and transformer-based models with superior quality, control, and diverse modality integration [1,2,3,4,5]."

- **SUPPORTED**. Each cited survey ([1](https://huggingface.co/papers/2405.03150), [2](https://huggingface.co/papers/2507.16869), [3](https://huggingface.co/papers/2510.04999), [4](https://huggingface.co/papers/2505.02567), [5](https://huggingface.co/papers/2509.03883)) describes a transition from earlier GAN/ VAE/ autoregressive architectures to diffusion and transformer-based models, with explicit mention of improved quality, expanded control, and broader modality integration.

**Claim 2.**
> "FlowAct-R2 introduces streaming multimodal reference diffusion transformers for real-time avatar control [6]."

- **SUPPORTED**. FlowAct-R2 ([6](https://arxiv.org/abs/2609.35728)) is described as a framework using a "Streaming Multimodal Reference Diffusion Transformer" for interactive humanoid video generation, supporting real-time, streaming avatar control.

**Claim 3.**
> "Benchmarks like CLIP-CC-Bench and UniVBench expand coverage to long-form video and integrate semantic evaluation [12,13]."

- **SUPPORTED**. The CLIP-CC-Bench ([12](https://arxiv.org/abs/2608.04302)) abstract states it is designed for long-form video (paragraph-level) semantic evaluation, while UniVBench ([13](https://arxiv.org/abs/2602.21835)) explicitly expands coverage to multi-shot, diverse videos, and integrates unified semantic evaluation.

**Claim 4.**
> "SpecFold enables up to 2x speedup in inference for large diffusion language models with practical application [10]."

- **SUPPORTED**. SpecFold ([10](https://arxiv.org/abs/2610.04875)) reports (abstract/main text) up to 1.99x throughput over vanilla decoding for diffusion language models, explicitly positioning its method as a practical inference speedup strategy.

**Claim 5.**
> "Faithfulness frameworks like FIFA align more closely with human judgment and improve factual consistency [14]."

- **SUPPORTED**. FIFA ([14](https://arxiv.org/abs/2507.06523)) is proposed as aligning more closely with human judgment in faithfulness evaluation, and its automated post-correction step is shown to improve factual consistency in both text and video outputs.


## Summary of Verdicts
- SUPPORTED: 5
- PARTIAL: 0
- UNSUPPORTED: 0
- UNVERIFIABLE: 0

All checked claims are strongly supported by the cited evidence and relevant source titles precisely match those reported in sources.json.