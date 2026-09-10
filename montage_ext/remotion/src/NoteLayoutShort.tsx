import React from "react";
import {
  AbsoluteFill,
  Audio,
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
      <Bg />

      {/* HEADLINE ZONE — fixed band near the top */}
      <div style={{ position: "absolute", top: 150, left: 0, right: 0, height: 320, display: "flex", alignItems: "flex-start", justifyContent: "center" }}>
        <Sequence from={0} durationInFrames={S(beats.hookOut)}>
          <KineticLine text="That spider web isn't decoration." sub="it's a map" accentWord="map" />
        </Sequence>
        <Sequence from={S(beats.hookOut)} durationInFrames={S(beats.setupOut - beats.hookOut)}>
          <KineticLine text="One sheet of steel." sub="clashing notes buzz" accentWord="steel" />
        </Sequence>
        <Sequence from={S(beats.setupOut)} durationInFrames={S(beats.buildOut - beats.setupOut)}>
          <KineticLine text="The layout splits them up." sub="apart · together" accentWord="splits" />
        </Sequence>
        <Sequence from={S(beats.buildOut)} durationInFrames={S(beats.payoffOut - beats.buildOut)}>
          <KineticLine text="It rings clean." sub="not rattling" accentWord="clean" />
        </Sequence>
        <Sequence from={S(beats.payoffOut)}>
          <KineticLine text="Anthony Williams · 1953" sub="the world still uses it" />
        </Sequence>
      </div>

      {/* PAN — centred, large */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", marginTop: 90 }}>
        <div
          style={{
            transform: `scale(${panZoom})`,
            opacity: interpolate(frame / fps, [0.3, 1.4], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          <SpiderWebPan beats={beats.pan} size={920} />
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
