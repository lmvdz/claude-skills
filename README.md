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

## Install

Copy (or symlink) a skill folder into `~/.claude/skills/` (user-wide) or `.claude/skills/` (per project):

```sh
git clone https://github.com/lmvdz/claude-skills
cp -r claude-skills/skills/* ~/.claude/skills/
```
