---
name: frame-budget
description: Diagnose and fix rendering jank — dropped frames during streaming/animation/typing, main-thread long tasks, and layout shifts that standard metrics miss. Uses deterministic headless frame stepping against a per-frame budget (8.33ms @120Hz) and attributed Layout Instability telemetry. Use for "janky", "stutters", "laggy while streaming", "content jumps", "layout shift", "hit 60/120fps", or when a /perf-sprint thread is about visual smoothness.
argument-hint: "<interaction> [hz=120]"
---

# Frame Budget

Smoothness is its own journey. The sprint pushed the target from 60Hz to **120Hz = 8.33ms per frame** and hit it for long streamed answers: main-thread blocking ~750ms → ~200ms, ~67% less CPU, sustained 120fps on a 120Hz MacBook, worst freeze 4.5x shorter, stalls 9x rarer on slow laptops. ~60 PRs from one thread.

Two tools: **deterministic frame stepping** (for dropped frames) and **attributed shift telemetry** (for things jumping around).

---

## A. Dropped frames

### 1. Make frames deterministic
Real-time frame measurement is noisy. Drive frames yourself:
- Headless Chrome with `--enable-begin-frame-control --deterministic-mode --run-all-compositor-stages-before-draw`, then step with CDP `HeadlessExperimental.beginFrame` at a fixed 8.33ms virtual interval.
- **Sanity check the harness:** N beginFrames must produce exactly N frames (theirs: 240 → 240). If not, the harness is lying — fix it before measuring anything.
- Feed the interaction a recorded, realistic input (a long reply's real chunk stream with code fences and tables).

### 2. Find the per-frame offenders
For each frame record main-thread work (CDP tracing). List frames over budget and what ran in them. Usually one of:

| Pattern | Fix shape |
|---|---|
| Work proportional to **total** content on each chunk (re-parse whole message) | Memoize finished blocks; only the growing tail is reprocessed |
| Heavy parse/tokenize of a **growing** block (code fence being streamed) | Move tokenization to a Web Worker; main thread only applies results |
| Big element revealed in one frame (a table) | Reveal incrementally (they went cell-by-cell) — but this is a **taste** call, ask the owner |
| Per-token animation (word-by-word fade) | Price it: what fraction of the 8.33ms does it cost? Take the number to the owner |
| Re-render fan-out | see `/perf-hunt` #1 |

### 3. Guard it
Once passing, run the 120Hz stepping benchmark as a **nightly job** (it became one) and ratchet worst-frame / over-budget-frame count via `/perf-ratchet`.

---

## B. Layout shift nobody measures

CLS is a single session score; it can read "good" (theirs: 0.008) while a third of loads visibly rearrange after they look ready. Build telemetry that tells you **where** and **when**:

1. `PerformanceObserver({type:'layout-shift', buffered:true})`; for each entry read `sources[].node` + `previousRect`/`currentRect`.
2. Map nodes to **named regions** (sidebar, header, composer, message list) via a data attribute or ancestor lookup.
3. Tag each shift with the **app phase** (pre-usable, post-usable/interactive, streaming, …). Shifts after "usable" are the ones users hate.
4. Report: % of loads with post-usable shifts, per region, magnitude in px (they tracked to 0.1px).
5. Fix causes one by one. Theirs: late-arriving header rows, misaligned carets, scrollbar appearing and narrowing content (reserve with `scrollbar-gutter: stable`).

### Static-placeholder handoff (instant first paint)
Showing static HTML for a component (e.g. the composer) before the framework hydrates is a big perceived-speed win and **brittle**. If you do it, ship all of these guardrails:
- Generate the static markup by rendering the **real component** (e.g. in jsdom) at build time, with a drift check that fails CI when they diverge.
- Integration test comparing static vs live render across many viewports (they used 14) asserting ≤1px alignment.
- Keystroke test: type during the handoff; assert no lost or reordered input.
- Field telemetry for shift at handoff.

### Environment edge cases
Test the unusual ways a page gets rendered. Their case: Chrome **prerendered** the new-tab page at new-tab height (~56px shorter), then resized after first paint → 15–20px shift. Fix: a test that simulates the prerender → resize flow and pins layout across it. Also consider: bfcache restore, zoom levels, background tabs, window resize during load.

## Output

```
Interaction: <name>   target: <hz> (<ms>/frame)
Harness check: <N> beginFrames → <N> frames ✓
Over-budget frames: <before> → <after>   worst frame: <ms> → <ms>
Main-thread blocking total: <ms> → <ms>   CPU: −x%
Post-usable shifts: <% loads> → <% loads>  by region: <...>
Taste calls for owner: <list with before/after recordings>
```
