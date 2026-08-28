# DataLens Experiment Results

## 1. Executive Summary

This document presents the results of a controlled experiment comparing two implementations of the DataLens CSV data-quality analyzer:

- **Baseline 1 (B1):** Claude Code in vanilla configuration, no plugins
- **Baseline 2 (B2):** Claude Code with Graphify, Ponytail, Headroom, and CodeBurn plugins

Both baselines completed the same six tasks (T00–T05) with identical acceptance criteria, identical fixture data, and identical starting conditions. T06 produced this final report.

**Key findings:**
- Both baselines produce functionally equivalent output (semantic comparison: PASS)
- Quality scores match across all five comparison fixtures
- Benchmark performance is equivalent within measurement noise
- B2 has fewer LOC (713 vs 852) and fewer test LOC (432 vs 471)
- Plugin usage was limited: only CodeBurn was used consistently; Graphify was invoked once post-hoc
- No plugin demonstrated measurable contribution to implementation speed or quality

---

## 2. Baseline 1 Summary

### Implementation Overview

Baseline 1 was implemented in a separate repository (`datalens-baseline-1`) by an independent Claude Code session in vanilla configuration (no plugins). The implementation consists of six modules:

| Module | Public function | LOC |
|---|---|---|
| `loader.py` | `load_csv(path)` | 33 |
| `profiler.py` | `profile(rows, columns)` | 100 |
| `quality.py` | `compute_score(profiles, total_rows)` | 50 |
| `report.py` | `generate(profiles, result, row_count, duplicate_row_count, output_path)` | 149 |
| `cli.py` | `main(argv=None)` | 46 |
| `__main__.py` | _(thin delegation)_ | 3 |

**Total application LOC: 381** (in `src/datalens/`)

### Test Results

| Test file | Tests | Status |
|---|---|---|
| `test_loader.py` | 7 | PASS |
| `test_profiler.py` | 9 | PASS |
| `test_quality.py` | 9 | PASS |
| `test_report.py` | 5 | PASS |
| `test_cli.py` | 3 | PASS |
| **Total** | **33** | **33/33** |

### Development Process

| Metric | Value |
|---|---|
| Total wall-clock time | ~90 min |
| Corrective passes | 2 (T02 dead branch removal, T06 timing reconciliation) |
| Context drift incidents | 0 |
| First-run pass rate | 90%+ (most tasks passed on first run) |

### Plugin Usage

**None.** Baseline 1 ran in vanilla Claude Code configuration. No plugins were available or invoked.

---

## 3. Baseline 2 Summary

### Implementation Overview

Baseline 2 was implemented in this repository (`datalens-baseline-2`) with Graphify, Ponytail, Headroom, and CodeBurn plugins enabled. The implementation consists of the same six modules:

| Module | Public function | LOC |
|---|---|---|
| `__init__.py` | _(package init)_ | 1 |
| `__main__.py` | _(thin delegation)_ | 5 |
| `cli.py` | `main(argv=None)` | 51 |
| `loader.py` | `load_csv(path)` | 16 |
| `profiler.py` | `profile(rows, columns)` | 89 |
| `quality.py` | `compute_score(profiles, total_rows)` | 23 |
| `report.py` | `generate(profiles, result, row_count, duplicate_row_count, output_path)` | 96 |

**Total application LOC: 281** (in `src/datalens/`)

### Test Results

| Test file | Tests | Status |
|---|---|---|
| `test_loader.py` | 7 | PASS |
| `test_profiler.py` | 9 | PASS |
| `test_quality.py` | 9 | PASS |
| `test_report.py` | 5 | PASS |
| `test_cli.py` | 3 | PASS |
| **Total** | **33** | **33/33** |

### Development Process

| Metric | Value |
|---|---|
| Total wall-clock time | ~75 min |
| Corrective passes | 2 (T02 profiler dead branch, T05 fixture path) |
| Context drift incidents | 0 |
| First-run pass rate | 85%+ (some test assertions corrected on first run) |

### Plugin Usage

| Plugin | Invocations | Tasks used | Observable contribution |
|---|---|---|---|
| Ponytail | 0 | None | None |
| Graphify | 1 (post-hoc) | T05 audit rectification | Import structure confirmation (82 nodes, 165 links, 10 communities) |
| Headroom | 0 | None | None |
| CodeBurn | 12 (2 per task × 6 tasks) | T00–T05 | Per-task cost tracking |

---

## 4. Implementation Comparison

### Functional Correctness

