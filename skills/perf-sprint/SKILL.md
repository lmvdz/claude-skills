---
name: perf-sprint
description: Run a measurement-driven performance sprint on an app — pick the few user journeys that matter, turn each slowness report into a reproducing benchmark, ship fixes as small flagged PRs, confirm in the field, then ratchet the benchmark into CI. Use when the user says "make X faster", "perf sprint", "why is X slow", "speed up the app", or reports a slow/janky interaction. Orchestrates /perf-bench, /perf-hunt, /frame-budget, /perf-ratchet.
argument-hint: "[journey | slow interaction description | 'plan']"
---

# Perf Sprint

Distilled from Anthropic's claude.ai performance sprint (Aug 2026): 3.1x geometric-mean speedup across 13 measurements in two weeks, 3,000+ changes, zero customer incidents. The method matters more than any single fix:

```
SCOPE → REPRODUCE (bench) → FIX (small flagged PRs) → CONFIRM (field) → RATCHET (CI) → next bottleneck, same journey
```

Core belief: **once something can be measured deterministically, it can be hill-climbed.** Don't wait on production metrics to iterate; build a lab number you can move in minutes, prove it tracks wall-clock, then climb.

---

### Phase 0: SCOPE — pick the journeys

If argument is `plan` or no journeys exist yet:

1. List the user journeys and estimate share of user activity. Pick the **3–5 that cover ~95%**. (Theirs: launch app, start conversation, load existing conversation, send message.)
2. For each journey, define **one headline metric at p75** per platform (fresh page load, desktop cold start, CLI session start, …). p75, not mean — it's what most users feel and it's stable enough to steer by. Record the baseline.
3. Write the journeys + baselines to `perf/JOURNEYS.md` (or the repo's equivalent). This is the scoreboard; report geometric-mean speedup across all rows at the end.

Out of scope until the core journeys are done: p95 tails, rare journeys, pathological inputs (very long conversations). Note them as "next".

### Phase 1: REPRODUCE — one thread per slow interaction

Each slow interaction gets its own narrow thread of work (a task, branch, or subagent). **One thread = one benchmark = one journey.** Narrow threads stay reviewable and parallelizable; broad ones stall.

1. Get the symptom concretely: a recording, a trace, repro steps. "Feels slow" isn't enough — ask for what the user *sees* (late rows, rearranging, input lag, blank frame).
2. Trace the code path end to end for that interaction.
3. Build a deterministic reproducing benchmark → **invoke `/perf-bench`**. Don't write a fix before this exists.
4. If standard metrics say "fine" but the user sees a problem, **the metric is wrong, not the user.** (Their CLS was 0.008 — "good" — while 31% of loads shifted after becoming usable. They built attributed telemetry instead; see `/frame-budget`.)

### Phase 2: FIX — small, flagged, reviewable

- **Size PRs by risk, not by feature.** A risky change ships alone behind a flag; mechanical wins can batch. Expect many PRs per thread (their 120Hz thread produced ~60).
- **Unit tests before the optimization**, pinning current behavior. The optimization must pass the same tests.
- **User-visible changes go behind a flag.** Classify every flag at creation:
  - *kill switch* — defaults on, exists to turn off in an emergency
  - *ramp* — defaults off, rolled out gradually
  Track them; retire them when confirmed (they retired >half of ~200 flags within the sprint). Unretired flags are debt.
- Run `/perf-hunt` against the journey once the obvious fix lands — every new measurement surfaces more targets.

### Phase 3: CONFIRM — field data

After deploy, check the field metric for that journey (RUM, telemetry, logs). Lab win without field movement means either the benchmark doesn't correlate (go back to `/perf-bench` validation) or the bottleneck moved. Say which.

### Phase 4: RATCHET

Once the field confirms, **invoke `/perf-ratchet`** to lock the new benchmark value in CI so the gain can't silently regress. Then return to Phase 1 for the next bottleneck in the *same* journey until it hits target.

---

## Steering (the human side — apply these to yourself and ask the user for them)

**Ambition.** The early failure mode was hedging on feasibility; the fix was leadership saying *"we have the power to do anything. please be braver."* Don't pad estimates or propose a "phase 1 investigation" when you can just build the benchmark and the first PR now. Default to delivering, not scoping.

**Taste.** Performance changes are UX changes. Every user-perceptible change needs a named human owner and **before/after recordings**. Surface the real tradeoffs as questions, not decisions you make silently:
- Stream content in progressively, or wait and show it complete?
- Show a skeleton immediately, or only after ~500ms (to avoid flashing on fast loads)?
- Is an animation worth X% of the frame budget?

**Direction.** Keep each thread narrow. Merge threads that overlap. **Say no to marginal wins that add lasting complexity** ("that 2ms isn't worth the build plugin complexity"). Rule of thumb: a win must be user-perceptible or compounding to justify a new build step, dependency, or brittle mechanism.

## Output per thread

```
Journey: <name>   Thread: <symptom>
Benchmark: <name> — proxy <metric>, validated r/ratio vs wall-clock: <evidence>
Before → After (lab): <n> → <n>  (<x>x)
Before → After (field p75): <n> → <n>   [or: pending deploy]
PRs: <list, each with flag name + kill/ramp>
Ratchet: <CI budget set to n> [or: pending field confirmation]
Next bottleneck in this journey: <what the profile shows now>
```
