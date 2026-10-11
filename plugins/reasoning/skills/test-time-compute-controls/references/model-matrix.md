# Reasoning model matrix (as of 7 October 2026)

Source: `test-time-compute.md` in `research_notes/LLM reasoning families 2026/`. Each row is the vendor page's statement on that date. Verify against the live docs before shipping.

## OpenAI

- Start model for most reasoning workloads: `gpt-6-astra`.
- Effort default: `gpt-5.5` and `gpt-6.1-sol` default to `medium`. GPT-5.6 defaults to `medium` in both modes.
- `none` rejected: `gpt-6-astra`. `none` and `minimal` rejected: `gpt-6.1-sol`.
- `reasoning.context`: GPT-5.6 defaults to `all_turns`; earlier models default to `current_turn`. Persisted reasoning does not cross model families.
- Mid-conversation effort: GPT-6 standard single-agent mode accepts a `configuration_update` item. Adjacent updates are rejected.
- Older (not the 2026 default): `o1`, `o3`, `o3-mini`, `o3-pro`, `o4-mini`, `codex-mini`. `o1-mini` does not support `reasoning_effort`.

## Microsoft Foundry

- `max`: GPT-6 and GPT-5.6, Responses API only.
- `xhigh`: GPT-6, GPT-5.6, GPT-5.5, GPT-5.4, and `gpt-5.1-codex-max`.
- `minimal`: original GPT-5 only; not on `gpt-5.1` or later.
- `gpt-5-pro`: supports only `high`, which is also its default.
- `gpt-5.1` defaults to `none`.
- Sending `tools` to `gpt-5.6-sol` on Chat Completions fails unless effort is `none`.
- Parallel tool calls are not supported with `minimal`.

## Anthropic

- Current: adaptive thinking with `output_config.effort`. Models named as rejecting `thinking.type: "enabled"`: Claude Opus 5.5, Sonnet 5, Sonnet 5.5, Fable 5.1, and Haiku 5.5.
- Claude Opus 5 with disabled thinking: effort is capped at `high`.
- Bedrock adaptive-only models: Fable 5.1, Mythos 5.1, Mythos 5, Fable 5, and Mythos Preview.
- Older Claude 4 models: manual `budget_tokens`, minimum 1,024, less than `max_tokens` except for interleaved thinking. Budgets above 32,000 tokens should use batch processing.

## Google Cloud (Vertex, 7 October 2026 page)

- `thinking_level` on Gemini 3.8 Flash, 3.8 Flash Cyber, and 3.7 Flash: `LOW`, `MEDIUM`, `HIGH`, default `MEDIUM`.
- `thinking_level` on Gemini 3.6 and 3.5 Flash: `MINIMAL` through `HIGH`, default `MEDIUM`.
- Defaults `MINIMAL`: Gemini 3.5 Flash-Lite and 3.1 Flash-Lite.
- Defaults `HIGH`: Gemini 3.1 Pro preview and Gemini 3 Flash preview.
- Gemini 3 Pro Image: `HIGH` only.
- `thinking_budget` on Gemini 2.5: Flash 1 to 24,576; Pro 128 to 32,768; Flash-Lite 512 to 24,576. Unset budget is dynamic up to 8,192. The budget is a soft limit.

## xAI

- Grok 4.5, 4.6, 4.7: `low`, `medium`, `high` (default), `xhigh`. `xhigh` on 4.5 is treated as `high`.
- On `grok-4.20-multi-agent`, the same field sets agent count (4 or 16), not depth.
- Grok 4.7 Responses API returns `reasoning.encrypted_content` on every response.
- Grok 4.7 list price on the model page: $2 input and $6 output per million tokens, with a long-context tier above 200k prompt tokens.

## Conflicts in the sources

- The Gemini API thinking page (25 September 2026) shows `thinking_level` on Gemini 2.5. The Vertex enterprise page (7 October 2026) says that errors. This matrix follows the Vertex page.
- CloudZero says Gemini 3.x defaults to `HIGH`. Google's table gives per-model defaults. This matrix follows Google.
- Foundry's feature table marks `temperature`, `top_p`, and `logprobs` as supported on GPT-6 models, but the same page says reasoning models other than GPT-6 Astra do not support them.
