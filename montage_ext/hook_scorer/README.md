# hook_scorer

**The make-or-break gate.** Runs after openmontage's `script` stage, before Gate 1.

## What it does

1. Takes the candidate hook(s) + script from openmontage.
2. Scores each against two things:
   - **Rubric scorer** — the v2.2 model: predicted stop rate, 3-second
     retention, completion, and **customer-reach fit** (framed for someone with
     a real pathway to the subject, or just general curiosity?).
   - **LLM-judge panel** — 2–3 prompts with different rubrics
     (scroll-stopper / payoff clarity / "would the target audience share this").
3. **Hard-fail checks** — subject-driven. The check *mechanism* is generic;
   the rules come from the active subject package
   (`subjects/<id>/copyright-rules.md` + `fact-corpus/`), never hard-coded here.
   Worked example, steelpan: headline claim stated without the word "acoustic"
   → fail; instrument dated to the 19th century → fail; a contested-credit
   attribution stated as fact → fail.
4. **Regenerate-until-bar** — up to N attempts; then surface the best N to the
   human at Gate 1 with all scores attached.

## Output

A `hook_scorecard` artifact attached to openmontage's proposal packet, so Gate 1
is "approve this hook + spend," not just "approve spend."

## Seed material

- openmontage `skills/creative/short-form.md`, `skills/creative/storytelling.md`
- the v2.2 hook-type / hook-copy taxonomy (doc §13–14)

## Subject-neutral

Steelpan is subject #1, not the only subject. This module holds no subject
facts. All subject-specific scoring weights, audience definitions, and hard-fail
rules are read from `subjects/<active>/`. Adding a subject never touches this code.
