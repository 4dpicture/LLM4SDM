# LLM4SDM

This repository is the codebase for our paper "LLM4SDM". Shared decision making includes the assessment of clinician–patient conversations based on OPTION-12 item criteria. For this task, we make use of 4 open-sourced LLMs;

1. General Domain: [Gemma-4-E4B (8B)](https://huggingface.co/google/gemma-4-E4B-it)
2. General Domain: [Qwen3.5 (9B)](https://huggingface.co/Qwen/Qwen3.5-9B)
3. Medical Domain: [MedGemma-1.5 (4B)](https://huggingface.co/google/medgemma-1.5-4b-it)
4. Medical Domain: [MedLlama-3 (8B)](https://huggingface.co/johnsnowlabs/JSL-MedLlama-3-8B-v2.0)

Converstations are provided as transcripts. We use preprocessing script to convert them into a format suitable for LLMs, with minimal text normalizations.
The evaluation is based on the OPTION-12 criteria, which includes 12 items that assess various aspects of shared decision making. Each item is scored on a scale from 0 to 4, with higher scores indicating better performance in that aspect of shared decision making.

We constructured our prompts based on item descriptions, and synthetically examples. We also apply chunking strategy to handle long conversations. Two strategy have been implemented:
A. Each LLM asked to produce all 12 item assessments for each chunk, After processing all chunks, LLM is asked to consolidate the assessments into a final score for each item.
B. Each LLM asked to produce assessment for each item separately, After processing all chunks, LLM is asked to consolidate the assessments into a final score for each item.

In our paper, we used strategy-B (per-item assessments). Strategy A implemented but not used due to resource constraints. It is kept in the codebase for future use.

Our codebase provides two backends for LLM inference, Ollama, and VLLM. In our paper, we used VLLM for all experiments and for ease of use corresponding docker-compose.yaml files provided for each models.
