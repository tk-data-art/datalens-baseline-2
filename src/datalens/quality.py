"""Quality score module — aggregates profiler output into a composite 0–100 score."""

import statistics


def compute_score(profiles: list[dict], total_rows: int) -> dict:
    """Compute a composite quality score from profiler output."""
    if total_rows == 0:
        return {"composite_score": 0.0, "column_scores": []}

    column_scores = []
    for p in profiles:
        completeness = 1.0 - (p["missing_pct"] / 100.0)
        if p["type"] == "mixed":
            type_consistency = 0.5
        else:
            type_consistency = 1.0
        distinctness = min(p["unique_count"] / total_rows, 1.0)
        column_score = 0.50 * completeness + 0.30 * type_consistency + 0.20 * distinctness
        column_scores.append({"name": p["name"], "score": column_score})

    composite_score = statistics.mean([c["score"] for c in column_scores]) * 100
    return {"composite_score": composite_score, "column_scores": column_scores}
