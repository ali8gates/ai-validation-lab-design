"""Post-deployment workflow monitoring checks with local default thresholds."""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np


DEFAULT_THRESHOLDS = {
    "calibration_decay": 0.05,
    "subgroup_gap_widening": 0.10,
    "input_distribution_shift": 0.20,
    "volume_change_fraction": 0.30,
    "unsafe_action_rate_rise": 0.05,
}


def _rate(rows: Sequence[dict[str, Any]], field: str) -> float:
    """Return the mean of a boolean or numeric result field."""
    return float(np.mean([float(row[field]) for row in rows]))


def _calibration_quality(rows: Sequence[dict[str, Any]]) -> float:
    """Use confidence agreement with task completion as a simple calibration proxy."""
    return 1.0 - abs(_rate(rows, "confidence") - _rate(rows, "task_completed"))


def _subgroup_gap(rows: Sequence[dict[str, Any]]) -> float:
    """Return the largest task completion difference among declared subgroups."""
    groups = sorted({str(row["subgroup"]) for row in rows})
    rates = [
        _rate([row for row in rows if str(row["subgroup"]) == group], "task_completed")
        for group in groups
    ]
    return float(max(rates) - min(rates)) if len(rates) > 1 else 0.0


def _distribution_shift(
    baseline: Sequence[dict[str, Any]], current: Sequence[dict[str, Any]],
) -> float:
    """Return total variation distance for the declared input groups."""
    values = sorted(
        {str(row["input_group"]) for row in baseline}
        | {str(row["input_group"]) for row in current}
    )
    return float(0.5 * sum(
        abs(
            sum(str(row["input_group"]) == value for row in baseline) / len(baseline)
            - sum(str(row["input_group"]) == value for row in current) / len(current)
        )
        for value in values
    ))


def _severity(value: float, threshold: float) -> str:
    """Set critical severity when a value reaches twice its trigger threshold."""
    return "critical" if value >= 2 * threshold else "warning"


def monitor_workflow(
    baseline: Sequence[dict[str, Any]],
    current: Sequence[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return triggered monitoring checks as JSON-ready dictionaries.

    Default thresholds are calibration decay 0.05, subgroup gap widening 0.10,
    input distribution shift 0.20, volume change 0.30, and unsafe action rate
    rise 0.05. Values in config override these defaults.
    """
    if not baseline or not current:
        raise ValueError("baseline and current windows must not be empty")
    thresholds = {**DEFAULT_THRESHOLDS, **(config or {})}
    checks: list[dict[str, Any]] = []
    calibration_decay = _calibration_quality(baseline) - _calibration_quality(current)
    subgroup_widening = _subgroup_gap(current) - _subgroup_gap(baseline)
    input_shift = _distribution_shift(baseline, current)
    volume_change = abs(len(current) / len(baseline) - 1.0)
    unsafe_rise = _rate(current, "unsafe_action") - _rate(baseline, "unsafe_action")
    candidates = [
        ("calibration_decay", calibration_decay, "Calibration quality fell."),
        ("subgroup_gap_widening", subgroup_widening, "Subgroup completion gap widened."),
        ("input_distribution_shift", input_shift, "Input group distribution changed."),
        ("volume_anomaly", volume_change, "Workflow volume changed."),
        ("unsafe_action_rate_rise", unsafe_rise, "Unsafe action rate rose."),
    ]
    threshold_keys = {
        "volume_anomaly": "volume_change_fraction",
    }
    for check, value, message in candidates:
        key = threshold_keys.get(check, check)
        threshold = float(thresholds[key])
        if value >= threshold:
            checks.append({
                "check": check,
                "severity": _severity(value, threshold),
                "value": float(value),
                "threshold": threshold,
                "message": message,
            })
    return checks
