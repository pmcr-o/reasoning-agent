# Effort tables by vendor (as of 7 October 2026)

Sources: `enterprise-selection.md` and `test-time-compute.md` in `research_notes/LLM reasoning families 2026/`. Values are as the vendor pages stated them on that date.

## OpenAI (Responses API `reasoning.effort`; Chat Completions `reasoning_effort`)

| Value | Vendor guidance |
| --- | --- |
| `none` | Latency-critical work that gains nothing from reasoning: voice, fast retrieval, classification. Not accepted by `gpt-6-astra`. |
| `minimal` | Original GPT-5 reasoning models only; not accepted by `gpt-6.1-sol`. |
| `low` | Try first for latency-sensitive `gpt-5.5`. Luna at low is listed for well-scoped edits and simple extraction. |
| `medium` | Default for most workloads with planning, complex reasoning, or judgment. Default on `gpt-5.5`, `gpt-6.1-sol`, and others. |
| `high` | Hard reasoning and complex debugging where quality matters more than latency. Compare with `medium` first. |
| `xhigh` | Deep research, async runs, security and code review. Use only when evals show a clear benefit. |
| `max` | Most complex tasks. If already on `xhigh`, evaluate whether `max` is better. |

`reasoning.mode` (`standard` or `pro`) is separate from effort. `pro` on GPT-5.6 and GPT-6 does more model work and costs more.

## Anthropic (`thinking: {type: adaptive}` plus `output_config.effort`)

| Value | Vendor guidance |
| --- | --- |
| `low` | Skips thinking for simple tasks where speed matters most. |
| `medium` | Default on Claude Opus 5.5 and Claude Haiku 5.5. |
| `high` | Default on most models. Deep reasoning on complex tasks. |
| `xhigh` | Extended exploration. |
| `max` | Greatest depth with no thinking-length constraint. |

Adaptive thinking means the model decides per request whether to think; no effort level guarantees a thinking block. Per-message effort changes are beta.

## Google Cloud (Vertex, Gemini 3 and later `thinking_level`)

| Value | Vendor guidance |
| --- | --- |
| `MINIMAL` | Straightforward tasks that need no extended reasoning. Requires thought signatures in multi-turn calls. |
| `LOW` | High-throughput work with low complexity. |
| `MEDIUM` | Moderate complexity that benefits from intermediate steps. |
| `HIGH` | Deep reasoning, formal code verification, multi-turn tool execution. |

Gemini 2.5 uses `thinking_budget` instead. `thinking_budget: 0` turns off thinking on 2.5 Flash and Flash-Lite. Gemini 2.5 Pro cannot turn thinking off.

## xAI (Grok 4.5, 4.6, 4.7)

`reasoning.effort` or `reasoning_effort`: `low`, `medium`, `high` (default), `xhigh`. `xhigh` is available on 4.6 and later; on 4.5 it is treated as `high`. Reasoning cannot be disabled.

## Conflicts between sources

- The Gemini API thinking page (25 September 2026) lists `thinking_level` on Gemini 2.5. The Vertex enterprise page (7 October 2026) says `thinking_level` errors on Gemini 2.5. This skill follows the Vertex page for enterprise use.
- A CloudZero post says Gemini 3.x defaults to `HIGH`. Google's model table lists a default per model, from `MINIMAL` to `HIGH`. This skill follows Google's table.
