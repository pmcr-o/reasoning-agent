---
name: dialogic-awareness
description: "Build a visible inter-agent reasoning surface from PMCR-O dialogic frames: problem model, evidence, uncertainty, rationale summary, challenge/response, dependency edges, and awareness delta; never hidden chain-of-thought."
---
# dialogic-awareness
Spoken route: `@dialogic-awareness-agent /reasoning:dialogic-awareness`.

## Product
A bounded conversation graph that lets a person inspect how a **messy source utterance becomes a clearer, checked intent hypothesis** across PMCR-O agents without exposing or requiring private chain-of-thought.

Each frame says: **I AM <speaker>; THOU is <listener>; this is the immutable source I am interpreting; this is my current intent hypothesis; these source fragments/constraints support it; this is what remains ambiguous; this is the concise rationale I can externalize; this is what I am asking/challenging; this is how the intent hypothesis changed.**

## Workflow
1. Preserve the immutable raw utterance/source reference. Never rewrite or replace the user's original messy input.
2. Treat `intentHypothesis` as versioned derived state. A newer hypothesis must name its parent hypothesis/frame and explain the delta; it never replaces the raw source.
3. Read/emit only the visible dialogic frame schema in `assets/dialogic-awareness.schema.json`.
4. Use `scripts/operate.py validate --input <frames.json>` to verify a conversation graph.
5. Use `scripts/operate.py render --input <frames.json>` to render a readable agent-to-agent transcript.
6. Do not infer hidden chain-of-thought. `rationaleSummary` is a concise external explanation, not private reasoning.
7. Dialogue may create dependency edges, but never authority. Phase order and inherited authority ceiling remain unchanged.
8. A later PLAN may consume a prior frame only when its evidence/resource references are admissible.

## Reasoning-agent composition
This skill may call registered `reasoning` skills such as routing, effort, voting, checker, or orchestrator-worker to choose *how much* reasoning work to request. Those skills do not change the dialogic evidence/authority contract.

## Validation
Run `scripts/validate.ps1`.

## Intent refinement law
`rawUtteranceRef` is immutable provenance. `intentHypothesis` is a derived, versioned interpretation that may become clearer through repeated PMCR-O cycles. CHECK validates whether the interpretation is supported by source/evidence and whether important ambiguity remains. REFLECT records the learned interpretation constraint and emits a next seed; the next cycle may refine the hypothesis again.

Use registered `reasoning/prompting-strategy-selection` when a different prompting strategy is needed to clarify an intent hypothesis. Prompt engineering changes the **interpretation procedure**, not the original utterance.
