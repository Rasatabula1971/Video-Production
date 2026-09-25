# Video-Production — Product Specification v2

**Stage:** 3 — Spec Freeze  
**Status:** DRAFT — HUMAN APPROVAL REQUIRED  
**Task tier:** ARCHITECTURAL  
**Scope:** Production workflow and product behavior. Architecture is frozen only after this specification is approved.

## 1. Purpose

Video-Production is a subject-neutral, AI-assisted short-form video production control plane.

It may begin with either:

1. an existing source video/content item to analyse and transform into a new, original treatment; or
2. a topic/brief that requires research before production.

The system automates repetitive analysis and production work while preserving human control over the three creative decisions that most strongly determine the result:

- **Gate 1 — Idea / Angle**
- **Gate 2 — Script**
- **Gate 3 — Rough Cut / Video**

The system must not silently progress through any of these gates.

The first production subject remains Trinidad steelpan, but subject-specific facts, rights rules and creative guidance remain isolated in `subjects/<id>/`. Brand-specific presentation remains isolated in `brands/<id>/`.

## 2. Problem being solved

The existing project has already proven an end-to-end free/local production chain, but its first dry run exposed a quality problem: technically valid output can still be visually weak, generic or skippable.

The revised system therefore optimizes for **controlled creative transformation**, not merely successful rendering.

For source-content workflows, the missing front half is:

`source video → understanding → original angles → human choice`

For production, the missing creative control is:

`script beat → best visual type → appropriate asset/tool`

AI image generation must not be the default visual solution.

## 3. Product outcome

Given a source video or topic, the system should produce a reviewable short-form video package containing:

- source analysis and provenance;
- claims/questions/moments worth developing;
- multiple materially different creative angles;
- an explicit statement of original contribution;
- a human-approved script;
- a beat-level visual plan;
- rights/provenance-aware assets;
- a short animatic/sample for early quality detection;
- a human-approved rough cut;
- a final render/export bundle.

Publishing and performance learning remain planned capabilities, but they are downstream of production-quality validation.

## 4. Governing principles

### 4.1 Human creative authority

AI proposes, analyses, drafts, scores and assembles. The human makes the final creative decision at Gates 1–3.

A rejection must return the workflow to the relevant prior stage rather than being treated as an error.

### 4.2 Original contribution is mandatory

Repurposing is not defined as cosmetic modification.

A candidate must identify the new contribution made by this production, such as:

- analysis;
- explanation;
- comparison;
- fact-checking;
- synthesis;
- counterargument;
- contextualization;
- commentary;
- a new narrative structure or teaching treatment.

Crop, speed changes, captions, music, AI voice or visual restyling alone do not satisfy this requirement.

### 4.3 Evidence before assertion

Claims that materially affect the script must be traceable to a source, the subject fact corpus, or be explicitly marked as unverified.

Known uncertainty must survive into the approval artifact instead of being silently resolved.

### 4.4 Visual type before visual provider

The system decides **what kind of visual best communicates a beat before deciding which tool/provider should make it**.

The preferred decision order is:

1. usable source-video clip/frame;
2. original/user-owned footage;
3. licensed/public-domain/approved real footage or still;
4. diagram/data visualization/map;
5. motion graphic/typography/animation;
6. AI-generated image;
7. AI-generated video, when later enabled and justified.

This is a preference order, not an absolute prohibition: the Visual Director may choose a later option when it is demonstrably better for the beat and passes rights/quality rules.

### 4.5 Free/local-first, replaceable providers

Prefer free/open-source/local capabilities where they meet the requirement. Paid services are fallbacks, not architectural dependencies.

Provider choice must remain replaceable.

### 4.6 Do not fork the production engine unnecessarily

`vendor/openmontage/` remains vendored upstream code. Project-specific behavior belongs in `montage_ext/`, subject packages, brand packages, pipeline definitions or adapters unless a documented reason requires otherwise.

## 5. Authoritative workflow

