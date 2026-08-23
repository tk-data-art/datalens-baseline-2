"""Tests for quality.py — composite quality scoring."""

import pytest

from datalens.profiler import profile
from datalens.quality import compute_score


def _load(path):
    from datalens.loader import load_csv
    return load_csv(path)


def test_score_clean_simple():
    rows, columns, row_count = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)
    assert result["composite_score"] >= 90.0
    assert len(result["column_scores"]) == 5
    for cs in result["column_scores"]:
        assert 0.0 <= cs["score"] <= 1.0


def test_score_missing_values():
    rows_miss, columns_miss, row_count_miss = _load("tests/fixtures/missing_values.csv")
    profiles_miss = profile(rows_miss, columns_miss)
    result_miss = compute_score(profiles_miss, row_count_miss)

    rows_clean, columns_clean, row_count_clean = _load("tests/fixtures/clean_simple.csv")
    profiles_clean = profile(rows_clean, columns_clean)
    result_clean = compute_score(profiles_clean, row_count_clean)

    assert result_miss["composite_score"] < result_clean["composite_score"]


def test_score_mixed_types():
    rows, columns, row_count = _load("tests/fixtures/mixed_types.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)
    assert result["composite_score"] < 100.0
    # composite < 100 because distinctness caps at 1.0 but columns have < 100% distinctness
    assert result["composite_score"] >= 90.0


def test_score_edge_empty():
    rows, columns, row_count = _load("tests/fixtures/edge_empty.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)
    assert result["composite_score"] == 0.0
    assert result["column_scores"] == []


def test_score_deterministic():
    rows, columns, row_count = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    result1 = compute_score(profiles, row_count)
    result2 = compute_score(profiles, row_count)
    assert result1 == result2


def test_score_range():
    profiles = [
        {"name": "a", "type": "integer", "missing_count": 0, "missing_pct": 0.0, "unique_count": 5},
        {"name": "b", "type": "string", "missing_count": 3, "missing_pct": 60.0, "unique_count": 2},
    ]
    result = compute_score(profiles, 5)
    assert 0.0 <= result["composite_score"] <= 100.0
    for cs in result["column_scores"]:
        assert 0.0 <= cs["score"] <= 1.0


def test_score_all_missing():
    profiles = [
        {"name": "a", "type": "string", "missing_count": 5, "missing_pct": 100.0, "unique_count": 0},
        {"name": "b", "type": "string", "missing_count": 5, "missing_pct": 100.0, "unique_count": 0},
    ]
    result = compute_score(profiles, 5)
    for cs in result["column_scores"]:
        assert cs["score"] == pytest.approx(0.30, abs=0.001)
    assert result["composite_score"] == pytest.approx(30.0, abs=0.001)


def test_score_single_row_missing():
    profiles = [
        {"name": "v", "type": "string", "missing_count": 1, "missing_pct": 100.0, "unique_count": 0},
    ]
    result = compute_score(profiles, 1)
    assert result["composite_score"] == pytest.approx(30.0, abs=0.001)
    assert result["column_scores"][0]["score"] == pytest.approx(0.30, abs=0.001)


def test_score_column_count():
    rows, columns, row_count = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)
    assert len(result["column_scores"]) == len(profiles)
    for cs, p in zip(result["column_scores"], profiles):
        assert cs["name"] == p["name"]
