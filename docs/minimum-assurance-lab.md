# The Minimum Viable Assurance Lab

What is the smallest version of this that produces a result someone will act on. Everything else is later.

## Inputs

1. One registry connector or one health system data agreement with a defined refresh.
2. Two or three pathway definitions with a named guideline reference.
3. One or two models to evaluate, ideally addressing the same pathway so the cohort work is shared.
4. One evaluation rubric, filled in and signed off before any data moves. The template is in [the model evaluation rubric](../templates/model-eval-rubric.md).
5. A review group with the standing to say the result is credible.

## Outputs

A validation report per model, written for a committee. A comparison table when more than one model addresses the same pathway. A recommendation with explicit conditions, meaning what population and what threshold, not a pass or fail. A monitoring plan with thresholds set before deployment. And a reproducible bundle holding the protocol version, data version, code commit, and environment.

## Roles

**The specialty society or convening body** owns clinical credibility, pathway definitions, and reviewer recruitment. Without this the result is a technical exercise nobody cites.

**The health system** provides population data, deployment context, and the operational reality that makes impact estimates honest.

**The model developer** provides the model, documentation, and reproduction support. They do not get to see the held back portion of the evaluation and they do not choose the metrics.

**The lab** owns the engine, the protocol, the analysis, and the report. It has to be able to publish an unfavorable result. If it cannot, none of the rest is worth anything.

## What the first version does not have

No self service portal. Studies are run by analysts. No automated ingestion beyond one connector. No public leaderboard, ever. No accreditation claim. No coverage across specialties. No regulatory positioning.

Each of those is a reasonable thing to want and every one of them slows down the only question that matters at the start, which is whether an independent read changes a buying decision.

## Cost structure to plan around

Analyst time dominates. Cohort preparation is the single largest line, and it is the one that becomes reusable, which is why shared cohort studies are the path to a lower price per buyer. Clinical review time is second and cannot be automated. Compute is a rounding error and anyone who tells you otherwise is selling infrastructure.

## How to know it is working

Within the first few studies: does a buyer change a decision because of a report, does a reviewer sign their name to it, and does a second buyer arrive without being recruited. Those three, in that order. Study volume and revenue are lagging indicators and they will tell you what you already knew six months earlier.
