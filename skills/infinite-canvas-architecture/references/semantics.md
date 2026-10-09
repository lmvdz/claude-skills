# Semantic model and diagram rules

Read before deriving entities and interfaces. A diagram can make a wrong assumption look precise; validate the meaning before polishing connectors.

## Identity and roles

Keep person/owner, authenticated principal, logical agent/worker, conversation/session/context, process/host and host incarnation separate where the domain distinguishes their lifetimes. An actor may join many networks and run multiple contexts. A display label or shared machine is not authority. If these are intentionally combined, record the constraint rather than assuming it.

Represent many-to-many associations with an explicit join record and its scope/lifetime. Separate source and target roles even if both reference the same entity type. Optional human/source contexts need optional cardinalities rather than invented agent sessions. One process can own several leases while one store has at most one current writer; state the actual ownership unit.

## Useful view families

- Context/component: actors, responsibilities, dependencies, data/control paths and excluded responsibilities.
- ER/domain: identities, keys/roles, ownership, cardinalities, lifecycle and invariants; conceptual models are not implemented SQL.
- Interface/class UML: public operations and return/error behavior, uses versus implements, proposed versus inspected signatures.
- Function/activity UML: decision gates, normal/alternate/error paths, authority/effects, cancellation and terminal states.
- Sequence UML: real exchanges in time, including model/external-provider calls, commits, acknowledgements, returns and uncertain gaps.
- State UML: independent lifecycle dimensions, transitions, triggers, guards, pause/stop and recovery.
- Deployment/trust: runtime versus tools/data/credentials, logical module versus separate process/service/machine, actual enforced isolation.
- Quality/cause/change: requirement, mechanism, intervention alternatives, consumers, costs, validation and developer walkthrough.

Use correct relationship notation and a small legend. A hollow triangle denotes generalization/implementation; a message return is not an ownership edge. Labels/cardinalities must remain readable and connectors must not disappear behind an intervening box. Rotate or route labels only when that improves inspection; keep the inspector as a readable alternative.

## Timing and guarantees

Observation, message receipt, owner viewing, acceptance, admission, running and completion are different states. Attachment lifetime need not own task lifetime. Cancellation of a wait is not always cancellation of admitted work. An explicit stop differs from a process crash.

Exactly-once admission is not exactly-once external effects or billing. Authorization, a local commit, an external ledger and a client acknowledgement may be independent durability domains. Show partial linkage, idempotent reconciliation and lost-response behavior. Prefer a real combined transaction where available rather than introducing distributed intents needlessly.

Current policy/spend references do not prove a restored task store is complete. A snapshot can lose a later intent/result. Show recovery points, checkpoint evidence and uncertain-effect handling if relevant; do not draw an old snapshot directly to Resume merely because a grant is valid.

Filtering projections does not isolate model context. Confidential audiences need isolated contexts or explicit shared-context disclosure. A VM containing shell tools and host secrets does not automatically protect those secrets. Model/gateway/credential helpers also need an independent lifetime if work must outlive the UI.

## Evidence and proposals

Attach sources and scope to factual claims. A reusable foundation can have target changes; label both. Mark hypothetical causes and API sketches as such. Keep candidates/rejected alternatives and proof gaps inspectable without implying they are chosen deployed services. Distinguish measured results from targets and source capabilities from hoped-for behavior.

Give each semantic object a stable ID. Use the same concept key for appearances of that object across views; different private contexts retain different session IDs. Renaming does not retarget requests or collapse actors. Preserve entity/relationship IDs during updates where meaning stays the same.
