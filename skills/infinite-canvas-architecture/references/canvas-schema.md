# Portable scene schema

Author the architecture in JSON; the renderer supplies an interactive viewer, not the design itself. See [example-scene.json](../assets/example-scene.json) for a small appointment-system example with shared concepts, a contract, quality targets and an unresolved causal hypothesis.

## Root

`schemaVersion: 1`, stable `id`, human `title`, optional `status`, `sourceRevision` and `layoutVersion`; arrays `boards`, `nodes`, `edges`, optional `sources`. At least one board and node are required. A changed `layoutVersion` starts a fresh browser layout namespace; otherwise stable node IDs retain saved positions. Keep proposed interfaces and targets labelled rather than presenting them as current APIs or measurements.

`sources` entries have a unique `id`, `label`, optional `href` and `note`. A board/node `source` is a declared source ID or the same object shape. Supplied prompt/session context can use a label and note without an invented URL. Link to actual source documents or primary documentation. HTTP, HTTPS, relative and file links are supported; executable URL schemes are rejected. Local documents are not automatically copied or exposed by the preview server.

## Boards and nodes

A board is `{id, title, subtitle?, source?, x?, y?, w?, h?, columns?}`. Coordinates are absolute world coordinates. Defaults place boards in three columns; a board defaults to 2300 × 1900. Titles/subtitles should be short enough to read in the allotted area.

A node is `{id, board, title, kind?, concept?, status?, lines?, detail?, invariants?, source?, references?, x?, y?, w?, h?}`:

- `kind`: component, authority, store, tool, entity, interface, activity, decision, state or boundary. These choose visual treatments, not runtime roles.
- `concept`: a stable semantic identity shared by nodes in different diagrams; the inspector links matching concepts. Do not equate distinct identities just to create links.
- `status`: e.g. observed, confirmed requirement, proposed, hypothesis, unknown or measured. Attach evidence for measured/observed claims.
- `lines`: concise visible fields, methods or behavior. Longer explanation belongs in `detail` and `invariants`, which appear on inspection.
- `references`: optional array of `{target, label?}`; `target` is an existing node ID on any board and `label` describes the link, e.g. "Defined by", "Answers", "Chosen because" or "Validated by". The inspector shows clickable outgoing and incoming links. This links different concepts without drawing cross-board edges or conflating their identity. Omitted references remain compatible with schema version 1; duplicate targets and self-references are rejected. External evidence belongs in `source`, not a node target.
- Default width is 620; height grows for wrapped contract text. Automatic node layout uses three columns within its board. Expand/rearrange boards when the validator warns of overflow. Coordinates supplied for individual nodes override automatic placement.

IDs use 1–100 letters/digits/dot/underscore/hyphen and start with a letter or digit. IDs must be unique within their object family. Finite geometry is required. The normalizer reports layout warnings; it cannot assess a cardinality, trust claim or causal explanation.

For example, a consumer can carry `"references": [{"target":"booking-contract","label":"Result defined by"}]`, while that definition links to a decision node and its proof plan. Those targets must be authored nodes. Reference links are inspector navigation; they are not extra runtime dependencies or visible SVG connectors.

## Relationships

An edge is `{id?, source, target, board?, label?, relation?, sourceCard?, targetCard?, note?, route?}`. `source` and `target` are node IDs in the same board. For cross-view navigation use node references, or repeat the same concept in relevant views, rather than drawing an unreadable line across the entire atlas.

`relation` defaults to dependency. `implements` uses a dashed line and hollow triangle; `generalization` a solid line and hollow triangle. Other relations use directional arrows. Describe direction and endpoint roles in `note` when ambiguous. ER multiplicities use `sourceCard`/`targetCard`, e.g. `1`, `0..1`, `0..*`; these are authored semantic claims, not computed from storage.

Optional routing:

```json
{"sourceSide":"right","targetSide":"left","sourceOffset":0,"targetOffset":0,
 "via":[[900,400],[900,700]],"label":[900,550],"labelAngle":-90}
```

Sides are top/bottom/left/right. `via` and `label` use world coordinates. Omitted routing produces a curve between node boundaries. Routed control points remain fixed when users move an endpoint; inspect/edit the route if changing the layout substantially.

## Sequences

A board can contain `sequence: {participants, messages, notes?, rowGap?}`. Participants are `{id,label,concept?}`. Messages are `[sourceIndex,targetIndex,label,"request"|"return"]`, with zero-based distinct participant indexes. For local self-calls use activity nodes. `notes` hold invariants displayed when inspecting a message. Lifelines occupy the board height; `rowGap` defaults according to message count and board height. Keep sequence boards free of overlapping automatically placed nodes or position supplementary nodes explicitly.

## Render and preview

```sh
python /absolute/skill/scripts/validate_canvas.py scene.json
python /absolute/skill/scripts/render_canvas.py scene.json --output /task-owned/atlas
python /absolute/skill/scripts/serve_canvas.py /task-owned/atlas
```

Output is `index.html`, `atlas.json`, `atlas.svg`, `view-<board-id>.svg` and `canvas-manifest.json`. HTML works directly offline. The loopback preview serves only manifest-listed artifacts, not source directories. Existing generated atlases can be rebuilt; unrelated files are retained. The renderer refuses collisions in an unmanaged directory unless `--overwrite` is explicitly supplied.

Optional `--penpot-file-id <observed-authorized-file-id>` adds a native import starter. It creates a new native page when later executed through a connected Penpot plugin. It neither connects nor publishes; review the current API, actual file and native rendering before use. Preserve IDs when updating the authored scene, regenerate connected views, and distinguish structural/DOM checks from live browser/native interaction and architectural validation.
