"""Checks for binary model metric calculations."""
import numpy as np

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from metrics import bootstrap_confidence_intervals, compute_metrics, expected_calibration_error, threshold_metrics


def test_perfect_threshold_metrics() -> None:
    labels = np.array([0, 0, 1, 1])
    scores = np.array([0.1, 0.2, 0.8, 0.9])
    result = threshold_metrics(labels, scores, 0.5)
    assert result["sensitivity"] == 1.0
    assert result["specificity"] == 1.0
    assert result["ppv"] == 1.0
    assert result["npv"] == 1.0


def test_discrimination_and_calibration_are_bounded() -> None:
    labels = np.array([0, 0, 0, 1, 1, 1])
    scores = np.array([0.05, 0.20, 0.40, 0.60, 0.80, 0.95])
    result = compute_metrics(labels, scores, 0.5)
    assert result["auroc"] == 1.0
    assert result["pr_auc"] == 1.0
    assert 0.0 <= result["brier_score"] <= 1.0
    assert 0.0 <= expected_calibration_error(labels, scores) <= 1.0


def test_bootstrap_intervals_have_ordered_bounds() -> None:
    labels = np.array([0, 0, 0, 1, 1, 1, 0, 1])
    scores = np.array([0.1, 0.2, 0.3, 0.6, 0.7, 0.8, 0.4, 0.9])
    intervals = bootstrap_confidence_intervals(labels, scores, 0.5, iterations=30, seed=2)
    assert intervals["auroc"]["lower"] <= intervals["auroc"]["upper"]
