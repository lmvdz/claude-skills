---
name: perf-bench
description: Build a deterministic, low-noise benchmark for a slow code path or interaction, and prove it correlates with real wall-clock time before anyone optimizes against it. Use when you need a number to hill-climb — "benchmark this", "measure X", "is this faster", "reproduce the slowness" — or as the REPRODUCE step of /perf-sprint.
argument-hint: "<code path | interaction | symptom>"
---

# Perf Bench

Wall-clock timing is noisy — you can't tell a 5% win from jitter without dozens of runs. The sprint's key move was optimizing against **deterministic proxies** that give the same number every run, so every edit gets an instant, trustworthy signal. But a proxy is only useful if it moves with the thing users feel, so **correlation is validated before the proxy is used.**

```
PICK PROXY → HARNESS → VALIDATE vs wall-clock → BASELINE → hand off
```

---

### Step 1: PICK THE PROXY

Choose the deterministic counter closest to the cost you suspect:

| Suspected cost | Proxy | How |
|---|---|---|
| Pure JS/CPU hot path | **Instruction count** | `valgrind --tool=callgrind node --predictable bench.js` (Linux/WSL); `perf stat -e instructions` as a fallback. `--predictable` removes V8 nondeterminism (concurrent GC/JIT threads). Other runtimes: cachegrind for Python/C, `iai-callgrind` for Rust. |
| "Too much work" / redundant calls | **Call counts** | V8 precise coverage (`Profiler.startPreciseCoverage({callCount:true, detailed:true})` via inspector/CDP) — counts per function, fully deterministic |
| React re-render churn | **Commit / render counts** | `<Profiler onRender>` or React DevTools profiler hook; count commits and components rendered per user action (e.g. per keystroke) |
| CSS cost | **Style recalc count + elements affected** | Chrome trace events `UpdateLayoutTree` / `RecalculateStyles` via CDP tracing |
| DOM thrash / late content | **DOM mutation count** | `MutationObserver` over the region, counted per phase |
| Visual instability | **Attributed layout shifts** | see `/frame-budget` |
| Frame drops during animation/streaming | **Deterministic frame stepping** | see `/frame-budget` |

Prefer counts over times. When nothing deterministic fits, fall back to wall-clock with many iterations, pinned CPU, warm-up, and median + IQR — and say so.

### Step 2: HARNESS

- Drive the **real code path** with realistic input (a real long conversation, a real markdown doc with non-ASCII chars — the sprint's worst regex bug only appeared with em dashes and curly quotes).
- Isolate: fixed seed, fixed data, no network (fixture it), fixed viewport.
- Script it so one command prints one number (plus secondary counters). It must run in under a minute so the edit → measure loop stays tight.
- Commit it next to the code (`bench/` or `perf/`), not in a scratch dir — `/perf-ratchet` will run it in CI.

### Step 3: VALIDATE — the step people skip

Before optimizing, show the proxy tracks wall-clock on *this* path:

1. Make or find 2+ variants with different costs (the fix prototype, a deliberately slowed version, an old commit).
2. Measure both the proxy and wall-clock (many runs, median) for each.
3. Report the pair. The sprint's reference points:
   - message-tree assembly: −48% instructions ↔ −78% wall-clock (4.6x)
   - status-line scanner: −31% instructions ↔ −44% wall-clock (1.8x)

   Same direction, comparable or larger magnitude = valid. (Wall-clock often improves *more* than instructions because fewer instructions also means less allocation, GC, and cache pressure.)
4. If the proxy moves and wall-clock doesn't, **the proxy is measuring the wrong thing** — the real cost is elsewhere (I/O, layout, GC, network, lock contention). Pick a different proxy; don't climb a hill that isn't there.

### Step 4: BASELINE & hand off

Record: proxy value, wall-clock median, environment, commit SHA. Then iterate fixes against the proxy, re-checking wall-clock at the end of each PR.

## Output

```
Benchmark: <name>   (<path to script>)   run: <command>
Proxy: <metric>  baseline <n>
Wall-clock: median <ms> (IQR <ms>, N runs)
Validation: <variant> proxy −x% ↔ wall −y%  → VALID | INVALID (why)
Noise: proxy variance across 5 runs = <n> (should be ~0)
```
