"""Subgroup validation summaries."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from metrics import compute_metrics


def run_subgroups(
    data: pd.DataFrame, fields: list[str], threshold: float, sensitivity_floor: float,
    minimum_n: int,
) -> list[dict[str, Any]]:
    """Compute subgroup metrics, gaps from overall values, and simple flags."""
    overall = compute_metrics(data["label"].to_numpy(), data["model_score"].to_numpy(), threshold)
    rows: list[dict[str, Any]] = []
    for field in fields:
        if field not in data.columns:
            raise ValueError(f"missing subgroup field: {field}")
        for value, group in data.groupby(field, dropna=False):
            metrics = compute_metrics(group["label"].to_numpy(), group["model_score"].to_numpy(), threshold)
            small_n = len(group) < minimum_n
            below_floor = np.isfinite(metrics["sensitivity"]) and metrics["sensitivity"] < sensitivity_floor
            rows.append({
                "field": field, "group": str(value), "n": int(len(group)),
                "sensitivity": metrics["sensitivity"], "specificity": metrics["specificity"],
                "auroc": metrics["auroc"], "ppv": metrics["ppv"],
                "sensitivity_gap_vs_overall": metrics["sensitivity"] - overall["sensitivity"],
                "auroc_gap_vs_overall": metrics["auroc"] - overall["auroc"],
                "small_n": bool(small_n), "below_sensitivity_floor": bool(below_floor),
                "flag": "small_n" if small_n else ("below_sensitivity_floor" if below_floor else "none"),
            })
    return rows