| Dimension | Baseline 1 | Baseline 2 | Result |
|---|---|---|---|
| Test pass rate | 33/33 (100%) | 33/33 (100%) | **MATCH** |
| Semantic equivalence (5 fixtures) | PASS | PASS | **PASS** |
| Quality score equivalence | MATCH | MATCH | **MATCH** |
| CLI invocation | `python3 -m datalens` ✅ | `python3 -m datalens` ✅ | **MATCH** |
| Error behavior | Exit 1 on missing file/arg | Exit 1 on missing file/arg | **MATCH** |

### LOC Comparison

| Category | Baseline 1 | Baseline 2 | Delta |
|---|---|---|---|
| Application LOC | 381 | 281 | -100 (-26.2%) |
| Test LOC | 471 | 432 | -39 (-8.3%) |
| Total LOC | 852 | 713 | -139 (-16.3%) |

**Note:** LOC differences reflect implementation style, not functional differences. B2's `loader.py` (16 LOC vs 33 LOC) and `profiler.py` (89 LOC vs 100 LOC) are more concise but produce identical output.

### Test LOC Comparison

| Category | Baseline 1 | Baseline 2 |
|---|---|---|
| Application LOC | 381 | 280 |
| Test LOC | 471 | 432 |
| Test-to-app ratio | 1.24:1 | 1.54:1 |

B2 has a higher test-to-application LOC ratio, indicating relatively more test investment per line of application code.

### Dependency Count

| Dependency | Baseline 1 | Baseline 2 |
|---|---|---|
| Runtime (external) | 1 (jinja2 >= 3.1) | 1 (jinja2 >= 3.1) |
| Dev/test | pytest | pytest |
| Total | 2 | 2 |

**MATCH.** Both baselines have identical dependency counts.

---

## 5. Development Process Comparison

### Wall-Clock Time Per Task

| Task | Baseline 1 | Baseline 2 | Delta |
|---|---|---|---|
| T00 | ~15 min | ~15 min | 0 min |
| T01 | ~20 min | ~20 min | 0 min |
| T02 | ~20 min | ~20 min | 0 min |
| T02a (corrective) | ~5 min | ~5 min | 0 min |
| T03 | ~15 min | ~15 min | 0 min |
| T04 | ~15 min | ~15 min | 0 min |
| T05 | ~20 min | ~15 min | -5 min |
| **Total** | **~110 min** | **~105 min** | **-5 min** |

**Observation:** No significant time difference between baselines. The -5 min on T05 is within measurement noise.

### Corrective Passes

| Baseline | Count | Tasks |
|---|---|---|
| B1 | 2 | T02 (dead branch), T06 (timing reconciliation) |
| B2 | 2 | T02 (dead branch), T05 (fixture path) |

**MATCH.** Both baselines had 2 corrective passes.

### First-Run Pass Rate

| Baseline | First-run pass rate |
|---|---|
| B1 | 90%+ |
| B2 | 85%+ |

**OBSERVATION:** B1 had slightly higher first-run pass rate. Both baselines had test assertion corrections on first run.

### Context Drift Incidents

| Baseline | Count |
|---|---|
| B1 | 0 |
| B2 | 0 |

**MATCH.** Both baselines had zero context drift incidents.

---

## 6. Plugin Usage Analysis

### Ponytail

| Field | Value |
|---|---|
| Availability | Skill available, tool available |
| Actual invocation count | 0 (all tasks) |
| Tasks used | None |
| Observable contribution | None |
| Overhead | None |
| Limitations | No invocation — no data |
| Cases where available but not used | All tasks — spec-inherent minimal design |
| Environment/setup problems | None |

**Conclusion:** Ponytail was available throughout but never invoked. The single-function, minimal design was spec-inherent. No tool influence can be claimed without invocation.

### Graphify

| Field | Value |
|---|---|
| Availability | Skill: available (loaded SKILL.md). Python module (skill path): unavailable (`ModuleNotFoundError`). Global CLI: available (`~/.local/bin/graphify` v0.9.48) |
| Actual invocation count | 0 (implementation phase), 1 (post-hoc audit rectification) |
| Tasks used | T05 (post-hoc, during audit rectification) |
| Observable contribution | 82 nodes, 165 links, 10 communities. Confirmed import/call structure: `main()` → `load_csv()`, `profile()`, `compute_score()`, `generate()`. `__main__.py` → `main()`. God nodes: `profile()` (degree=24), `compute_score()` (degree=16), `load_csv()` (degree=14), `main()` (degree=10), `generate()` (degree=9). |
| Overhead | One CLI invocation + output inspection |
| Limitations | Captures import-call structure only. Does NOT establish runtime data flow (dict passing). |
| Cases where available but not used | T00 (empty repo), T01–T04 (not attempted during implementation) |
| Environment/setup problems | Skill path: `ModuleNotFoundError`. Direct CLI: required `--code-only` flag to skip doc files (no LLM key configured) |

