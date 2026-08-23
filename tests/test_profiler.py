"""Tests for profiler.py — per-column profiling."""

import pytest

from datalens.profiler import profile


def test_profile_clean_simple():
    rows, columns, _ = _load("tests/fixtures/clean_simple.csv")
    profiles = profile(rows, columns)
    assert len(profiles) == 5
    age = _find(profiles, "age")
    assert age["type"] == "integer"
    assert age["missing_count"] == 0
    assert age["missing_pct"] == 0.0
    assert age["unique_count"] == 5
    assert age["min"] == 25
    assert age["max"] == 35
    assert age["mean"] == 30.0
    assert age["median"] == 30.0


def test_profile_missing_values():
    rows, columns, _ = _load("tests/fixtures/missing_values.csv")
    profiles = profile(rows, columns)
    salary = _find(profiles, "salary")
    assert salary["missing_count"] == 1
    assert salary["missing_pct"] == pytest.approx(16.67, rel=0.01)
    assert salary["unique_count"] == 5
    department = _find(profiles, "department")
    assert department["missing_count"] == 1
    assert department["type"] == "string"


def test_profile_mixed_types():
    rows, columns, _ = _load("tests/fixtures/mixed_types.csv")
    profiles = profile(rows, columns)
    salary = _find(profiles, "salary")
    assert salary["type"] == "integer"
    name = _find(profiles, "name")
    assert name["type"] == "string"
    assert name["unique_count"] == 6


def test_profile_duplicates():
    rows, columns, _ = _load("tests/fixtures/duplicates.csv")
    profiles = profile(rows, columns)
    name = _find(profiles, "name")
    assert name["unique_count"] == 3
    assert name["missing_count"] == 0


def test_profile_edge_empty():
    rows, columns, _ = _load("tests/fixtures/edge_empty.csv")
    profiles = profile(rows, columns)
    assert len(profiles) == 5
    for p in profiles:
        assert p["missing_count"] == 0
        assert p["missing_pct"] == 0.0
        assert p["unique_count"] == 0
        assert p["type"] == "string"
        assert "min" not in p


def test_profile_all_missing_column():
    rows = [{"a": "", "b": "1"}, {"a": "", "b": "2"}]
    profiles = profile(rows, ["a", "b"])
    col_a = _find(profiles, "a")
    assert col_a["type"] == "string"
    assert col_a["missing_count"] == 2
    assert col_a["missing_pct"] == 100.0
    assert col_a["unique_count"] == 0
    assert "min" not in col_a
    assert "max" not in col_a
    assert "std" not in col_a


def test_profile_std_sample():
    rows = [{"v": "1"}, {"v": "2"}, {"v": "3"}]
    profiles = profile(rows, ["v"])
    v = _find(profiles, "v")
    assert v["std"] == pytest.approx(1.0, rel=0.01)


def test_profile_std_single_value():
    rows = [{"v": "5"}]
    profiles = profile(rows, ["v"])
    v = _find(profiles, "v")
    assert v["std"] == 0.0
    assert v["mean"] == 5.0


def _load(path):
    from datalens.loader import load_csv
    return load_csv(path)


def _find(profiles, name):
    for p in profiles:
        if p["name"] == name:
            return p
    raise KeyError(f"Column {name} not found")
