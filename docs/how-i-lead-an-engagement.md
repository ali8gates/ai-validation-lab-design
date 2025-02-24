# How I Lead an Engagement

I led the product and technical work for this lab, and I wore several hats to get it from an open question to a program with a clear buyer, a working evaluation scaffold, and a path to revenue. This page covers the roles I played and the habits I rely on, with what each looked like here.

## The hats I wore

- **Discovery lead.** I ran the listening tour across academic centers, community and rural hospitals, payers, regulators, and model developers, and turned it into three problem statements, one for each side of the market.
- **Product owner.** I designed the product so one evaluation run feeds four offerings: validation, impact analysis, monitoring, and evidence packaging.
- **Architect.** I designed the data architecture around how data can be accessed under governance, not around moving it, and set the rule that every result must be reproducible on demand.
- **Hands on engineer.** I wrote the evaluation scaffold in this repo so an engineer could pick it up and extend it instead of starting from a document.
- **Commercial lead.** I built the buyer and pricing model and changed the go to market when discovery said the plan was wrong.
- **Program lead.** I worked with the cross functional task force covering clinical practice, research, and ethics, and set out decision rights so the lab could run without me in every room.

## Earning trust early and finding who matters

The first step was mapping who had a stake and what success meant to each of them in their own words. Hospitals needed an evaluation they could hand to both a clinical committee and a finance committee. Developers needed third party results that would move buyers, regulators, and payers. The organization needed a program that fit its mission and did not compete with the tools it evaluated. I wrote all three down side by side, because a program that only works for one of them does not get off the ground.

## Hearing the need behind the ask

The market kept asking for accuracy numbers. What buyers actually asked about in conversation was total cost, disruption to how their teams work, and what happens when the model is wrong. So the lab reports results in language a clinician and an executive can both act on, not a leaderboard score.

The bigger shift was the buyer. My starting assumption was that model developers would pay first. Discovery said health systems were the primary buyer and developers the follow on. I proposed flipping the go to market, which was not what the original plan called for, and it is the most important thing discovery changed.

## Using early pilots to learn the domain

Small modeling pilots early on did more than prove the concept. They showed that data access is the real bottleneck, that governance takes longer than the analysis, and that nobody agreed on what a good result looks like. Those lessons shaped the architecture and the protocol template before anything was built at scale.

## Talking early and often

I kept the task force and leadership up to date on what discovery was finding, including the parts that cut against the plan. The pricing problem is a good example. Rather than hide it, I wrote it up as a problem I could not engineer away, so the people deciding had the real picture early instead of a surprise later.

## Not over-promising

I was clear about what the lab would not do: build or sell models, or act as a regulator. I also wrote down the minimum viable version, the smallest thing that produces a result someone will act on, so the first commitment was one we could actually deliver, and the bigger program could follow once that landed.

## Setting the team up to do their best work

The operating model spells out who decides what, per model and per study, so clinical experts, data scientists, and program staff each own the part where their expertise counts. The scaffold and the protocol template gave engineers and study leads a concrete starting point they could own and push back on.

## Leading and building at the same time

I set the direction and I also wrote the code that proved it could work. Being close to the build meant I could answer hard questions from clinicians and developers in the room, and it set the level of ownership I expect from anyone on a team I lead.
