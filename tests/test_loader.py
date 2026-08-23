"""Tests for loader.py — CSV reading and parsing."""

import pytest

from datalens.loader import load_csv


def test_load_clean_simple():
    rows, columns, count = load_csv("tests/fixtures/clean_simple.csv")
    assert count == 5
    assert columns == ["name", "age", "salary", "department", "city"]
    assert len(rows) == 5
    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == "30"


def test_load_missing_values():
    rows, columns, count = load_csv("tests/fixtures/missing_values.csv")
    assert count == 6
    assert columns == ["name", "age", "salary", "department", "city"]
    assert rows[1]["age"] == ""
    assert rows[2]["salary"] == ""


def test_load_mixed_types():
    rows, columns, count = load_csv("tests/fixtures/mixed_types.csv")
    assert count == 6
    assert columns == ["name", "age", "salary", "department", "city"]
    assert rows[0]["name"] == "Alice"


def test_load_duplicates():
    rows, columns, count = load_csv("tests/fixtures/duplicates.csv")
    assert count == 5
    assert columns == ["name", "age", "salary", "department", "city"]
    assert rows[0] == rows[2]


def test_load_edge_empty():
    rows, columns, count = load_csv("tests/fixtures/edge_empty.csv")
    assert count == 0
    assert columns == ["name", "age", "salary", "department", "city"]
    assert rows == []


def test_quoted_fields_with_embedded_commas():
    rows, columns, count = load_csv("tests/fixtures/quoted_commas.csv")
    assert count == 3
    assert columns == ["name", "description", "value"]
    assert rows[0]["description"] == "Senior Engineer, Lead"
    assert rows[1]["description"] == "Manager, Sales"


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        load_csv("nonexistent_file.csv")
