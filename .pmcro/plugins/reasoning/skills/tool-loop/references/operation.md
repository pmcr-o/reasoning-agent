# tool-loop

The 7 October 2026 report says a native tool loop declares JSON-schema tools, reads the call id, and returns the tool result. The production setting keeps a finite stop. The report names 10 turns on the OpenAI Agents SDK unless the caller removes that limit. This contract sets `cap` to 10. A missing cap exits non-zero. `default` stays `lightest`.

`scripts/validate.ps1` reads `assets/contract.json` only. It does not call the network, read an API key, or invoke a model.

Chain-of-thought, self-consistency, tree or graph search, Reflexion, least-to-most, debate, and mixture-of-agents are papers. They are not this skill.
