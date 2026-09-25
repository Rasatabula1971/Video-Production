# Build status

Plan: `docs/PLAN_v1.md`. Sequence is that document's §5.

## Done

- [x] **1a. Vendor openmontage** — `vendor/openmontage/` at upstream commit
  `08e2151` (2026-09-05). AGPL noted in `NOTICE` and `vendor/VENDORED.md`.
  Three example media files removed; no code changes.
- [x] **2. Steelpan Subject Package** — `subjects/steelpan/`:
  - `profile.yaml` — brand, audience, platform (YouTube Shorts first), pillars, cadence, measurement.
  - `copyright-rules.md` — the hard rules (no archival figure photos, no AI depictions of real pioneers, provenance required).
  - `fact-corpus/` — headline claim, verified timeline, pioneers + contested-credit rule, note layout, music rights. Transcribed from the Series 1 doc.
- [x] Repo skeleton — `README.md`, `.gitignore`, `.python-version`, `montage_ext/` module stubs.

- [x] **1b. Environment** —
  - `.venv` + openmontage core requirements, imports green.
  - FFmpeg 9.0.1 installed via `winget install Gyan.FFmpeg` (adds `ffmpeg`/`ffprobe`
    aliases; new shells pick it up on PATH).
  - `remotion-composer` npm install — 199 packages.
  - `pip install piper-tts faster-whisper manim` — all green.
  - `vendor/openmontage/.env` created from `.env.example` (all keys blank = free mode).
- [x] **1c. Capability check** — openmontage tool registry: **46 of 121 tools
  available** with the free stack (up from 24 pre-FFmpeg). Includes the full
  render + caption + QC chain: `video_compose`, `remotion_caption_burn`,
  `transcriber`, `scene_detect`, `silence_cutter`, `audio_mixer`, `color_grade`,
  `auto_reframe`, `visual_qa`, `frame_sampler`, `subtitle_gen`, `diagram_gen`,
  `google_tts`, `pixabay_music`, `export_bundle`.
  Remaining 74 are paid providers (FAL/Kling/MiniMax/etc.) and local-GPU tools
  (torch/transformers) — not needed for Series 1.

- [x] **1d. Render smoke test** — `python render_demo.py world-in-numbers`
  produced a valid MP4: H.264 1920×1080 @ 30fps, AAC, 23s, 4.3 MB, exit 0.
  Title cards + animated bar charts render clean. This is the same Remotion
  component stack Series 1 will use for timelines, stat reveals, and comparison
  charts. **The free render chain is proven end-to-end.**
  (Remotion's first run pulls a headless Chromium + bundles — ~5 min once;
  subsequent renders are fast.)

- [x] **3. First steelpan dry run** — `projects/steelpan-note-layout/`.
  Topic "Why is there a spider web on a steelpan?" through `animated-explainer`,
  free stack, no publish. All artifacts schema-valid (research_brief → proposal
  → script → scene_plan → asset_manifest → edit_decisions → render_report).
  Gate 1 was a real decision point (user picked C2, redirected it). Guardrails
  held. Rendered end to end: Remotion → H.264 1080p + AAC, ~36.6s, $0.
  See `projects/steelpan-note-layout/DRY_RUN_NOTES.md` for the 6 build items
  it surfaced (biggest: a bespoke steelpan-diagram component; native 9:16
  composition; the `hook_scorer` module; a vendored caption bug to work around).

## Next

- [ ] **Brand module** — `brands/` sibling to `subjects/`, multi-brand,
  conversational brand-intake skill. Author `brands/the-chrome-factory/`.
- [ ] **4. `montage_ext/hook_scorer/`** — automate the guardrail + scoring loop.
- [ ] A `SpiderWebPan` (or general subject-diagram) Remotion/Manim component.
- [ ] Native 9:16 Explainer composition (stop centre-cropping).
- [ ] **3. Free end-to-end dry run** — one steelpan-history topic through
  `documentary-montage` or `animated-explainer`, free stack only, no publish.
  Confirm format + copyright guardrails hold.
- [ ] **4. `montage_ext/hook_scorer/`** — the make-or-break loop.
- [ ] **5. `montage_ext/ledger/`** — append-only run record.
- [ ] **6. `montage_ext/publishers/youtube_shorts/`** — publish handoff.
- [ ] **7. Metrics retrieval + learning store.**
- [ ] **8. Series 1, episode 1.**
- [ ] **9. TikTok + Reels adapters.**

## Environment prerequisites (this machine)

| Tool | Needed | Status |
|---|---|---|
| Python 3.10+ | yes | ✅ 3.13.9 |
| Node.js 18+ | yes | ✅ v24.10 |
| npm | yes | ✅ 11.14 |
| FFmpeg | yes (render, ffprobe QC) | ✅ 9.0.1 (winget Gyan.FFmpeg) |
| Git | yes | ✅ |
| GPU | no (optional, for faster Whisper/local video-gen) | none |


## v2.2 demand-validation update

- [x] Added `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md`.
- [x] Added `montage_ext/discovery/` contract and `opportunity.schema.json`.
- [x] Added `montage_ext/learning/` contract.
- [x] Added Gate 0 architecture while preserving Gate 1 (approve before spend) and Gate 2 (approve before publish).
- [x] Updated repo README and `montage_ext/README.md` to make the repo self-describing.

### Next implementation slice

- [ ] Discovery observation schema for normalized video/channel evidence.
- [ ] Deterministic outlier calculator with tests and null-safe baseline handling.
- [ ] Winner/failure comparison record.
- [ ] Gate 0 decision-packet generator.
- [ ] Connect approved opportunity id into the existing OpenMontage run/ledger.
- [ ] Join YouTube metrics back to opportunity/package records in `montage_ext/learning/`.
