# Validation Report: cv-risk-validation-template-001

> **SYNTHETIC DATA TEMPLATE ONLY.** All results in this report come from locally generated fake data. They are not clinical evidence and must not support patient care or deployment decisions.

## Study

- **Model:** example-cardiovascular-risk-model
- **Intended use:** Support review of adults who may benefit from follow-up cardiovascular risk assessment. It is not a diagnosis or treatment recommendation.
- **Monitoring cadence:** quarterly
- **Cohort:** synthetic cardiovascular cohort generated locally; n=1200.
- **Inclusion:** Adults age 40 to 84 years; At least one synthetic encounter
- **Exclusion:** Missing synthetic model score; Records outside the age range

## Primary metrics

| Metric | Value | 95% bootstrap interval |
| --- | --- | --- |
| auroc | 0.676 | 0.645 to 0.711 |
| pr_auc | 0.460 | 0.423 to 0.515 |
| sensitivity | 0.551 | 0.507 to 0.600 |
| specificity | 0.714 | 0.683 to 0.744 |
| ppv | 0.456 | 0.413 to 0.507 |
| npv | 0.786 | 0.754 to 0.817 |
| brier_score | 0.202 | 0.189 to 0.216 |

Decision threshold: 0.350. Prevalence: 0.302.

## Subgroup checks

| Field | Group | n | Sensitivity | AUROC | Sensitivity gap | Flag |
| --- | --- | --- | --- | --- | --- | --- |
| sex | female | 618 | 0.557 | 0.683 | 0.006 | below_sensitivity_floor |
| sex | male | 582 | 0.545 | 0.668 | -0.006 | below_sensitivity_floor |
| race_group | group_a | 503 | 0.532 | 0.684 | -0.019 | below_sensitivity_floor |
| race_group | group_b | 316 | 0.536 | 0.673 | -0.015 | below_sensitivity_floor |
| race_group | group_c | 226 | 0.578 | 0.720 | 0.027 | below_sensitivity_floor |
| race_group | group_d | 155 | 0.590 | 0.575 | 0.039 | below_sensitivity_floor |
| site_id | site_1 | 544 | 0.535 | 0.689 | -0.016 | below_sensitivity_floor |
| site_id | site_2 | 424 | 0.558 | 0.665 | 0.007 | below_sensitivity_floor |
| site_id | site_3 | 232 | 0.577 | 0.663 | 0.027 | below_sensitivity_floor |
| rural_flag | rural | 306 | 0.624 | 0.706 | 0.073 | none |
| rural_flag | urban | 894 | 0.520 | 0.662 | -0.031 | below_sensitivity_floor |
| payer | coverage_a | 581 | 0.527 | 0.649 | -0.024 | below_sensitivity_floor |
| payer | coverage_b | 384 | 0.583 | 0.700 | 0.032 | below_sensitivity_floor |
| payer | coverage_c | 235 | 0.557 | 0.698 | 0.006 | below_sensitivity_floor |

A `small_n` flag means the group did not meet the configured minimum size. A `below_sensitivity_floor` flag means sensitivity was below the configured floor.

## Calibration

- Calibration intercept: -0.369
- Calibration slope: 0.528
- Brier score: 0.202
- Expected calibration error: 0.066

## Drift status

- Status: **ALERT**
- PSI: 0.014
- KS statistic: 0.035; p-value: 0.448
- Baseline to current calibration slope change: -0.009
- Alert reasons: calibration_slope

## Illustrative decision impact

Illustrative only. These are synthetic decision estimates, not observed outcomes.

| Measure | Per 1000 |
| --- | --- |
| alerts per 1000 | 365.833 |
| true positives per 1000 | 166.667 |
| false positives per 1000 | 199.167 |
| avoided events per 1000 | 8.333 |
| event value units per 1000 | 83.333 |
| alert management units per 1000 | 36.583 |
| net value units per 1000 | 46.750 |

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
