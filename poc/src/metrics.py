"""Metrics for binary model validation."""
from __future__ import annotations

from typing import Callable

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


def _arrays(y_true: np.ndarray, scores: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y = np.asarray(y_true, dtype=int)
    s = np.asarray(scores, dtype=float)
    if y.ndim != 1 or s.ndim != 1 or len(y) != len(s):
        raise ValueError("labels and scores must be aligned one-dimensional arrays")
    if len(y) == 0 or not np.isin(y, [0, 1]).all() or not np.isfinite(s).all():
        raise ValueError("inputs must contain finite scores and binary labels")
    return y, np.clip(s, 1e-6, 1 - 1e-6)


def threshold_metrics(y_true: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, float]:
    """Compute threshold-based binary classification metrics."""
    y, s = _arrays(y_true, scores)
    pred = s >= threshold
    tp = int(np.sum((y == 1) & pred))
    tn = int(np.sum((y == 0) & ~pred))
    fp = int(np.sum((y == 0) & pred))
    fn = int(np.sum((y == 1) & ~pred))
    div = lambda numerator, denominator: float(numerator / denominator) if denominator else float("nan")
    return {
        "sensitivity": div(tp, tp + fn), "specificity": div(tn, tn + fp),
        "ppv": div(tp, tp + fp), "npv": div(tn, tn + fn),
        "true_positives": float(tp), "false_positives": float(fp),
        "true_negatives": float(tn), "false_negatives": float(fn),
    }


def calibration_parameters(y_true: np.ndarray, scores: np.ndarray) -> dict[str, float]:
    """Fit logistic calibration intercept and slope from predicted scores."""
    y, s = _arrays(y_true, scores)
    if len(np.unique(y)) < 2:
        return {"calibration_intercept": float("nan"), "calibration_slope": float("nan")}
    logits = np.log(s / (1 - s)).reshape(-1, 1)
    model = LogisticRegression(C=1e6, max_iter=1000).fit(logits, y)
    return {"calibration_intercept": float(model.intercept_[0]),
            "calibration_slope": float(model.coef_[0][0])}


def expected_calibration_error(y_true: np.ndarray, scores: np.ndarray, bins: int = 10) -> float:
    """Compute equal-width expected calibration error."""
    y, s = _arrays(y_true, scores)
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (s >= low) & ((s < high) if high < 1 else (s <= high))
        if mask.any():
            ece += mask.mean() * abs(y[mask].mean() - s[mask].mean())
    return float(ece)


def compute_metrics(y_true: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, float]:
    """Compute all primary discrimination, calibration, and threshold metrics."""
    y, s = _arrays(y_true, scores)
    result = threshold_metrics(y, s, threshold)
    result.update({
        "n": float(len(y)),
        "prevalence": float(y.mean()),
        "auroc": float(roc_auc_score(y, s)) if len(np.unique(y)) == 2 else float("nan"),
        "pr_auc": float(average_precision_score(y, s)) if len(np.unique(y)) == 2 else float("nan"),
        "brier_score": float(brier_score_loss(y, s)),
        "expected_calibration_error": expected_calibration_error(y, s),
    })
    result.update(calibration_parameters(y, s))
    return result


def bootstrap_confidence_intervals(
    y_true: np.ndarray, scores: np.ndarray, threshold: float, iterations: int = 200,
    seed: int = 101,
) -> dict[str, dict[str, float]]:
    """Return percentile 95 percent bootstrap intervals for selected metrics."""
    y, s = _arrays(y_true, scores)
    rng = np.random.default_rng(seed)
    names = ["auroc", "pr_auc", "sensitivity", "specificity", "ppv", "npv", "brier_score"]
    values: dict[str, list[float]] = {name: [] for name in names}
    for _ in range(iterations):
        index = rng.integers(0, len(y), len(y))
        sample = compute_metrics(y[index], s[index], threshold)
        for name in names:
            if np.isfinite(sample[name]):
                values[name].append(sample[name])
    return {
        name: {"lower": float(np.quantile(series, 0.025)), "upper": float(np.quantile(series, 0.975))}
        if series else {"lower": float("nan"), "upper": float("nan")}
        for name, series in values.items()
    }
