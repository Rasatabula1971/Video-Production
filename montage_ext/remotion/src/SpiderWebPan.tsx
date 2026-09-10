import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "./theme";

/**
 * Animated tenor-pan face. A ring of note dots arranged in a circle (the
 * cycle of fourths and fifths), with radial "spider web" grooves. Four beats,
 * driven by absolute seconds so it can be lined up with narration:
 *
 *   webInEnd    grooves + rim draw in
 *   clashEnd    two adjacent dots go red and rattle
 *   splitEnd    red dots travel to opposite sides; two others glow + pair up
 *   (after)     whole pan pulses warm once — the "rings clean" beat
 */
export type PanBeats = {
  webInEnd: number;
  clashStart: number;
  clashEnd: number;
  splitEnd: number;
  ringStart: number;
};

const N = 12; // notes around the ring
const R = 330; // ring radius (px, in a 1000x1000 viewbox centred at 500,500)
const C = 500;
const DOT = 26; // base dot radius

const dotAngle = (i: number) => (i / N) * Math.PI * 2 - Math.PI / 2;
const dotXY = (i: number, radius = R) => ({
  x: C + Math.cos(dotAngle(i)) * radius,
  y: C + Math.sin(dotAngle(i)) * radius,
});

// deterministic tiny wobble
const wobble = (seed: number, t: number, amp: number) =>
  Math.sin(t * 37 + seed * 2.399) * amp;

export const SpiderWebPan: React.FC<{ beats: PanBeats; size?: number }> = ({
  beats,
  size = 760,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // resolve the pan quickly so the opening frames look intentional, not murky
  const webIn = interpolate(t, [0.15, 2.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const clash = interpolate(t, [beats.clashStart, beats.clashStart + 0.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const split = interpolate(t, [beats.clashEnd, beats.splitEnd], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ring = interpolate(
    t,
    [beats.ringStart, beats.ringStart + 0.5, beats.ringStart + 1.6],
    [0, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // the two clashing notes start adjacent (indices 0 and 1), end opposite (0 and 6)
  const clashA = 0;
  const clashBFrom = 1;
  const clashBTo = 6;
  const bIndexFloat = interpolate(split, [0, 1], [clashBFrom, clashBTo]);

  // two "friendly" notes snap together (3 and 8 -> 5 and 6)
  const fAFloat = interpolate(split, [0, 1], [3, 5]);
  const fBFloat = interpolate(split, [0, 1], [9, 6]);

  const rattleAmp = clash * (1 - split) * 10;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 1000 1000"
      style={{ overflow: "visible" }}
    >
      {/* pan bowl */}
      <circle
        cx={C}
        cy={C}
        r={R + 90}
        fill={theme.inkDeep}
        stroke={theme.steel}
        strokeOpacity={0.35}
        strokeWidth={3}
        strokeDasharray={2 * Math.PI * (R + 90)}
        strokeDashoffset={(1 - webIn) * 2 * Math.PI * (R + 90)}
      />
      <circle cx={C} cy={C} r={R + 90} fill="url(#panSheen)" opacity={0.5} />

      {/* radial grooves (the "web") — between each pair of note positions */}
      {Array.from({ length: N }).map((_, i) => {
        const outer = dotXY(i + 0.5, R + 82);
        const draw = interpolate(webIn, [(i / N) * 0.6, (i / N) * 0.6 + 0.4], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <line
            key={`g${i}`}
            x1={C}
            y1={C}
            x2={C + (outer.x - C) * draw}
            y2={C + (outer.y - C) * draw}
            stroke={theme.steel}
            strokeOpacity={0.5}
            strokeWidth={3}
          />
        );
      })}
      {/* concentric web arcs — scale up from centre as the web resolves */}
      {[0.4, 0.62, 0.84, 1.03].map((rr, k) => {
        const on = interpolate(webIn, [0.15 + k * 0.12, 0.55 + k * 0.12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <circle
            key={`arc${k}`}
            cx={C}
            cy={C}
            r={R * rr * on}
            fill="none"
            stroke={theme.steel}
            strokeOpacity={0.34 * on}
            strokeWidth={2.5}
          />
        );
      })}

      {/* note dots */}
      {Array.from({ length: N }).map((_, i) => {
        let x: number, y: number, fill = theme.paper, r = DOT, glow = 0;

        if (i === clashA) {
          const p = dotXY(clashA);
          x = p.x + wobble(1, t, 1) * rattleAmp;
          y = p.y + wobble(2, t, 1) * rattleAmp;
          fill = clash > 0 ? theme.clash : theme.paper;
          glow = clash * (1 - split);
        } else if (i === clashBFrom) {
          // this dot travels
          const lo = Math.floor(bIndexFloat);
          const hi = Math.ceil(bIndexFloat);
          const f = bIndexFloat - lo;
          const a = dotXY(lo), b = dotXY(hi);
          x = a.x + (b.x - a.x) * f + wobble(3, t, 1) * rattleAmp;
          y = a.y + (b.y - a.y) * f + wobble(4, t, 1) * rattleAmp;
          fill = clash > 0 ? theme.clash : theme.paper;
          glow = clash * (1 - split);
        } else if (i === 3) {
          const lo = Math.floor(fAFloat), hi = Math.ceil(fAFloat), f = fAFloat - lo;
          const a = dotXY(lo), b = dotXY(hi);
          x = a.x + (b.x - a.x) * f;
          y = a.y + (b.y - a.y) * f;
          fill = split > 0.1 ? theme.accent : theme.paper;
          glow = split * 0.9;
        } else if (i === 9) {
          const lo = Math.floor(fBFloat), hi = Math.ceil(fBFloat), f = fBFloat - lo;
          const a = dotXY(lo), b = dotXY(hi);
          x = a.x + (b.x - a.x) * f;
          y = a.y + (b.y - a.y) * f;
          fill = split > 0.1 ? theme.accent : theme.paper;
          glow = split * 0.9;
        } else {
          const p = dotXY(i);
          x = p.x;
          y = p.y;
        }

        const pulse = 1 + ring * 0.12;
        return (
          <g key={`d${i}`}>
            {glow > 0 && (
              <circle cx={x} cy={y} r={r * 2.4} fill={fill} opacity={glow * 0.25} />
            )}
            <circle
              cx={x}
              cy={y}
              r={r * pulse}
              fill={fill}
              opacity={interpolate(webIn, [0.05, 0.35], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })}
            />
          </g>
        );
      })}

      {/* warm ring flash on the payoff */}
      <circle
        cx={C}
        cy={C}
        r={R + 90}
        fill="none"
        stroke={theme.glow}
        strokeWidth={10}
        opacity={ring * 0.9}
      />

      <defs>
        <radialGradient id="panSheen" cx="38%" cy="32%" r="75%">
          <stop offset="0%" stopColor="#1b2f3b" />
          <stop offset="70%" stopColor={theme.inkDeep} />
          <stop offset="100%" stopColor="#030c11" />
        </radialGradient>
      </defs>
    </svg>
  );
};