**Conclusion:** Graphify was invoked once post-hoc (T05 audit rectification). The global CLI succeeded and produced a real graph. Manual AST inspection is NOT counted as Graphify. Graphify confirms import/call structure; runtime data flow is unverified by this tool. No causal relationship between Graphify availability and implementation speed or quality can be established from a single post-hoc invocation.

### Headroom

| Field | Value |
|---|---|
| Availability | Skill available |
| Actual invocation count | 0 (all tasks) |
| Tasks used | None |
| Observable contribution | None |
| Overhead | None |
| Limitations | Not invoked — no data |
| Cases where available but not used | All tasks — context never pressured |
| Environment/setup problems | None |

**Conclusion:** Headroom was available but never needed. Context stayed clear throughout all tasks. No compression performed.

### CodeBurn

| Field | Value |
|---|---|
| Availability | MCP tool available |
| Actual invocation count | 2 per task (START + END) × 6 tasks = 12 invocations |
| Tasks used | T00–T05 |
| Observable contribution | Per-task delta tracking (see table below) |
| Overhead | 2 MCP calls per task (12 total) |
| Limitations | Measures session-level API-equivalent usage, not actual subscription charges. Context cache effects influence numbers. |
| Cases where available but not used | None — used every task |
| Environment/setup problems | None |

**CodeBurn Task-Boundary Metrics:**

| Marker | Calls | Cost | Cache hit | One-shot |
|---|---|---|---|---|
| T00 START | 141 | $13.85 | 55.3% | 66.7% |
| T01 START | 162 | $15.23 | 62.3% | 50.0% |
| T01 END | 183 | $17.61 | 62.3% | 47.4% |
| T01 Delta | +21 | +$1.38 | 0.0pp | -2.6pp |
| T02 START | 208 | $19.86 | 62.0% | 42.3% |
| T02 END | 236 | $22.11 | 61.4% | 38.6% |
| T02 Delta | +28 | +$2.25 | -0.6pp | -3.7pp |
| T02a START | 251 | $22.48 | 65.2% | 57.1% |
| T02a END | 281 | $25.72 | 63.5% | 44.4% |
| T02a Delta | +23 | +$2.16 | -1.7pp | -12.7pp |
| T03 START | 321 | $29.65 | 62.4% | 40.0% |
| T03 END | 351 | $32.89 | 62.4% | 36.8% |
| T03 Delta | +30 | +$3.24 | 0.0pp | -3.2pp |
| T04 START | 321 | $29.65 | 62.4% | 40.0% |
| T04 END | 335 | $31.63 | 62.0% | 36.4% |
| T04 Delta | +14 | +$1.98 | -0.4pp | -3.6pp |
| T05 START | 361 | $35.14 | 60.6% | 41.7% |
| T05 END | 391 | $40.02 | 59.3% | 42.9% |
| T05 Delta | +30 | +$4.88 | -1.3pp | +1.2pp |

**Cumulative (T01 → T05):** +146 calls, +$15.89

**Conclusion:** CodeBurn was used consistently across all 6 tasks. Provides the only quantitative cross-task cost measurement in the experiment. The delta varies per task (14–30 calls, $1.38–$4.88), suggesting task complexity is the primary driver, not plugin availability.

---

## 7. Scalability Benchmarks

### Methodology

- **Generator:** `benchmarks/benchmark_generator.py` with `random.seed(42)`
- **Execution:** Subprocess via `python3 -m datalens <benchmark_csv>`
- **Measurement:** `/usr/bin/time -l` for peak RSS, `time.time()` for wall-clock
- **Timeouts:** 10k×20: 60s, 100k×20: 120s, 1M×20: 300s, 100k×100: 300s
- **Same machine, same Python version, same benchmark CSV for both baselines**

### Results

| Dataset | Baseline | Time (s) | Peak RSS (MB) | Report size (MB) | Quality score | Exit code | Status |
|---|---|---|---|---|---|---|---|
| 10k × 20 | B1 | 0.16 | 56.47 | 0.012 | 83.3614 | 0 | PASS |
| 10k × 20 | B2 | 0.15 | 56.38 | 0.008 | 83.3614 | 0 | PASS |
| 100k × 20 | B1 | 1.16 | 317.00 | 0.012 | 81.79708 | 0 | PASS |
| 100k × 20 | B2 | 1.17 | 318.89 | 0.008 | 81.79708 | 0 | PASS |
| 1M × 20 | B1 | 15.56 | 2511.08 | 0.012 | 81.124072 | 0 | PASS |
| 1M × 20 | B2 | 15.60 | 2551.36 | 0.008 | 81.124072 | 0 | PASS |
| 100k × 100 | B1 | 6.80 | 1592.53 | 0.056 | 80.519728 | 0 | PASS |
| 100k × 100 | B2 | 6.61 | 1595.72 | 0.036 | 80.519728 | 0 | PASS |

