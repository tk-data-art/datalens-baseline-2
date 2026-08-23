"""Tests for report.py — HTML report generation."""

import pytest

from datalens.profiler import profile
from datalens.quality import compute_score
from datalens.report import generate


def _load(path):
    from datalens.loader import load_csv
    return load_csv(path)


def test_generate_clean_simple(tmp_path):
    rows, columns, row_count = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)

    output = tmp_path / "reports" / "clean_simple.html"
    generate(profiles, result, row_count, 0, str(output))

    assert output.exists()
    html = output.read_text()

    assert "<!DOCTYPE html>" in html
    assert "Rows:" in html
    assert "Columns:" in html
    assert "Duplicate rows:" in html
    assert "Data Types" in html
    assert "Missing Values" in html
    assert "Unique Values" in html
    assert "Numeric Statistics" in html
    assert "Quality Score" in html
    assert "Per-Column Scores" in html


def test_generate_html_escaping(tmp_path):
    profiles = [
        {"name": "<script>", "type": "string", "missing_count": 0, "missing_pct": 0.0, "unique_count": 1},
        {"name": "a&b", "type": "string", "missing_count": 0, "missing_pct": 0.0, "unique_count": 1},
        {"name": '"quoted"', "type": "string", "missing_count": 0, "missing_pct": 0.0, "unique_count": 1},
        {"name": "it's", "type": "string", "missing_count": 0, "missing_pct": 0.0, "unique_count": 1},
    ]
    result = {
        "composite_score": 100.0,
        "column_scores": [
            {"name": "<script>", "score": 1.0},
            {"name": "a&b", "score": 1.0},
            {"name": '"quoted"', "score": 1.0},
            {"name": "it's", "score": 1.0},
        ],
    }

    output = tmp_path / "escape.html"
    generate(profiles, result, 1, 0, str(output))

    html = output.read_text()

    assert "<script>" not in html
    assert "a&b" not in html
    assert '"quoted"' not in html
    assert "it's" not in html

    assert "&lt;script&gt;" in html
    assert "a&amp;b" in html
    assert "&#34;" in html
    assert "&#39;" in html


def test_generate_valid_html(tmp_path):
    rows, columns, row_count = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)

    output = tmp_path / "report.html"
    generate(profiles, result, row_count, 0, str(output))

    html = output.read_text()

    assert html.startswith("<!DOCTYPE html>")
    assert "<html" in html
    assert "<head>" in html
    assert "<body>" in html
    assert "</body>" in html
    assert "</html>" in html


def test_generate_empty_dataset(tmp_path):
    rows, columns, row_count = _load("tests/fixtures/edge_empty.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)

    output = tmp_path / "report.html"
    generate(profiles, result, row_count, 0, str(output))

    html = output.read_text()

    assert "Rows: 0" in html
    assert f"Columns: {len(profiles)}" in html
    assert "Quality Score: 0.0 / 100" in html


def test_generate_score_display(tmp_path):
    profiles = [
        {"name": "col_a", "type": "integer", "missing_count": 0, "missing_pct": 0.0, "unique_count": 5, "min": 1, "max": 5, "mean": 3.0, "median": 3.0, "std": 1.58},
    ]
    result = {"composite_score": 85.5, "column_scores": [{"name": "col_a", "score": 0.855}]}

    output = tmp_path / "report.html"
    generate(profiles, result, 5, 2, str(output))

    html = output.read_text()

    assert "Quality Score: 85.5 / 100" in html
    assert "Per-Column Scores" in html
    assert "col_a" in html
