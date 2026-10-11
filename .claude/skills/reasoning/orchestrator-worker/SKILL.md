---
name: orchestrator-worker
description: "Run one orchestrator and its workers only with a required finite turn cap. USE FOR: orchestrator-workers, a manager that calls specialists, and a worker turn cap. DO NOT USE FOR: reasoning effort (effort), a native tool loop (tool-loop), routing, a separate checker call (checker), one-shot votes (voting), debate, or mixture-of-agents."
license: MIT
---

# orchestrator-worker

Run one orchestrator and its workers only when the local contract has a finite turn cap. This skill does not call a model.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- One orchestrator hands work to workers
- A turn cap must be present before the workers start

## When Not to Use

- Reasoning effort, a native tool loop, routing, a separate checker call, or one-shot votes
- Debate or mixture-of-agents

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| assets/contract.json | Yes | Local contract. The turn cap is `cap` |

## Workflow

1. Read `references/operation.md`.
2. Run `scripts/validate.ps1`.
3. Stop when the script exits non-zero. A missing turn cap is that failure.

## Validation

- [ ] `scripts/validate.ps1` exits 0 when the turn cap is a positive integer, the default is lightest, and network, apiKey, and modelInvocation are false
- [ ] The same script exits non-zero when the required cap is missing
- [ ] Validation fails if `scripts/`, `references/`, or `assets/` is missing

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Letting the worker count float with no cap | Keep `cap` in the local contract |
| Splitting into a debate | Debate is a paper and is not this skill |
