#!/usr/bin/env python3
"""
Benchmark data generator for DataLens scalability testing.

Generates deterministic CSV benchmark datasets using random.seed(42).
Datasets are stored in benchmarks/data/ (gitignored).

Usage:
    python benchmarks/benchmark_generator.py

Generated files (not committed):
    benchmarks/data/benchmark_10k_20.csv   — 10,000 rows × 20 columns
    benchmarks/data/benchmark_100k_20.csv  — 100,000 rows × 20 columns
    benchmarks/data/benchmark_1m_20.csv    — 1,000,000 rows × 20 columns
    benchmarks/data/benchmark_100k_100.csv — 100,000 rows × 100 columns
"""

import csv
import os
import random

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

NAME_POOL = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank",
    "Ivy", "Jack", "Kate", "Leo", "Mia", "Nick", "Olivia", "Paul",
]

DEPT_POOL = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Legal"]
CITY_POOL = ["NYC", "LA", "Chicago", "SF", "Boston", "Seattle", "Austin"]


def generate_rows(num_rows, num_cols):
    """Generate deterministic rows for a benchmark dataset."""
    rows = []
    for i in range(num_rows):
        row = {
            "id": i + 1,
            "name": NAME_POOL[i % len(NAME_POOL)],
            "age": random.randint(22, 65),
            "salary": random.randint(40000, 150000),
            "department": DEPT_POOL[i % len(DEPT_POOL)],
            "city": CITY_POOL[i % len(CITY_POOL)],
        }
        for j in range(6, num_cols):
            row[f"col_{j}"] = random.randint(0, 1000)
        rows.append(row)
    return rows


def write_csv(path, rows):
    """Write rows to a CSV file."""
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    datasets = [
        ("benchmark_10k_20.csv", 10_000, 20),
        ("benchmark_100k_20.csv", 100_000, 20),
        ("benchmark_1m_20.csv", 1_000_000, 20),
        ("benchmark_100k_100.csv", 100_000, 100),
    ]
    for filename, num_rows, num_cols in datasets:
        path = os.path.join(OUTPUT_DIR, filename)
        print(f"Generating {filename} ({num_rows} rows x {num_cols} cols)...")
        rows = generate_rows(num_rows, num_cols)
        write_csv(path, rows)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"  Written: {path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
