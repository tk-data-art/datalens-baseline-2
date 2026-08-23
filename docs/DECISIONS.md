# DataLens — Architecture Decisions

---

## ADR-001: Python with stdlib csv module for CSV parsing

**Status:** Accepted

**Context:** DataLens needs to read and parse CSV files. Multiple approaches available: stdlib `csv` module, `pandas`, `polars`, `csvkit`.

**Decision:** Use the Python standard library `csv.DictReader` for CSV parsing.

**Rationale:** Stdlib is sufficient for the task scope. No external dependency needed for CSV parsing. `csv.DictReader` handles quoted fields, embedded commas, and header mapping natively. Zero additional dependencies.

**Consequences:** CSV parsing is limited to what `csv.DictReader` supports (which covers all required fixtures). No type inference during loading — that is profiler's responsibility.

---

## ADR-002: One public function per module

**Status:** Accepted

**Context:** DataLens has 5 modules in a pipeline. Each needs a defined interface for inter-module communication.

**Decision:** Each module exposes exactly one public function. Internal helpers use underscore prefix.

**Rationale:** Single public function per module keeps the API surface minimal and the module boundaries clear. Each module has exactly one job. This matches the pipeline architecture where data flows linearly from loader → profiler → quality → report.

**Consequences:** Any additional functionality must be added as a new module with its own public function, not as a second public function in an existing module.

---

## ADR-003: Plain Python data structures for inter-module communication

**Status:** Accepted

**Context:** Modules need to exchange data: loader → profiler → quality → report.

**Decision:** Use plain Python data structures (lists, dicts) for inter-module data exchange. No custom classes, no dataclasses, no TypedDicts.

**Rationale:** Plain dicts require zero boilerplate, are easy to inspect during debugging, and have no serialization concerns. The data shapes are simple and well-documented. A custom type system would add complexity without solving a real problem.

**Consequences:** Module contracts are documented in CLAUDE.md and ARCHITECTURE.md rather than enforced by types. Callers must respect the documented shape.

---

## ADR-004: Six fixture CSV files for testing

**Status:** Accepted

**Context:** Tests need representative CSV data covering normal cases and edge cases.

**Decision:** Six fixture files: `clean_simple.csv`, `missing_values.csv`, `mixed_types.csv`, `duplicates.csv`, `edge_empty.csv`, `quoted_commas.csv`.

**Rationale:** Five files cover the core test scenarios: clean data, missing values, mixed types, duplicates, and empty. The sixth (`quoted_commas.csv`) covers the quoted-field-with-embedded-commas edge case explicitly.

**Consequences:** All fixture files must be valid CSV and must be parseable by the stdlib `csv` module. Fixture content is the same for both Baseline 1 and Baseline 2.

---

## ADR-005: jinja2 for HTML report templating

**Status:** Accepted

**Context:** report.py needs to generate self-contained HTML with dynamic content. Options: string formatting, f-strings, string.Template, jinja2.

**Decision:** Use jinja2 `Environment(autoescape=True)` with an inline template string. No separate template file.

**Rationale:** jinja2 provides auto-escaping (critical for CSV-derived values that may contain HTML special characters), clean template syntax, and is a well-known library. Inline template string avoids file I/O for the template. `autoescape=True` ensures HTML security without manual escaping.

**Consequences:** jinja2 >= 3.1 is the only external runtime dependency. No separate `.html` template files are needed.

---

## ADR-006: Single branch main, one commit per task

**Status:** Accepted

**Context:** Git workflow strategy for the experiment.

**Decision:** Single branch `main`. One commit per completed task. No feature branches, no pull requests.

**Rationale:** Simplifies the experiment comparison. Each task's changes are a single commit, making diffs between baselines straightforward. No merge conflicts possible.

**Consequences:** Commit history is linear. Each task commit is independently comparable between Baseline 1 and Baseline 2.

---

## ADR-007: report.py receives all data as parameters

**Status:** Accepted

**Context:** report.py needs profiling results, quality scores, row count, and duplicate count to render the HTML report.

**Decision:** report.py receives all data as function parameters: `generate(profiles, result, row_count, duplicate_row_count, output_path)`. It does not call loader, profiler, or quality modules directly.

**Rationale:** report.py is a pure renderer. Receiving data as parameters keeps it decoupled from the data pipeline. This preserves module boundaries — report.py does not import from other datalens modules.

**Consequences:** cli.py (the orchestrator) is responsible for passing all required data to report.py. The duplicate_row_count is computed in cli.py from raw rows, not in report.py.
