"""Create clearly fake cardiovascular validation data."""
from __future__ import annotations

from typing import Any

import numpy as np


def generate_synthetic_cohort(n_patients: int, seed: int) -> Any:
    """Return a clearly synthetic cardiovascular cohort with fake records."""
    if n_patients < 20:
        raise ValueError("n_patients must be at least 20")
    rng = np.random.default_rng(seed)
    age = rng.integers(40, 85, n_patients)
    sex = rng.choice(["female", "male"], n_patients, p=[0.51, 0.49])
    race = rng.choice(["group_a", "group_b", "group_c", "group_d"], n_patients,
                      p=[0.42, 0.25, 0.20, 0.13])
    site = rng.choice(["site_1", "site_2", "site_3"], n_patients, p=[0.45, 0.35, 0.20])
    rural = rng.choice(["urban", "rural"], n_patients, p=[0.72, 0.28])
    payer = rng.choice(["coverage_a", "coverage_b", "coverage_c"], n_patients,
                       p=[0.48, 0.32, 0.20])
    age_risk = (age - 40) / 44
    latent = (
        -2.2 + 2.0 * age_risk + 0.20 * (sex == "male") + 0.20 * (rural == "rural")
        + 0.15 * (site == "site_3") + rng.normal(0, 0.65, n_patients)
    )
    probability = 1 / (1 + np.exp(-latent))
    label = rng.binomial(1, probability)
    score_logit = latent + 0.20 * (race == "group_d") + rng.normal(0, 0.75, n_patients)
    score = np.clip(1 / (1 + np.exp(-score_logit)), 0.001, 0.999)
    import pandas as pd

    return pd.DataFrame({
        "age": age, "sex": sex, "race_group": race, "site_id": site,
        "rural_flag": rural, "payer": payer, "label": label, "model_score": score,
    })


def cohort_from_config(config: dict[str, Any]) -> Any:
    """Generate a fake cohort using values in the study config."""
    cohort = config["cohort"]
    return generate_synthetic_cohort(int(cohort["n_patients"]), int(cohort["seed"]))


def generate_synthetic_registry(
    n_records: int, seed: int, visits_per_record: int = 3,
) -> np.ndarray:
    """Return local synthetic longitudinal registry rows in a NumPy array."""
    if n_records < 20:
        raise ValueError("n_records must be at least 20")
    if visits_per_record < 2:
        raise ValueError("visits_per_record must be at least 2")
    rng = np.random.default_rng(seed)
    record_ids = np.repeat(np.arange(n_records), visits_per_record)
    visit_number = np.tile(np.arange(1, visits_per_record + 1), n_records)
    age = np.repeat(rng.integers(45, 86, n_records), visits_per_record)
    heart_failure = np.repeat(rng.binomial(1, 0.70, n_records), visits_per_record)
    follow_up_open = np.repeat(rng.binomial(1, 0.93, n_records), visits_per_record)
    rural_flag = np.repeat(
        rng.choice(["urban", "rural"], n_records, p=[0.70, 0.30]), visits_per_record,
    )
    visit_days = np.tile(
        np.linspace(3, 35, visits_per_record, dtype=int), n_records,
    ) + rng.integers(-1, 2, len(record_ids))
    settings = np.where(visit_number == visits_per_record, "routine", "follow_up")
    registry = np.empty(len(record_ids), dtype=[
        ("record_id", "i4"),
        ("visit_number", "i4"),
        ("days_since_discharge", "i4"),
        ("age", "i4"),
        ("heart_failure", "i1"),
        ("follow_up_open", "i1"),
        ("care_setting", "U12"),
        ("rural_flag", "U8"),
    ])
    registry["record_id"] = record_ids
    registry["visit_number"] = visit_number
    registry["days_since_discharge"] = visit_days
    registry["age"] = age
    registry["heart_failure"] = heart_failure
    registry["follow_up_open"] = follow_up_open
    registry["care_setting"] = settings
    registry["rural_flag"] = rural_flag
    return registry
