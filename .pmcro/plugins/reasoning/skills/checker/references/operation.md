# checker

The 7 October 2026 report says ship a separate checker call with a stop. The call that produced the work does not grade itself. This contract sets `cap` to 1, one separate call, then stop. A missing cap exits non-zero. `default` stays `lightest`.

`separateCall` is true. `sameCallGradesItself` is false. `sharedAccountProvesSecondPrincipal` is false. A shared Windows account does not prove a second principal.

`scripts/validate.ps1` reads `assets/contract.json` only. It does not call the network, read an API key, or invoke a model. This skill does not issue a trail verdict.

Chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, and mixture-of-agents are papers. They are not this skill.
