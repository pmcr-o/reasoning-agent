---
name: voting
description: "Take one-shot parallel votes and fix the sample cap before the wave. USE FOR: one parallel vote wave and a programmatic threshold on a discrete judgment. DO NOT USE FOR: multi-round debate, self-consistency, a checker loop (checker), effort, tool-loop, orchestrator-worker, routing, tree or graph search, Reflexion, least-to-most, or mixture-of-agents."
license: MIT
---

# voting

Take one-shot parallel votes only after the sample cap is fixed. This skill does not call a model.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- One parallel wave votes on a discrete judgment
- The sample cap is fixed before that wave

## When Not to Use

- Multi-round debate, self-consistency, or a separate checker call
- Effort, tool-loop, orchestrator-worker, or routing
- Tree or graph search, Reflexion, least-to-most, or mixture-of-agents

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| assets/contract.json | Yes | Local contract. The sample cap is `cap`. `wave` is `one-shot` |

## Workflow

1. Read `references/operation.md`.
2. Run `scripts/validate.ps1`.
3. Stop when the script exits non-zero. A missing sample cap is that failure.

## Validation

- [ ] `scripts/validate.ps1` exits 0 when the sample cap is a positive integer, the wave is one-shot, the default is lightest, and network, apiKey, and modelInvocation are false
- [ ] The same script exits non-zero when the required cap is missing
- [ ] Validation fails if `scripts/`, `references/`, or `assets/` is missing

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Adding rounds until the vote settles | Keep `wave` at one-shot |
| Sampling with no cap | The script exits non-zero |
