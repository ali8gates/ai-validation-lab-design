# Independent AI Validation Lab: Product and Architecture Work

Product strategy, discovery, and system design for an independent lab that evaluates clinical AI models before hospitals deploy them, with a cardiovascular focus.

Public references for the program this work supports:
- [AHA AI Assessment Lab](https://www.heart.org/en/professional/quality-improvement/aha-ai-assessment-lab)
- [Fierce Healthcare coverage of the HLTH 2025 announcement](https://www.fiercehealthcare.com/ai-and-machine-learning/hlth25-aha-unveils-ai-assessment-lab-validate-models-heart-health)

I led product and architecture work for this. The repository holds the problem framing, the product structure, the operating model, the reference diagrams, and a runnable evaluation scaffold. It contains no internal documents, no partner or donor names, no pricing, no contract terms, and no patient data. Everything here is either public or written at a level of generality that gives away nothing.

## What this is optimized for

Four things, and it is worth being blunt about them because they are what separate this from a benchmarking exercise.

**Validation that follows guideline rigor.** Evaluation designs are anchored in published clinical pathways, and results are written as candidate input to a guideline revision rather than as a technical score. [Guideline aligned evaluation](docs/guideline-alignment.md).

**Registry grade longitudinal data as the substrate.** Outcomes measured at a real interval after the decision, repeat encounters for the same person, site level breakdowns, and time ordered splits rather than random ones.

**Health systems as the primary buyer, developers as the secondary path.** That was the opposite of my starting assumption and it is the most consequential thing discovery changed. [Buyers, tiers, and what they will actually pay for](docs/commercial-model.md).

**Agentic and multi step tools, plus what happens after go live.** Per call accuracy says almost nothing about a tool that takes eight steps and calls three other systems. [Evaluating agentic and multi step workflows](docs/agentic-workflow-eval.md).

## Who this is for

This is relevant if you are coordinating validation work across several specialty societies, tying evaluations to guideline processes rather than to leaderboards, selling into health systems as the primary buyer, or working out what an assurance lab has to contain before it is credible. The cardiovascular focus is where the pathways and the data were strongest. The structure underneath is not specialty specific, and the seams where another specialty plugs in are named in [the multi specialty pattern](docs/multi-specialty-pattern.md).

If you want the shortest possible version, read [the minimum viable assurance lab](docs/minimum-assurance-lab.md). It is the smallest thing that produces a result somebody will act on.

## The problem

A hospital that wants to buy a clinical AI tool has almost no way to check whether it works for their patients.

The vendor supplies a paper and a performance curve from a population that may look nothing like the one walking through the door. Large academic centers can run their own check because they have data scientists and evaluation infrastructure. Small, rural, and mid-size hospitals cannot. Those are the same places where cardiovascular outcomes are already worst, so the gap compounds.

Four specific failures:

1. **No independent read.** Evaluation is done by the party selling the tool. Buyers have no neutral comparison.
2. **No capacity on the buyer side.** Most hospitals have no way to test a model against their own population before signing.
3. **Population mismatch is invisible.** Overall accuracy hides the subgroups where a model quietly fails.
4. **Nothing after go-live.** Performance decays and almost nobody is watching.

The buyers want proof. The developers want a credible third party to give it to them. Neither side wants to build the evaluation apparatus. That gap is the product.

## What the lab does

Four connected offerings under one program.

| Offering | What it produces | Who buys it |
| --- | --- | --- |
| **Validation** | Performance and calibration results against a defined population, with subgroup breakdowns | Model developers, health systems |
| **Impact analysis** | Clinical and operational effect estimates for a specific deployment setting | Health systems |
| **Monitoring** | Scheduled re-checks for drift, calibration decay, and new subgroup gaps | Both, as a subscription |
| **Evidence packaging** | Validation output assembled for regulatory and payer conversations | Model developers |

Validation is the anchor. The other three only exist because the first one produces reusable evidence.

## Documents

| File | Contents |
| --- | --- |
| [docs/discovery.md](docs/discovery.md) | How the problem was framed, what the market said, why this organization can run it |
| [docs/product-architecture.md](docs/product-architecture.md) | The four offerings, tiers, inputs, outputs, and what is deliberately out of scope |
| [docs/operating-model.md](docs/operating-model.md) | Governance, review structure, the per-model process, and decision rights |
| [docs/data-architecture.md](docs/data-architecture.md) | Data access patterns, evaluation stack, reproducibility requirements |
| [docs/roadmap.md](docs/roadmap.md) | Phasing, entry and exit criteria per phase, and what could sink it |
| [docs/guideline-alignment.md](docs/guideline-alignment.md) | How evaluation designs anchor to clinical pathways, and why registry grade data is the substrate |
| [docs/commercial-model.md](docs/commercial-model.md) | Buyer personas, tiering by scope, the pricing problem, and return on investment stated the way a buyer states it |
| [docs/agentic-workflow-eval.md](docs/agentic-workflow-eval.md) | Workflow level measures, scenario libraries, non determinism, and post deployment monitoring |
| [docs/multi-specialty-pattern.md](docs/multi-specialty-pattern.md) | What generalizes to other specialties, what does not, and the failure mode to avoid |
| [docs/minimum-assurance-lab.md](docs/minimum-assurance-lab.md) | Inputs, outputs, roles, and what the first version deliberately lacks |
| [docs/validation-protocol-template.md](docs/validation-protocol-template.md) | Fill in the blank protocol used before any evaluation runs |
| [templates/model-eval-rubric.md](templates/model-eval-rubric.md) | Rubric completed and signed off before any data moves |

## Diagrams

The loop everything here is built around:

![The guideline loop](docs/guideline-loop.png)

How a multi step workflow gets evaluated, and what carries on after deployment:

![Evaluating a multi step workflow](docs/agentic-eval.png)

The validation process, intake through follow up:

![Model validation pipeline](docs/validation-pipeline.png)

The data and evaluation architecture underneath it:

![Evaluation data architecture](docs/data-architecture.png)

Sources are in `docs/`. Both diagrams have `.svg` versions, and `docs/validation-pipeline.mmd` is Mermaid source that Lucidchart imports directly and GitHub renders in the browser.

## Code

`poc/` holds a working evaluation scaffold that runs on synthetic data. It is a template for how a study is specified, run, and reported, not a production system.

```
python poc/run_validation.py --config poc/config/example_study.yaml
```

That writes a validation report and a results file to `poc/output/`.

The second entry point is the worked pathway example, which is the one that shows how the pieces fit:

```
cd poc && python run_pathway_example.py
```

It generates synthetic registry style records, applies the cohort rules from a pathway definition, runs a rule baseline and a mock agent across a scenario library, computes the workflow measures, runs the monitoring checks, and writes `poc/output/pathway_report.md` in a form a review committee could read without touching code. The mock agent fails one hazard scenario on purpose, so the report shows what a triggered safety check actually looks like rather than a clean run.

See [poc/README.md](poc/README.md) for what each module covers.

## What I brought to this work

- Framed the problem around the buyer who cannot self-evaluate, which is what made the program fundable and mission-aligned rather than a generic testing service.
- Designed the product structure so one evaluation run feeds four offerings instead of four separate builds.
- Designed the data architecture around access patterns rather than data movement, since the governance constraint, not the compute, is what decides whether a study can run.
- Set the reproducibility requirement: locked protocol, locked environment, archived results, re-runnable on demand. A validation body that cannot reproduce its own results has no standing.
- Wrote the evaluation scaffold that turned the concept into something an engineer could pick up and extend.
- Changed the go to market on the strength of what discovery said rather than what the plan said, moving health systems to the front and developers to the follow on.

## How to read all of this

My bias throughout was to start from real buyer constraints and clinical rigor instead of from abstract benchmarks. That is why the commercial document sits next to the metric definitions, and why the pricing problem is written up as a problem I could not engineer away rather than as a solved item.

Everything here is meant to be adapted. Plug in your own registry, your own pathways, and your own governance structure. The one thing worth keeping intact is the loop: guideline, evaluation, evidence, guideline revision. Break the loop and you are producing numbers that nobody uses.

## Contact

GitHub: [ali8gates](https://github.com/ali8gates)
