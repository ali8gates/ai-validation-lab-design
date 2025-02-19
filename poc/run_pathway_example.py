"""Run the local synthetic pathway workflow example."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from agentic import AgentResponse, DeterministicMockAgent, Scenario, load_scenario_library
from agentic import run_workflows, subgroup_workflow_measures, workflow_measures
from monitoring import monitor_workflow
from pathway import apply_cohort_rules, load_pathway
from synth_data import generate_synthetic_registry


def _json_ready(value: Any) -> Any:
    """Convert NumPy values and non-finite floats for JSON output."""
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if hasattr(value, "item"):
        return _json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _baseline_rule(scenario: Scenario) -> AgentResponse:
    """Return the defined action sequence as a transparent rule baseline."""
    return AgentResponse(scenario.expected_action, 0.98)


def _number(value: float) -> str:
    """Format one rate or elapsed step cost for a narrow table."""
    return f"{value:.3f}"


def _table(headers: list[str], rows: list[list[str]]) -> str:
    """Build a compact markdown table."""
    return "\n".join(
        ["| " + " | ".join(headers) + " |",
         "| " + " | ".join(["---"] * len(headers)) + " |"]
        + ["| " + " | ".join(row) + " |" for row in rows]
    )


def render_pathway_report(results: dict[str, Any]) -> str:
    """Render a plain-language report for a clinical committee."""
    cohort = results["cohort"]
    baseline = results["baseline_measures"]
    mock = results["mock_agent_measures"]
    measure_rows = [
        [name.replace("_", " "), _number(baseline[name]), _number(mock[name])]
        for name in [
            "task_completion_rate",
            "step_level_agreement",
            "pathway_adherence_rate",
            "mean_time_to_decision",
            "unsafe_action_rate",
            "escalation_to_human_rate",
        ]
    ]
    cohort_rows = [
        ["registry rows", str(cohort["registry_rows"])],
        ["eligible rows", str(cohort["eligible_rows"])],
        *[[rule, str(count)] for rule, count in cohort["excluded_by_rule"].items()],
    ]
    subgroup_rows = [
        [
            str(row["subgroup"]),
            str(int(row["n"])),
            _number(float(row["task_completion_rate"])),
            _number(float(row["pathway_adherence_rate"])),
            _number(float(row["unsafe_action_rate"])),
        ]
        for row in results["mock_agent_subgroups"]
    ]
    trigger_rows = [
        [row["check"], row["severity"], _number(row["value"]), _number(row["threshold"])]
        for row in results["monitoring_triggers"]
    ]
    if not trigger_rows:
        trigger_rows = [["none", "none", "0.000", "0.000"]]
    return f"""# Synthetic Pathway Workflow Report

## Plain language summary

This local example tests a heart failure follow-up workflow after discharge. It uses synthetic registry rows and fixed action scenarios. The rule baseline follows every expected action. The mock agent misses the required human escalation for one hazard scenario. Monitoring flags that unsafe response, a subgroup completion gap, and a decline in the simple confidence check. This report is a code example. It is not clinical evidence.

Pathway: {results["pathway_id"]}. Outcome window: {results["outcome_window"]}.

## Cohort

{_table(["Measure", "Count"], cohort_rows)}

## Workflow measures

{_table(["Measure", "Rule", "Mock"], measure_rows)}

Time to decision is measured in configured step-cost units. Higher completion and agreement values are better. Lower unsafe action values are better.

## Subgroup results

{_table(["Group", "n", "Complete", "Adherent", "Unsafe"], subgroup_rows)}

## Monitoring triggers

{_table(["Check", "Severity", "Value", "Limit"], trigger_rows)}

## Limitations

- The registry rows and scenarios are synthetic. They do not represent real records or real care.
- The expected actions are authored examples. They do not establish clinical correctness.
- The confidence check is a simple proxy. It does not replace formal calibration analysis.
- The mock agent is deterministic. A real workflow needs prospective review and human oversight.
"""


def run() -> dict[str, Any]:
    """Generate local inputs, evaluate workflows, and return JSON-ready results."""
    pathway = load_pathway(ROOT / "config" / "example_pathway.yaml")
    scenarios = load_scenario_library(ROOT / "config" / "example_scenarios.yaml")
    registry = generate_synthetic_registry(80, seed=31, visits_per_record=3)
    eligible_indexes, excluded_by_rule = apply_cohort_rules(pathway, registry)
    baseline_results = run_workflows(scenarios, _baseline_rule)
    mock_results = run_workflows(scenarios, DeterministicMockAgent())
    monitoring = monitor_workflow(baseline_results, mock_results)
    return {
        "pathway_id": pathway.pathway_id,
        "guideline_reference": pathway.guideline_reference,
        "outcome_window": pathway.outcome_window,
        "cohort": {
            "registry_rows": int(len(registry)),
            "eligible_rows": int(len(eligible_indexes)),
            "excluded_by_rule": excluded_by_rule,
        },
        "baseline_measures": workflow_measures(baseline_results),
        "mock_agent_measures": workflow_measures(mock_results),
        "mock_agent_subgroups": subgroup_workflow_measures(mock_results),
        "monitoring_triggers": monitoring,
        "baseline_results": baseline_results,
        "mock_agent_results": mock_results,
    }


def main() -> None:
    """Write the pathway example JSON and markdown report."""
    results = _json_ready(run())
    output = ROOT / "output"
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / "pathway_report.md"
    results_path = output / "pathway_results.json"
    report_path.write_text(render_pathway_report(results), encoding="utf-8")
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {report_path}")
    print(f"Wrote {results_path}")


if __name__ == "__main__":
    main()
