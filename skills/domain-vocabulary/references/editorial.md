# Editorial method

## What the reference contributes

Analyzed source: [Animation Vocabulary](https://animations.dev/vocabulary), observed 2026-10-07.

The page presents 12 topical groups. A short introduction explains its use for describing desired behavior to AI. Each group has a one-sentence orientation followed by compact term/explanation rows. The inventory mixes visible patterns, operations, controls, implementation concerns, and guiding principles. It prioritizes practical recognition and naming over exhaustive or alphabetic coverage. Some entries bundle alternate names or paired behaviors; selected entries include examples or contextual advice.

The transferable teaching pattern is a map of useful intentions into recognizable terminology. Its subject-specific categories and recommendations are not a universal taxonomy. Some practical simplifications lose technical distinctions when generalized; retain the concise surface while verifying the new domain's meaning.

This analysis describes the content, not a verified visual or runtime inspection of the site. The skill creates original domain content and does not reproduce the site's wording or branding.

## Selection decisions

Ask what readers need to name in their actual work. Useful candidates might describe a thing, action, state, relation, parameter, measurement, outcome, or constraint. These are selection lenses, not required headings.

Use a coherence test: every entry in a group should fit the group's orientation sentence. If the sentence needs several unrelated clauses, regroup. If a useful concept fits several groups, choose one main display location and cross-reference it rather than changing its meaning or duplicating divergent definitions.

A technical domain may benefit from operations, controls, and failure states. A humanities domain may need schools, interpretive distinctions, genres, and historical qualifiers. A natural-science domain may need entities, processes, measurement, and competing explanatory frameworks. Determine the groups from evidence and the audience's purpose.

## Definition repairs

- Circular: “A checkpoint is a checkpoint of the system.” Repair by naming the state saved and the purpose of restoring it.
- Mere advice: “Use an index for speed.” Repair by defining the lookup structure, then retain a context-dependent qualification about its cost only if relevant.
- False alias: “Quality / accuracy” collapses two different ideas. Split them and specify what each assesses in this domain.
- Mechanism/outcome conflation: a procedure and the desired result may be related without being interchangeable names. Define them separately.
- Invisible abstraction: for a concept that cannot be recognized directly, describe its role in an example or the evidence by which it is inferred. Do not promise a visible cue that the domain does not have.

The repairs are editorial examples, not definitions intended to populate every output.

## Example invocations

```text
/domain-vocabulary Create vocabulary for ceramic surface decoration, aimed at first-year
pottery students. Give 25 terms grouped by practical purpose, distinguish
terms that overlap in studio usage, and ground the content in supplied sources.
```

```text
/domain-vocabulary Create vocabulary for PostgreSQL 18 integrity constraints. Keep it to
12 terms. Explain the distinctions needed to ask an AI for a schema change.
```

```text
/domain-vocabulary Turn the attached SKOS scheme into a bilingual
glossary. Cover every concept, preserve preferred and alternate labels and
both broader parents where supplied, and include structured JSON.
```

These are different content tasks. The latter requires a source-preserving view, not a newly invented classification.
