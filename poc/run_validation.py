"""Run the local synthetic validation template."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from drift import assess_drift
from impact import estimate_impact
from metrics import bootstrap_confidence_intervals, compute_metrics
from report import render_report
from subgroups import run_subgroups
from synth_data import cohort_from_config, generate_synthetic_cohort


def validate_config(config: dict[str, Any]) -> None:
    """Check that the compact study config has the needed fields."""
    required = {
        "study_id", "model_name", "intended_use", "cohort", "primary_metrics",
        "subgroup_fields", "thresholds", "monitoring_cadence", "impact", "drift",
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"config is missing fields: {sorted(missing)}")
    cohort_required = {"source", "n_patients", "seed", "inclusion", "exclusion"}
    threshold_required = {
        "decision", "subgroup_sensitivity_floor", "minimum_subgroup_n",
        "psi_alert", "ks_pvalue_alert", "calibration_slope_min",
        "calibration_slope_max",
    }
    impact_required = {
        "avoided_event_fraction_per_true_positive", "event_cost_units",
        "alert_management_cost_units",
    }
    for section, fields in {
        "cohort": cohort_required, "thresholds": threshold_required, "impact": impact_required,
    }.items():
        absent = fields - set(config[section])
        if absent:
            raise ValueError(f"{section} is missing fields: {sorted(absent)}")
    if int(config["cohort"]["n_patients"]) < 20:
        raise ValueError("cohort.n_patients must be at least 20")
    if not 0 < float(config["thresholds"]["decision"]) < 1:
        raise ValueError("thresholds.decision must be between zero and one")
    if int(config["thresholds"]["minimum_subgroup_n"]) < 1:
        raise ValueError("thresholds.minimum_subgroup_n must be positive")


def _json_ready(value: Any) -> Any:
    """Convert NumPy-like values and non-finite floats for JSON output."""
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if hasattr(value, "item"):
        return _json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def load_data_or_generate(config: dict[str, Any], data_path: str | None) -> pd.DataFrame:
    """Read a CSV when provided or create the configured fake cohort."""
    if data_path:
        data = pd.read_csv(data_path)
        required = {"label", "model_score", *config["subgroup_fields"]}
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"input data is missing columns: {sorted(missing)}")
        return data
    return cohort_from_config(config)


def run(config: dict[str, Any], data_path: str | None = None) -> dict[str, Any]:
    """Calculate all template results from local cohort data."""
    validate_config(config)
    data = load_data_or_generate(config, data_path)
    threshold = float(config["thresholds"]["decision"])
    labels, scores = data["label"].to_numpy(), data["model_score"].to_numpy()
    baseline = generate_synthetic_cohort(int(config["cohort"]["n_patients"]), int(config["drift"]["baseline_seed"]))
    return {
        "study_id": config["study_id"], "data_type": "synthetic" if not data_path else "user_supplied",
        "n": int(len(data)), "threshold": threshold,
        "metrics": compute_metrics(labels, scores, threshold),
        "confidence_intervals": bootstrap_confidence_intervals(labels, scores, threshold, int(config.get("bootstrap_iterations", 200))),
        "subgroups": run_subgroups(data, config["subgroup_fields"], threshold,
                                    float(config["thresholds"]["subgroup_sensitivity_floor"]),
                                    int(config["thresholds"]["minimum_subgroup_n"])),
        "drift": assess_drift(baseline["label"].to_numpy(), baseline["model_score"].to_numpy(), labels, scores, config["thresholds"]),
        "impact": estimate_impact(labels, scores, threshold, config["impact"]),
    }


def main() -> None:
    """Parse inputs and write JSON plus markdown report."""
    parser = argparse.ArgumentParser(description="Run a local model validation template")
    parser.add_argument(
        "--config", default=str(ROOT / "config" / "example_study.yaml"),
        help="Path to study YAML",
    )
    parser.add_argument("--data", help="Optional CSV with label, model_score, and subgroup columns")
    parser.add_argument("--output", default=str(ROOT / "output"), help="Directory for generated files")
    args = parser.parse_args()
    with open(args.config, encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    results = run(config, args.data)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps(_json_ready(results), indent=2), encoding="utf-8")
    (output / "validation_report.md").write_text(render_report(config, _json_ready(results)), encoding="utf-8")
    print(f"Wrote {output / 'validation_report.md'}")
    print(f"Wrote {output / 'results.json'}")


if __name__ == "__main__":
    main()
