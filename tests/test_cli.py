"""Tests for cli.py — CLI entry point."""

import pathlib

import pytest

from datalens.cli import main


FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


def test_main_success(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    exit_code = main([str(FIXTURES / "clean_simple.csv")])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""
    assert "Report written to: reports/clean_simple.html" in captured.out
    assert "Rows:" in captured.out
    assert "Columns:" in captured.out
    assert "Quality Score:" in captured.out


def test_main_missing_file(capsys):
    exit_code = main(["tests/fixtures/nonexistent.csv"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error:" in captured.err


def test_main_integration_clean_simple(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exit_code = main([str(FIXTURES / "clean_simple.csv")])

    assert exit_code == 0

    report_path = tmp_path / "reports" / "clean_simple.html"
    assert report_path.exists()

    html = report_path.read_text()
    assert "<!DOCTYPE html>" in html
    assert "Quality Score:" in html
