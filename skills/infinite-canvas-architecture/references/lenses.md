# Architecture coverage and judgment lenses

Use this inventory to find consequential relationships. Classify each lens as included, excluded, deferred or unknown at the selected scope. Expand the relevant lenses, not every row into a service. Extreme breadth is broad investigation; extreme depth is stronger reasoning and evidence, not decorative diagram density.

## Quality and causal judgment

| Principle | Inspectable representation | Evidence or useful question |
| --- | --- | --- |
| Define quality concretely | QualityScenario: trigger, context/workload, response, measure, bound and evidence | Correctness, real latency/resource/cost, readability and likely change effort |
| Understand beyond the immediate task | Data/dependency/resource map, consumers and operating constraints | What shared mechanism influences this result? |
| Distinguish symptoms and causes | Observation → candidate mechanism → competing explanation → discriminating test | Does the mechanism explain the symptom and its other effects? |
| Match scope to cause | Local/shared/broader intervention alternatives and consumer impact | What is the smallest sufficient repair? What evidence requires widening it? |
| Explicit assumptions | Requirement/fact/default/hypothesis/question ledger | Which unknown could reverse the preferred design? |
| Complexity earns its place | Decision → demonstrated need → simpler alternative → benefit/cost/dependencies | Can an existing module or colocated responsibility meet the requirement? |
| Boundaries follow responsibility and change | Contract/ownership map plus likely ChangeScenario | Does the same responsibility stay coherent? Does a likely change stay localized? |
| Verify whole-system consequences | Affected and unaffected paths, regressions, failures, realistic extension | Did a local fix merely shift the cost or break another consumer? |
| Developer understanding is a property | Unfamiliar-developer walkthrough/debug/change task | Can someone trace responsibility without hidden session knowledge? |

A quality scenario may have an unknown threshold. Label that gap and guide the human to a useful bound. A proposed target is not a measurement. Do not invent confidence percentages, performance wins, development times or correctness guarantees to make a diagram look complete.

## System angles

| Lens | What to investigate | Views when useful |
| --- | --- | --- |
| Purpose and value | Problem, users/jobs, outcomes, non-goals, economic constraints | Context, journey, quality scenarios |
| Domain | Concepts, terminology, entity lifetimes, associations and cardinalities | ER/domain model |
| Identity and ownership | Actors, principals, sessions/contexts, hosts/incarnations, tenant boundaries | Identity graph and responsibility matrix |
| Behavior | Normal/alternate flows, decisions, side effects and observations | Activity/function UML, sequence |
| Responsibilities | Cohesion, who decides, authoritative state, contracts and consumers | Component/layer/contract views |
| Interfaces | Real versus proposed API, payload/return/errors, streaming, pagination and versions | Interface/class UML, protocol envelopes |
| Dependencies | Calls, data/control flow, shared resources, upstream/downstream coupling | Dependency and cause/impact graph |
| Deployment | Local/cloud/device/edge, replicas, provider capabilities, supervision | Deployment and trust boundaries |
| Data | Schema, invariants, provenance, data quality, indexing and lifecycle | ER, data flow, storage ownership |
| Persistence | Acknowledgement barriers, checkpoints, state provenance, recovery-point window | Commit/recovery sequence and state |
| Consistency | Transactions, independent durability domains, reconciliation, cache staleness | Transaction/intent/outbox view |
| Concurrency | Admission, writer ownership, locks/fences, fairness, cancellation and races | State/sequence/race cases |
| Distributed systems | Discovery, membership, leases, partitions, leader/failover, routing, clock assumptions | Federation and failure topology |
| Effects and retries | Stable request/digest, duplicate admission, uncertain external effects, billing attempts | Retry/reconciliation sequence |
| Security | Assets, attackers, principals, capabilities, trust boundaries, secret/privileged access | Threat and permission views |
| Privacy and context | Audiences, retention, disclosure, inference and cross-context data transfer | Projection/audience/context model |
| Performance | Real workload, critical path, saturation, hot/cold paths, shared bottlenecks | Costed path, queues and benchmarks |
| Resource efficiency | CPU/memory/IO/bandwidth, bounded buffers, caches, energy where material | Resource budgets and ownership |
| Scalability | Distribution versus one-host capacity, sparse subscriptions, fan-out, quotas | Scale topology and load envelope |
| Reliability | Crash, timeout, degradation, recovery, restore/rollback and disaster handling | Fault tree, failure matrix, recovery state |
| Observability | Correlation, diagnostics, metrics, safe logs, audit and reproducibility | Evidence/instrumentation map |
| UX | Intent, states, feedback, target/audience clarity, onboarding, errors and recovery | Journeys, state matrix, UI/backend contracts |
| Accessibility/localization | Keyboard/focus, assistive technology, contrast, RTL/locale, device limits | Interaction and acceptance scenarios |
| Developer experience | Traceability, testing, debugging, comprehension, code boundaries and setup | Walkthrough/change-impact map |
| Evolution | Compatibility, schema/protocol upgrades, migrations, rollback, deprecation | Change scenarios and migration sequence |
| Extensibility | Plugins, capability negotiation, replay/approval integration, adapters | Extension/interface compatibility matrix |
| Delivery and operations | Build/artifact immutability, rollout, ownership/on-call, configuration, runbooks | Deployment/change and operating model |
| Cost and business effects | Provisioning/model/operation costs, budgets, pricing assumptions, abuse limits | Separate cost/reservation ledgers |
| Governance and organizational constraints | Data/control accountability, approvals, responsibilities and material requirements | Decision/authority and evidence traceability |
| Interoperability and ecosystems | External contracts, vendor boundaries, portability, networks/tenants and integration | Context/interface/federation views |

Use formal methods, fault trees, privacy/compliance analysis or capacity models when the risk/scope warrants them. Do not invent a domain requirement or turn every angle into an unsolicited compliance checklist.

## Test whether a structure is proportionate

For a consequential abstraction, service, queue or data boundary, record:

1. The demonstrated need and the specific quality scenario it addresses.
2. A simpler alternative and why it is sufficient or insufficient.
3. Affected consumers and unchanged paths.
4. New failure modes, dependencies, operating burden and cognitive cost.
5. A likely extension/change and whether the boundary localizes it.
6. An observable proof that would accept or reject the decision.

For example, a suspected slow input path could arise from a global serial queue, repeated catalog serialization, an overloaded store or UI rendering. Compare these mechanisms using traces/load fixtures before adding another queue/service. A shared cause needs a repair for its affected consumers; a local defect does not justify rebuilding the system.

## Breadth without losing readability

Maintain an overview with links to subsystem, contract, quality and failure views. Reuse stable concepts across views. Group by meaningful responsibility/trust/lifecycle, not arbitrary colors or equal card counts. For extreme work, split deep atlases by subsystem while preserving explicit cross-atlas references and a coverage frontier.

The canvas should help a human answer: what happens, who owns it, what depends on it, what can fail, why this boundary exists, how to change it, and what evidence supports it.
