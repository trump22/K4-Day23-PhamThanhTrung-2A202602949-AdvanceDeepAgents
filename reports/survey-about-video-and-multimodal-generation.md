# Survey of Video and Multimodal Generation: Foundations, Advances, and Evaluation

## TL;DR

1. Video and multimodal generation has evolved from GANs and VAEs focusing on temporal consistency to unified diffusion and transformer-based models with superior quality, control, and diverse modality integration [1][2][3][4][5].
2. Recent advances include large, unified diffusion transformers, agentic frameworks, improved cross-modal alignment, real-time correction via multimodal LLMs, and fast speculative decoding for practical deployment [6][7][8][9][10][11].
3. Evaluation now emphasizes unified, reproducible protocols and blends automated metrics with human judgment; persistent challenges remain in cross-modal benchmarking, scalability, and real-world generalization [12][13][14][15][16].
4. Classic datasets like UCF-101, Kinetics, and curated benchmarks underpin progress but still pose unresolved challenges for long-range coherence and generalizability [1][3][5].

## Background

Video and multimodal generation refers to machine learning systems that synthesize video content conditioned on one or more inputs (e.g., text, images, audio) and integrate multiple perceptual modalities. Early work relied on generative adversarial networks (GANs) and variational autoencoders (VAEs) to learn temporal and cross-modal representations [1][3]. The central challenge was maintaining both spatial and temporal consistency while conditioning outputs on external signals—such as poses, text, or audio [2][5]. 

Classic datasets like UCF-101, Kinetics, and Something-Something provided the backbone for benchmarking these systems and enabled systematic evaluation of generative capacity and control [1][3][5]. 

With the introduction of diffusion models and transformer-based architectures post-2020, the field experienced dramatic gains in generative quality, capacity for long-range dependencies, and ability to unify text, image, audio, and video processing in a single foundation model [1][2][3][4]. These advances underpin current research directions.

## Foundations and Theoretical Frameworks

Early research focused on modeling temporal dynamics explicitly using recurrent architectures and hybrid discriminative-generative methods [1]. GANs and VAEs made the first breakthroughs in both unconditional and conditional video generation [1][2][3], but suffered from computational limitations and insufficient temporal or cross-modal coherence [3]. 

Controllable video generation emerged by integrating external signals (camera motion, depth, pose, and later, text) into the generative pipeline [2]. Taxonomies from recent surveys distinguish single-condition, multi-condition, and universal controllable methodologies [2].

Multimodal generative frameworks initially used separate autoregressive models for understanding versus diffusion models for generation, eventually converging into more unified architectures [4]. Human motion video generation serves as both a canonical application and a rich testing ground for advances in modeling, with surveys covering over 200 milestone works and curating key models and datasets [5].

Despite rapid technical progress, persistent foundational challenges include:
- Long-range temporal coherence
- Efficient conditioning and modality fusion
- Evaluation metric alignment with human perception
- Scaling computational costs for high-fidelity generation [1][2][3][4][5]

## Recent Advances: Transformer, Diffusion, and Agentic Architectures

Recent years have seen the consolidation of transformer-driven and diffusion-based techniques at the core of both video and multimodal generation models [6][8]. Unified, large-parameter diffusion transformers now support text-to-video, reference-guided, editing, and restoration tasks within the same pipeline, leveraging sophisticated data cleaning and annotation for improved control [8].

Significant technical advances include:
- Streaming multimodal references enabling dynamic, real-time interactive video responses (FlowAct-R2) [6]
- Asymmetric cross-attention alignment correction (RecCAR) for improving mutual constraints between video and other modalities [7]
- Real-time semantic correction by integrating multimodal LLMs into the generation loop without retraining base models, boosting semantic accuracy and reducing factual errors [9]
- Efficient speculative decoding (SpecFold) enabling up to 2x speedup in inference for large diffusion language models, improving scalability for real-world workflows [10]

Agentic approaches now frame video generation as part of more general visual or cross-modal workflows, incorporating proactive planning and multimodal prompt execution [6][8]. Specialized agents continuously refine output, intent alignment, and user interaction without human-in-the-loop retraining [11].

These advances enable broader input variety, finer control, and practical deployment at scale, but remain constrained by dataset biases and the bottlenecks of high-fidelity, long-range, cross-modal coherence [8][10][11].

## Cross-Modal Alignment and Multimodality

Unifying multiple modalities (text, audio, image, video) in generative models presents unique technical challenges. Recent models employ cross-modal attention, reciprocal regularization, and novel tokenization strategies to better align conditioning signals with desired outputs [4][7][8]. 

Surveys highlight the persistent issue of asymmetric correlations—where strong video-to-text links are not always matched by equally robust text-to-video or audio-to-video correspondence [7]. Solutions such as reciprocal attention regularization show improvement in objective alignment and human evaluation metrics [7].

Multimodal benchmarks now address both integration and task specialization, supporting evaluation of human emotion, voice synthesis, scene editing, and cross-modal referencing in both controlled and semi-realistic settings [8][16].

## Evaluation Methodologies and Limitations

