# Close implementation contracts and references

Read for implementation-ready designs, interface reviews, or engineering questions left unanswered by a canvas. Apply only to the agreed boundary and relevant dependencies. A named return type or plausible method list alone is not an implementable contract.

## Derive the answer from the system

Trace **requirement → participating consumer → decision/action → required field or operation**. Inspect callers, adapters, stores, UI/operator flows and failure paths that actually use the boundary. For each consequential field, explain who produces it, who reads it, which behavior changes because of it, and why existing information cannot suffice. Eliminate speculative fields and duplicated sources of truth; do not build a universal registry or new service merely to organize the explanation.

When answering an engineering question, identify its stable ID, the uncertainty, the owning boundary, affected consumers and any constraint from existing source. Work through an actual normal/failure/extension scenario before selecting the contract. Supply a reasoned scoped default when the choice can be made within the authorized design; seek human input when missing facts materially change the design. Do not convert every unresolved implementation choice into a blocking question.

## Define enough to implement

Close the reachable public contract at the selected depth: each relevant named type, enum, identifier and error resolves to a definition, an inspected external contract/source, or an explicit deferred boundary with its consequence. Stop at existing external APIs, standard primitives and out-of-scope internals. Do not recursively specify an entire dependency ecosystem.

For a data contract, specify the fields, types/units, optionality, legal values and defaults; identity/scope, producer and lifetime; invariants and invalid/missing/unknown behavior where applicable. Capability or configuration descriptions need their operational meaning: availability for which scope/revision, who establishes it, when it is refreshed, and what callers do when unsupported, stale or unknown. Add these only when the system needs them.

For each relevant method, specify:

- Exact signature and input types, including caller/authority context and preconditions where required.
- Result shape, legal success/partial/terminal outcomes and what a receipt actually guarantees.
- Named error conditions and caller response; distinguish deterministic rejection, transient failure and an uncertain effect when relevant.
- State/effects and ownership, ordering/durability point, retry/idempotency, cancellation/deadline and concurrency rules needed by participating consumers.

Keep examples subordinate to the contract; an example payload does not define all valid values. Leave facts not established by source or tests labelled as proposals. A chosen timeout, supported mode or fallback is a **scoped design default** with rationale, scope and reconsideration trigger, not a provider guarantee. Distinguish unsupported, unknown and absent only where callers behave differently. Contracts should not promise atomicity, isolation or replay safety beyond the actual mechanism.

## Make the reasoning inspectable

Give consequential questions, definitions, decisions and proof items stable IDs. They may share a compact node when the answer is simple; add a detail board only when it improves inspection. For a decision, record the question/requirement, selected answer and status, rationale from consumers and constraints, a viable alternative, consequences and remaining uncertainty. Consequences should cover the affected behavior/data/failure and quality/change costs, not a generic benefit list. Reflect those consequences back against the original requirements and neighboring decisions; revise a choice when it creates a contradiction or shifts an unacceptable cost to another consumer.

Connect consumers to the canonical definition, the definition to the decision that chose it, and the decision to evidence or a discriminating proof plan. Evidence identifies the observed source/test and what it supports; a planned check records scenario, expected result and which claim it would challenge. Preserve rejected/deferred choices when useful to future changes. Do not present a resolved design question as runtime proof.

In portable scenes, use optional `node.references` for these typed-by-label links across boards; the inspector provides outgoing and incoming navigation. Use `concept` only for appearances of the same semantic object. Keep source citations in `source`/`sources`. In native canvases, supply equivalent navigable links/portals. Searchable prose mentioning an ID is not a substitute for a working link when the selected depth requires traceability.

## Propagate and check closure

Update the canonical contract and all affected interface, data, sequence, activity/state and deployment/quality views that exist in scope. Check their inputs, outcomes, error branches, ownership and guarantees against each other; update the decision and proof backlog when consequences change. Preserve IDs and layouts where meaning survives. Do not add an unrelated diagram family solely to satisfy a checklist.

Walk from a consumer to every relevant signature and named type, from the answer to its requirement/decision, and back from the definition to affected consumers. Trace a failure and a likely extension: can an engineer determine the payload, branch and owner without inventing semantics? Record genuinely remaining gaps and their implementation consequences. Scene validation proves link integrity, not semantic closure or operational correctness.
