# hook_scorer

**The make-or-break gate.** Runs after openmontage's `script` stage, before Gate 1.

## What it does

1. Takes the candidate hook(s) + script from openmontage.
2. Scores each against two things:
   - **Rubric scorer** — the v2.2 model: predicted stop rate, 3-second
     retention, completion, and **customer-reach fit** (framed for someone who
     could care about pan, or just general curiosity?).
   - **LLM-judge panel** — 2–3 prompts with different rubrics
     (scroll-stopper / payoff clarity / "would a Trini share this").
3. **Hard-fail checks** for steelpan (from `subjects/steelpan/fact-corpus/`):
   - headline claim stated without the word "acoustic" → fail
   - the instrument dated to the 19th century → fail
   - a contested-credit attribution stated as fact → fail
4. **Regenerate-until-bar** — up to N attempts; then surface the best N to the
   human at Gate 1 with all scores attached.

## Output

A `hook_scorecard` artifact attached to openmontage's proposal packet, so Gate 1
is "approve this hook + spend," not just "approve spend."

## Seed material

- openmontage `skills/creative/short-form.md`, `skills/creative/storytelling.md`
- the v2.2 hook-type / hook-copy taxonomy (doc §13–14)
