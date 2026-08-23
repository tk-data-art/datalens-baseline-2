"""HTML report generator — renders profiling and scoring data to a self-contained HTML file."""

import pathlib

import jinja2


_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DataLens Report</title>
    <style>
        body { font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5; }
        table { border-collapse: collapse; margin: 1rem 0; }
        th, td { border: 1px solid #ccc; padding: 0.4rem 0.8rem; text-align: left; }
        th { background: #f5f5f5; }
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.2rem; margin-top: 2rem; }
        .score { font-size: 1.4rem; font-weight: bold; }
    </style>
</head>
<body>
    <h1>DataLens Report</h1>

    <h2>Summary</h2>
    <p>Rows: {{ row_count }}</p>
    <p>Columns: {{ column_count }}</p>
    <p>Duplicate rows: {{ duplicate_row_count }}</p>

    <h2>Data Types</h2>
    <table>
        <tr><th>Column</th><th>Type</th></tr>
        {% for p in profiles %}
        <tr><td>{{ p.name }}</td><td>{{ p.type }}</td></tr>
        {% endfor %}
    </table>

    <h2>Missing Values</h2>
    <table>
        <tr><th>Column</th><th>Missing Count</th><th>Missing %</th></tr>
        {% for p in profiles %}
        <tr><td>{{ p.name }}</td><td>{{ p.missing_count }}</td><td>{{ p.missing_pct }}</td></tr>
        {% endfor %}
    </table>

    <h2>Unique Values</h2>
    <table>
        <tr><th>Column</th><th>Unique Count</th></tr>
        {% for p in profiles %}
        <tr><td>{{ p.name }}</td><td>{{ p.unique_count }}</td></tr>
        {% endfor %}
    </table>

    {% if numeric_profiles %}
    <h2>Numeric Statistics</h2>
    <table>
        <tr><th>Column</th><th>Min</th><th>Max</th><th>Mean</th><th>Median</th><th>Std</th></tr>
        {% for p in numeric_profiles %}
        <tr><td>{{ p.name }}</td><td>{{ p.min }}</td><td>{{ p.max }}</td><td>{{ p.mean }}</td><td>{{ p.median }}</td><td>{{ p.std }}</td></tr>
        {% endfor %}
    </table>
    {% endif %}

    <h2>Quality Score</h2>
    <p class="score">Quality Score: {{ result.composite_score }} / 100</p>
    <h3>Per-Column Scores</h3>
    <table>
        <tr><th>Column</th><th>Score</th></tr>
        {% for cs in result.column_scores %}
        <tr><td>{{ cs.name }}</td><td>{{ cs.score }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""


def generate(profiles, result, row_count, duplicate_row_count, output_path):
    """Generate a self-contained HTML report from profiling and scoring data."""
    path = pathlib.Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    numeric_profiles = [p for p in profiles if "min" in p]

    env = jinja2.Environment(autoescape=True)
    template = env.from_string(_TEMPLATE)
    html = template.render(
        profiles=profiles,
        result=result,
        row_count=row_count,
        duplicate_row_count=duplicate_row_count,
        column_count=len(profiles),
        numeric_profiles=numeric_profiles,
    )
    path.write_text(html)
