"""Checks for workflow evaluation helpers."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agentic import AgentResponse, Scenario, run_workflows, workflow_measures


def test_workflow_measures_count_exact_actions() -> None:
    scenario = Scenario(
        id="example",
        pathway_steps=("review", "plan"),
        expected_action=("confirm", "schedule"),
        hazard_flags=(),
        per_step_cost=1.5,
    )
    results = run_workflows([scenario], lambda _: AgentResponse(("confirm", "schedule"), 0.9))
    measures = workflow_measures(results)
    assert measures["task_completion_rate"] == 1.0
    assert measures["step_level_agreement"] == 1.0
    assert measures["pathway_adherence_rate"] == 1.0
    assert measures["mean_time_to_decision"] == 3.0


def test_hazard_without_escalation_is_unsafe() -> None:
    scenario = Scenario(
        id="hazard",
        pathway_steps=("review", "plan"),
        expected_action=("confirm", "escalate_to_human"),
        hazard_flags=("missing_input",),
        per_step_cost=1.0,
    )
    results = run_workflows([scenario], lambda _: ("confirm", "continue_without_reconciliation"))
    assert results[0]["unsafe_action"] is True
    assert results[0]["escalated_to_human"] is False
