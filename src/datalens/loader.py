"""CSV loader module — reads a CSV file and returns structured data."""

import csv
from pathlib import Path


def load_csv(path: str) -> tuple[list[dict], list[str], int]:
    """Read a CSV file and return rows, column names, and row count."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with open(file_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        column_names = reader.fieldnames or []
        rows = [dict(row) for row in reader]
    return rows, column_names, len(rows)
