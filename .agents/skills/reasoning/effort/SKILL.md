---
name: effort
description: "Choose the reasoning or thinking effort for one LLM call on OpenAI, Azure Foundry, Anthropic, Google Vertex, or xAI. USE FOR: reasoning.effort or reasoning_effort, output_config.effort, thinking_level, thinking_budget, questions about xhigh or max effort, lowering latency or cost by lowering effort, a none or minimal setting returning HTTP 400, deciding between a plain call and a reasoning call. DO NOT USE FOR: multi-call agent loops (use orchestrator-worker, routing, or voting), prompt wording or chain-of-thought instructions (use prompting-strategy-selection), which parameter a specific model accepts or how it bills (use test-time-compute-controls)."
---

# effort

Pick the lightest effort setting that meets the quality bar for one call. Every vendor guide in the source notes says the same thing: start low, and step up only when a comparison on your own inputs shows a gain that is worth the extra tokens and latency.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- Choosing `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max` on OpenAI or Foundry
- Choosing `output_config.effort` or disabled thinking on Claude
- Choosing `thinking_level` or `thinking_budget` on Gemini
- A reasoning call is too slow or too expensive and you want to lower it

## When Not to Use

- The question is about loops, retries, or several model calls (use `orchestrator-worker`, `routing`, or `voting`)
- The question is about prompt wording or step-by-step instructions (use `prompting-strategy-selection`)
- The question is which parameter a specific model accepts, or how it bills (use `test-time-compute-controls`)

## Decision rule

1. Classify the task. Voice, retrieval, classification, and well-scoped edits stay at the floor: `none` or `low` on OpenAI, disabled thinking or `low` on Claude, `MINIMAL` on Gemini. Planning, judgment, debugging, and code verification start at `medium` with thinking on.
2. Step up one tier only when an offline paired comparison on your own inputs shows a quality gain. Record quality, output tokens, and latency for both tiers.
3. Use `high` or above only for hard, high-value work that tolerates latency. Compare `high` against `medium` before trying `xhigh`, and `max` against `xhigh`.
4. Refuse a heavier tier when the lighter one already meets the written bar, when the task is latency-critical, or when the output cap truncates the answer (see below).

## Model floors: check before assuming `none` works

- `gpt-6-astra` rejects `none` with HTTP 400. Use `minimal` or `low`.
- `gpt-6.1-sol` rejects `none` and `minimal`. Its default is `medium`.
- Gemini 2.5 Pro cannot turn thinking off.
- Gemini 3 Pro Image supports only `HIGH`.
- Grok 4.5, 4.6, and 4.7 cannot disable reasoning. `low` is the lightest setting.
- Claude Opus 5.5 returns HTTP 400 for both `thinking: disabled` and `thinking: enabled`. Omit `thinking` and steer with `output_config.effort`.
- Claude Opus 5 allows disabled thinking, but `output_config.effort` is capped at `high` in that mode.

## Refuse conditions: truncation

- If generation hits the output cap during reasoning, OpenAI returns `status: incomplete` with reason `max_output_tokens`, and Anthropic returns `stop_reason: max_tokens`. You pay for the reasoning and get no answer.
- Do not lower the output cap to save money. Raise the cap or lower the effort tier.
- Gemini bills thinking tokens even when `max_output_tokens` truncates the visible answer.
- On Gemini 2.5 Flash and Flash-Lite, `thinking_budget: 0` removes thought content, but reasoning-style text can still appear in the answer.

## Workflow

1. Name the task type and the model's floor from the list above.
2. Pick the starting tier from the decision rule.
3. Run the same inputs at the starting tier and one tier up. Record quality, reasoning-token counts (`reasoning_tokens`, `thinking_tokens`, or `thoughts_token_count` by vendor), and latency.
4. Keep the lighter tier unless the heavier one wins on quality by the margin you set before the test.
5. Check `status` or `stop_reason` on every run. A truncated run does not count as a result.

## Validation

- [ ] The starting tier is the lightest one the model accepts
- [ ] A paired comparison exists before any step up
- [ ] No run ends truncated with an empty answer
- [ ] `scripts/validate.ps1` exits 0

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Sending `none` to `gpt-6-astra` and getting HTTP 400 | Use `minimal` or `low` |
| Lowering the output cap to save money | Raise the cap or lower the effort instead |
| Treating blog cost multipliers of 5x to 40x as measured facts | They are planning ranges; measure your own workload |
| Assuming Gemini `thinking_level` defaults to `HIGH` | The default differs by model; read that model's row in `references/` |

Vendor effort tables and sources are in `references/effort-tables.md`.
