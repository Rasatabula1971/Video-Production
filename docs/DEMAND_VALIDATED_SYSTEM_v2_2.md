# Demand-Validated Video System v2.2

## Purpose

Extend the existing subject-neutral production control plane so expensive production begins only after there is evidence that the audience wants the subject and the proposed package can earn a click without misleading the viewer.

The existing OpenMontage production engine remains unchanged.

## Architecture

```text
MARKET
  -> SEED TOPICS
  -> DEPTH-FIRST RESEARCH
  -> WINNERS + FAILURES
  -> DEMAND CLUSTERS
  -> AUDIENCE / AWARENESS
  -> TOPIC x FORMAT DECOMPOSITION
  -> OPPORTUNITY RECORD
  -> TITLE + THUMBNAIL PACKAGE
  -> GATE 0: SHOULD WE MAKE THIS?
  -> EXISTING RESEARCH / PROPOSAL / SCRIPT / PRODUCTION PIPELINE
  -> GATE 1: APPROVE BEFORE SPEND
  -> ASSET / EDIT / COMPOSE / QC
  -> GATE 2: APPROVE BEFORE PUBLISH
  -> PUBLISH
  -> MEASURE
  -> LEARNING STORE
  -> NEXT OPPORTUNITY
```

Gate 0 is an editorial production-decision gate. Gates 1 and 2 retain their existing meanings.

## Core rules

1. **Demand before production.** A subject being interesting is not enough.
2. **Outliers over raw views.** Store both absolute performance and performance relative to the channel baseline.
3. **Failures are evidence.** Deliberately collect comparable underperformers to reduce survivorship bias.
4. **Separate topic from format.** Do not treat a successful video as one indivisible idea.
5. **Package before spend.** Create title/thumbnail hypotheses before expensive asset generation.
6. **Original contribution required.** A reference video is evidence, not the product.
7. **Measurement closes the loop.** Published-video behavior becomes evidence for future opportunity decisions.
8. **Human decides.** Automated scores prioritize investigation; they do not authorize production.

## Discovery engine

Start from roughly 20-30 seed topics for a market. Explore promising branches depth-first:

```text
seed
  -> relevant video
  -> channel
  -> channel outliers
  -> related videos
  -> adjacent problem
  -> adjacent audience
  -> new outlier
```

Stop a branch when it stops producing useful evidence, then return to another seed.

### Evidence collected

For each candidate video store, where available:

- platform and video id
- URL
- title
- channel id/name
- publish date
- views
- channel baseline views
- outlier multiple
- upload age / view velocity
- duration / format
- title pattern
- thumbnail observations
- hook / opening observations
- topic
- promise
- target audience
- winner/failure/comparator classification
- evidence confidence

Do not invent unavailable metrics. Missing values remain explicit.

## Outlier model

A useful starting signal is:

```text
outlier_multiple = video_views / channel_baseline_views
```

Absolute-view thresholds may be retained as configurable heuristics, but they are not universal laws and must not be hard-coded as proof of demand.

## Winner/failure comparison

For promising topic/format combinations, collect both winners and comparable failures.

Compare:

- topic
- promise
- title
- thumbnail
- hook
- channel baseline
- duration
- format
- opening
- structure
- payoff
- audience fit
- timing
- visual execution

The goal is not to copy winners. The goal is to identify which hypotheses survive comparison.

## Demand clusters

Cluster evidence around recurring:

- problems
- desired outcomes
- questions
- fears
- curiosity
- aspirations
- mechanisms
- myths
- conflicts
- transformations

A cluster supported by multiple independent observations is stronger evidence than a single viral video.

## Audience awareness

Each opportunity should distinguish:

```text
desired outcome -> perceived problem -> mechanism -> awareness
```

Record whether the intended viewer is unaware, problem-aware, mechanism-aware, solution-aware, or highly informed when that distinction is useful.

## Topic x format decomposition

For every reference decompose:

- topic
- promise
- format
- hook
- structure
- payoff

A new proposal must state its original contribution separately.

### Source dependency test

Ask:

> If the reference video disappeared tomorrow, could we still make our video?

If no, rework the proposal.

## Opportunity record

An opportunity record contains evidence and hypotheses, not a declaration that a video will succeed.

Suggested dimensions:

- demand evidence
- outlier evidence
- repetition across independent videos
- winner/failure comparison quality
- audience clarity
- problem/desire strength
- knowledge gap
- original contribution
- packaging potential
- production feasibility
- evidence confidence

Scores are prioritization aids. Store the underlying evidence and uncertainty with every score.

## Packaging before production

For serious candidates prepare:

- 3-5 title concepts
- 3-5 thumbnail concepts
- core promise
- curiosity gap
- intended viewer
- expected payoff

Treat title and thumbnail as one communication unit. The package must remain truthful to the proposed content.

## Gate 0 - production decision

Human decision:

- PRODUCE
- RESEARCH_MORE
- REFRAME
- REJECT

Review demand, opportunity, originality, packaging, viewer value, evidence quality, and feasibility.

Only PRODUCE proceeds into the existing production pipeline.

## Existing production pipeline

After Gate 0, the current OpenMontage-based workflow remains authoritative:

```text
research -> proposal -> script -> scene -> asset -> edit -> compose -> publish bundle
```

The existing hook/script scorer remains a separate pre-spend quality control. This document does not replace it.

## Learning engine

For each published video join:

### Research
topic, audience, desired outcome, perceived problem, mechanism, awareness, demand cluster

### Evidence
reference videos, channel baselines, outlier multiples, winners, failures, confidence

### Packaging
title, thumbnail, promise, hook, format

### Content
structure, opening, duration, story type, visual strategy, editing strategy

### Performance
impressions, CTR when available, views, view velocity, average view duration, average percentage viewed, retention, subscribers, shares, revenue/conversion where applicable

### Interpretation
what worked, what failed, confidence, next hypothesis

## Diagnostic framework

- **High click response + high retention:** packaging and content both deserve further study.
- **High click response + low retention:** inspect promise mismatch, opening, pacing and payoff.
- **Low click response + high retention:** inspect packaging, framing and audience targeting.
- **Low click response + low retention:** revisit opportunity, package and execution rather than repeating the same idea.

These are diagnostic hypotheses, not automatic causal conclusions.

## Experiment discipline

Prefer changing one or a small number of variables per experiment. Examples:

- outlier-based selection vs non-outlier selection
- pre-production packaging variants
- Proof -> Promise -> Plan openings
- problem-aware vs mechanism-aware framing
- evidence-driven visual changes vs arbitrary visual resets

## State additions

Pre-production discovery states:

```text
SEED
RESEARCHING
DEMAND_FOUND
OPPORTUNITY_FOUND
PACKAGING
AWAITING_PRODUCTION_DECISION
REJECTED
APPROVED_FOR_EXISTING_PIPELINE
```

Do not replace OpenMontage's internal production checkpoints with a second state machine. The event ledger records transitions across both layers.

## Implementation boundary

Build this layer under `montage_ext/discovery/` and `montage_ext/learning/`.

Do not modify `vendor/openmontage/` for this feature.

The first implementation should focus on contracts, deterministic calculations, evidence storage, and human-readable decision packets before adding autonomous crawling or LLM scoring.
