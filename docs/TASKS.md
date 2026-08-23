# DataLens — Tasks

> **Completion reports:** After every completed task (T01–T06), a Task Completion Report must be produced using the template in `docs/TASK_COMPLETION.md`. Claude must STOP after producing the report and wait for human approval before starting the next task.

---

## Live Progress Tracker

| ID | Title | Status | Est. | Actual | Tests | Context Drift | Git Commit |
|---|---|---|---|---|---|---|---|
| T00 | Project Operating System | Complete | 110 min | — | N/A | NONE | — |
| T01 | loader.py — CSV reading and parsing | Complete | 35 min | ~20 min | 7/7 | NONE | `feat(T01): CSV loader module` |
| T02 | profiler.py — per-column profiling | Corrective Pass | 40 min | ~20 min | 9/9 | NONE | `feat(T02): column profiler module` |
| T03 | quality.py — composite quality score | Complete | 30 min | ~15 min | 9/9 | NONE | `feat(T03): quality score module` |
| T04 | report.py — HTML report generation | Pending | 40 min | — | 5/5 | — | — |
| T05 | cli.py — CLI entry point | Pending | 30 min | — | 3/3 | — | — |
| T06 | Final review and polish | Pending | 130 min | — | 29/29 | — | — |

---

## Task Index

| ID | Title | Est. | Status |
|---|---|---|---|
| T00 | Project Operating System | 110 min | Complete |
| T01 | loader.py — CSV reading and parsing | 35 min | Pending |
| T02 | profiler.py — per-column profiling | 40 min | Pending |
| T03 | quality.py — composite quality score | 30 min | Complete |
| T04 | report.py — HTML report generation | 40 min | Pending |
| T05 | cli.py — CLI entry point | 30 min | Pending |
| T06 | Final review and polish | 25 min | Pending |

---

## T00 — Project Operating System

**Objective:** Establish the project's operating system: documentation, scaffolding, fixtures, and experiment protocol. No application implementation code.

**Dependencies:** None

**Acceptance criteria:**
- [x] All project directories exist (`src/datalens/`, `tests/`, `tests/fixtures/`, `docs/`, `reports/`)
- [x] `pyproject.toml` defines project metadata, `pytest` as dev dependency, and `[project.scripts]` entry
- [x] `src/datalens/__init__.py` exists (empty)
- [x] `CLAUDE.md` contains: scope boundaries, context-drift pre-flight protocol, code style, session discipline rules
- [x] `docs/ARCHITECTURE.md` contains: module map, data flow, I/O ownership, dependency rationale
- [x] `docs/TASKS.md` contains: all tasks (T00–T06) with objective, dependencies, acceptance criteria, estimated time, DoD
- [x] `docs/DECISIONS.md` contains: initial ADR entries for all architecture choices
- [x] `docs/EXPERIMENT.md` contains: experiment objective, baseline definitions, controlled variables, measured variables, hypotheses, comparison methodology
- [x] `docs/SESSION_LOG.md` contains: header structure and initial entry
- [x] `docs/CHANGELOG.md` contains: header and initial entry
- [x] `README.md` contains: project description, install instructions, run instructions
- [x] 6 fixture CSV files exist in `tests/fixtures/` and are valid CSV

**Estimated time:** 110 minutes

**Definition of Done:**
1. All files listed above exist and are non-empty
2. `pyproject.toml` is valid TOML
3. Fixture CSVs are valid and parseable
4. All documentation files are internally consistent
5. SESSION_LOG.md initial entry written
6. CHANGELOG.md initial entry written
7. Git checkpoint created: `chore(T00): project operating system`

---

## T01 — loader.py: CSV Reading and Parsing

**Objective:** Implement `loader.py` to read CSV files from disk, parse them with the stdlib `csv` module, and return structured data.

**Dependencies:** T00 complete

**Acceptance criteria:**
- [x] `loader.py` has a public function `load_csv(path: str)` that returns `(rows, column_names, row_count)`
- [x] Returns `rows` as `list[dict]`, `column_names` as `list[str]`, `row_count` as `int`
- [x] Correctly parses all 5 fixture files without error
- [x] Handles quoted fields with embedded commas
- [x] Handles empty CSV (header only, 0 data rows) without crashing
- [x] Raises a clear error for a file that does not exist
- [x] All 4 `test_loader.py` tests pass

**Test coverage note:** Acceptance criteria define behavior, not a fixed test count. Baseline 2 provides 7 tests covering all 6 fixtures plus the missing-file case. The "All 4 tests" wording in the original specification is a Baseline 1 historical artifact and does not constrain Baseline 2 test count.

