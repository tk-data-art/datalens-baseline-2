"""Column profiler module — computes per-column statistics from CSV data."""

import statistics


def _try_numeric(value: str) -> tuple[bool, bool, float]:
    """Return (is_numeric, is_int, numeric_value)."""
    try:
        return True, True, float(int(value))
    except (ValueError, TypeError):
        pass
    try:
        return True, False, float(value)
    except (ValueError, TypeError):
        pass
    return False, False, 0.0


def _infer_type(values: list[str]) -> str:
    int_count = 0
    float_count = 0
    string_count = 0
    for v in values:
        if not v:
            continue
        is_num, is_int, _ = _try_numeric(v)
        if is_num:
            if is_int:
                int_count += 1
            else:
                float_count += 1
        else:
            string_count += 1
    if int_count > 0 and float_count == 0 and string_count == 0:
        return "integer"
    if (int_count > 0 or float_count > 0) and string_count == 0:
        return "float"
    if int_count > 0 and float_count > 0 and string_count == 0:
        return "float"
    if int_count > 0 or float_count > 0:
        return "mixed"
    return "string"


def _numeric_stats(values: list[float]) -> dict[str, float]:
    nums = sorted(values)
    n = len(nums)
    result = {
        "min": nums[0],
        "max": nums[-1],
        "mean": sum(nums) / n,
        "median": nums[n // 2] if n % 2 == 1 else (nums[n // 2 - 1] + nums[n // 2]) / 2,
    }
    if n >= 2:
        result["std"] = statistics.stdev(nums)
    else:
        result["std"] = 0.0
    return result


def profile(rows: list[dict], column_names: list[str]) -> list[dict]:
    """Profile each column and return per-column statistics."""
    total_rows = len(rows)
    profiles = []
    for name in column_names:
        values = [row.get(name, "") for row in rows]
        missing = [v for v in values if v == ""]
        non_missing = [v for v in values if v != ""]
        missing_count = len(missing)
        missing_pct = (missing_count / total_rows * 100) if total_rows > 0 else 0.0
        unique_values = set(non_missing)
        unique_count = len(unique_values)
        col_type = _infer_type(non_missing)
        profile: dict = {
            "name": name,
            "type": col_type,
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_count,
        }
        if col_type in ("integer", "float"):
            numeric_values = []
            for v in non_missing:
                try:
                    numeric_values.append(float(v))
                except (ValueError, TypeError):
                    pass
            if numeric_values:
                profile.update(_numeric_stats(numeric_values))
        profiles.append(profile)
    return profiles
