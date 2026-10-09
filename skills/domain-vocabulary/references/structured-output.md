# Optional structured content

Use this shape only when structured output or an ontology-backed handoff is useful or requested. Ordinary vocabulary content need not include JSON.

```json
{
  "title": "Example Domain Vocabulary",
  "intro": "What this vocabulary helps its audience describe.",
  "domain": "Explicit domain boundary",
  "language": "en",
  "coverage": "curated",
  "scope_note": "Audience, exclusions, and relevant version.",
  "sections": [
    {"id": "operations", "title": "Operations", "intro": "What these operations accomplish."}
  ],
  "terms": [
    {
      "id": "source-concept-id-or-local-stable-id",
      "label": "Displayed term",
      "labels": [{"text": "Displayed term", "language": "en", "role": "preferred"}],
      "kind": "concept",
      "definition": "An original, distinguishing explanation.",
      "section_id": "operations",
      "source_ids": ["source-1"],
      "notes": "Optional ambiguity, generated translation, or version qualification."
    }
  ],
  "external_terms": [],
  "relations": [],
  "sources": [
    {"id": "source-1", "title": "Source title", "locator": "Exact URL, supplied file path, or document identifier"}
  ]
}
```

Every displayed term is represented by a non-hidden label in `labels`. Keep source IDs exact; generate local stable IDs only when none exist. `kind` follows the source model or a clearly described local convention. Roles are `preferred`, `alternate`, `hidden`, and `generated`; the last distinguishes an unsupplied translation or explanatory label. Language tags remain as supplied. Notes may be omitted.

An external endpoint is `{"id": "exact-source-id", "label": "Source label if known"}`. Its label may be absent when unknown. It does not constitute a generated definition or an invented concept.

A relation is:

```json
{
  "subject": "exact-subject-id",
  "predicate": "exact-predicate-identifier",
  "object": "exact-object-id",
  "status": "asserted",
  "source_ids": ["source-1"]
}
```

Allowed statuses are `asserted`, `inferred`, and `proposed`. This shape models identifier-to-identifier relations, not literals, blank nodes, OWL expressions, or arbitrary axioms. Preserve those in the original source; do not flatten them into misleading triples. Section assignment is for presentation only. No relation is inferred from `section_id`.

Use source references only when they actually support the entry. Supplied material can be identified by a file path or document ID; offline work need not invent a URL. If working without verified sources, `source_ids` can be empty, but identify the epistemic limitation in the scope note. Empty sources do not make a claim verified.

```text
python scripts/validate_vocabulary.py vocabulary.json
python scripts/validate_vocabulary.py vocabulary.json --baseline normalized-source.json
```

The baseline needs `terms`, `relations`, and `coverage`. For `complete`, all baseline terms must appear. For `curated`, all generated term IDs must be in the baseline, and included terms preserve their recorded labels, kinds, and asserted relations involving them. A baseline can also have the full content shape. Validate the output against the original artifact as well: normalization can itself introduce errors.

## Optional prompting object

Only in prompting mode, a selected term may add this object. Its canonical label, definition, and supporting sources remain in the existing term fields.

```json
{
  "prompting": {
    "sense": "Intended interpretation of this term",
    "version": "Applicable edition/version, unspecified, or not versioned",
    "task": "Bounded task and intended deliverable",
    "definition_basis": "What the cited sources establish and any grounding limitations",
    "expansion": "Concrete task-specific instructions, including evidence, actions, and deliverable",
    "success_checks": ["Observable artifact property and the evidence used to check it"],
    "model_evidence": {
      "status": "untested",
      "applicability_note": "Standalone term use is untested; carry the expansion with the term",
      "records": []
    }
  }
}
```

All five text fields and `applicability_note` must be nonempty. `success_checks` is a nonempty array of nonempty strings. Definition grounding is reported in `definition_basis` with the term's source references; it is not a model-support score.

`model_evidence.status` is `untested` with no records, or `tested` with at least one record. Each record requires nonempty text fields `model_id`, `model_version`, `date`, `results`, and `record_locator`, plus nonempty arrays of nonempty strings `tasks` and `conditions`. Conditions are `task_only`, `term`, `definition`, `contract`, or `paraphrase`. Use an ISO date or timestamp; if no model snapshot is exposed, state that limitation in `model_version`. `results` summarizes outcomes, run counts, failures, and uncertainty. `record_locator` identifies the retained prompts, artifacts, rubric, settings, and per-run judgments described in [prompting.md](prompting.md).

`tested` means records exist, including failed experiments; it does not certify standalone term support. Use `applicability_note` to state whether the records cover the intended receiving model and context. Evidence for other versions, tasks, or conditions leaves standalone use in the intended context untested.

The validator checks field shape and the status/record invariant. It does not inspect source contents or record locators, assess the expansion or success checks, verify experiments, or determine behavioral reliability. Ordinary records without `prompting` remain valid.