**Estimated time:** 35 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_loader.py` passes (7 tests after corrective pass)
3. `docs/TASKS.md` updated (T01 marked complete)
4. `docs/SESSION_LOG.md` updated
5. `docs/CHANGELOG.md` entry written
6. Git checkpoint: `feat(T01): CSV loader module` (original) + `fix(T01): add explicit quoted-comma fixture and expand test coverage` (corrective)

---

## T02 — profiler.py: Per-Column Profiling

**Objective:** Implement `profiler.py` to compute per-column statistics from loaded CSV data.

**Dependencies:** T01 complete

**Acceptance criteria:**
- [x] `profiler.py` has a public function `profile(rows, column_names)` returning `list[dict]`
- [x] Per-column output includes: `name`, `type` (integer/float/string/mixed), `missing_count`, `missing_pct`, `unique_count`
- [x] Numeric columns include: `min`, `max`, `mean`, `median`, `std`
- [x] Correctly profiles all 6 fixture files
- [x] Handles empty columns (all missing) without crashing
- [x] All 9 `test_profiler.py` tests pass (corrective pass)

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_profiler.py` passes (5 tests)
3. `docs/TASKS.md` updated (T02 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T02): column profiler module`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T03

---

## T03 — quality.py: Composite Quality Score

**Objective:** Implement `quality.py` to aggregate profiler output into a composite 0–100 quality score.

**Dependencies:** T02 complete

**Scoring contract:**

```
completeness = 1 - (missing_pct / 100)

type_consistency:
    integer, float, string → 1.0
    mixed → 0.5

distinctness:
    min(unique_count / total_rows, 1.0)
    when total_rows > 0

column_score =
    0.50 × completeness
  + 0.30 × type_consistency
  + 0.20 × distinctness

composite_score =
    mean(column_scores) × 100
```

**Boundary conditions:**
- If `total_rows == 0`: `composite_score = 0.0`, `column_scores = []`
- All scores are floats in range [0, 100]

**API:** `compute_score(profiles: list[dict], total_rows: int) -> dict`

**Acceptance criteria:**
- [x] `quality.py` has a public function `compute_score(profiles, total_rows)` returning `dict`
- [x] Returned dict has keys `composite_score` (float 0–100) and `column_scores` (list of dicts with `name` and `score`)
- [x] Composite score is a float in range [0, 100]
- [x] A completely clean dataset (clean_simple.csv) scores >= 90
- [x] A dataset containing missing values scores lower than an otherwise equivalent complete dataset
- [x] Score computation is deterministic (same input → same output)
- [x] Edge case: empty dataset (total_rows=0) returns composite_score=0.0
- [x] All 9 `test_quality.py` tests pass

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_quality.py` passes (9 tests)
3. `docs/TASKS.md` updated (T03 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T03): quality score module`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T04

---

## T04 — report.py: HTML Report Generation

**Objective:** Implement `report.py` to generate a self-contained HTML report from profiling and scoring data.

**Dependencies:** T03 complete

**API contract:**
```python
def generate(
    profiles: list[dict],
    result: dict,
    row_count: int,
    duplicate_row_count: int,
    output_path: str,
) -> None
```

**Templating:** jinja2 `Environment(autoescape=True)` with an inline template string. No separate template file.

**Styling:** Minimal inline CSS — readable typography, section headings, table borders, padding, readable score display. No JavaScript, no responsive frameworks, no themes.

**Quality score display:** "Quality Score: X / 100" with a compact per-column score breakdown within the same section.

**Required report sections:**
1. Row count
2. Column count
3. Duplicate-row count
4. Detected type per column (data types table)
5. Missing count and percentage per column
6. Unique/distinct count per column
7. Numeric statistics (min, max, mean, median, std) — numeric columns only
8. Composite quality score (0–100)
9. Compact per-column score breakdown
10. Self-contained valid HTML

**Edge cases:**
- `edge_empty.csv` has 0 data rows + header columns — report shows row_count=0, column_count=N, score=0.0
- CSV-derived values with HTML-special characters must be escaped

**Acceptance criteria:**
- [ ] `report.py` has a public function `generate(profiles, result, row_count, duplicate_row_count, output_path)` that writes an HTML file
- [ ] Output file exists at the specified path after the function returns
- [ ] HTML contains all required sections
- [ ] HTML is valid and readable in a browser (DOCTYPE, proper HTML structure, inline CSS)
- [ ] HTML-escapes CSV-derived values (test with `<`, `>`, `&`, `"` characters)
- [ ] All 5 `test_report.py` tests pass

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_report.py` passes (5 tests)
3. `docs/TASKS.md` updated (T04 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T04): HTML report generator`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T05

