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
