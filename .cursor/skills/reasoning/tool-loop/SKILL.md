---
name: tool-loop
description: "Run a native tool-calling loop only when a finite stop cap is present. USE FOR: JSON-schema tools, a call id, a tool result, and a required stop cap. DO NOT USE FOR: reasoning effort (effort), orchestrator-worker, routing, a separate checker call (checker), one-shot votes (voting), chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, or mixture-of-agents."
license: MIT
---

# tool-loop

Run a native tool-calling loop only when the local contract has a finite stop cap. This skill does not call a model.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- The caller declares JSON-schema tools, a call id, and a tool result
- A stop cap must be present before the loop starts

## When Not to Use

- Reasoning effort, orchestrator-worker, routing, a separate checker call, or one-shot votes
- Chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, or mixture-of-agents

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| assets/contract.json | Yes | Local contract. The stop cap is `cap` |

## Workflow

1. Read `references/operation.md`.
2. Run `scripts/validate.ps1`.
3. Stop when the script exits non-zero. A missing stop cap is that failure.

## Validation

- [ ] `scripts/validate.ps1` exits 0 when the stop cap is a positive integer, the default is lightest, and network, apiKey, and modelInvocation are false
- [ ] The same script exits non-zero when the required cap is missing
- [ ] Validation fails if `scripts/`, `references/`, or `assets/` is missing

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Omitting the stop cap | The script exits non-zero |
| Hand-writing a paper tool scaffold | Keep the native tool contract and the cap |
