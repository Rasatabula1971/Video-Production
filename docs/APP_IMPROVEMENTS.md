# App improvements — from the first dry run

The dry run proved the plumbing but produced a video you'd skip. That's the
right result for a test, and the reasons are specific and fixable. Prioritised.

---

## The core problem

We shipped a **slideshow of text cards read by a synthetic American voice, with
a music bed too quiet to hear.** Every one of those is a scroll-past signal on
Shorts. None of them are pipeline bugs — they're default choices the pipeline
made that we should override.

---

## P0 — the three things that make it skippable

### 1. Voice — synthetic and wrong for the brand

Piper (`en_US-lessac-medium`) is the floor: clearly robotic, and a flat American
read on a video about Trinidadian pride is actively off-brand. The fact corpus
already says *"do not fake a Trinidadian accent with TTS — it reads as mockery."*

**Path, cheapest first:**

| Option | Cost | Quality | Notes |
|---|---|---|---|
| **Kokoro-82M** (local, Apache-2.0) | $0 | Big jump on Piper — natural prosody, runs on CPU | Not in openmontage yet; add as a `kokoro_tts` tool next to `piper_tts`. Best free-local option available. |
| **ElevenLabs free tier** | $0 (10k chars/month ≈ 8–10 shorts) | Broadcast | openmontage already has `elevenlabs_tts`. Just needs a key. |
| **Google TTS** | $0 (1M chars/month) | Good, 700+ voices | openmontage has `google_tts`. Already works. |
| **Real Trinidadian VO, recorded once, then cloned** | one session | Authentic — the actual right answer | Record a local voice reading ~40 lines, clone with Chatterbox (MIT) or XTTS-v2, reuse across the series. |

**Recommendation:** wire up **Kokoro now** for an immediate free upgrade; switch
narration provider per brand in `brands/<id>/brand.yaml`; plan the real-VO
recording as the target state.

### 2. Motion — it's a slideshow

The pipeline routed to `render_runtime: remotion` + the `explainer-data` family,
which is the text-card stack. For a punchy culture short that's the wrong engine.

- **Use HyperFrames, not the Remotion card stack**, for motion-led briefs.
  openmontage already has it (`skills/core/hyperframes.md`) — HTML/CSS/GSAP,
  built for kinetic typography and continuous camera movement. The
  proposal/decision stage should pick it whenever `delivery_promise.promise_type
  == "motion_led"`.
- **Vendor `video-shotcraft`** (Apache-2.0, 7.7k★) as an openmontage skill — 152
  Remotion shot-recipe cards + 209 motion previews. Instantly gives the pipeline
  a real motion vocabulary instead of "fade text in, hold 6s."
- **Pacing rules** in the playbook: max hold 3s on any static element, a visible
  change every 1–2s, one continuous slow camera move per scene, text animates in
  word-by-word synced to the VO.

### 3. Music — inaudible and generic

Bed was at volume 0.12 with an 8-second offset — effectively silent, and the
Pixabay result was a generic ambient track.

- Mix: bed at **0.22–0.28**, duck to ~0.10 under narration, **no long offset**,
  energy that lifts into the payoff beat.
- Use openmontage's `audio_energy` tool to pick the track's best window.
- Source: the free Pixabay catalog is thin. Add a **Freesound** key (free) for a
  wider pool; keep a small curated `music_library/` of vetted beds per brand mood.
- Constraint to bake in: **no steelpan performance music** (rights) — beds must
  complement pan content without being pan music.

---

## P1 — make the hook_scorer actually catch "I'd skip this"

The dry run's guardrail checks were run by hand and only looked at text. The
scorer's real job is to predict the skip.

- Score the **animatic**, not just the script — generate a 10–15s rough cut first,
  then judge it.
- Add a **boredom check**: static-element ratio, cuts per 10s, "is anything
  moving in the first 2 seconds", first-frame interest.
- Add a **reference-match check**: feed 2–3 steelpan/culture shorts that *do*
  work (via openmontage's `video-reference-analyst`), extract their pacing and
  structure, score ours against that energy profile.

## P2 — renderer/pipeline routing

The proposal stage locked the runtime before anyone could see it was wrong.

- `proposal-director` should choose `render_runtime` from the delivery promise
  and show the user a **10-second sample** in the chosen runtime *before* Gate 1,
  not after the full render.
- If the sample looks like a slideshow, that's a Gate-1 reject, cheaply.

## P3 — the bespoke subject visual

Every strong episode needs one hero visual. For the note-layout episode it's an
animated pan face with note positions. Build a reusable
`montage_ext/scenes/` library — parametric components (a pan diagram, a timeline,
a map) that any subject can fill. Manim for true geometry, HyperFrames/Remotion
for the motion around it.

## P4 — developer friction

- `montage_ext/` helper that emits schema-valid artifact skeletons and validates
  them (hit ~8 schema errors hand-writing JSON this run).
- Native 9:16 composition so we stop centre-cropping a 16:9 render.
- Fix the vendored caption concatenation bug with a `montage_ext` caption layer.

---

## What this looks like sequenced

1. **Brand module** (in progress) — so voice, palette, type, pacing, music mood
   are per-brand inputs, not defaults.
2. Kokoro TTS tool + ElevenLabs key → voice stops being robotic.
3. HyperFrames routing + `video-shotcraft` vendored → motion stops being a slideshow.
4. Music mix fix + Freesound key.
5. `hook_scorer` with the animatic + boredom + reference checks.
6. `montage_ext/scenes/` with the first hero component.
7. Re-run the note-layout episode. If it's still skippable, the scorer failed and
   we fix the scorer.
