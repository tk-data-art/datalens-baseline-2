# DataLens

A command-line CSV data-quality analyzer. Reads a CSV file, profiles its contents, computes quality metrics, and produces a self-contained HTML report.

This project is Baseline 2 of a controlled experiment comparing Claude Code with and without optimization plugins. See `docs/EXPERIMENT.md` for details.

## Install

```bash
pip install -e .
```

## Run

```bash
datalens path/to/file.csv
```

The report is written to `reports/<input_filename_stem>.html`.

## Requirements

- Python 3.11+
- jinja2 >= 3.1
