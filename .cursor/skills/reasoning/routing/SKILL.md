---
name: routing
description: "Route easy work to a lighter model and hard work to a stronger model, and keep a required cap. USE FOR: a classifier that sends easy or common work to a lighter model and hard or unusual work to a stronger model. DO NOT USE FOR: reasoning effort (effort), a native tool loop (tool-loop), orchestrator-worker, a separate checker call (checker), one-shot votes (voting), or a paper-only family."
license: MIT
---

# routing

Route easy work to a lighter model and hard work to a stronger model only when the local contract has a cap. This skill does not call a model.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- Easy or common work goes to a lighter model
- Hard or unusual work goes to a stronger model
- A cap is required before the route runs

## When Not to Use

- Raising reasoning effort, a native tool loop, orchestrator-worker, a separate checker call, or one-shot votes
- Chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, or mixture-of-agents

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| assets/contract.json | Yes | Local contract. The route cap is `cap` |

## Workflow

1. Read `references/operation.md`.
2. Run `scripts/validate.ps1`.
3. Stop when the script exits non-zero. A missing cap is that failure.

## Validation

- [ ] `scripts/validate.ps1` exits 0 when the cap is a positive integer, the default is lightest, and network, apiKey, and modelInvocation are false
- [ ] The same script exits non-zero when the required cap is missing
- [ ] Validation fails if `scripts/`, `references/`, or `assets/` is missing

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Sending every request to the stronger model | Keep the easy path on the lighter model |
| Routing with no cap | The script exits non-zero |
