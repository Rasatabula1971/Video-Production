# brands/

One folder per brand. **A brand is the stable container; the subject varies.**
One brand → many subjects → many videos. A production run = brand × subject × topic.

Multi-brand by design — this system can run for more than one business.

## Adding a brand

Run the brand-intake conversation (`montage_ext/brand_intake/`). It walks the
14-step build sequence from the Brand Building Kit and writes:

```
brands/<id>/
  brand.yaml          foundation, messaging, colour, typography, motion,
                      content strategy, platform roles, AI-content policy
  voice.md            words to use / avoid, tone rules per context, the
                      hard-fail list the hook_scorer enforces
  visual-identity.md  photography/video style, grading, shapes, motion
                      vocabulary, "what must never appear"
  logo/               logo files (optional at first)
  templates/          reel cover, thumbnail, intro/outro (optional at first)
```

Validate `brand.yaml` against `brands/_schema/brand.schema.json`.

## Scope

The video system **consumes** a brand kit. It does not design a logo suite —
that's a design job. It may generate a *theme* (colour + type + motion tokens)
via `theme-factory` or openmontage's playbook generator when a brand has none.

## How the pipeline reads a brand

| Stage | Reads from the brand |
|---|---|
| creative-intake / research | positioning, audience, pillars, proof points |
| script | messaging, voice.md (words to use/avoid, tone) |
| hook_scorer | voice.md hard-fail list + brand-fit weighting |
| scene / compose | visual-identity.md → Remotion/HyperFrames theme + motion vocab |
| publish | content strategy → caption structure, CTA rules, hashtag strategy, required attributions |

## Current brands

- `the-chrome-factory/` — **pending intake.** Trinidad steelpan chrome-plating
  shop. Launching culture-first (steelpan history) before selling.
