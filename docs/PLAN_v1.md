# Video-Production — Build Plan v1 (CIP-revised)

**Status:** plan only — no code yet.
**Supersedes the build strategy of** `video-production-repo-scaffold.zip` (the from-scratch, station-by-station scaffold). The v3.0 / v2.2 specs in `D:\video producer` remain the source of truth for *what the system must do*; this document changes *how we build it*.

---

## 1. The decision

**Adopt an existing agentic video engine. Build only the connective tissue and the two things it doesn't do.**

The from-scratch scaffold had ~15 stations marked "not started." A registry search (CIP, ~448 components) found that the hardest stations — an agentic research→script→scene→asset→edit→compose→publish loop with checkpoints, cost governance, artifact schemas, and asset provenance — already exist, maintained, Claude-Code-native, and runnable on a fully free/local stack.

### Adopt: `calesthio/openmontage`

- 56.6k★, **AGPL-3.0** (free + open — acceptable per project decision).
- Architecture is a near-match to the v3.0 spec:

  | v3.0 spec concept | openmontage equivalent |
  |---|---|
  | Laptop control plane, outsourced media, replaceable adapters | executive-producer orchestration + provider registry (15+ providers, all swappable) |
  | Gate 1 — approve before spend | `proposal` stage: itemized cost estimate + `human_approval_default: true` before any asset is generated |
  | Gate 2 — approve before publish | `compose` / `publish` checkpoints |
  | Evidence before script, claim ledger | `research` stage: ≥5 sources with URLs, ≥3 grounded angles, specific sourced data points |
  | Decision records | `decision_log` artifact per run |
  | QC gates | `meta/reviewer` skill + per-stage `success_criteria` + ffprobe validation |
  | Asset provenance & rights | provenance (provider, original_url, license) required on every asset |
  | Deterministic assembly | schema-valid `edit_decisions` → `compose`; "silent runtime swap = CRITICAL governance violation" |
  | Platform derivatives | `target_platform` canvas per pipeline |
  | Cost governor | `tools/cost_tracker.py`, per-pipeline `budget_default_usd` |

- **Free / local path is first-class:** Pexels + Pixabay (stock, $0), **Piper local TTS** ($0, offline, no key), Google TTS (1M chars/mo free), `whisperx` caption sync (local, is a bundled core skill), Remotion, Manim (`creative/manim-usage.md`), plus `creative/storytelling.md`, `creative/short-form.md`, `creative/typography.md`, `creative/data-visualization.md`.
- **`documentary-montage` pipeline** retrieves real footage from Pexels / Archive.org (Prelinger) / NASA / Wikimedia Commons / Unsplash with CLIP retrieval — exactly the copyright-safe sourcing steelpan history needs.
- Reference example **"How Salt Made History"** (100-second cinematic history doc: narration + hand-authored motion graphics for etched title, etymology reveal, animated maps, historical timeline, closing thesis) is the target format for Series 1.

### Not adopted (but useful reference)

- `s1dashu/director` (MIT) — 3 modes: Animated Explainer / Storytime / Cinematic Drama. openmontage is a superset; keep as a storytelling-flow reference.
- `vincentwei1021/video-talkcraft` — **PolyForm Noncommercial license → cannot be used commercially.** Its Apache-2.0 sibling `video-shotcraft` (Remotion shot-recipe cards) is fine if we want it later.

---

## 2. What we build (the glue + the two gaps)

openmontage covers roughly 80% of the v3.0 wants. Four things it does **not** do well enough — these are the entire build scope for v1:

### 2.1 Steelpan Subject Package + house rules  *(config, not much code)*

A profile + playbook layer that every run reads:

- **Brand:** palette, typography, motion vocabulary, end-tag line, logo/close.
- **Hard copyright rules (enforced, not advisory):**
  - no archival photographs of Spree Simon, Ellie Mannette, Anthony Williams, TASPO 1951, etc.
  - no AI-generated depictions of real historical figures or historical pans (Pipeline v1.0 §2.3).
  - allowed sources only: original diagrams/animation, motion graphics, text-on-screen, CC0 / public-domain stills (Ken Burns), platform-licensed audio, our own filmed pan footage (later).
