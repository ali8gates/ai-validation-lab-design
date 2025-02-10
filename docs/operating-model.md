# Operating Model

Who decides what, in what order, and what stops the process.

## Governance

**Program governance group.** Sets the standing rules: what qualifies for evaluation, the minimum evidence bar, how the organization's name may be used on a result, and conflict of interest policy. Owns the rules, not individual verdicts.

**External review panel.** Cardiologists, imaging specialists, statisticians, and health economists, rotating, disclosed, and independent of the developer under review. Judges endpoint appropriateness, clinical interpretation, and use recommendations for a specific study.

**Lab operations.** Runs studies, holds the protocol, and produces reports. Cannot change an acceptance decision.

Separation matters. The group that sets the bar, the group that runs the analysis, and the group that judges the result are not the same group.

## Process per model

1. **Intake and scoping.** Developer submits the model, intended use, target population, and documentation. Lab confirms whether a defensible study is even possible with available data. Some submissions should be declined here, and declining has to be normal.
2. **Protocol.** Cohort, endpoints, primary metrics, subgroups, thresholds, and analysis plan are written and locked before any data is touched. See [validation-protocol-template.md](validation-protocol-template.md).
3. **Data preparation.** Cohort extracted against inclusion and exclusion criteria, quality checked, snapshot versioned, environment locked.
4. **Evaluation run.** Protocol executed. No metric added after seeing results without an amendment recorded in the report.
5. **Review.** Statistical review, then clinical review. Panel sets the acceptance decision and the limitations. Dissent is recorded, not resolved by rewriting.
6. **Report.** Results, interpretation, limitations, and appropriate use conditions. Findings are published on the same terms whether they are favorable or not.
7. **Follow up.** Monitoring schedule set. Re-review triggers defined: elapsed time, model version change, case mix shift, or a safety signal.

## Decision rights

| Decision | Owner |
| --- | --- |
| What qualifies for evaluation | Governance group |
| Minimum evidence bar | Governance group |
| Study protocol | Lab operations, panel approves |
| Acceptance decision and limitations | Review panel |
| Use of the organization's name on a result | Governance group |
| Publication of an unfavorable result | Governance group, not the developer |
| Retire recommendation from monitoring | Review panel |

The last two are the ones under pressure. Both need to sit outside the commercial relationship.

## Rules that hold the thing up

- The protocol is locked before data access. Changes are amendments and appear in the report.
- The developer sees the result before publication and may correct factual errors about the model. They do not get to change the finding.
- Every report names its limitations and the populations where the model was not tested.
- No result is unconditional. Every finding is bound to an intended use and a population.
- Any study can be re-run from the archived protocol, snapshot, and environment.

## Conflicts

- Reviewers disclose relationships with developers and recuse where they exist.
- The lab does not hold financial interest in models it evaluates.
- Funding that supports evaluation for under-resourced hospitals is separated from the fee that pays for a specific study, so nobody can trace a favorable finding to who wrote the check.

## What failure looks like

Worth naming, because these are the realistic ways it goes wrong.

- The bar drifts down as revenue depends on throughput.
- Seals outlive the performance that earned them.
- Unfavorable results go quiet and only favorable ones get published.
- The evaluation queue fills with well-funded developers while the hospitals the program exists for see nothing.
- Reviews become a formality because the panel never has time to actually read the analysis.

Each of these has a countermeasure above. None of the countermeasures survive without someone whose job is to enforce them.