---

## T05 — cli.py: CLI Entry Point

**Objective:** Implement `cli.py` as the command-line entry point that orchestrates the full pipeline. cli.py is an orchestrator only.

**Dependencies:** T04 complete

**Command syntax:**
```
datalens <csv_path>
```

**Arguments:**
- `csv_path` (positional, required) — path to the CSV file to analyze

No options, no flags, no subcommands.

**Output path:** `reports/<input filename stem>.html`

**CLI stdout summary:**
```
Report written to: reports/<stem>.html | Rows: N | Columns: N | Quality Score: X / 100
```

**Duplicate-row detection:**
- Two rows are duplicates when they have exactly the same column/value pairs
- Implementation: `tuple(sorted(row.items()))`
- Computed in cli.py from raw rows returned by `load_csv()`

**Error handling:**
- Missing file → print error to stderr, exit 1
- Malformed CSV → print error to stderr, exit 1
- Permission errors → print error to stderr, exit 1

**Exit codes:**
- `0` — success, report generated
- `1` — failure (any error)

**Acceptance criteria:**
- [ ] `cli.py` provides `main()` callable via `python -m datalens <path>` or the `pyproject.toml` scripts entry
- [ ] Accepts a single positional argument: path to a CSV file
- [ ] Runs the full pipeline: load → profile → score → duplicate count → report
- [ ] Prints a one-line summary to stdout: report path, row count, column count, quality score
- [ ] Writes the HTML report to `reports/<stem>.html`
- [ ] Exits with code 0 on success, non-zero on failure
- [ ] All 3 `test_cli.py` tests pass (2 unit + 1 integration)

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_cli.py` passes (3 tests: 2 unit + 1 integration)
3. `docs/TASKS.md` updated (T05 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T05): CLI entry point`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T06

---

## T06 — Final Review and Polish

**Objective:** Verify the complete project meets all requirements and is ready for experiment comparison. Run scalability benchmarks, produce experiment results, and finalize Baseline 2.

**Dependencies:** T05 complete

**Benchmark methodology:**
- Benchmark data generated by `benchmarks/benchmark_generator.py` with `random.seed(42)`
- Generated CSVs stored in `benchmarks/data/` (gitignored — not committed)
- Reproducibility: deterministic generator + seed + dimensions + environment metadata + Git commit
- Peak memory measured via `/usr/bin/time -l` (macOS), normalized to MB
- Environment metadata recorded: machine, CPU architecture, macOS version, Python version, Git commit
- Timeouts: 10k×20: 60s, 100k×20: 120s, 1M×20: 300s, 100k×100: 300s

**Benchmark datasets (not committed):**
- `benchmarks/data/benchmark_10k_20.csv` — 10,000 rows × 20 columns
- `benchmarks/data/benchmark_100k_20.csv` — 100,000 rows × 20 columns
- `benchmarks/data/benchmark_1m_20.csv` — 1,000,000 rows × 20 columns
- `benchmarks/data/benchmark_100k_100.csv` — 100,000 rows × 100 columns

**Experiment results document:**
- `docs/EXPERIMENT_RESULTS.md` — Baseline 2 implementation summary, test results, development process, context drift, scalability benchmarks, limitations, environment metadata, Git commit used for benchmarking

**Acceptance criteria:**
- [ ] Full `pytest` suite passes (29/29)
- [ ] README.md contains realistic example run with fixture output
- [ ] docs/CHANGELOG.md has entries for all completed tasks (T00–T05)
- [ ] docs/SESSION_LOG.md has final entry
- [ ] No unused imports or dead code visible on review
- [ ] pyproject.toml installs cleanly (`pip install -e .`)
- [ ] benchmarks/benchmark_generator.py exists and is functional
- [ ] benchmarks/data/ is gitignored
- [ ] All 4 benchmarks run and results recorded
- [ ] docs/EXPERIMENT_RESULTS.md written with Baseline 2 metrics

**Estimated time:** 130 minutes

**Definition of Done:**
1. All acceptance criteria met
2. Full test suite green
3. Benchmark data generated and results recorded
4. docs/EXPERIMENT_RESULTS.md written
5. docs/TASKS.md updated (T06 marked complete)
6. docs/SESSION_LOG.md final entry written
7. docs/CHANGELOG.md entry written
8. Git checkpoint: `chore(T06): final review and polish`
9. Human approval received before push/tag