- **Audience & measurement targets** from v2.2: Trinidad + diaspora + music-curious; the pillars `culture_history`, `education`, `craftsmanship`, `surprising_fact`; hold ~1 in 5 as `craftsmanship` to keep a "making things" signal.
- **Fact base:** the verified timeline, the pioneers, the note-layout and music sections from `Steelpan_Artistry_Series_1_Pan_The_Story.docx`, loaded as a local corpus so the research stage cites *our* vetted facts first.

Implemented as: a `subjects/steelpan/` folder (profile.yaml + playbook + fact corpus) that maps onto openmontage's `meta/creative-intake` and `research-director`.

### 2.2 Hook & script scoring loop  *(the make-or-break piece)*

openmontage's `script-director` produces a competent arc (hook → setup → build → climax → landing) but generically. The user's judgement — *the hook and script make or break the video* — gets its own gate:

- After `script` stage, run each candidate hook + script through:
  1. a **rubric scorer** against the v2.2 model — predicted stop rate, 3-second retention, completion, and **customer-reach fit** (is this framed for someone who could own a pan, or just for general curiosity?);
  2. an **LLM-judge** panel (2–3 prompts, different rubrics: scroll-stopper, payoff clarity, "would a Trini share this");
  3. **regenerate-until-clears-bar** — up to N attempts, then surface the best-N to the human at Gate 1 with scores attached.
- Seed the hook library from openmontage's `creative/short-form.md` + `creative/storytelling.md` and the v2.2 hook-type / hook-copy taxonomy.
- Output: a `hook_scorecard` artifact attached to the proposal packet, so Gate 1 is "approve this hook + spend," not just "approve spend."

### 2.3 YouTube Shorts publish + metrics + learning loop  *(the v2.2 measurement loop openmontage lacks)*

openmontage's `publish` stage only writes an export bundle. Build:

- **Publish handoff:** export bundle → YouTube Data API v3 upload (free), Shorts metadata (title, description, hashtags, chapters), scheduled or manual.
- **Metrics retrieval:** scheduled pulls (YouTube Analytics API, free) — impressions, swipe-away / stop rate proxy, average view %, completion, shares, followers gained, non-subscriber reach. A failed pull is recorded as `METRICS_MISSING`, never a silent blank (v3.0 invariant).
- **Learning store:** each published item's `hook_type`, `structure`, `pillar`, `duration` → outcome. Feeds the next run's decision engine (which hooks/structures actually reach the target audience).
- TikTok + Rels adapters added after Shorts works — same interface.

### 2.4 Thin decision / event ledger  *(traceability)*

openmontage keeps a `decision_log` per run; the v3.0 spec wants an append-only event ledger across runs (DOC-02 / DOC-08 rigour). Build a lightweight SQLite ledger that records: run id, subject, every checkpoint decision, cost, provider calls, publish + metric events. Not a full state machine — just a durable, append-only record.

---

## 3. The free stack for Series 1 (steelpan history)

Series 1 is motion-graphics-led and needs **zero paid API calls and no local GPU**:

| Need | Tool | Cost |
|---|---|---|
| Research (cite our fact corpus first, then web) | openmontage `research-director` + local fact corpus; `local-deep-research` if we want offline web | $0 |
| Script + hook | openmontage `script-director` + our scoring loop (§2.2) | $0 (LLM tokens only) |
| Narration (VO) | **Piper** (local, offline) or Google TTS free tier | $0 |
| Caption timing | **whisperx** (local; laptop CPU may be slow → optional cloud GPU @ $0.30–0.60/hr) | ~$0 |
| Motion graphics: title, timeline, maps, quotes | **Remotion** (bundled) | $0 |
| Animated diagrams: note layout, cycle of 4ths/5ths, pan families | **Manim** (`creative/manim-usage.md`) | $0 |
| Stills (Ken Burns) — CC0 / public-domain only | Pexels / Pixabay / Wikimedia / Archive.org | $0 |
| Music | Pixabay / platform-licensed library | $0 |
| Assemble + render | FFmpeg / `pyav` (bundled) | $0 |
| Publish + metrics | YouTube Data + Analytics APIs | $0 |

