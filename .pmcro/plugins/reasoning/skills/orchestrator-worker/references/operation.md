# orchestrator-worker

The 7 October 2026 report says ship orchestrator-worker with a finite worker and iteration cap. The orchestrator page publishes no numeric worker count. This contract uses the finite turn cap the report names for the OpenAI Agents SDK, 10. A missing turn cap exits non-zero. `default` stays `lightest`.

`scripts/validate.ps1` reads `assets/contract.json` only. It does not call the network, read an API key, or invoke a model.

Debate and mixture-of-agents are papers. They are not this skill.
