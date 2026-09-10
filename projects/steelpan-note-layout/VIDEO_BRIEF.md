# Video brief — "Why Is There a Spider Web on a Steelpan?"

| | |
|---|---|
| **Series** | Steelpan Artistry, Series 1 — *Pan: The Story* |
| **Subject / Brand** | Steelpan history · The Chrome Factory (culture-first) |
| **Topic** | The tenor-pan note layout — the cycle of fourths and fifths |
| **Platform** | YouTube Shorts (9:16, 1080×1920, 30 fps) — then TikTok / Reels |
| **Duration** | ~29 s (narration 27.5 s + 1.5 s end tag) |
| **Pillar** | `surprising_fact` / `education` |
| **Cost** | $0 — Kokoro voice, FLUX atmosphere images (keyless), Pixabay music, Remotion + FFmpeg, all local |
| **Status** | v7 rendered — `renders/note-layout_v7.mp4`. Draft. Not published. |
| **Current build** | `montage_ext/remotion/` (composition `NoteLayoutShort`) |

---

## 1. Script (narration — verbatim, with timing)

Voice: Kokoro `bm_george` (British male, documentary tone) at 0.92 speed — **placeholder** for a real Trinidadian voice.

| Time | Line | Delivery |
|---|---|---|
| 0.0 – 2.0 | This pattern on a steel pan looks random. | Sly. Full stop and a beat after "random." |
| 2.0 – 3.1 | It's the opposite. | Flat, certain. |
| 3.1 – 5.5 | Every note is on the same sheet of metal. | Matter-of-fact. |
| 5.5 – 9.4 | Put two clashing notes side by side, and the whole pan buzzes. | Beat before "and the whole pan buzzes." |
| 9.4 – 11.0 | The layout fixes that. | Brisk. |
| 11.0 – 13.2 | Clashing notes go to opposite sides. | |
| 13.2 – 14.9 | Friendly notes stay close. | |
| 14.9 – 15.9 | That's the trick. | Small pause before. |
| 15.9 – 18.8 | It's why a steel pan sings instead of rattling. | Small lift on "sings." Let it land. |
| 18.8 – 23.7 | A Trinidadian tuner named Anthony Williams worked it out in 1953. | Warm, proud. |
| 23.7 – 27.5 | Every lead pan in the world is still built from his map. | Unhurried. Down on "his map." |

**Word count:** 81. **On-screen captions:** word-by-word, karaoke highlight, burned in, lower third (safe of the Shorts UI).

---

## 2. Scene-by-scene

Full-frame photographic **bed** runs the whole video: a real hand-hammered metal disc, darkened, with a slow push-in + drift. The **pan diagram** (accurate cycle-of-fourths-and-fifths ring of 12 note dots + radial "web" grooves + concentric arcs) is composited semi-transparent over the bed so the metal reads through. One continuous slow zoom on the whole frame.

| # | Time | Headline (top) | Pan diagram state | Cutaway / effect | Caption |
|---|---|---|---|---|---|
| **1 — Hook** | 0.0 – 3.7 | **IT LOOKS RANDOM.** / *it's the opposite* | (hidden — fades in at ~1.6–2.7 s) | **Sparks** fill the frame 0.0–1.7 s (hammer-on-steel), then clear | "This pattern on a steel pan looks random. It's the opposite." |
| **2 — Setup** | 3.7 – 10.0 | **ONE SHEET OF METAL.** / *clashing notes buzz* | Web + arcs + 12 white dots resolve by ~2.4 s. At ~6 s two adjacent dots (top) flare **red** and rattle. | **Rippling-steel** insert ~7.4–8.9 s | "Every note is on the same sheet of metal. Put two clashing notes side by side, and the whole pan buzzes." |
| **3 — Build** | 10.0 – 15.7 | **THE LAYOUT FIXES IT.** / *apart · together* | The red dots travel to **opposite sides** of the ring and go calm white; the home dot at the destination fades as the traveller arrives. Two other dots (lower-right) glow **warm orange** and nudge together. | — | "The layout fixes that. Clashing notes go to opposite sides. Friendly notes stay close." |
| **4 — Payoff** | 15.7 – 20.2 | **IT SINGS.** / *instead of rattling* | Whole pan **pulses warm** once (gold rim flash, ~16–17.5 s); the orange pair settles to a low glow. | **Molten-metal** insert ~19.6–21.2 s | "That's the trick. It's why a steel pan sings instead of rattling." |
| **5 — Landing** | 20.2 – 27.5 | **ANTHONY WILLIAMS · 1953** / *still built from his map* | Calm ring, dots at rest. | *(planned, not yet built: web pattern multiplies small across a faint world map)* | "A Trinidadian tuner named Anthony Williams worked it out in 1953. Every lead pan in the world is still built from his map." |
| **End tag** | 27.5 – 29.0 | — | Fades. | Lower-third type: **PAN. MADE IN TRINIDAD.** | — |

