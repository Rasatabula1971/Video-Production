# brand_intake

A **conversation**, not a UI. Walks a person through building a brand kit and
writes `brands/<id>/`. Modelled on openmontage's `skills/meta/onboarding.md`
and `creative-intake.md`.

## Principle (from the Brand Building Kit)

> Do not begin with the logo, colours, or fonts. Visual identity is the
> expression of the brand strategy. Define audience, positioning, personality
> and message first. Then choose visual elements that reinforce them.

So the intake runs in that order and will not let the visual questions start
until the foundation and messaging are answered.

## The flow (14 steps → `brand.yaml` sections)

| # | Step | Writes to |
|---|---|---|
| 1 | What the business does, in one sentence | `foundation.what_we_do` |
| 2 | Who the customer is; who it is *not* | `foundation.target_customer`, `audience` |
| 3 | The customer problem; positioning vs alternatives | `foundation.customer_problem`, `foundation.positioning` |
| 4 | Brand promise; 3–5 core values; personality words; desired perception | `foundation.*` |
| 5 | One-line / 30-second / full description; value proposition | `messaging.*` |
| 6 | 3–5 key messages; pain points; reasons to believe (proof points); CTAs | `messaging.*` |
| 7 | Tone of voice; words to use; words to avoid; per-context tone | `voice.*` |
| 8 | Hard-fail rules — statements a script must never make | `voice.hard_fail_rules` |
| 9 | Colour system: ink, paper, accent(s), positive/negative, usage rules | `visual.palette` |
| 10 | Typography: display, body, caps rules, licensing | `visual.typography` |
| 11 | Motion vocabulary + pacing rules + runtime preference | `visual.motion` |
| 12 | Imagery style; **what must never appear** | `visual.imagery_style`, `visual.must_never_appear` |
| 13 | Content pillars (3–5); caption structure; CTA rules; hashtag strategy; cadence | `content_strategy.*` |
| 14 | Platforms and their roles; AI-content policy; human-review gate; measurement | `platforms`, `ai_content_policy`, `measurement` |

At the end: write `brand.yaml` (status `draft`), `voice.md`, `visual-identity.md`;
validate against `brands/_schema/brand.schema.json`; show the person a summary and
set status `approved` on their confirmation.

## Shortcuts

- **Import an existing kit** (PDF / Figma / guidelines): parse what's there,
  pre-fill the answers, only ask about gaps. (Second-phase feature.)
- **Generate a theme**: if the brand has no palette/type, offer `theme-factory`
  or openmontage's `lib/playbook_generator.py` to propose a coherent set, then
  confirm.

## Subject-neutral

Holds no brand facts. It is the same conversation for any brand.
