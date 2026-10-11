---
name: test-time-compute-controls
description: "Look up the request fields, error messages, billing meters, and availability for 2026 reasoning models on OpenAI GPT-5.6 and GPT-6, Microsoft Foundry, Anthropic adaptive thinking, Google Gemini thinking_level and thinking_budget on Vertex, and xAI Grok 4.5 to 4.7. USE FOR: which parameter a model accepts, HTTP 400 errors from reasoning fields, a Foundry error about reasoning_effort with tools, budget_tokens rejected on Claude 4.7 or later, thinking_budget and thinking_level conflicts, which usage field counts reasoning tokens, whether a model is preview or generally available on a given platform. DO NOT USE FOR: choosing an effort tier (use effort), agent loop bounds (use orchestrator-worker, routing, voting, or checker), prompt wording (use prompting-strategy-selection)."
---

# test-time-compute-controls

Look up what a reasoning model accepts, what it bills, and whether it is available on the platform you use. Parameter support differs by model and by platform, and a field that works on one surface can return HTTP 400 on another. Check the model's row before writing code.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- A request with a reasoning field returns HTTP 400
- Choosing which field to send for a given model and platform
- Reading usage output to see how many reasoning tokens were billed
- Confirming whether a model is preview, quota-limited, or generally available

## When Not to Use

- Choosing the effort value for a task (use `effort`)
- Designing loops, orchestrators, or checker calls (use `orchestrator-worker`, `routing`, `voting`, or `checker`)
- Deciding whether to keep step-by-step prompt text (use `prompting-strategy-selection`)

## Request fields by vendor

| Vendor | Field to send | Values and notes |
| --- | --- | --- |
| OpenAI (Responses) | `reasoning.effort`; `reasoning.mode` on GPT-5.6 and GPT-6 | Effort: `none` to `max`, model-dependent. Mode: `standard` (default) or `pro`. |
| OpenAI (Chat Completions) | `reasoning_effort` | Function tools are rejected on GPT-6 Astra and GPT-6.1 Sol; use Responses. |
| Microsoft Foundry | `reasoning_effort` (Chat) or `reasoning.effort` and `reasoning.mode` (Responses) | `max` only on GPT-6 or GPT-5.6 Responses. `minimal` only on original GPT-5 models. |
| Anthropic | `thinking: {type: "adaptive"}` plus `output_config.effort` | Effort: `low`, `medium`, `high`, `xhigh`, `max`. `budget_tokens` is deprecated on Claude 4.6 and rejected on 4.7 and later. |
| Google Vertex, Gemini 3 and later | `thinking_level` | `MINIMAL`, `LOW`, `MEDIUM`, `HIGH`; the set and default depend on the model. Do not send with `thinking_budget`. |
| Google Vertex, Gemini 2.5 | `thinking_budget` | Flash and Flash-Lite accept `0`. Pro cannot turn thinking off. |
| xAI Grok 4.5 to 4.7 | `reasoning.effort` (Responses) or `reasoning_effort` (Chat) | `low`, `medium`, `high` (default), `xhigh`. Cannot be disabled. |

## Errors you will see

- OpenAI: `none` on `gpt-6-astra` returns HTTP 400.
- Foundry: "Function tools with reasoning_effort are not supported for gpt-5.6-sol in /v1/chat/completions." Send `reasoning_effort: "none"` or use `/v1/responses`.
- Anthropic: `budget_tokens` on Claude 4.7 or later returns HTTP 400. On Claude Opus 5.5, `thinking: disabled` and `thinking: enabled` both return HTTP 400.
- Anthropic on Bedrock: `xhigh` or `max` effort with disabled thinking returns `invalid_request_error`.
- Google: sending `thinking_level` to Gemini 2.5 returns an error; sending `thinking_level` and `thinking_budget` together returns an error. `MINIMAL` in multi-turn calls returns HTTP 400 if thought signatures are not passed back.
- xAI: `presencePenalty`, `frequencyPenalty`, and `stop` return an error on reasoning models.

## Billing meters

| Vendor | Field | Note |
| --- | --- | --- |
| OpenAI | `usage.output_tokens_details.reasoning_tokens` | Billed as output. Counts against `max_output_tokens`. |
| Anthropic | `usage.output_tokens_details.thinking_tokens` | Billed as output even when `display` is `omitted`. Prior thinking blocks in context bill as input. |
| Google Gemini API | `total_thought_tokens` | Billed on the full thought, not the summary. |
| Google Vertex | `usage_metadata.thoughts_token_count` | Billed when thinking is on, which is the default on Gemini 3 Pro and 2.5 Pro. |
| xAI | Included in total consumption | No separate reasoning price on the reasoning page. |

Reasoning tokens are not a separate SKU on these platforms. Read the meter above and multiply by the model's output rate from its pricing page.

## Availability

- Microsoft Foundry: GPT-6 and GPT-5.6 deployments need no access request on most rows. GPT-6 Astra and GPT-5.6 still depend on quota tier, and the Tier 5 and Tier 6 subscriptions include quota by default.
- xAI: `grok-4.7`, `grok-4.6`, and `grok-4.5` are on the public API. Grok 4.7 Fast is available in Cursor and Grok Build, not on the public xAI API.
- Google Vertex: Gemini 3.1 Pro preview and Gemini 3 Flash preview carry the preview label. Gemini 3.8, 3.7, 3.6, and 3.5 Flash do not, on the 7 October page.
- Anthropic: Claude Mythos Preview is named as a preview. Per-message effort changes are beta and need a request header. Claude Haiku 5.5 was announced 7 October 2026.
- OpenAI's pages do not print a preview label on `gpt-6-astra` or `gpt-6.1-sol`. Foundry's no-access-request statement is the availability source used here.

## Workflow

1. Identify the vendor, platform, and model ID. The same model can differ across Foundry, Vertex, Bedrock, and direct APIs.
2. Find the model's row in the request-field table and the errors list. Send only the fields that row allows.
3. Check the usage fields after a test call. Confirm the reasoning count is present before you estimate cost.
4. If a model's availability matters for production, confirm it on the platform's own status page. This skill's sources are dated 7 October 2026.

## Validation

- [ ] The field sent matches the model's row for that platform
- [ ] No request sends two reasoning fields that the platform rejects together
- [ ] Usage output is checked for the reasoning-token meter
- [ ] Preview or quota-limited models are flagged in any production plan
- [ ] `scripts/validate.ps1` exits 0

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Using one shared `reasoning_effort` across OpenAI, Grok, and Claude | Each vendor has its own field and value set; map per vendor |
| Trusting the Gemini API page for a Vertex call | The 7 October Vertex page is the enterprise contract; the 25 September API page conflicts on Gemini 2.5 |
| Treating "no access request" as unlimited quota | Quota depends on tier; check the quota column |
| Estimating cost from the visible answer only | Add the reasoning-token meter to output tokens |

Source conflicts and the full per-model table are in `references/model-matrix.md`.
