# Evaluating Agentic and Multi Step Workflows

Single prediction evaluation is a solved shape. You have inputs, one output, a label, and a metric. The tools arriving now do not have that shape. They take several steps, call other systems, and produce an action or a draft rather than a score.

Per call accuracy is close to meaningless for those. A tool can be right at every individual step and still walk a patient to the wrong place.

See [the workflow evaluation diagram](agentic-eval.png) for how this fits together.

## Measure the workflow, not the call

Six measures, all defined at the level of a completed task.

**Task completion.** Did the workflow reach a terminal state that a clinician can act on, or did it stall, loop, or hand back something unusable.

**Step agreement.** At each decision point, did the action match what the pathway calls for. Reported per step, because a tool that is strong for four steps and wrong on the fifth needs the fifth step named.

**Pathway adherence.** Share of runs that followed the guideline defined sequence. A shortcut that reaches a correct answer still gets counted as a deviation, because the shortcut is what will break on the next case.

**Time to decision.** Steps taken and the cost attached to each. This is where these tools earn their keep, so it gets measured rather than asserted.

**Unsafe action rate.** Frequency of actions flagged as hazardous in the scenario definition. This is a rate that has to be reported even when it is zero, because zero out of eight hundred is a very different statement than zero out of twelve.

**Escalation to human.** How often the tool stopped and asked. Too low is dangerous. Too high means it does not save anyone time. Neither direction is good, so the target is a band, not a maximum or a minimum.

## Scenario libraries instead of test sets

A test set of rows cannot exercise a multi step workflow. What replaces it is a scenario library.

A scenario is a defined starting state, an expected sequence of pathway steps, an expected terminal action, and hazard flags marking actions that must never be taken in that situation. The library is built from real pathways and includes the ordinary cases, the ambiguous ones, and the ones designed to bait an unsafe shortcut.

Two properties make the library trustworthy. It is versioned, so a result can be tied to the exact library that produced it. And a portion of it is held back, so a vendor cannot tune against the full set. Both are boring. Both are the difference between an evaluation and a demo.

`poc/config/example_scenarios.yaml` holds a small working library and `poc/src/agentic.py` holds the measures.

## Non determinism

The same input can produce different runs. That is a property of the tools, not a defect in the test, and evaluation has to account for it.

Every scenario runs multiple times. Report the distribution rather than a point value, and report the variance explicitly, because a tool that is correct eighty percent of the time on identical input is a different product than one that is correct eighty percent of the time across varied inputs. Failure modes get grouped by kind rather than counted in aggregate, since ten instances of one pattern is a fixable bug and ten different patterns is a boundary problem.

## Monitoring after go live

The evaluation is the beginning. Five checks run on a schedule after deployment.

Calibration decay against the baseline result set. Subgroup gaps widening, watched separately since aggregate numbers hide them. Input distribution shift, which usually shows up before performance does. Volume anomalies, meaning use dropping off or spiking, both of which signal something changed in the workflow. And unsafe action rate rising, which is the one that pages a person rather than filing a report.

Each check has a documented threshold and a severity, and each site sees its own results. Sites are not compared to each other by default, since that turns a safety tool into a scoreboard and people stop reporting honestly. `poc/src/monitoring.py` holds the checks and the default thresholds.

## Honest limitations

Scenario libraries are expensive to build and they encode the assumptions of whoever wrote them. Hazard flags require clinical review to be worth anything. And a workflow evaluation cannot tell you how a tool behaves when the humans around it start trusting it more than they should, which is probably the largest real risk and the hardest thing to instrument.
