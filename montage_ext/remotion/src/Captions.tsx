import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "./theme";

export type Word = { word: string; startMs: number; endMs: number };

/**
 * Word-by-word captions that actually keep their spaces (the vendored
 * openmontage CaptionOverlay puts the separator inside a `display:inline-block`
 * span, so it collapses — see projects/steelpan-note-layout/DRY_RUN_NOTES.md).
 * Here each word is a plain inline span and the space is real text between them.
 * Active word is lifted + accented; a rolling window of ~5 words shows at once.
 */
export const Captions: React.FC<{ words: Word[]; bottom?: number; windowSize?: number }> = ({
  words,
  bottom = 300,
  windowSize = 5,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;

  let active = words.findIndex((w) => ms >= w.startMs && ms < w.endMs);
  if (active === -1) {
    // between words: hold on the last one that started
    for (let i = words.length - 1; i >= 0; i--) {
      if (ms >= words[i].startMs) {
        active = i;
        break;
      }
    }
  }
  if (active === -1) active = 0;

  const start = Math.max(0, Math.min(active - Math.floor(windowSize / 2), words.length - windowSize));
  const win = words.slice(start, start + windowSize);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom,
        display: "flex",
        justifyContent: "center",
        padding: "0 90px",
      }}
    >
      <div
        style={{
          fontFamily: theme.body,
          fontWeight: 800,
          fontSize: 62,
          lineHeight: 1.25,
          textAlign: "center",
          color: `${theme.paper}88`,
          textShadow: "0 4px 20px rgba(0,0,0,0.6)",
          maxWidth: 900,
        }}
      >
        {win.map((w, i) => {
          const idx = start + i;
          const isActive = idx === active;
          const pop = isActive
            ? interpolate(ms, [w.startMs, w.startMs + 90], [0.85, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            : 1;
          return (
            <span
              key={idx}
              style={{
                color: isActive ? theme.paper : idx < active ? `${theme.paper}cc` : `${theme.paper}66`,
                display: "inline-block",
                transform: `scale(${pop})`,
              }}
            >
              {w.word}
              {i < win.length - 1 ? " " : ""}
            </span>
          );
        })}
      </div>
    </div>
  );
};
