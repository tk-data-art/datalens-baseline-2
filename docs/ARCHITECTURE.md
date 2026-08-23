# DataLens — Architecture

## Module Map

| Module | Public function | Responsibility |
|---|---|---|
| `loader.py` | `load_csv(path: str)` | Reads CSV from disk, returns (rows, column_names, row_count) |
| `profiler.py` | `profile(rows, column_names)` | Computes per-column type, missing count/pct, unique count, numeric stats |
| `quality.py` | `compute_score(profiles, total_rows)` | Aggregates column scores into composite 0–100 quality score |
| `report.py` | `generate(profiles, result, row_count, duplicate_row_count, output_path)` | Renders self-contained HTML report |
| `cli.py` | `main()` | Orchestrates pipeline: load → profile → score → duplicate count → report |

## Data Flow

```
CSV file
  → loader.load_csv()        → (rows, column_names, row_count)
    → profiler.profile()     → list[column_profile]
      → quality.compute_score() → {"composite_score", "column_scores"}
        → report.generate()  → HTML file on disk
  ← cli.main() orchestrates the chain and computes duplicate_row_count from raw rows
```

## I/O Ownership

| Module | Inputs | Outputs | Side effects |
|---|---|---|---|
| `loader.py` | CSV file path | rows (list[dict]), column_names (list[str]), row_count (int) | Reads file from disk |
| `profiler.py` | rows, column_names | list[dict] (column profiles) | None |
| `quality.py` | profiles, total_rows | dict (composite_score, column_scores) | None |
| `report.py` | profiles, result, row_count, duplicate_row_count, output_path | None | Writes HTML file to disk |
| `cli.py` | CSV file path (CLI arg) | None (stdout summary) | Runs pipeline, writes report |

## Dependency Rationale

- **std only:** loader.py, profiler.py, quality.py, cli.py use only the Python standard library
- **jinja2 only:** report.py uses jinja2 for HTML templating — the only external dependency
- **No circular imports:** Each module depends only on modules upstream in the data flow
- **Plain Python data structures:** Lists and dicts for inter-module communication — no custom types or classes

## Scoring Contract

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

## Edge Cases

- `std=0.0` for numeric columns with fewer than 2 non-missing observations
- Empty CSV (header only): returns zero rows without crashing
- Missing file: raises `FileNotFoundError` with descriptive message
- CSV-derived values with HTML-special characters: auto-escaped in report output
