# Independent AI Model Validation Lab Template

This is a small local Python scaffold for validating a binary cardiovascular model with fake data. It is a template for study planning and code review, not a clinical validation package.

## Setup

```bash
python -m pip install -r poc/requirements.txt
python poc/run_validation.py --config poc/config/example_study.yaml
```

The command writes `poc/output/validation_report.md` and `poc/output/results.json`. The default run creates a clearly synthetic local cohort. It makes no network calls.

To use a local CSV, add `--data path/to/file.csv`. The CSV must include `label`, `model_score`, and each configured subgroup field. A supplied CSV changes the data label in JSON, but users are responsible for all governance and privacy controls.

## Contents

- `src/synth_data.py`: fake cohort generator.
- `src/metrics.py`: discrimination, threshold, calibration, and bootstrap metrics.
- `src/subgroups.py`: subgroup summaries and configured flags.
- `src/drift.py`: PSI, KS score comparison, calibration change, and alert rules.
- `src/impact.py`: illustrative per-1000 decision estimates driven by config inputs.
- `src/report.py`: markdown report rendering.

## Tests

Run `pytest poc/tests/test_metrics.py`. The requirements file intentionally contains only the requested runtime packages. Install pytest separately if it is not already available.

## Limits

The default output is fake and template-only. Real validation needs an approved protocol, representative data, predefined analyses, appropriate review, and clinical governance.
