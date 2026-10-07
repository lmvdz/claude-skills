---
name: domain-vocabulary
description: Generate practical, grouped vocabulary content for a field, domain, or supplied taxonomy/ontology so readers can recognize concepts and describe or request work precisely. Use for domain vocabulary pages, prompting lexicons, and ontology-to-glossary adaptation. Not for an isolated definition or formal ontology engineering alone.
---

# Domain Vocabulary

Create original content with the teaching function of a practical vocabulary page: help a reader turn an intention or observation into precise domain language. The default deliverable is finished, readable content, not a plan, an alphabetical dictionary, or a website implementation.

## Establish the target

Infer the domain boundary, reader, intended tasks, language, depth, and output format from the request. Ask only about missing information that would materially change selection; when the domain is given, use a stated useful assumption and proceed. A bare invocation with no domain needs a domain before content generation.

Default to an introductory practitioner audience and a curated selection. If the field is too broad, state a coherent boundary and cover it well; do not imply completeness. Honor requested counts, full coverage, formats, and supplied terminology. Do not add implementation, publishing, exercises, or extensive examples unless requested or needed to resolve a confusing distinction.

## Choose and ground concepts

- **Field mode:** select names practitioners use to specify actions, identify objects or states, adjust parameters, compare results, and recognize constraints. Choose the facets that actually fit the domain; do not force every field into a universal list of categories.
- **Supplied taxonomy/ontology mode:** read [references/ontology.md](references/ontology.md). The source determines concept identity and relationships. Grouping for teaching is a separate presentation decision.

Use supplied authoritative material first. Verify niche, changing, disputed, or consequential claims with primary sources and cite the exact supporting pages. Keep source opinions and platform-specific defaults scoped to their context. Do not reuse another field's heuristics as universal rules. If the necessary evidence is unavailable, narrow the claim or mark the gap; do not invent standard names, aliases, citations, or definitions to meet a count.

## Write the vocabulary

1. Organize by meaningful work, conceptual facets, or the supplied taxonomy. Make groups help the reader find the term needed for a task. Order groups from foundations toward application and interpretation when useful. Use alphabetical order when requested or required by the source.
2. Give each group one plain sentence explaining what belongs there. Give each entry a recognized label and a concise, distinguishing explanation: **Term — what it is or does, with the condition, effect, or contrast needed to use it correctly.** Aim for one sentence; retain a short qualification when omitting it would change the meaning.
3. Prefer operational descriptions over circular definitions or unexplained jargon. Define prerequisites before using them. Include a small example only when it makes an abstract concept identifiable or prevents a likely confusion.
4. Combine true aliases or paired operations only when their shared explanation remains accurate. Split near-neighbors with different meanings and state the distinction. Qualify ambiguous labels by sense or subdomain.
5. Check coverage against the reader's tasks. Include relevant limitations or evaluation vocabulary when needed; omit filler and tangential terms. Avoid unsupported judgments such as “always best,” arbitrary numbers, and directives presented as definitions.

See [references/editorial.md](references/editorial.md) for the analyzed reference pattern, definition repairs, and generation examples. Do not copy its domain-specific entries or promote the reference page's categories into mandatory slots.

## Deliver and check

Default shape:

```text
# [Domain] Vocabulary
[One or two sentences: audience, boundary, and what this vocabulary helps describe.]

## [Meaningful group]
[One sentence: this group's purpose.]

- **[Term]** — [Concise distinguishing explanation.]
```

Attach citations near source-dependent definitions or tightly bounded groups. Keep a short scope/version note when applicable. Cite the vocabulary-page inspiration only when discussing the method, not as evidence for a new domain's facts. Generate fresh prose; do not mechanically substitute domain nouns into copied sentences. Keep any established output template authoritative.

For requested machine-readable content or an ontology-backed handoff, read [references/structured-output.md](references/structured-output.md). Validate its JSON with `python scripts/validate_vocabulary.py output.json`; a normalized ontology baseline can be passed with `--baseline baseline.json`. This checks structure and preservation, not truth or formal consistency.

Before finishing, sample entries from different groups: can the intended reader recognize the concept, distinguish its nearest neighbor, and request an appropriate use? Check whether labels actually belong to this domain, group introductions fit their entries, claims retain their scope, and coverage matches the request. For ontology mode, also check the selected source concepts and asserted relationships against the original. Correct concrete failures rather than adding extra output to compensate.
