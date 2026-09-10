"""Build src/props/note-layout.json from a Kokoro narration's word timings.

Usage: python build_props.py <voice_key>   e.g. bm_george  |  am_michael
Reads projects/steelpan-note-layout/assets/captions_kokoro_<voice>_full.json,
stages the voice wav into public/voice.wav, writes the props file.
"""
import json, io, sys, shutil, os

VOICE = sys.argv[1] if len(sys.argv) > 1 else "bm_george_v2"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJ = os.path.join(ROOT, "projects", "steelpan-note-layout")
HERE = os.path.dirname(os.path.abspath(__file__))

_capname = f"captions_kokoro_{VOICE}.json"
if not os.path.exists(os.path.join(PROJ, "assets", _capname)):
    _capname = f"captions_kokoro_{VOICE}_full.json"
caps = json.load(io.open(os.path.join(PROJ, "assets", _capname), encoding="utf-8"))


def fix_caption_tokens(words):
    """Whisper mishears Kokoro's 'steelpan' as 'steel pen' / 'lead pen'.
    Merge those pairs back using the combined timing. Strip stray punctuation
    that reads oddly one-word-at-a-time."""
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        nxt = words[i + 1] if i + 1 < len(words) else None
        a = w["word"].lower().strip(".,")
        b = nxt["word"].lower().strip(".,") if nxt else ""
        if a == "steel" and b == "pen":
            out.append({"word": "steelpan" + nxt["word"][len(b):], "startMs": w["startMs"], "endMs": nxt["endMs"]})
            i += 2
            continue
        if a == "lead" and b == "pen":
            out.append(w)
            out.append({"word": "pan" + nxt["word"][len(b):], "startMs": nxt["startMs"], "endMs": nxt["endMs"]})
            i += 2
            continue
        out.append(w)
        i += 1
    return out


caps = fix_caption_tokens(caps)
last = caps[-1]["endMs"] / 1000.0
dur = round(last + 1.4, 2)  # small tail for the end tag

shutil.copy(os.path.join(PROJ, "assets", "audio", f"kokoro_{VOICE}.wav"),
            os.path.join(HERE, "public", "voice.wav"))
shutil.copy(os.path.join(PROJ, "assets", "audio", "music_bed.mp3"),
            os.path.join(HERE, "public", "music.mp3"))


def word_time(substr, nth=1, which="start"):
    """The nth word whose text contains substr (case-insensitive)."""
    hits = [w for w in caps if substr.lower() in w["word"].lower()]
    if len(hits) < nth:
        return None
    w = hits[nth - 1]
    return w["startMs"] / 1000.0 if which == "start" else w["endMs"] / 1000.0


# scene boundaries anchored to real narration words (reworked script)
hook_out = word_time("Every") or 4.5            # "Every note is on the same sheet..."
setup_out = word_time("layout", 1) or 12.5      # "The layout fixes that..."
build_out = word_time("trick") or word_time("That's") or 19.0  # "That's the trick..."
payoff_out = word_time("tuner") or word_time("Trinidadian") or 25.0  # "A Trinidadian tuner named..."

props = {
    "voiceSrc": "voice.wav",
    "musicSrc": "music.mp3",
    "captions": caps,
    "durationSeconds": dur,
    "beats": {
        "pan": {
            "webInEnd": round(min(hook_out + 2.5, setup_out - 0.5), 2),
            "clashStart": round(setup_out - 4.0, 2),
            "clashEnd": round(setup_out + 0.5, 2),
            "splitEnd": round(build_out - 0.5, 2),
            "ringStart": round(build_out + 0.3, 2),
        },
        "hookOut": round(hook_out, 2),
        "setupOut": round(setup_out, 2),
        "buildOut": round(build_out, 2),
        "payoffOut": round(payoff_out, 2),
    },
}
io.open(os.path.join(HERE, "src", "props", "note-layout.json"), "w", encoding="utf-8").write(
    json.dumps(props, indent=2, ensure_ascii=False)
)
print(f"voice={VOICE}  duration={dur}s  beats: hook<{hook_out:.1f} setup<{setup_out:.1f} "
      f"build<{build_out:.1f} payoff<{payoff_out:.1f}  ({len(caps)} caption words)")