### 5.1 Entry modes

**Mode A — Source Content**

`source content → ingest → transcript/timestamps → scene/frame analysis → source understanding`

**Mode B — Topic / Brief**

`topic/brief → research → evidence package → source understanding`

Both modes converge before idea generation.

### 5.2 Source Understanding

The system produces a structured source-understanding artifact containing, where applicable:

- source identity and provenance;
- transcript with timestamps;
- detected scenes and representative frames;
- main argument/story;
- important claims;
- questions raised;
- strong/interesting moments;
- contradictions or ambiguities;
- weak or missing explanations;
- candidate source excerpts;
- claims requiring verification;
- rights/reuse notes;
- potential directions for original contribution.

The system must distinguish source statements from independently verified facts.

### 5.3 Idea Engine

From the source-understanding/evidence package, generate multiple **materially different** treatments rather than paraphrases of the same idea.

Default target: **5 candidates**. A run may request more when useful.

Each candidate contains:

- working title;
- hook concept;
- central question;
- audience tension/need;
- story direction;
- expected payoff;
- original contribution;
- likely source moments/assets;
- research/fact-check needs;
- rights concerns;
- initial visual approach.

Near-duplicate candidates must be collapsed or regenerated.

### 5.4 Gate 1 — Idea / Angle approval

The system stops.

Human actions:

- **APPROVE**
- **MODIFY**
- **REGENERATE**
- **REJECT**
- **DEFER**

Approval selects the creative direction. No full script or expensive asset generation should proceed without approval.

The existing OpenMontage pre-spend approval behavior may be reused, but the product meaning of Gate 1 is now **creative-direction approval**, not merely cost approval.

### 5.5 Research and fact verification

After Gate 1, the selected angle is researched deeply enough to support its claims.

The output must identify:

- supported claims;
- contested claims;
- unresolved claims;
- corrections to source material;
- usable citations/provenance;
- rights restrictions relevant to production.

Subject fact corpora should be consulted first when applicable, but must not be treated as infallible.

### 5.6 Script Engine

The approved angle is converted into a short-form script using the core narrative structure:

**HOOK → STORY/BUILD → RE-HOOK → PAYOFF/ANSWER → TAKEAWAY**

The exact timing may vary by video.

The script artifact must include:

- narration;
- beat/timing structure;
- factual support links/IDs;
- source excerpts, if any;
- intended original contribution;
- visual intent notes;
- unresolved warnings;
- estimated duration.

The hook and re-hook must create attention without promising a payoff the video does not deliver.

### 5.7 Gate 2 — Script approval

The system stops before full production.

Human actions are the same as Gate 1.

Editing the script is a first-class path. Human changes become the authoritative script for downstream stages.

### 5.8 Visual Director

The Visual Director converts each approved script beat into a visual requirement.

For each beat it records:

- communication goal;
- preferred visual type;
- candidate source moment, if applicable;
- required asset;
- motion/pacing intent;
- rights/provenance requirements;
- fallback visual type;
- generation/retrieval tool only after the type is selected.

AI imagery must not be generated merely because an image provider is available.

Generated depictions must obey subject/brand rights rules. Existing steelpan restrictions on historical figures remain hard constraints for that subject.

### 5.9 Asset acquisition/generation

Assets may come from:

- approved excerpts of the source content;
- original/user-owned media;
- approved stock/public-domain repositories;
- reusable bespoke scene components;
- diagrams/Manim;
- Remotion/HyperFrames/motion graphics;
- generated imagery where appropriate.

Every externally sourced or generated asset must carry provenance sufficient for later review.

### 5.10 Animatic / early quality check

Before committing to the full rough cut, produce a representative **10–15 second animatic/sample** when practical.

Quality checks include:

- first-frame interest;
- visible activity in the opening seconds;
- static-element duration;
- pacing/cut/change density;
- visual relevance to narration;
- obvious slideshow behavior;
- caption/readability problems;
- voice/music balance where present;
- reference-energy comparison when approved references exist.

