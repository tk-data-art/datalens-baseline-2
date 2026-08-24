# DataLens — Changelog

---

## [0.1.0] — 2026-08-23

### Added
- Project scaffolding: directory structure, pyproject.toml, gitignore
- Package initialization: `src/datalens/__init__.py`
- Documentation: CLAUDE.md, README.md, docs/ARCHITECTURE.md, docs/TASKS.md, docs/DECISIONS.md, docs/EXPERIMENT.md, docs/TASK_COMPLETION.md, docs/EXPERIMENT_RESULTS.md
- Session tracking: docs/SESSION_LOG.md initial entry
- Fixture CSV files: clean_simple.csv, missing_values.csv, mixed_types.csv, duplicates.csv, edge_empty.csv, quoted_commas.csv
- Test placeholders: empty test files for all 5 modules
- Benchmark scaffold: benchmarks/benchmark_generator.py
- Reports directory: reports/ (gitignored output target)

### Changed
- Initial project structure established

### Fixed
- N/A (T00 setup)

---

## [0.2.0] — 2026-08-23

### Added
- `src/datalens/loader.py` — CSV loader module with `load_csv(path)` public function
- `tests/test_loader.py` — 7 unit tests covering all 6 fixtures plus missing-file edge case

### Changed
- `tests/test_loader.py` — replaced placeholder with test functions

### Fixed
- N/A (T01 implementation)

---

## [0.3.0] — 2026-08-23

### Added
- `src/datalens/profiler.py` — column profiler module with `profile(rows, column_names)` public function
- `tests/test_profiler.py` — 8 unit tests covering all 6 fixtures, all-missing column, std edge cases

### Changed
- `src/datalens/profiler.py` — removed dead branch in `_infer_type()` (line 38)
- `tests/test_profiler.py` — added `test_profile_quoted_commas` for quoted_commas.csv coverage (9 tests total)

### Fixed
- N/A (T02 implementation)

---

## [0.4.0] — 2026-08-23

### Added
- `src/datalens/quality.py` — quality score module with `compute_score(profiles, total_rows)` public function
- `tests/test_quality.py` — 9 unit tests covering clean dataset, missing values, mixed types, edge cases, determinism, and all-missing column

### Changed
- N/A (T03 implementation)

### Fixed
- N/A (T03 implementation)

---

## [0.5.0] — 2026-08-23

### Added
- `src/datalens/report.py` — HTML report generator with `generate(profiles, result, row_count, duplicate_row_count, output_path)` public function
- `tests/test_report.py` — 5 unit tests covering clean_simple, HTML escaping (`< > & " '`), valid HTML structure, empty dataset, and score display

### Changed
- N/A (T04 implementation)

### Fixed
- N/A (T04 implementation)

---

## [0.6.0] — 2026-08-23

### Added
- `src/datalens/cli.py` — CLI entry point with `main(argv=None) -> int` public function; orchestrates full pipeline (load → profile → score → duplicate count → report)
- `src/datalens/__main__.py` — thin module-entry wrapper delegating to `cli.main()`
- `tests/test_cli.py` — 3 tests (2 unit + 1 integration) covering success path, missing-file error, and end-to-end pipeline

### Changed
- N/A (T05 implementation)

### Fixed
- N/A (T05 implementation)
