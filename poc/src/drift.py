"""Simple monitoring checks for score distribution and calibration drift."""
from __future__ import annotations

from typing import Any

import numpy as np

from metrics import calibration_parameters


def two_sample_ks_test(baseline: np.ndarray, current: np.ndarray) -> tuple[float, float]:
    """Return the two-sample KS statistic and an asymptotic p-value."""
    base = np.sort(np.asarray(baseline, dtype=float))
    cur = np.sort(np.asarray(current, dtype=float))
    if len(base) == 0 or len(cur) == 0:
        raise ValueError("score distributions must not be empty")
    points = np.sort(np.concatenate([base, cur]))
    base_cdf = np.searchsorted(base, points, side="right") / len(base)
    cur_cdf = np.searchsorted(cur, points, side="right") / len(cur)
    statistic = float(np.max(np.abs(base_cdf - cur_cdf)))
    effective_n = len(base) * len(cur) / (len(base) + len(cur))
    adjusted = (np.sqrt(effective_n) + 0.12 + 0.11 / np.sqrt(effective_n)) * statistic
    p_value = 2 * sum(
        (-1) ** (index - 1) * np.exp(-2 * index**2 * adjusted**2)
        for index in range(1, 101)
    )
    return statistic, float(np.clip(p_value, 0, 1))


def population_stability_index(baseline: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Compute PSI using bins defined by baseline score quantiles."""
    base = np.asarray(baseline, dtype=float)
    cur = np.asarray(current, dtype=float)
    edges = np.unique(np.quantile(base, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return float("nan")
    edges[0], edges[-1] = -np.inf, np.inf
    base_counts = np.histogram(base, bins=edges)[0]
    cur_counts = np.histogram(cur, bins=edges)[0]
    base_share = np.clip(base_counts / len(base), 1e-6, None)
    cur_share = np.clip(cur_counts / len(cur), 1e-6, None)
    return float(np.sum((cur_share - base_share) * np.log(cur_share / base_share)))


def assess_drift(
    baseline_labels: np.ndarray, baseline_scores: np.ndarray, current_labels: np.ndarray,
    current_scores: np.ndarray, thresholds: dict[str, Any],
) -> dict[str, Any]:
    """Compare synthetic baseline and current data and apply alert rules."""
    psi = population_stability_index(baseline_scores, current_scores)
    ks_statistic, ks_pvalue = two_sample_ks_test(baseline_scores, current_scores)
    base_cal = calibration_parameters(baseline_labels, baseline_scores)
    current_cal = calibration_parameters(current_labels, current_scores)
    decay = current_cal["calibration_slope"] - base_cal["calibration_slope"]
    reasons: list[str] = []
    if np.isfinite(psi) and psi >= float(thresholds["psi_alert"]):
        reasons.append("psi")
    if ks_pvalue < float(thresholds["ks_pvalue_alert"]):
        reasons.append("ks_score_distribution")
    slope = current_cal["calibration_slope"]
    if np.isfinite(slope) and not (float(thresholds["calibration_slope_min"]) <= slope <= float(thresholds["calibration_slope_max"])):
        reasons.append("calibration_slope")
    return {
        "psi": psi, "ks_statistic": ks_statistic, "ks_pvalue": ks_pvalue,
        "baseline_calibration_slope": base_cal["calibration_slope"],
        "current_calibration_slope": slope, "calibration_slope_decay": decay,
        "status": "alert" if reasons else "pass", "alert_reasons": reasons,
    }
