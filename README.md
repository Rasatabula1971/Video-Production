# Video-Production

Subject-neutral short-form video production control plane. Topic in → published
short video + performance metrics out, with two human decision points
(Gate 1: approve before spend, Gate 2: approve before publish) and no recurring
manual work in between.

**First subject:** the history of the Trinidad steelpan — its pioneers and how
the instrument evolved. Culture-first launch for YouTube Shorts.

## How this repo is put together

| Path | What it is |
|---|---|
| `docs/PLAN_v1.md` | The build plan. Read this first. |
| `vendor/openmontage/` | Vendored copy of [calesthio/openmontage](https://github.com/calesthio/openmontage) (AGPL-3.0) — the production engine we adopt. See `vendor/VENDORED.md`. |
| `subjects/steelpan/` | The steelpan Subject Package: brand, audience, hard copyright rules, and the vetted fact corpus the research stage cites first. |
| `montage_ext/` | The code we build *on top of* openmontage — the four things it doesn't do (see `docs/PLAN_v1.md` §2). |
| `BUILD_STATUS.md` | What is done, what is next. |

## Governing specs (not in this repo)

Live in `D:\video producer`:
- `Subject_Driven_Video_Intelligence_Production_Orchestration_System_v3_0.docx` — architecture, invariants.
- `Steelpan_Artistry_Short_Form_Video_System_v2_2.docx` — the measurement loop.
- `Steelpan_Artistry_Series_1_Pan_The_Story.docx` — Series 1 content.

## Licensing

This project vendors AGPL-3.0 code (`vendor/openmontage/`). See `NOTICE`.
Free / open-source components are preferred throughout; paid services are a
fallback only where a free or local tool cannot do the job.