The assessment of generative models remains a key bottleneck. Early research relied on short-form metrics and isolated dataset benchmarks. Recent literature introduces unified protocols, diverse multi-shot data, and a mix of automatic (e.g., LLM-ensemble) and subjective (e.g., mean opinion score) evaluation [12][13][16]. 

Benchmarks such as CLIP-CC-Bench and UniVBench expand coverage to long-form video and integrate both coarse- and fine-grained semantic evaluation, with an emphasis on reproducibility (standardized scripts, public model outputs) [12][13]. Faithfulness frameworks like FIFA extract semantic graphs and use automated VideoQA modules to assess factual consistency for both text-to-video and video-to-text tasks [14].

Surveys of world model evaluation uncover persistent fragmentation—domain- and task-specific protocols with poor generalization to real-world, interactive cases [15]. HUG-VIS highlights that automatic and human-judged rankings can diverge, and that joint reporting is needed for robust assessment [16]. Common limitations across evaluation studies include:
- Limited scalability beyond studio-constructed videos or controlled datasets
- Insufficient benchmarking of compounding errors and dynamics over long temporal horizons
- Lack of criteria for safety, interactivity, and reasoning
- Gaps in sim-to-real transfer and in-the-wild deployment readiness [12][13][14][15][16]

## Trends and Open Problems

Several clear trends emerge from the literature:
- Diffusion and transformer-based architectures dominate current research and have unified multi-modal, multi-task generation under a single model family [1][2][3][4][6][7][8][9].
- There is rapid progress toward more controllable, agentic, and semantically aligned generation, with frameworks for real-time correction and intent fulfillment [6][9][11].
- Benchmarks have improved in scale, diversity, and reproducibility but still struggle with generalization from controlled or synthetic data to real-world, user-driven scenarios [12][13][14][15][16].
- Automatic metrics increasingly align with human rankings, but divergences persist—dual reporting and human-in-the-loop evaluation remain essential [14][16].

Open problems and unresolved questions include:
- Establishment of universal, cross-domain, and cross-modal benchmarks for holistic evaluation [13][15][16]
- Achieving consistent, high-fidelity, long-range temporal and cross-modal coherence at practical computational cost [1][3][5][8]
- Enhancing sim-to-real transfer, robustness, and safety for deployment beyond controlled testbeds [15]
- Developing agentic models capable of proactive planning, adaptation, and dynamic interaction in evolving real-world contexts [6][8][11]

The field advances rapidly, yet addressing these open challenges is vital for the next generation of creative, robust, and trustworthy video and multimodal generation systems.

## References
[1] Video Diffusion Models: A Survey. hf-search. https://huggingface.co/papers/2405.03150 (2024-05-06)
[2] Controllable Video Generation: A Survey. hf-search. https://huggingface.co/papers/2507.16869 (2025-07-22)
[3] Bridging Text and Video Generation: A Survey. hf-search. https://huggingface.co/papers/2510.04999 (2025-10-06)
[4] Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities. hf-search. https://huggingface.co/papers/2505.02567 (2025-05-05)
[5] Human Motion Video Generation: A Survey. hf-search. https://huggingface.co/papers/2509.03883 (2025-09-04)
[6] FlowAct-R2: Beyond Talking Avatar via Streaming Multimodal References and Proactive Agent Planning. arxiv. https://arxiv.org/abs/2609.35728 (2026-09-28)
[7] All modalities are equal, but video is more equal: Closing the Cross-Attention Gap in Joint Video Generation. arxiv. https://arxiv.org/abs/2609.27901 (2026-09-23)
[8] LynnReal-Omni: Native multi-modal Video Generation for Agentic Visual Workflows. arxiv. https://arxiv.org/abs/2609.15863 (2026-09-14)
[9] MLLM-Guided Semantic Correction for Text-to-Video Generation. arxiv. https://arxiv.org/abs/2608.16513 (2026-08-17)
[10] SpecFold: Folding Multi-Branch Redundancy for Faster Speculative Decoding in Diffusion Language Models. hf-daily. https://huggingface.co/papers/2610.04875 (2026-10-06)
[11] MIRA: A Musical Intent Refinement Agent for Aligning Text-to-Music Generation with User Intent. hf-daily. https://huggingface.co/papers/2610.10355 (2026-10-07)
[12] CLIP-CC-Bench: Evaluating Paragraph-Level Video Descriptions in Video-Language Models. arxiv. https://arxiv.org/abs/2608.04302 (2026-08-05)
[13] UniVBench: Towards Unified Evaluation for Video Foundation Models. hf-search. https://huggingface.co/papers/2602.21835 (2026-02-25)
[14] FIFA: Unified Faithfulness Evaluation Framework for Text-to-Video and Video-to-Text Generation. hf-search. https://huggingface.co/papers/2507.06523 (2025-07-09)
[15] World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications. arxiv. https://arxiv.org/abs/2606.00133 (2026-05-28)
[16] HUG-VIS: A Multimodal Benchmark for Human-centered Understanding and Generation in Visual Intelligence. arxiv. https://arxiv.org/abs/2608.26517 (2026-08-27)
