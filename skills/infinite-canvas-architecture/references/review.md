# Architecture canvas review

Review semantics, consequences and usability. Visual quality is useful only when it helps expose the system and its uncertainty.

## Model review

Trace one normal operation, one failure/retry, one authority change where relevant, and one likely extension. Follow the data and dependency path through every responsibility that actually participates. Check:

- Missing actors or external calls, including a model/provider invocation omitted between a reservation and tool execution.
- Collapsed principal/session/host identities, ambiguous source/target roles, false many-to-many joins and writer cardinalities.
- Acknowledgements represented as completion or unverified viewing.
- Implied atomicity across independent stores/services, unsafe replay and restored-state gaps.
- Isolation, privacy, version compatibility or scale guarantees unsupported by the inspected mechanism.
- A new service/layer without a demonstrated need or a simpler alternative comparison.
- A repair that fixes a symptom while leaving the shared cause or affected consumers unchanged.
- Changes that spread implementation details through unrelated contracts or make comprehension worse.
- Relevant named types/results/errors that have no reachable definition, or fields with no requirement and consuming behavior.
- Scoped defaults presented as observed guarantees, and decisions marked proven without discriminating evidence.
- A changed contract whose connected views still use old inputs, outcomes, ownership or failure behavior.

State what the canvas revealed and the evidence. Do not claim that a previously known issue was discovered by visualization. Do not claim what would certainly have happened without the canvas. Compare actual corrections and changed decisions, not the diagram's size.

## Validation plan

For important quality scenarios, identify baseline, target/limit, realistic workload, method and discriminating evidence. Validate affected and unaffected consumers, regressions, failure ordering and a realistic extension. Include an unfamiliar-developer task to trace/debug/change the system where developer understanding matters.

Separate structural/schema checks, DOM/controller checks, rendered readability, actual browser/native interaction, and runtime architectural proof. None substitutes for the others. Existing tests from an earlier implementation do not prove proposed APIs, isolation or fleet targets.

## Canvas checks

Validate unique IDs, all endpoints and explicit references, board containment, sources, cardinality roles and supported UML markers. Inspect text/label overflow, hidden/crossing connectors, readable defaults and zoomed detail. Verify pan/zoom, target selection, search, cross-view links, layout persistence and JSON/SVG export. For implementation detail, follow a consumer to its contract/definition and the linked decision/evidence, then follow incoming links back to affected consumers. Keep user layout stable where feasible and make stale-layout migration explicit when needed.

A native import requires readback of actual page/shapes and visual inspection. If disconnected, accurately report that limitation and deliver the portable atlas where allowed. Never repeat an uncertain native mutation just to obtain a success response.

## Update loop

Record the consequential decision, uncertainty, proposed intervention and expected consequences. Change the smallest sufficient model/code boundary. Update its related views and contracts, preserve sources/status, and rerun only checks affected by the change or unresolved concern. Keep a prioritized proof/change backlog after the agreed scope is complete.
