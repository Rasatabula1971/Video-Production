# Dry run — findings

First end-to-end pass of the pipeline. Topic: "Why is there a spider web on a
steelpan?" (the note layout). Free stack, no publish.

## What the pipeline proved

| Stage | Tool | Result |
|---|---|---|
| Research | WebSearch + fact corpus | Schema-valid `research_brief.json` — 4 sourced data points, 3 angles, 6 sources. Content gap confirmed (no short-form owns this). |
| Gate 1 | human | Worked as a real decision point — user picked C2 and redirected it (less technical, mass appeal). Recorded as `approved_with_changes`. |
| Script | (agent) | Schema-valid `script.json`, ~35s, 99 words. |
| Guardrails | `subjects/steelpan/copyright-rules.md` + fact corpus | All hard-fail checks applied and pass: no archival photos, no AI depiction of Williams, no contested-credit claim stated as fact, not dated to the 19th century, no pan-performance audio. One review flag raised (the 1953 date is secondary-sourced). |
| Assets | `piper_tts` | Local narration, $0, 34.9s. Clear and intelligible. |
| Assets | `pixabay_music` | "Warm" by The_Mountain, free Pixabay licence, provenance recorded. |
| Assets | `faster_whisper` (small, CPU) | Word-level captions, 99 words. **Ran fine on the laptop — no cloud GPU needed for captioning.** |
| Compose | Remotion (`Explainer`) | Valid MP4: H.264 1920x1080 + AAC stereo, ~36.6s. |
| Reframe | ffmpeg cover-crop | 1080x1920 (9:16) version produced for Shorts. |
| QA | ffprobe + frame sampling | Duration, codecs, resolution all verified. |

**The free chain works end to end: topic in -> schema-valid decision trail + narrated, captioned, scored, rendered MP4 out, $0, no GPU.**

## What needs building before a real episode

1. **A steelpan-diagram Remotion component.** The stock component set (hero title,
   callout, comparison card, text cards, charts) has nothing that draws a pan
   face or animates note positions. The concept's spider-web reveal needs a
   bespoke `SpiderWebPan` component (React/Remotion or a Manim clip). This is
   the single biggest gap and belongs in a project scene library.
2. **Native 9:16 composition.** `Explainer` renders 1920x1080; we currently
   center-crop to vertical, which wastes resolution and risks clipping wide
   content. Needs a portrait Explainer variant or a `video_compose` profile path.
3. **Theme = brand.** First render used a default theme (wrong colours). Wire the
   Remotion `theme` to the brand kit (`brands/<id>/`) once that module exists.
4. **hook_scorer module.** Guardrail checks were applied by hand this run. The
   `montage_ext/hook_scorer/` scoring loop should run them automatically and
   attach a `hook_scorecard` to Gate 1.
5. **Caption polish.** Word spacing needed a manual fix; caption style (font,
   size, position, safe-area for the Shorts UI) should come from the brand kit.
6. **Artifact authoring is fiddly.** Hand-writing schema-valid JSON for each
   stage took several correction passes. A thin helper in `montage_ext/` that
   emits valid skeletons would speed this up.

## Cost

$0.00. Piper (local), Pixabay (free), faster-whisper (local), Remotion (local),
FFmpeg (local). No API calls.
