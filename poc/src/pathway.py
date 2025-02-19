"""Load pathway definitions and apply their cohort rules to record arrays."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class ClinicalPathway:
    """Represent the parts of a pathway used by this local example."""

    pathway_id: str
    guideline_reference: str
    inclusion_rules: tuple[dict[str, Any], ...]
    exclusion_rules: tuple[dict[str, Any], ...]
    decision_points: tuple[dict[str, Any], ...]
    outcome_window: str


def _load_json_yaml(path: str | Path) -> dict[str, Any]:
    """Read JSON-compatible YAML without a YAML package dependency."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            "pathway YAML must use JSON-compatible YAML so this example needs only NumPy"
        ) from error


def load_pathway(path: str | Path) -> ClinicalPathway:
    """Load and validate one pathway definition from a YAML file."""
    data = _load_json_yaml(path)
    required = {
        "pathway_id",
        "guideline_reference",
        "cohort",
        "decision_points",
        "outcome_window",
    }
    missing = required - set(data)
    if missing:
        raise ValueError(f"pathway is missing fields: {sorted(missing)}")
    cohort = data["cohort"]
    if not isinstance(cohort, dict):
        raise ValueError("pathway cohort must be a mapping")
    inclusion = tuple(cohort.get("inclusion_rules", []))
    exclusion = tuple(cohort.get("exclusion_rules", []))
    if not inclusion:
        raise ValueError("pathway must include at least one inclusion rule")
    for rule in (*inclusion, *exclusion):
        if not {"id", "field", "operator"} <= set(rule):
            raise ValueError("each cohort rule needs id, field, and operator")
    return ClinicalPathway(
        pathway_id=str(data["pathway_id"]),
        guideline_reference=str(data["guideline_reference"]),
        inclusion_rules=inclusion,
        exclusion_rules=exclusion,
        decision_points=tuple(data["decision_points"]),
        outcome_window=str(data["outcome_window"]),
    )


def _rule_mask(records: np.ndarray, rule: dict[str, Any]) -> np.ndarray:
    """Return the records that meet one simple structured-array rule."""
    if records.dtype.names is None:
        raise ValueError("records must be a named NumPy structured array")
    field = str(rule["field"])
    if field not in records.dtype.names:
        raise ValueError(f"record array is missing rule field: {field}")
    values = records[field]
    operator = str(rule["operator"])
    target = rule.get("value")
    if operator == "eq":
        return values == target
    if operator == "not_eq":
        return values != target
    if operator == "gte":
        return values >= target
    if operator == "gt":
        return values > target
    if operator == "lte":
        return values <= target
    if operator == "lt":
        return values < target
    if operator == "in":
        return np.isin(values, target)
    if operator == "not_in":
        return ~np.isin(values, target)
    if operator == "is_true":
        return values.astype(bool)
    if operator == "is_false":
        return ~values.astype(bool)
    raise ValueError(f"unsupported cohort rule operator: {operator}")


def apply_cohort_rules(
    pathway: ClinicalPathway, records: np.ndarray,
) -> tuple[np.ndarray, dict[str, int]]:
    """Return eligible indexes and an independent exclusion count for each rule."""
    eligible = np.ones(len(records), dtype=bool)
    excluded_counts: dict[str, int] = {}
    for rule in pathway.inclusion_rules:
        matches = _rule_mask(records, rule)
        excluded_counts[str(rule["id"])] = int((~matches).sum())
        eligible &= matches
    for rule in pathway.exclusion_rules:
        matches = _rule_mask(records, rule)
        excluded_counts[str(rule["id"])] = int(matches.sum())
        eligible &= ~matches
    return np.flatnonzero(eligible), excluded_counts
