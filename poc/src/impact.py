"""Illustrative decision impact calculations using config placeholders."""
from __future__ import annotations

from typing import Any

import numpy as np

from metrics import threshold_metrics


def estimate_impact(y_true: np.ndarray, scores: np.ndarray, threshold: float, config: dict[str, Any]) -> dict[str, float | str]:
    """Estimate illustrative per-1000 alert and event effects from config inputs."""
    base = threshold_metrics(y_true, scores, threshold)
    scale = 1000 / len(y_true)
    tp = base["true_positives"] * scale
    fp = base["false_positives"] * scale
    alerts = (base["true_positives"] + base["false_positives"]) * scale
    avoided = tp * float(config["avoided_event_fraction_per_true_positive"])
    event_value = avoided * float(config["event_cost_units"])
    alert_cost = alerts * float(config["alert_management_cost_units"])
    return {
        "label": "Illustrative only. These are synthetic decision estimates, not observed outcomes.",
        "alerts_per_1000": alerts, "true_positives_per_1000": tp,
        "false_positives_per_1000": fp, "avoided_events_per_1000": avoided,
        "event_value_units_per_1000": event_value, "alert_management_units_per_1000": alert_cost,
        "net_value_units_per_1000": event_value - alert_cost,
    }
