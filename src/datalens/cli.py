"""CLI entry point — orchestrates the full DataLens pipeline."""

import sys

from datalens.loader import load_csv
from datalens.profiler import profile
from datalens.quality import compute_score
from datalens.report import generate


def main(argv=None):
    """Run the DataLens pipeline on a CSV file.

    Returns 0 on success, 1 on failure.
    """
    try:
        if argv is None:
            argv = sys.argv[1:]

        if not argv:
            print("Error: missing csv_path argument", file=sys.stderr)
            return 1

        csv_path = argv[0]

        rows, columns, row_count = load_csv(csv_path)
        profiles = profile(rows, columns)
        result = compute_score(profiles, row_count)

        seen = set()
        duplicate_row_count = 0
        for row in rows:
            key = tuple(sorted(row.items()))
            if key in seen:
                duplicate_row_count += 1
            else:
                seen.add(key)

        stem = csv_path.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]
        output_path = f"reports/{stem}.html"

        generate(profiles, result, row_count, duplicate_row_count, output_path)

        print(
            f"Report written to: {output_path} | Rows: {row_count} | Columns: {len(profiles)} | Quality Score: {result['composite_score']} / 100"
        )
        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