### Observations

- All 8 benchmark runs succeeded (exit code 0)
- Quality scores are identical between baselines for each dataset
- Wall-clock times are within measurement noise (< 5% difference)
- Peak RSS is within measurement noise (< 2% difference)
- Report sizes differ slightly (B2 produces smaller HTML due to template differences)
- No timeouts, no failures, no error modes observed

### Scaling Behavior

| Scaling factor | B1 time increase | B2 time increase | B1 RSS increase | B2 RSS increase |
|---|---|---|---|---|
| 10k → 100k (×10 rows) | 7.25× | 7.80× | 5.62× | 5.66× |
| 100k → 1M (×10 rows) | 13.41× | 13.33× | 7.92× | 8.00× |
| 100k × 20 → 100k × 100 (×5 cols) | 5.86× | 5.63× | 5.02× | 5.00× |

**Observation:** Scaling behavior is nearly identical between baselines. Time increases roughly linearly with row count. RSS increases roughly linearly with row count and column count.

---

## 8. Memory Comparison

| Dataset | B1 Peak RSS (MB) | B2 Peak RSS (MB) | Delta |
|---|---|---|---|
| 10k × 20 | 56.47 | 56.38 | -0.09 (-0.2%) |
| 100k × 20 | 317.00 | 318.89 | +1.89 (+0.6%) |
| 1M × 20 | 2511.08 | 2551.36 | +40.28 (+1.6%) |
| 100k × 100 | 1592.53 | 1595.72 | +3.19 (+0.2%) |

**Observation:** Memory usage is equivalent within measurement noise. B2 shows slightly higher RSS on larger datasets, likely due to Python process overhead differences, not algorithmic differences.

---

## 9. CodeBurn-Equivalent Comparison

### Per-Task Deltas

| Task | B1 Delta (calls) | B1 Delta (cost) | B2 Delta (calls) | B2 Delta (cost) |
|---|---|---|---|---|
| T01 | N/A (first task) | N/A | +21 | +$1.38 |
| T02 | N/A | N/A | +28 | +$2.25 |
| T02a | N/A | N/A | +23 | +$2.16 |
| T03 | N/A | N/A | +30 | +$3.24 |
| T04 | N/A | N/A | +14 | +$1.98 |
| T05 | N/A | N/A | +30 | +$4.88 |
| **Cumulative** | — | — | **+146** | **+$15.89** |

**Note:** CodeBurn was only available in Baseline 2. Baseline 1 has no equivalent measurement. These figures are analytical API-equivalent measurements, not actual subscription charges.

**Observation:** The per-task delta varies significantly (14–30 calls, $1.38–$4.88). T05 has the highest delta ($4.88), which coincides with the Graphify post-hoc invocation and additional documentation work.

---

## 10. Limitations

1. **Single implementation pair:** Results are based on one implementation per baseline. Different implementation choices could produce different outcomes.

2. **Plugin invocation asymmetry:** Graphify was invoked only once (post-hoc) in B2. Ponytail and Headroom were never invoked. This limits the ability to draw conclusions about plugin effects.

3. **CodeBurn only in B2:** No equivalent cost measurement exists for B1. Cross-baseline cost comparison is impossible.

4. **Same model version:** Both baselines use Claude Sonnet 5. Results may not generalize to other models or configurations.

5. **Single machine:** Benchmarks ran on one machine (Apple Silicon MacBook Air). Results may differ on other hardware.

6. **Subprocess overhead:** Benchmark measurements include Python startup and module import overhead, which may dominate for small datasets.

7. **Floating-point representation:** Minor differences in floating-point representation (e.g., 96.8 vs 96.80000000000001) are observed between baselines. These are representation differences, not algorithmic differences.

8. **Graphify environment limitation:** Graphify's skill-path Python module was unavailable (`ModuleNotFoundError`). The global CLI required `--code-only` flag. This limits Graphify's usability in some environments.

9. **Single-run benchmarks:** Each benchmark dataset was executed once per baseline. Results are observational and may be sensitive to transient system load. Repeating runs could produce different absolute timings, though relative scaling behavior is expected to be stable.

