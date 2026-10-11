---
name: prompting-strategy-selection
description: "Choose a prompting strategy for LLM calls in 2026: whether to keep or drop chain-of-thought once a model has a reasoning mode, when caller-side decomposition or explicit prompt chaining helps, and where self-consistency, Tree of Thoughts, Reflexion, least-to-most, or ReAct still apply. USE FOR: think step by step or explain your reasoning prompts, chain-of-thought versus a reasoning model, majority-vote sampling, Tree of Thoughts or graph-of-thoughts search, Reflexion retry loops, least-to-most decomposition, Thought Action Observation loops, deciding whether to keep step-by-step instructions. DO NOT USE FOR: effort tier values (use effort), agent loop bounds or checker design (use orchestrator-worker, routing, voting, or checker), per-model parameter support or billing (use test-time-compute-controls)."
---

# prompting-strategy-selection

Decide how to prompt a call before you add scripted reasoning. The 2026 vendor guides say the same thing about models that have a reasoning mode: a handwritten step-by-step plan is often redundant or harmful, and you should test it against the bare prompt. Most research prompting families (self-consistency, Tree of Thoughts, Reflexion, least-to-most) have paper evidence on older or math-only tasks and no named vendor switch.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- A prompt tells the model to think step by step, and the model already has a reasoning mode
- Choosing between majority voting, search, reflection, or decomposition for a task with a checkable answer
- Converting a ReAct-style text loop into a production design
- Deciding whether a long prompt should be split into several calls

## When Not to Use

- Picking an effort tier (use `effort`)
- Bounding a multi-call loop or choosing an orchestrator (use `orchestrator-worker`, `routing`, `voting`, or `checker`)
- Checking which parameter a model accepts or what it bills (use `test-time-compute-controls`)

## Default rule for models with a reasoning mode

1. Send the task and the outcome you want. Do not add a numbered plan.
2. If output quality is poor, compare the bare prompt against one version with explicit step-by-step instructions, on the same inputs.
3. Keep the step-by-step version only if it wins on your measure.
4. If the model returns no visible reasoning, that is expected. Do not ask it to write its reasoning out; Anthropic says always-on thinking models may decline that request.

## Family status

| Family | 2026 status in vendor guides | Where the evidence is |
| --- | --- | --- |
| Chain-of-thought | Redundant on reasoning models; OpenAI says avoid it. Anthropic keeps it only as a fallback when thinking is off. | Strong on math and symbolic tasks; weak elsewhere (Sprague et al., ICLR 2025) |
| Self-consistency | Not an API switch. A caller-side loop over sampled answers. | Math and fixed-answer tasks on PaLM-540B, 2022 |
| Tree of Thoughts and graph search | Not in vendor guides. | GPT-4 era; authors say search may be unnecessary for tasks the model already solves |
| Reflexion | Not in vendor guides. | A 2026 equal-token study on Qwen2.5 1.5B to 7B finds it loses to repeated sampling |
| Least-to-most | Not in vendor guides. Google's caller-side splitting is a related but weaker idea. | Strong on SCAN length split; little gain on GSM8K |
| ReAct (text Thought, Action, Observation) | Replaced by native tool calling and stored reasoning items | 2022 paper; the production loop is the tool API |

## Decision guide

- Task has a single checkable answer and the budget allows many samples: a vote over sampled answers can help. Measure at matched token cost.
- Task needs an external tool or lookup: use native tool calling, not a text ReAct format.
- Output must be inspected between steps for audit: use explicit prompt chaining, one call per stage.
- One prompt asks for several unrelated actions (summarize, extract, translate, draft): split it into separate calls. This is caller-side decomposition, not least-to-most.
- Reflection or self-correction: only with an external checker. Asking a model to correct itself without feedback often makes it worse (Huang et al., as summarized in Mirzaei 2026).

## Workflow

1. Identify the model. Does it have a reasoning mode that is on by default? If yes, start from the default rule above.
2. Write the bare prompt: the task, the inputs, the output format, and the acceptance criterion.
3. Run a paired test: bare prompt against the family under evaluation, on the same inputs, reporting quality and tokens.
4. Keep the family only when it wins at matched cost.
5. Record the result next to the prompt so the next person does not repeat the test.

## Validation

- [ ] The bare-prompt baseline was run before any scripted reasoning was added
- [ ] Any family used has a measured gain at matched token cost
- [ ] No prompt asks a reasoning model to write out its thinking
- [ ] Tool use goes through the native tool API, not a parsed text format
- [ ] `scripts/validate.ps1` exits 0

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Keeping "think step by step" on a reasoning model out of habit | Test the bare prompt first |
| Reading an equal-token math result as a verdict on frontier models | The 2026 Reflexion study covers models up to 7B and math only |
| Using self-consistency on free-form answers | It needs a discrete answer that can be parsed and voted on |
| Splitting prompts without checking the output of each step | Log intermediate outputs when splitting, so failures can be traced |

Sources and paper details are in `references/family-evidence.md`.
