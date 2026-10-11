# Dialogic intent-refinement contract

The raw user utterance is immutable provenance and may be messy, abbreviated, speech-to-text corrupted, or incomplete. PMCR-O never silently rewrites that source.

The loop operates on a versioned `intentHypothesis`. Each phase may narrow or clarify it within its authority and product boundary. Each hypothesis records preserved constraints, remaining ambiguities, source references, confidence, and an explicit delta from its parent frame.

CHECK asks whether the hypothesis is supported by the raw source and validated evidence. REFLECT turns the difference between intended/observed meaning into one earned constraint and one unexecuted next seed. A new cycle may then refine the hypothesis again.

The objective is the best-current validated interpretation of user intent—not a claim of mind-reading or access to hidden thoughts.