**Colour language:** off-white dots = notes · **red** = clashing (dissonant) · **warm orange** = friendly (harmonically related) · gold = the "it works" pulse.
**Motion rules:** nothing static > 3 s; one slow camera move per scene; text animates in word-by-word with the voice.

---

## 3. Audio

| Layer | Source | Level |
|---|---|---|
| Narration | Kokoro `bm_george` 0.92× (`assets/audio/kokoro_bm_george_v3.wav`) | full |
| Music bed | Pixabay "Warm" — The_Mountain (`assets/audio/music_bed.mp3`), free licence, no attribution required | 0.24, lifting to 0.34 across the payoff (~18–28 s), 1 s fade-in / 2.5 s fade-out |
| SFX | none (the spark/molten cutaways are silent visuals) | — |

**No steelpan performance audio** — rights. Music bed only.

---

## 4. Assets

| Asset | File | Origin |
|---|---|---|
| Metal-disc bed | `assets/images/v6_bg_disc.jpg` → `montage_ext/remotion/public/bed.jpg` | FLUX via Pollinations (keyless), prompt "hand-hammered metal disc, spider-web grooves" |
| Spark cutaway | `v6_broll_hammer.jpg` → `broll_spark.jpg` | FLUX, "hammer striking curved steel, orange sparks" |
| Ripple cutaway | `v6_broll_ripple.jpg` → `broll_ripple.jpg` | FLUX, "thin sheet of steel vibrating" |
| Molten cutaway | `v6_broll_molten.jpg` → `broll_molten.jpg` | FLUX, "glowing molten metal surface" |
| Pan diagram | `montage_ext/remotion/src/SpiderWebPan.tsx` | Bespoke SVG — accurate 4ths-and-5ths ring |

All AI images are **non-figurative atmosphere/texture only** — no people, no claimed-historical or "accurate" pan. Compliant with `subjects/steelpan/copyright-rules.md`.

---

## 5. Facts & rights notes

- **"Anthony Williams … 1953"** — from Wikipedia and steelpan-layout histories. The vetted Series 1 fact base names Williams but does not commit to a year. **Confirm 1953 with a pan source before publishing, or soften to "the early 1950s."**
- Williams is credited here with the **fourths-and-fifths "spider web" layout** — well established. The video does **not** touch the contested credit for who first used the 55-gallon oil drum.
- No archival photographs. No depiction of Williams. No performance footage.

---

## 6. Publish metadata (draft — for when it ships)

- **Title:** Why is there a spider web on a steelpan?
- **Description:**
  > That "spider web" pattern on a steel pan isn't decoration — it's a map. Every note sits on the same sheet of metal, so clashing notes are pushed to opposite sides and harmonically friendly notes sit close. It's why a pan rings clean instead of rattling. Trinidadian tuner Anthony Williams worked out the fourths-and-fifths layout, and it's still the standard on lead pans worldwide.
  >
  > Music: "Warm" by The_Mountain (Pixabay).
  > Diagram is an original illustration. No archival images used.
- **Hashtags:** #steelpan #steeldrum #trinidad #panorama #musictheory #trinidadandtobago #caribbean #howitsmade
- **Chapters (if long enough):** 0:00 It looks random · 0:04 One sheet of metal · 0:10 The layout · 0:16 Why it sings · 0:20 Anthony Williams
- **Thumbnail concept:** the pan diagram mid-"clash" (two red dots) over the metal bed, headline "IT'S NOT RANDOM."

---

## 7. Known gaps before this is publishable

1. Voice is a placeholder — record a real Trinidadian VO and clone it.
2. Bed image reads a bit "dark tunnel" — swap for a better hammered-metal texture, or (best) a real overhead photo of a pan with the diagram traced onto it.
3. Landing scene's "web multiplies across a world map" is scripted but not built.
4. Confirm the 1953 date.
5. Bolder web grooves; close the residual gap between headline and pan.
