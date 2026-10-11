---
name: checker
description: "Make a separate checker call with a required stop cap. The same call must not grade itself. USE FOR: an evaluator, a screening call, or a critic that is a different call from the call that produced the work. DO NOT USE FOR: the same call grading itself, treating a shared Windows account as a second principal, the pmcro check skill, voting, effort, tool-loop, orchestrator-worker, routing, or a paper-only family."
license: MIT
---

# checker

Make one separate checker call. The call that produced the work does not grade itself. A shared Windows account does not prove a second principal. This skill does not call a model.

```powershell
pwsh -NoProfile -File scripts/validate.ps1
```

## When to Use

- An evaluator, screening call, or critic is a different call from the producer
- A stop cap is required on that checker call

## When Not to Use

- The same call grading itself
- Treating a shared Windows account as a second principal
- The pmcro check skill, voting, effort, tool-loop, orchestrator-worker, or routing
- Chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, or mixture-of-agents

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| assets/contract.json | Yes | Local contract. The stop cap is `cap`. `separateCall` is true |

## Workflow

1. Read `references/operation.md`.
2. Run `scripts/validate.ps1`.
3. Stop when the script exits non-zero. A missing cap is that failure.

## Validation

- [ ] `scripts/validate.ps1` exits 0 when the cap is present, the call is separate, the default is lightest, and network, apiKey, and modelInvocation are false
- [ ] The same script exits non-zero when the required cap is missing
- [ ] Validation fails if `scripts/`, `references/`, or `assets/` is missing

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| The producer grades its own output | Require `separateCall` and refuse `sameCallGradesItself` |
| A shared Windows account is offered as a second principal | It does not prove a second principal. The contract is a separate call |
