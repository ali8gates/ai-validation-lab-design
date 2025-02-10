"""Create clearly fake cardiovascular validation data."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def generate_synthetic_cohort(n_patients: int, seed: int) -> pd.DataFrame:
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
    return pd.DataFrame({
        "age": age, "sex": sex, "race_group": race, "site_id": site,
        "rural_flag": rural, "payer": payer, "label": label, "model_score": score,
    })


def cohort_from_config(config: dict[str, Any]) -> pd.DataFrame:
    """Generate a fake cohort using values in the study config."""
    cohort = config["cohort"]
    return generate_synthetic_cohort(int(cohort["n_patients"]), int(cohort["seed"]))
