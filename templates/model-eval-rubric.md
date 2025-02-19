# Model Evaluation Rubric

Filled in and signed off before any data moves. A rubric completed after results exist is not a rubric.

## 1. Clinical context

- Pathway id and version:
- Guideline reference, including section:
- Decision point this model informs:
- Action the clinician takes at that point:
- What happens today without the model:

## 2. Intended use

- Population the developer claims:
- Setting claimed, for example inpatient, ambulatory, or remote:
- Output type, for example risk score, classification, ranked list, or draft action:
- Explicitly out of scope:

## 3. Population definition

- Registry or source, with access tier stated:
- Inclusion criteria, each traceable to the guideline or the protocol:
- Exclusion criteria, with expected count for each:
- Index event and time zero definition:
- Outcome definition and window, fixed before results are seen:
- Time based split, with train and test periods named:

## 4. Metrics

Discrimination, reported because it will be asked for.

Calibration in the local population, which is the primary read. Include calibration slope, intercept, and a plot.

Decision curve behavior across the plausible threshold range, not at one chosen operating point.

Workflow measures where the tool is multi step: task completion, step agreement, pathway adherence, time to decision, unsafe action rate, escalation rate.

Estimated effect on the pathway action, stated with uncertainty.

## 5. Subgroups

Pre specified, never chosen after seeing results. At minimum age band, sex, race and ethnicity as recorded, insurance or payer category, site type including rural and critical access, and volume tier of the site.

For each: minimum sample size to report, and what gets said when a subgroup is too small rather than quietly dropping it.

## 6. Longitudinal requirements

- Follow up available and follow up required:
- Repeat encounter handling:
- Censoring approach:
- Whether temporal drift within the evaluation window was checked:

## 7. Safety

- Hazardous actions defined for this pathway:
- Clinical reviewer who signed off on the hazard list:
- Stopping rule, meaning what result halts the study and escalates:

## 8. Monitoring plan

- Checks enabled and threshold for each:
- Schedule:
- Who receives the alert and who can act on it:
- What triggers a full revalidation rather than a report:

## 9. Governance

- Reviewers and their conflicts, declared:
- Who signs the final report:
- Publication commitment, including for unfavorable results:
- Embargo terms, if any, stated up front:
- What the developer may and may not say about the result:

## 10. Reproducibility

- Protocol version:
- Data version and extraction date:
- Code commit:
- Environment specification:
- Where the bundle is stored and who can retrieve it:

## Sign off

| Role | Name | Date |
| --- | --- | --- |
| Clinical reviewer |  |  |
| Methods reviewer |  |  |
| Lab lead |  |  |
