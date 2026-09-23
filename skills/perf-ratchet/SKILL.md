---
name: perf-ratchet
description: Lock in a confirmed performance win by turning its benchmark into a CI budget that can only tighten, and manage the feature flags that shipped it (kill switch vs ramp, retirement). Use after a perf fix is confirmed in the field, for "add a perf budget", "prevent regressions", "ratchet", "clean up perf flags", or as the final step of a /perf-sprint thread.
argument-hint: "<benchmark name | 'flags'>"
---

# Perf Ratchet

Speed is lost by default: every future change can quietly add work. The sprint's answer was a ratchet — once field data confirmed a win, the benchmark's new value became the CI ceiling, and the ceiling only moves down. This is what let them merge 3,000+ changes fast without giving gains back.

---

### Step 1: Preconditions
- The benchmark exists and was validated against wall-clock (`/perf-bench`).
- The win is confirmed in **field** data, not just the lab. Ratcheting an unconfirmed lab number locks in a proxy that may not matter.

### Step 2: Set the budget
- Deterministic proxies (instruction/call/commit/recalc/mutation counts, over-budget frames): budget = new value + small headroom (~1–3%) for harmless drift. Near-zero noise is what makes a tight budget possible.
- Wall-clock metrics: don't gate PRs on them; run nightly with many samples and alert on trend.
- Store budgets in a checked-in file (e.g. `perf/budgets.json`) with benchmark name, value, date, and the PR that earned it.

### Step 3: Wire into CI
- Fast deterministic benches → per-PR check. Failure message must print: benchmark, budget, actual, delta, and how to run it locally.
- Slow or environment-heavy benches (120Hz frame stepping, full page loads) → nightly job, alert on regression.
- **Ratchet down automatically or by prompt:** when a PR beats the budget by more than the headroom, update the budget in that PR (or have CI suggest it). Never raise a budget silently — raising requires an explicit justification in the PR description and owner approval.

### Step 4: Flags
Every flag from the sprint is classified at creation:
- **kill switch** — on by default; exists so ops can turn a risky optimization off instantly.
- **ramp** — off by default; rolled out by percentage while field metrics are watched.

With argument `flags`: list all perf flags with type, age, rollout %, and field status. Propose retirement for any flag at 100% with confirmed metrics and no incidents — remove the flag *and* the dead branch. (They created ~200 and retired over half during the sprint; unretired flags multiply test paths.)

## Output

```
Ratcheted: <benchmark>  <old budget> → <new budget>  (CI: per-PR | nightly)
Flags: <n> active (<k> kill, <r> ramp) — retire now: <list>
```
