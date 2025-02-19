"""Checks for workflow monitoring helpers."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from monitoring import monitor_workflow


def _row(subgroup: str, complete: bool, unsafe: bool, confidence: float) -> dict[str, object]:
    return {
        "subgroup": subgroup,
        "input_group": subgroup,
        "task_completed": complete,
        "unsafe_action": unsafe,
        "confidence": confidence,
    }


def test_monitoring_flags_unsafe_rate_rise() -> None:
    baseline = [_row("a", True, False, 0.95), _row("b", True, False, 0.95)]
    current = [_row("a", True, False, 0.95), _row("b", False, True, 0.95)]
    checks = monitor_workflow(
        baseline, current,
        {"unsafe_action_rate_rise": 0.10, "calibration_decay": 1.0,
         "subgroup_gap_widening": 2.0, "input_distribution_shift": 1.0,
         "volume_change_fraction": 1.0},
    )
    assert checks[0]["check"] == "unsafe_action_rate_rise"
    assert checks[0]["severity"] == "critical"


def test_monitoring_returns_plain_dicts() -> None:
    baseline = [_row("a", True, False, 0.90), _row("a", True, False, 0.90)]
    current = [_row("a", False, True, 0.90), _row("a", False, True, 0.90)]
    checks = monitor_workflow(baseline, current)
    assert checks
    assert all(isinstance(check, dict) for check in checks)
