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

## Next

- [ ] **1d. First render smoke** — run `framework-smoke`, then a tiny
  `documentary-montage` render, to confirm the chain end-to-end with the venv active.
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
