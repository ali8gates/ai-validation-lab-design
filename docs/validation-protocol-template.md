# Validation Protocol Template

Completed and approved before any data is accessed. Locked at approval. Changes after that point are amendments, numbered and dated, and they appear in the final report.

## 1. Study identification

| Field | Value |
| --- | --- |
| Study id | |
| Model name and version | |
| Submitting organization | |
| Tier | Standard or Extended |
| Protocol version | |
| Approval date | |
| Protocol owner | |

## 2. Intended use

- Clinical question the model answers:
- Population it is intended for:
- Care setting:
- Decision it informs:
- Action triggered by a positive result:
- Who acts on the output:
- Stated contraindications and known limits from the developer:

If the intended use cannot be written in five plain sentences, the study is not ready to design.

## 3. Training context, as declared

- Training population, size and composition:
- Outcome definition used in training:
- Known performance claims and their source:
- Populations the developer has not tested:

## 4. Evaluation cohort

- Data source and access pattern (extract, in place, federated):
- Snapshot id:
- Observation window:
- Inclusion criteria:
- Exclusion criteria:
- Expected cohort size and event rate:
- Sites represented, by type and region:

## 5. Endpoints

- Primary endpoint and its exact definition:
- Secondary endpoints:
- Outcome ascertainment method:
- Time window for outcome capture:
- Handling of competing events:

## 6. Metrics and thresholds

| Metric | Reported | Pre-specified threshold |
| --- | --- | --- |
| AUROC | | |
| PR AUC | | |
| Sensitivity at operating point | | |
| Specificity at operating point | | |
| PPV at expected prevalence | | |
| Calibration slope and intercept | | |
| Brier score | | |
| Alerts per 1000 patients | | |

- Operating point and how it was chosen:
- Uncertainty method and interval width:

Thresholds are set before results are seen. A threshold chosen afterward is not a threshold.

## 7. Subgroup plan

| Subgroup field | Levels | Minimum cell size |
| --- | --- | --- |
| Age band | | |
| Sex | | |
| Race and ethnicity | | |
| Geography | | |
| Site type | | |
| Payer | | |

- Gap definition and the size of gap that gets flagged:
- Handling of cells below minimum size:
- Whether subgroup findings can change the overall recommendation:

## 8. Missing data and quality

- Expected missingness by field:
- Handling rule, declared in advance:
- Quality checks run before analysis and the failure thresholds:
- What happens if the cohort fails a quality check:

## 9. Sensitivity analyses

- Site level variation:
- Alternative operating points:
- Alternative outcome window:
- Exclusion of the largest contributing site:

## 10. Reproducibility

- Code version:
- Environment reference:
- Snapshot reference:
- Archive location:
- Person who can re-run this study in two years:

## 11. Review and decision

- Statistical reviewer:
- Clinical reviewers:
- Disclosed conflicts and recusals:
- Acceptance decision:
- Conditions and limitations attached to the result:
- Dissenting views, recorded verbatim:

## 12. Follow up

- Monitoring cadence:
- Re-review triggers (elapsed time, version change, case mix shift, safety signal):
- Result expiry date:
- Conditions that would withdraw the result:

## Amendments

| Number | Date | Change | Reason | Approved by |
| --- | --- | --- | --- | --- |
| | | | | |
