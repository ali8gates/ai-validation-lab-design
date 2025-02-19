# Guideline Aligned Evaluation

A validation result only matters if the people who write clinical practice can use it. That constraint shaped the whole design.

## The loop this work is built around

Guideline defines the pathway. Pathway defines the evaluation. Evaluation produces evidence. Evidence feeds the next guideline revision. Then it repeats.

Most model evaluation stops at a benchmark number and never enters that loop, which is why so much of it has no effect on care. Every design decision in this repository is meant to keep the loop closed. See [the guideline loop diagram](guideline-loop.png).

## What anchoring to a pathway actually means

A pathway definition is not a paragraph of context. It is a structured object the evaluation code reads, holding a guideline reference, cohort inclusion and exclusion rules, the decision points where a clinician acts, and the outcome window.

That gives three things a benchmark cannot:

The cohort is defensible. Inclusion and exclusion come from published criteria, not from whatever rows happened to be in the extract. Every exclusion is counted and reported, so a reviewer can see who was dropped and ask why.

The metric attaches to a decision. A model that scores well but sits at a point in the pathway where nobody can act on it is not useful. Naming the decision point forces that conversation early.

The outcome window is fixed before results are seen. Thirty day, ninety day, one year. Chosen up front, in writing, so nobody negotiates the window after looking at the curve.

`poc/config/example_pathway.yaml` is a working example, and `poc/src/pathway.py` is the code that reads it.

## Registry grade data as the substrate

Evaluation quality is bounded by the data underneath it. Cross sectional snapshots cannot answer the questions that matter, so registry style longitudinal data is the preferred substrate.

What longitudinal data makes possible:

- Outcomes at a real interval after the decision, rather than a proxy label captured at the same moment as the prediction.
- Repeat encounters for the same person, which is where a risk model's calibration usually falls apart.
- Site level breakdowns, because a model that holds nationally can still fail at a specific type of hospital.
- Time ordered validation, training and testing separated by time rather than by random split, which is the only version of the test that resembles deployment.

Where registry access is not available, the fallback ranks as follows: health system extract with a defined refresh, then a curated multi site research set, then vendor supplied data used only for reproduction and never as the primary read. That order is a quality statement, and it appears in every report so a reader knows which one they are looking at.

## Outcomes aware metrics

Discrimination is reported because everyone asks for it. It is not the point.

The metrics that carry weight in a guideline conversation are calibration in the local population, subgroup calibration and error rates, decision curve behavior across plausible thresholds, and the estimated effect on the action the pathway actually calls for. A model with a mediocre area under the curve and honest calibration is more useful to a committee than the reverse, and the report should say so plainly.

## Evaluation output as candidate evidence

Reports are written to be read by a review committee, not by an engineer. Plain language summary first. Cohort and exclusions next. Then results, subgroups, and limitations. Every number traceable to a protocol version, a data version, and a code commit.

The limitations section is mandatory and is written before the results are final. A report that only lists strengths gets discounted by exactly the audience it is trying to persuade.

## What this deliberately does not claim

An evaluation is not an endorsement, and none of this replaces regulatory review. The lab produces evidence and the boundaries around it. The decision to change practice belongs to the people who own the guideline.