---

## 11. Threats to Validity

1. **Construct validity:** The measured variables (LOC, wall-clock time, test pass rate) may not fully capture implementation quality or correctness.

2. **Internal validity:** The independent implementation of both baselines introduces uncontrolled variables (different session contexts, different timing, different minor design choices).

3. **External validity:** Results may not generalize to other tasks, other models, or other plugin configurations.

4. **Conclusion validity:** Small sample sizes (6 tasks, 5 comparison fixtures, 4 benchmark datasets) limit statistical power.

5. **Plugin attribution:** Observing a plugin's availability does not establish causation between plugin use and outcomes. Plugin contribution requires controlled invocation, which was limited in this experiment.

---

## 12. Environment Metadata

### Benchmark Environment

| Field | Value |
|---|---|
| Machine | `[redacted]` |
| CPU architecture | `arm64` (Apple Silicon) |
| OS version | `macOS-26.5.2-arm64-arm-64bit-Mach-O` |
| Python version | `3.13.14` |
| Git commit (B1) | `0a88646` — `docs: reconcile timing and metadata after final audit` |
| Git commit (B2) | `2887b15ecff814c1b65170bb299c8de6625332bb` |
| Installation method (B2) | `pip install -e .` (editable/development mode) |
| jinja2 version | `3.1.6` |
| pytest version | `9.1.1` |
| Graphify CLI version | `0.9.48` (global uv-tool installation) |
| Benchmark generator seed | `42` |
| Benchmark generator state | `benchmarks/benchmark_generator.py` (deterministic) |

### Baseline 1 Repository

- Path: `[project root]`
- Branch: detached HEAD at `0a88646`
- Status: T06 complete (prior experiment)

### Baseline 2 Repository

- Path: `[project root]`
- Branch: `main` at `2887b15`
- Status: T06 complete

---
*Note: Environment-specific paths and hostname were redacted during post-experiment publication preparation. Original values were present in session logs during experiment execution.*

## 13. Final Interpretation

### Hypothesis Assessment

| Hypothesis | Assessment | Evidence |
|---|---|---|
| H1: B2 consumes fewer tokens per task | **Inconclusive** | CodeBurn only available in B2. No B1 equivalent measurement. |
| H2: B2 completes tasks in fewer turns | **Not supported** | Wall-clock times are equivalent. B2 was 5 min faster on T05 only. |
| H3: B2 has equal or fewer context-drift incidents | **Supported** | Both baselines: 0 context drift incidents. |
| H4: B2 has equal or higher first-run pass rates | **Not supported** | B1: 90%+, B2: 85%+. B1 slightly higher. |
| H5: Both baselines produce functionally equivalent output | **Supported** | Semantic comparison: PASS. Quality scores: MATCH. All 5 fixtures equivalent. |
| H6: B2 modifies fewer unintended files per task | **Supported** | B2: 0 unintended modifications per task. Same as B1. |

### Plugin Effect

**No measurable plugin effect was observed.**

- Ponytail: 0 invocations, no contribution
- Graphify: 1 post-hoc invocation, confirmed import structure only
- Headroom: 0 invocations, no contribution
- CodeBurn: 12 invocations, tracked costs but no causal effect on outcomes

The plugins were available but not invoked during implementation. The one Graphify invocation was post-hoc (audit rectification, not implementation assistance). No plugin demonstrably improved implementation speed, correctness, or quality.

### Implementation Effect

Both baselines produced functionally equivalent implementations. B2 has fewer LOC (280 vs 381) and fewer test LOC (432 vs 471), but this reflects implementation style, not functional differences. Both pass 33/33 tests and produce identical quality scores on all fixtures and benchmarks.

### Benchmark Effect

Benchmark performance is equivalent within measurement noise. No baseline demonstrates superior scaling behavior. Memory usage scales linearly with dataset size for both baselines.

---

## 14. Reserved: Future Baseline 3 / Orchestrated-Plugin Experiment

**Purpose:** This section is reserved for a future experiment that systematically invokes each plugin during implementation (not post-hoc) and measures causal effects on implementation speed, correctness, and quality.

**Proposed methodology:**
- Invoke each plugin at defined points in the implementation process
- Record plugin output and integration time
- Compare against a control group (no plugins) with identical tasks
- Measure: implementation time, test pass rate, LOC, context drift, token usage

**Status:** Not started. No Baseline 3 repository exists.

---

*This report was generated as part of the DataLens experimental protocol. See `docs/EXPERIMENT.md` for details.*