A failed animatic returns to Visual Director, asset selection, script or idea stage as appropriate.

Automated scoring informs the human; it does not replace a human creative gate.

### 5.11 Rough-cut assembly

Use deterministic edit decisions and the existing rendering toolchain to create the complete rough cut.

The rough cut must be reviewable as the actual intended platform format, with native 9:16 preferred for Shorts rather than relying on a late center crop.

### 5.12 Gate 3 — Rough Cut / Video approval

The system stops before finalization/publish.

Human actions:

- **APPROVE FINAL**
- **REVISE EDIT**
- **REVISE VISUALS**
- **REVISE SCRIPT**
- **RETHINK IDEA**
- **REJECT**
- **DEFER**

Revision returns to the relevant upstream artifact while retaining the decision trail.

### 5.13 Final render/export

After Gate 3 approval:

- perform final render;
- run technical QC;
- generate captions/subtitles as required;
- produce export bundle;
- preserve provenance and decision artifacts.

Automatic publishing is not required for the production-quality milestone.

## 6. Reuse / Adapt / Build / Defer

| Capability | Decision | Notes |
|---|---|---|
| FFmpeg media handling | REUSE | Existing proven render/media dependency |
| Transcription | REUSE | Existing transcriber capability; benchmark source-video workflow |
| Scene detection | REUSE | Existing capability |
| Frame sampling | REUSE | Existing capability |
| Existing visual QA | ADAPT | Use as one signal, not creative authority |
| OpenMontage research | ADAPT | Must support source-video-derived claims and fact verification |
| Existing proposal/checkpoint | ADAPT | Gate 1 becomes creative idea/angle approval |
| Existing script director | ADAPT | Enforce revised narrative contract |
| Remotion/FFmpeg assembly | REUSE | Already proven end-to-end |
| HyperFrames / motion runtime | EVALUATE/ADAPT | Candidate for motion-led briefs |
| Source Understanding | BUILD | New structured orchestration/artifact |
| Idea Engine | BUILD | Multiple distinct treatments + original contribution |
| Original-contribution validator | BUILD | Guard against cosmetic repurposing |
| Visual Director | BUILD | Visual-type decision before provider |
| Hook/attention scorer | BUILD/EXPAND | Include animatic signals, not text only |
| Cross-run ledger | BUILD | Thin append-only record as previously planned |
| AI image generation | ADAPT | Optional asset type, not default |
| YouTube publishing | DEFER | Resume after production quality clears |
| Metrics/learning loop | DEFER | Preserve design; implement after publish path |
| TikTok/Reels adapters | DEFER | After Shorts production/publish path |
| Text-to-video generation | DEFER | Not required for v1 |

## 7. Required artifacts

A completed run should preserve structured artifacts equivalent to:

1. `source_manifest`
2. `transcript` / timestamp map, when source media exists
3. `source_understanding`
4. `idea_candidates`
5. `gate_1_decision`
6. `research_brief` / fact verification
7. `script`
8. `gate_2_decision`
9. `scene_plan`
10. `asset_manifest`
11. `animatic_report`
12. `edit_decisions`
13. `render_report`
14. `gate_3_decision`
15. `final_export_manifest`
16. append-only decision/event records where the ledger is enabled

Exact filenames/schema boundaries are an architecture-stage decision. Existing OpenMontage artifact schemas should be reused where they satisfy this contract.

## 8. V1 acceptance criteria

V1 production workflow is accepted only when a representative run can demonstrate all of the following:

