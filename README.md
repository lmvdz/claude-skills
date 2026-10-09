# claude-skills

Skills for [Claude Code](https://claude.com/claude-code).

## Performance suite

Distilled from Anthropic's write-up on making claude.ai 3x faster (Aug 2026): measure deterministically, validate against wall-clock, ship small flagged PRs, confirm in the field, ratchet into CI.

| Skill | Purpose |
|---|---|
| [`perf-sprint`](skills/perf-sprint/SKILL.md) | Orchestrator: journeys → benchmark → flagged fix → field confirm → ratchet, plus steering (ambition, taste, direction) |
| [`perf-bench`](skills/perf-bench/SKILL.md) | Build a deterministic proxy benchmark and prove it correlates with wall-clock |
| [`perf-hunt`](skills/perf-hunt/SKILL.md) | Catalogue of hidden perf pathologies to sweep for |
| [`frame-budget`](skills/frame-budget/SKILL.md) | Jank: deterministic 120Hz frame stepping and attributed layout-shift telemetry |
| [`perf-ratchet`](skills/perf-ratchet/SKILL.md) | Tighten-only CI budgets and feature-flag lifecycle |

## Domain vocabulary

| Skill | Purpose |
|---|---|
| [`domain-vocabulary`](skills/domain-vocabulary/SKILL.md) | Create practical, grouped vocabulary for any field, or adapt a supplied taxonomy/ontology while preserving identifiers, multilingual labels, and relationships |

Inspired by the teaching structure of [Animation Vocabulary](https://animations.dev/vocabulary): useful categories, brief introductions, and concise explanations that help readers describe or request work precisely. Categories and terminology are derived from the target domain and grounded in its sources.

```text
/domain-vocabulary Create 40 cinematography terms for beginning filmmakers,
grouped by practical purpose. Distinguish commonly confused concepts and
cite primary sources.
```

For semantic anchors and reusable prompt terms, the optional [prompting mode](skills/domain-vocabulary/references/prompting.md) adds task-specific instructions, observable success checks, and model-evidence records. Definition grounding remains separate from behavioral evidence; standalone term use is untested unless relevant experiments support it. The mode also includes a comparison design for tasks alone, terms, definitions, operational contracts, and plain-language controls. Ordinary glossaries remain concise.

The skill includes optional structured JSON and a Python 3 validator for content shape, prompting-record shape, and preservation against a normalized source baseline. The validator does not check factual truth, verify behavioral experiments, or perform RDF/OWL reasoning.

## Install

Copy (or symlink) a skill folder into `~/.claude/skills/` (user-wide) or `.claude/skills/` (per project):

```sh
git clone https://github.com/lmvdz/claude-skills
cp -r claude-skills/skills/* ~/.claude/skills/
```
