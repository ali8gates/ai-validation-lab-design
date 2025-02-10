# Product Architecture

Four offerings, one evaluation engine underneath them. The structure matters more than the list: a single validation run produces artifacts that the other three reuse, so the marginal cost of the second, third, and fourth offering is small.

## A. Validation

Independent evaluation of a model against a defined population.

**Tiers**

| Tier | Scope | Output |
| --- | --- | --- |
| Standard | Discrimination, calibration, and operating point analysis on a reference cohort | Performance report with clinical interpretation |
| Extended | Adds subgroup analysis by age, sex, race and ethnicity, geography, site type, and payer, plus site level variation | Performance and equity report with named limitations |

Modality coverage starts with structured record based risk models and signal data, then imaging. The sequence follows data availability and clinical readiness, not technical difficulty.

**Inputs**
- The model, in a form that can be run in a controlled environment, or scored outputs under a documented procedure.
- An intended use statement: population, clinical question, decision it supports, and the action it triggers.
- Developer documentation of training population and known limitations.

**Outputs**
- Primary metrics against the target population with confidence intervals.
- Subgroup performance with explicit gaps and small sample flags.
- Calibration in the deployment range, not just overall.
- A written clinical interpretation, including where the model should not be used.
- A limitations register that travels with the result.

The last item is the one that gets negotiated. It should not be.

## B. Impact analysis

What changes if this model is deployed in a specific setting.

- Clinical effect: event detection rate, time to intervention, downstream testing volume.
- Operational effect: length of stay, throughput, staff time, alert burden per unit of clinical benefit.
- Financial effect: cost of care, avoidable utilization, penalty exposure.

Method is matched cohort or pre and post comparison built from record and registry data, scoped to one setting at a time. Results are setting specific and do not transfer without restating the assumptions.

Alert burden is the number that decides adoption. A model with excellent discrimination and an unworkable false positive rate at the operating point is not deployable, and that should be visible in the report rather than discovered six months in.

## C. Monitoring

Validation is a snapshot. Deployment is continuous.

- Scheduled re-evaluation on refreshed data at a contracted cadence.
- Covariate shift detection against the validation baseline.
- Calibration decay tracking, separately from discrimination.
- Subgroup gap tracking, since new gaps open as case mix changes.
- Threshold based alerts with a defined recommendation: keep, recalibrate, re-validate, or retire.

The retire path has to exist and has to be usable. A monitoring service that can only recommend recalibration is a rubber stamp.

## D. Evidence packaging

Assembling validation output for regulatory and payer conversations.

- Clinical validity, analytical validity, and real world performance organized into a submission ready structure.
- Documentation of the subgroup analysis and the post-deployment monitoring plan.
- Study design consultation for prospective and post-market work.

This is packaging and consultation only. The lab does not represent a developer to any authority, and the report says the same thing regardless of who is reading it.

## Shared engine

All four run on the same components, which is the entire reason the portfolio holds together.

- Cohort definition and extraction bound to a written protocol.
- A metric library that produces identical results across studies.
- A subgroup engine with consistent group definitions and small sample handling.
- A calibration module.
- A report generator driven by templates, so two studies are comparable on sight.
- A results archive that allows any past study to be re-run.

`poc/` is a working sketch of this engine on synthetic data.

## Out of scope, on purpose

- Model development, tuning, or repair. The lab evaluates. It does not fix.
- Pass or fail as a single verdict. Results are reported against an intended use, with conditions.
- Ranking vendors against each other. Different intended uses are not comparable, and league tables invite exactly the wrong behavior.
- Any use of the lab's name by a developer that is not the full report with its limitations attached.