No text-to-video model is used for Series 1. That capability (and its provider adapters) is deferred until a later series needs it.

---

## 4. What we keep from the old scaffold

- The **specs** (`docs/…v3_0`, `v2_2`, `DOC-14` correction log) as the governance reference.
- `contracts.py` **concepts** — where openmontage's artifact schemas are looser than a v3.0 invariant, tighten via our validation layer rather than forking openmontage.
- `timing.py` — only if openmontage's timing proves weaker in practice; otherwise drop it.

Everything else in the scaffold (`state/`, `persistence/`, `intake/`, `research/`, `decision/`, `compiler/`, `broker/`, `adapters/`, `qc/`, `assembly/`, `publish/` as empty stubs) is **not built** — openmontage is those stations.

---

## 5. Build sequence

1. **Vendor openmontage** into the repo (git subtree or submodule; AGPL note in `NOTICE`). Get its free-path smoke test green (`framework-smoke.yaml`).
2. **`subjects/steelpan/`** — profile, playbook, copyright rules, fact corpus (§2.1).
3. **Dry-run `documentary-montage` / `animated-explainer`** on one steelpan history topic end-to-end, free stack only, no publish. Confirm the format and the copyright guardrails hold.
4. **Hook & script scoring loop** (§2.2) — the highest-value custom work.
5. **Decision / event ledger** (§2.4).
6. **YouTube Shorts publish handoff** (§2.3 part 1).
7. **Metrics retrieval + learning store** (§2.3 parts 2–3).
8. Produce Series 1, episode 1. Review against v2.2 scorecard.
9. TikTok + Reels adapters.

Gate 1 and Gate 2 (human approval) are live from step 3 onward.

---

## 6. Open items

- Confirm whether to vendor openmontage as **submodule** (easy upstream pulls) or **subtree** (self-contained repo). Recommendation: subtree — this is a product, not a fork we'll upstream.
- AGPL-3.0 obligation: if the control plane is ever offered as a network service, the whole thing must be offered as source. Fine for now (personal/internal), flag before any SaaS.
- Whisperx speed on the laptop — benchmark before committing to cloud GPU.
- The `mcp__cip__*` MCP tools need a Claude session reload to load; the `cip-composer` CLI works now.


---

## 7. v2.2 demand-validation amendment (2026-09-25)

The original plan began at subject research and production. The system now adds a pre-production intelligence layer described in `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md`.

### New upstream sequence

```text
market -> seed topics -> depth-first evidence collection
-> winners + failures -> demand clusters
-> audience awareness -> topic x format decomposition
-> opportunity record -> title/thumbnail package
-> Gate 0 -> existing OpenMontage pipeline
```

### New build scope

5. **`montage_ext/discovery/`** — evidence contracts, deterministic outlier calculations, winner/failure pairing, demand clustering, opportunity records, packaging records and Gate 0 decision packet.
6. **`montage_ext/learning/`** — join opportunity/package/content hypotheses to measured post-publication outcomes.

These are extensions to the original four custom modules, not replacements.

### Gate compatibility

The original two gates retain their meaning:

- Gate 1: approve before production spend.
- Gate 2: approve before publish.

v2.2 adds Gate 0 before both: *should this opportunity enter the production pipeline at all?*

### Implementation order amendment

Before Series 1 scales beyond dry runs:

1. keep the proven free render chain intact;
2. implement Discovery Engine contracts and deterministic calculations;
3. generate a human-readable Gate 0 decision packet;
4. continue hook/script scorer work;
5. complete ledger + YouTube metrics;
6. join measured outcomes in the Learning Engine;
7. only then add more autonomous discovery/scoring behavior.

Do not build a second production engine or modify vendored OpenMontage to implement this layer.