- ingest a local source video **or** start from a topic brief;
- create a timestamped transcript when source speech exists;
- identify scenes/representative frames when source video exists;
- produce structured source understanding;
- generate at least 5 materially different angle candidates by default;
- state the original contribution for every candidate;
- stop at Gate 1 and honor human modification;
- verify material claims before script approval;
- produce the required narrative structure without forcing artificial wording;
- stop at Gate 2 and honor human edits;
- produce a beat-level Visual Director plan;
- avoid defaulting every beat to AI imagery;
- preserve provenance for selected external/generated assets;
- create a representative animatic/sample when practical;
- detect or flag obvious static/slideshow-style output before full render;
- produce a native short-form rough cut;
- stop at Gate 3;
- route requested revisions to the correct prior stage;
- render a technically valid final output after approval;
- preserve the run's decision trail.

## 9. Quality acceptance criteria

Technical success alone is insufficient.

A candidate rough cut must be reviewable against:

- hook clarity;
- payoff integrity;
- narrative coherence;
- original contribution;
- visual relevance;
- visual variety appropriate to the story;
- pacing;
- readability;
- narration suitability;
- audio balance;
- rights/provenance compliance;
- factual support.

Automated scores are advisory unless a separate hard rule explicitly defines a failure.

## 10. Hard constraints

- No silent progression through Gates 1–3.
- No silent runtime/provider swap that changes the approved creative plan.
- No fabricated provenance.
- No unsupported material factual claim presented as verified.
- No bypassing subject-specific copyright/rights rules.
- No requirement for paid APIs to complete the baseline workflow.
- No assumption that AI-generated imagery is superior to source/real/diagrammatic visuals.
- No automatic publication in the initial revised production milestone.
- No unnecessary rewrite of working OpenMontage functionality.

## 11. Non-goals for this milestone

This specification does not require:

- autonomous channel operation;
- automatic mass republishing;
- guaranteed virality or performance;
- multi-user SaaS;
- a new video renderer;
- a new transcription engine;
- a new scene detector;
- a new stock-media platform;
- AI generation of every visual;
- automatic TikTok/Reels publishing;
- full performance-learning automation.

## 12. Existing project behavior that remains valid

The following existing decisions remain unless contradicted by this specification:

- subject-neutral core with subject packages;
- brand configuration separated from subject configuration;
- OpenMontage as the production engine;
- project extensions layered in `montage_ext/`;
- provenance and rights metadata;
- free/open-source preference;
- deterministic assembly from structured edit decisions;
- technical QC before export;
- steelpan-specific hard copyright rules;
- real Trinidadian voice as the desired target state for the steelpan series.

Where older documents describe only two human gates, **this specification supersedes that product behavior with three creative gates**.

Where `docs/PLAN_v1.md` says "plan only — no code yet," `BUILD_STATUS.md` is the authoritative record of implementation progress.

## 13. Deferred but preserved roadmap

After the revised production workflow consistently produces acceptable videos:

1. YouTube Shorts publish handoff;
2. metrics retrieval;
3. learning store;
4. outcome-informed idea/hook feedback;
5. TikTok/Reels adapters;
6. optional additional generation providers.

These capabilities are deferred, not discarded.

## 14. Stage-3 freeze conditions

This specification becomes frozen only after explicit human approval.

Approval freezes:

- product workflow;
- three creative gates;
- required product behaviors;
- V1 acceptance criteria;
- hard constraints;
- milestone non-goals.

Approval does **not** freeze implementation details that belong to Stage 4 Architecture.

Any later change to a frozen product requirement must be recorded as a specification change rather than introduced silently during coding.

---

## Source / decision provenance

This draft is derived from the repository's existing `README.md`, `BUILD_STATUS.md`, `docs/PLAN_v1.md`, `docs/APP_IMPROVEMENTS.md`, `montage_ext/README.md`, the completed steelpan `VIDEO_BRIEF.md`, and the Stage-1/Stage-2 decisions made for the revised source-repurposing workflow.

**Model-added specification decisions requiring human approval:** default of 5 idea candidates; exact Gate action vocabulary; Visual Director preference order; proposed artifact list; precise acceptance-test wording; publication being deferred until the revised production-quality milestone passes.

These are intentionally visible rather than silently treated as settled requirements.
