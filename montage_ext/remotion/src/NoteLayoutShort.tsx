import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
} from "remotion";
import { theme } from "./theme";
import { SpiderWebPan, PanBeats } from "./SpiderWebPan";
import { Captions, Word } from "./Captions";

/** Full-bleed photographic bed: a real hammered-metal disc, darkened, slow push. */
const Bed: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const z = interpolate(frame, [0, durationInFrames], [1.08, 1.2]);
  const pan = interpolate(frame, [0, durationInFrames], [-2, 2]);
  return (
    <AbsoluteFill style={{ background: theme.inkDeep }}>
      <Img
        src={staticFile("bed.jpg")}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${z}) translateX(${pan}%)`,
          filter: "saturate(0.85) brightness(0.78) contrast(1.05)",
        }}
      />
      <AbsoluteFill style={{ background: `radial-gradient(75% 50% at 50% 48%, rgba(11,31,42,0.0) 0%, rgba(7,23,32,0.6) 78%)` }} />
      <AbsoluteFill style={{ background: "rgba(7,23,32,0.18)" }} />
    </AbsoluteFill>
  );
};

/** Brief atmosphere insert — flashes over the frame, then cuts back. */
const Cutaway: React.FC<{ src: string; holdFrames: number }> = ({ src, holdFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inA = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  const outA = interpolate(frame, [holdFrames - 6, holdFrames], [1, 0], { extrapolateLeft: "clamp" });
  const z = interpolate(frame, [0, holdFrames], [1.02, 1.12]);
  return (
    <AbsoluteFill style={{ opacity: inA * outA }}>
      <Img
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${z})` }}
      />
      <AbsoluteFill style={{ background: "rgba(7,23,32,0.2)" }} />
    </AbsoluteFill>
  );
};

export type NoteLayoutProps = {
  voiceSrc: string;
  musicSrc?: string;
  captions: Word[];
  durationSeconds: number;
  beats: {
    pan: PanBeats;
    hookOut: number;
    setupOut: number;
    buildOut: number;
    payoffOut: number;
  };
};

const Bg: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const d = interpolate(frame, [0, durationInFrames], [0, 1]);
  return (
    <AbsoluteFill style={{ background: theme.ink }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(130% 60% at ${34 + d * 10}% ${30 + d * 8}%, #133240 0%, ${theme.ink} 52%, ${theme.inkDeep} 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
          backgroundSize: "72px 72px",
          opacity: 0.7,
        }}
      />
    </AbsoluteFill>
  );
};

