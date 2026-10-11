# Prompting family evidence (as of 7 October 2026)

Source: `prompting-strategies.md` in `research_notes/LLM reasoning families 2026/`. Paper results are published evaluations. Shipping controls are vendor guides. Customer quotes are not controlled tests.

## Vendor guidance

- OpenAI reasoning best practices (fetched 7 October 2026): "think step by step" may not help and can hinder; the page lists "Avoid chain-of-thought prompts." For multi-call tool runs on Chat Completions, dropping prior reasoning items spends more reasoning tokens and performs slightly worse; use the Responses API with stored items.
- Anthropic prompt engineering (chain-of-thought section): a general instruction such as "think thoroughly" often beats a prescribed plan. Manual chain-of-thought is a fallback only when thinking is off. Explicit prompt chaining remains useful when intermediate outputs must be inspected.
- Google Cloud prompting strategies (updated 7 October 2026): compare thinking alone with explicit step-by-step instructions. Split a prompt that asks for several distinct cognitive actions into separate prompts.

## Paper results

- Chain-of-thought: Wei et al., NeurIPS 2022. Sprague et al., ICLR 2025, meta-analysis of over 100 papers and 14 models: the gain sits mostly in math, logic, and algorithmic tasks. On MMLU, most of the gain comes from questions containing an equals sign.
- Chain-of-thought can hurt: Liu et al., ICML 2025, on psychology tasks where deliberation hurts humans. The 36.3-point figure compares o1-preview with GPT-4o and is not a within-model ablation.
- Self-consistency: Wang et al., ICLR 2023. On PaLM-540B, 40 sampled paths raised GSM8K from 56.5 to 74.4 over greedy chain-of-thought. The method needs a fixed answer set. The authors say most of the gain appears with 5 to 10 paths.
- Tree of Thoughts: Yao et al., NeurIPS 2023. On Game of 24 with GPT-4, ToT reached 74 percent against 4 percent for chain-of-thought. The authors state the method may cost 5 to 100 times more generated tokens and may be unnecessary for tasks GPT-4 already solves.
- Reflexion: Shinn et al., NeurIPS 2023, 91 percent pass@1 on HumanEval against 80 percent for GPT-4 in the abstract. Mirzaei 2026 (24 August 2026): at matched generated tokens on Qwen2.5 1.5B, 3B, and 7B, forced Reflexion scored 5.5 points lower on 7B GSM8K and 10.1 points lower on 7B MATH-500. On 1.5B, Reflexion judged its first answer correct on every question, so the loop never ran. Scope: math with a checkable answer, models up to 7B, one prompt wording.
- Least-to-most: Zhou et al., ICLR 2023. On SCAN length split, 99.7 percent against 16.2 percent for chain-of-thought. On GSM8K, only 62.39 percent against 60.87 percent. The authors write that the decomposition prompt does not transfer to other domains.
- ReAct: Yao et al., ICLR 2023. The paper caps the loop at 7 steps on HotpotQA and 5 on FEVER because more steps did not help. The production form is the native tool API.

## Conflicts and gaps

- No fetched 2026 study compares these families against a plain call on a named enterprise task.
- Mirzaei 2026 reports on Wang et al. 2024 (equal-budget comparison) and Huang et al. 2024 (intrinsic self-correction) as summaries; neither paper was re-read for these notes.
- The OpenAI reasoning best-practices page still uses o-series examples; other OpenAI pages cover GPT-5.5 and later. Treat them as coexisting, not as one rewritten guide.
