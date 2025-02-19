# Buyers, Tiers, and What They Will Actually Pay For

Discovery answered a question I went in with the wrong assumption about. I expected model developers to be the primary buyer. They are not.

## Two buyers, different math

**Model developers.** They want independent evidence because their buyers keep asking for it. The problem is when they need it. Early and mid stage companies are shopping for validation exactly when cash is tightest, and the price of a rigorous study competes directly with engineering headcount. Interest was high and conversion at a serious price point was weak. That is not a sales problem. It is the buyer's budget being real.

**Health systems.** Different math entirely. They face the same buy versus build decision several times a year, across multiple models, and each wrong decision is expensive in a way that shows up on a balance sheet. They already pay for evaluation work indirectly through internal data science time or through consultants. A validation service replaces a cost they are already carrying, which is a much easier case than creating a new line item.

The conclusion that changed the plan: sell to health systems first, and treat developers as the secondary path that opens up once the evidence base and the reputation exist.

## Tiering

Three tiers, described by scope rather than by number.

| Tier | Scope | Typical buyer |
| --- | --- | --- |
| Tier 1 | Single model, single population, discrimination and calibration, subgroup breakdown, standard report | Developer needing a first independent read |
| Tier 2 | Tier 1 plus impact analysis for a named deployment setting, threshold selection, and workflow effect estimates | Health system evaluating a purchase |
| Tier 3 | Tier 2 plus multi site validation, monitoring subscription, and evidence packaging for external review | Enterprise buyer or a developer preparing for regulatory and payer conversations |

The tier ratio matters more than the absolute prices. Tier 2 lands at roughly double Tier 1, and Tier 3 at roughly triple, because the cost driver is analyst time and site coordination, not compute. Actual figures are omitted here on purpose.

## The pricing problem I could not engineer away

A study priced to cover analyst time is out of reach for the companies that most need an independent read. Three ways to soften that, none free:

1. Subsidize developer studies from health system revenue once that side is stable. Cleanest, and it requires the first side to work.
2. A shared cohort tier where several models are evaluated against the same prepared population, splitting the expensive preparation step across buyers. Lower margin per study, much lower price per buyer, and it only works when the models address the same pathway.
3. Grant funded studies for pathways with clear public health value. Real money, slow money, and it cannot be the base of a business.

Option two is the one worth building toward, because cohort preparation is the dominant cost and it is the part that genuinely can be reused.

## Return on investment, stated the way a buyer states it

Health systems do not buy rigor. They buy avoided cost and defensibility.

- One avoided bad purchase. A model that does not work in their population, caught before the contract, against the cost of a study.
- Internal analyst time not spent. Weeks of data science capacity returned to work only they can do.
- A faster decision. Procurement cycles stall on unanswerable questions. An independent read ends the stall.
- Something to show a board or a regulator when asked how the model was checked.

That last one is underrated. A large share of the interest was not about accuracy at all. It was about being able to answer the question.

## What I would test next

Whether monitoring sells better than validation. Validation is a one time purchase decision, and monitoring is a subscription tied to a fear that never goes away. The revenue quality is better and the buying trigger is more reliable. It might be the correct wedge rather than the follow on.