const KineticLine: React.FC<{ text: string; sub?: string; accentWord?: string }> = ({
  text,
  sub,
  accentWord,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const subEnter = spring({ frame: frame - 6, fps, config: { damping: 18, stiffness: 130 } });
  const words = text.split(" ");
  return (
    <div style={{ textAlign: "center", padding: "0 70px" }}>
      <div
        style={{
          fontFamily: theme.display,
          fontWeight: 800,
          fontSize: 74,
          lineHeight: 1.08,
          color: theme.paper,
          letterSpacing: "-0.02em",
          textTransform: "uppercase",
          textShadow: "0 6px 30px rgba(0,0,0,0.55)",
        }}
      >
        {words.map((w, i) => {
          const wp = spring({ frame: frame - i * 3, fps, config: { damping: 20, stiffness: 150 } });
          const isAccent =
            accentWord && w.toLowerCase().replace(/[^a-z]/g, "") === accentWord.toLowerCase();
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: 20,
                opacity: wp,
                transform: `translateY(${(1 - wp) * 22}px)`,
                color: isAccent ? theme.accent : theme.paper,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
      {sub && (
        <div
          style={{
            marginTop: 20,
            fontFamily: theme.body,
            fontWeight: 800,
            fontSize: 38,
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            color: theme.accent,
            opacity: interpolate(subEnter, [0.3, 1], [0, 1]),
          }}
        >
          {sub}
        </div>
      )}
    </div>
  );
};

export const NoteLayoutShort: React.FC<NoteLayoutProps> = ({
  voiceSrc,
  musicSrc,
  captions,
  beats,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const S = (s: number) => Math.round(s * fps);

  // gentle pan-only push-in; layout stays put
  const panZoom = interpolate(frame, [0, durationInFrames], [1.0, 1.05]);

  return (
    <AbsoluteFill>
      <Bed />

      {/* atmosphere cutaways — quick inserts for texture */}
      <Sequence from={0} durationInFrames={S(1.7)}>
        <Cutaway src="broll_spark.jpg" holdFrames={S(1.7)} />
      </Sequence>
      <Sequence from={S(beats.setupOut - 2.6)} durationInFrames={S(1.5)}>
        <Cutaway src="broll_ripple.jpg" holdFrames={S(1.5)} />
      </Sequence>
      <Sequence from={S(beats.payoffOut - 0.6)} durationInFrames={S(1.6)}>
        <Cutaway src="broll_molten.jpg" holdFrames={S(1.6)} />
      </Sequence>

      {/* HEADLINE ZONE — fixed band near the top */}
      <div style={{ position: "absolute", top: 118, left: 0, right: 0, height: 300, display: "flex", alignItems: "flex-start", justifyContent: "center" }}>
        <Sequence from={0} durationInFrames={S(beats.hookOut)}>
          <KineticLine text="It looks random." sub="it's the opposite" accentWord="random" />
        </Sequence>
        <Sequence from={S(beats.hookOut)} durationInFrames={S(beats.setupOut - beats.hookOut)}>
          <KineticLine text="One sheet of metal." sub="clashing notes buzz" accentWord="metal" />
        </Sequence>
        <Sequence from={S(beats.setupOut)} durationInFrames={S(beats.buildOut - beats.setupOut)}>
          <KineticLine text="The layout fixes it." sub="apart · together" accentWord="fixes" />
        </Sequence>
        <Sequence from={S(beats.buildOut)} durationInFrames={S(beats.payoffOut - beats.buildOut)}>
          <KineticLine text="It sings." sub="instead of rattling" accentWord="sings" />
        </Sequence>
        <Sequence from={S(beats.payoffOut)}>
          <KineticLine text="Anthony Williams · 1953" sub="still built from his map" />
        </Sequence>
      </div>

      {/* PAN — centred, large. Fades in after the opening spark clears. */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", marginTop: 40 }}>
        <div
          style={{
            transform: `scale(${panZoom})`,
            opacity: interpolate(frame / fps, [1.6, 2.7], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          <SpiderWebPan beats={beats.pan} size={1000} />
        </div>
      </AbsoluteFill>

      {/* CAPTIONS — lower third, clear of the platform UI */}
      <Captions words={captions} bottom={260} />

      {/* END TAG — final 3s */}
      <Sequence from={durationInFrames - S(3)}>
        <div style={{ position: "absolute", bottom: 120, left: 0, right: 0, textAlign: "center" }}>
          <span
            style={{
              fontFamily: theme.display,
              fontWeight: 800,
              fontSize: 38,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: theme.steel,
            }}
          >
            Pan. Made in Trinidad.
          </span>
        </div>
      </Sequence>

      <Audio src={staticFile(voiceSrc)} />
      {musicSrc && <MusicBed src={musicSrc} />}
    </AbsoluteFill>
  );
};

const MusicBed: React.FC<{ src: string }> = ({ src }) => {
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <Audio
      src={staticFile(src)}
      volume={(f) => {
        const fadeIn = interpolate(f, [0, fps * 1], [0, 1], { extrapolateRight: "clamp" });
        const fadeOut = interpolate(f, [durationInFrames - fps * 2.5, durationInFrames], [1, 0], {
          extrapolateLeft: "clamp",
        });
        const lift = interpolate(
          f,
          [fps * 18, fps * 20, fps * 26, fps * 28],
          [0.24, 0.34, 0.34, 0.22],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        return lift * fadeIn * fadeOut;
      }}
    />
  );
};
