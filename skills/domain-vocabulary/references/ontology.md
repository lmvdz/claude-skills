# Source-preserving ontology adaptation

## Interpret the input before simplifying

A taxonomy, SKOS concept scheme, and OWL ontology have different semantics. Determine the actual input model. Do not call an ordinary grouped glossary a formal ontology or silently convert one model into another.

The supplied artifact is authoritative for identifiers, labels, declared kinds, relations, and constraints. Retain an unchanged original or a stable source reference. The generated content is a teaching view; it is not a complete formal reserialization or a reasoner's result.

Record the intended coverage: all supplied concepts, a named subset, or a curated selection. If the source is enormous and no exhaustive request exists, choose and disclose a bounded selection. If full coverage was requested, complete it in manageable batches and reconcile the resulting inventory; a representative sample is not completion.

## Preserve identity and meaning

- Keep exact source identifiers. Labels can change across languages without changing concept identity. Identical text can label different concepts; qualify the displayed sense rather than merging IDs.
- Retain supplied preferred, alternate, and hidden labels with their language tags and roles. Hidden labels remain metadata; do not show them as endorsed human-facing aliases. An unsupplied translation or explanatory name has generated status, not an official source-label role.
- Keep concepts, classes, individuals, properties, and literals distinct. A named relation or property may itself be an entry when the audience needs to use it. Record formal restrictions without rewriting them into stronger claims.
- Preserve the direction and type of asserted relations. Do not turn “part of,” “causes,” “used for,” “related to,” or a mapping into “is a.” Multiple parents are not a defect to repair. Presentation sections do not imply hierarchy.
- Distinguish asserted, inferred, and proposed relationships. Do not invent formal edges to make the explanation flow. If derived edges are useful, state the rule or reasoner responsible; without that evidence, leave them out or label them as a proposal.
- Preserve source definitions where the task requires exact text. Otherwise write a plain-language explanation beside the original, keeping qualifiers and source attribution. Flag contradictory or missing source material instead of silently editing the ontology.

For SKOS, language-qualified labeling and hierarchical/associative relations are distinct features; concepts can have multiple broader concepts. Keep these distinctions when adapting such a source. [W3C SKOS Primer](https://www.w3.org/TR/skos-primer/)

## Relationships beyond the selected entries

A selected concept may relate to an unselected concept. Keep that endpoint as an external reference with its exact ID; do not fabricate a local glossary entry or discard the relation. Keep original axioms and restrictions accessible through the source when the teaching format cannot represent them.

The optional structured format records selected terms, external endpoints, and typed relation triples. A normalized baseline for preservation checks has `terms` and `relations` in the same shape, with `coverage` set to `complete` or `curated`. Preserve labels for each selected concept and asserted edges involving it recorded in that baseline. Include all needed external endpoints in the generated output.

The validator is a consistency check for that normalized view. It neither parses arbitrary RDF/OWL nor proves logical consistency, source authenticity, or the correctness of a paraphrase. Compare any baseline normalization against the original before relying on the check.
