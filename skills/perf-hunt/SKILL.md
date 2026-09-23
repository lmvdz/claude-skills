---
name: perf-hunt
description: Sweep a codebase or a single user journey for known classes of hidden performance pathologies (per-keystroke re-render storms, expensive CSS selectors, hidden reloads, string-encoding slow paths, main-thread storage writes, O(n)-per-chunk streaming work). Use for "find perf problems", "audit performance", "what else is slow", or after the obvious fix in a /perf-sprint thread lands.
argument-hint: "[journey | path | 'all']"
---

# Perf Hunt

In the sprint, **every new measurement revealed new targets** — and the biggest wins were things nobody was looking for. This skill is the catalogue of pathology *classes* they found, turned into a checklist you can sweep with measurements plus grep.

Rule: **measure first, grep second.** Grep finds candidates; only a counter (via `/perf-bench`) proves one matters. Report findings with their measured cost, not "this looks slow".

For broad scopes, fan out one Explore agent per class below, then rank by measured cost × journey traffic.

---

## The catalogue

### 1. Input-path fan-out (re-render storms)
*Found: 6,900 hooks and 900 store subscriptions running on every keystroke in the composer.*
- Measure: React commits + components rendered **per keystroke** / per hot interaction.
- Look for: global store subscriptions without selectors, context providers whose value changes each render, parent state that should be local, unstable props (inline objects/closures) defeating memo.
- Fix shape: narrow subscriptions to the slice needed; move input state down to the leaf; split contexts.

### 2. Expensive global CSS selectors
*Found: one `:root:has(...)` selector added 24ms to **every** DOM change.*
- Measure: style recalc duration + elements affected per mutation.
- Look for: `:has()` (especially on `:root`/`html`/`body`), universal/descendant selectors on huge subtrees, `*` in hot rules, attribute selectors on frequently-mutated attributes.
- Fix shape: scope the selector, or replace with a class toggled from JS.

### 3. Hidden / forgotten code paths
*Found: a leftover `location.reload()` caused ~500,000 hidden reloads per day.*
- Look for: `location.reload`, `window.location =`, retry loops, `setInterval` without cleanup, remount-on-error boundaries, polling left from debugging.
- Measure: add a counter/telemetry event at each site; field data tells you how often it fires. Rare-looking code × huge traffic = big cost.

### 4. String-encoding slow paths
*Found: syntax highlighting hit slow regex paths when markdown contained any non-Latin-1 char (em dash, curly quote), because V8 stores the whole string as two-byte UTF-16. A 20-line fix — copy code blocks into one-byte strings before highlighting — cut first-code-block main-thread blocking 250ms → 40ms.*
- Measure: benchmark the hot regex/parse path with pure-ASCII input vs the same input plus one `—`. A big gap = this bug.
- Look for: regex-heavy tokenizers/highlighters/parsers run over substrings of large mixed documents.
- Fix shape: operate on the smallest slice possible (a code block's substring usually is one-byte if its content is ASCII — make sure it's a fresh copy, not a slice of the two-byte parent).

### 5. Main-thread persistence churn
*Found: identical cache snapshots structured-cloned into IndexedDB twice a minute on the main thread.*
- Look for: periodic `put`/`setItem`/`postMessage` of large objects, serialization on timers, writes that don't check for change.
- Fix shape: diff/hash before writing; debounce; move serialization to a worker; write deltas.

### 6. O(total)-per-increment work
*Found: streaming replies re-processed the whole message on every chunk.*
- Look for: anything run on each streamed chunk / appended item / scroll tick that walks the whole collection — markdown re-parse, full re-tokenize, re-sort, full list re-render.
- Fix shape: memoize finished blocks and only process the growing tail; move tokenization of the growing block to a worker. Detail in `/frame-budget`.

### 7. Late-arriving content & layout shift after "ready"
*Found: sidebar rows arriving late and rearranging; CLS said 0.008 ("good") but 31% of loads shifted after the page was usable.*
- Measure with attributed shift telemetry → `/frame-budget`.

### 8. Startup waterfalls
Not a named finding in the source, but the natural sweep for "launch" journeys: sequential awaits that could be parallel, eager imports of cold features, blocking auth/config fetches before first paint. Measure with a trace of the startup critical path.

---

## Output

Ranked table, measured costs only:

| # | Class | Location (file:line) | Measured cost | Journey / frequency | Fix shape | Complexity |
|---|---|---|---|---|---|---|

Drop anything whose win isn't user-perceptible or compounding relative to the complexity it adds — say so explicitly rather than silently omitting. Actionable rows become `/perf-sprint` threads.
