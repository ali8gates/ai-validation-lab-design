"""Render a concise markdown validation report."""
from __future__ import annotations

from typing import Any


def _number(value: Any, digits: int = 3) -> str:
    """Format numbers for display, preserving unavailable values."""
    try:
        return "NA" if value != value else f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def _table(headers: list[str], rows: list[list[str]]) -> str:
    """Build a markdown table."""
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(row) + " |" for row in rows])


def render_report(config: dict[str, Any], results: dict[str, Any]) -> str:
    """Render results into a reviewer-ready markdown template."""
    cohort = config["cohort"]
    metrics = results["metrics"]
    ci = results["confidence_intervals"]
    primary_rows = []
    for name in config["primary_metrics"]:
        interval = ci.get(name)
        ci_text = f"{_number(interval['lower'])} to {_number(interval['upper'])}" if interval else "Not bootstrapped"
        primary_rows.append([name, _number(metrics.get(name)), ci_text])
    subgroup_rows = [[
        row["field"], row["group"], str(row["n"]), _number(row["sensitivity"]),
        _number(row["auroc"]), _number(row["sensitivity_gap_vs_overall"]), row["flag"],
    ] for row in results["subgroups"]]
    drift = results["drift"]
    impact = results["impact"]
    return f"""# Validation Report: {config['study_id']}

> **SYNTHETIC DATA TEMPLATE ONLY.** All results in this report come from locally generated fake data. They are not clinical evidence and must not support patient care or deployment decisions.

## Study

- **Model:** {config['model_name']}
- **Intended use:** {config['intended_use']}
- **Monitoring cadence:** {config['monitoring_cadence']}
- **Cohort:** {cohort['source']}; n={results['n']}.
- **Inclusion:** {'; '.join(cohort['inclusion'])}
- **Exclusion:** {'; '.join(cohort['exclusion'])}

## Primary metrics

{_table(['Metric', 'Value', '95% bootstrap interval'], primary_rows)}

Decision threshold: {_number(results['threshold'])}. Prevalence: {_number(metrics['prevalence'])}.

## Subgroup checks

{_table(['Field', 'Group', 'n', 'Sensitivity', 'AUROC', 'Sensitivity gap', 'Flag'], subgroup_rows)}

A `small_n` flag means the group did not meet the configured minimum size. A `below_sensitivity_floor` flag means sensitivity was below the configured floor.

## Calibration

- Calibration intercept: {_number(metrics['calibration_intercept'])}
- Calibration slope: {_number(metrics['calibration_slope'])}
- Brier score: {_number(metrics['brier_score'])}
- Expected calibration error: {_number(metrics['expected_calibration_error'])}

## Drift status

- Status: **{drift['status'].upper()}**
- PSI: {_number(drift['psi'])}
- KS statistic: {_number(drift['ks_statistic'])}; p-value: {_number(drift['ks_pvalue'])}
- Baseline to current calibration slope change: {_number(drift['calibration_slope_decay'])}
- Alert reasons: {', '.join(drift['alert_reasons']) if drift['alert_reasons'] else 'none'}

## Illustrative decision impact

{impact['label']}

{_table(['Measure', 'Per 1000'], [[key.replace('_', ' '), _number(value)] for key, value in impact.items() if key != 'label'])}

## Limitations

- This run uses fake data only and does not assess clinical validity, safety, workflow fit, or equity in practice.
- Synthetic labels and scores cannot establish generalization, benefit, or harm.
- Reviewers should define governance, data quality checks, protocol details, and acceptance criteria before any real-world study.

## Reviewer sign-off

| Role | Name | Date | Decision | Notes |
| --- | --- | --- | --- | --- |
| Clinical reviewer |  |  |  |  |
| Statistical reviewer |  |  |  |  |
| Responsible owner |  |  |  |  |
"""
