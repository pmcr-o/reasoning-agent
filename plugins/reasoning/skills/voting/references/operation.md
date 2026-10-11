# voting

The 7 October 2026 report says voting is one parallel wave plus programmatic aggregation, and the sample count is fixed before that wave. The report does not publish a universal sample count. This contract fixes `cap` at 2, the lightest parallel sample, and sets `wave` to `one-shot`. That 2 is a contract constant, not a figure from the report. A missing sample cap exits non-zero. `default` stays `lightest`.

`scripts/validate.ps1` reads `assets/contract.json` only. It does not call the network, read an API key, or invoke a model.

Self-consistency, debate, tree or graph search, Reflexion, least-to-most, and mixture-of-agents are papers. They are not this skill.
