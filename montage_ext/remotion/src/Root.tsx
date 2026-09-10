import { Composition } from "remotion";
import { NoteLayoutShort, NoteLayoutProps } from "./NoteLayoutShort";
import { CANVAS } from "./theme";
import defaultProps from "./props/note-layout.json";

export const Root: React.FC = () => {
  const p = defaultProps as unknown as NoteLayoutProps;
  return (
    <Composition
      id="NoteLayoutShort"
      component={NoteLayoutShort}
      durationInFrames={Math.round((p.durationSeconds ?? 36) * CANVAS.fps)}
      fps={CANVAS.fps}
      width={CANVAS.width}
      height={CANVAS.height}
      defaultProps={p}
      calculateMetadata={({ props }) => ({
        durationInFrames: Math.round(((props as NoteLayoutProps).durationSeconds ?? 36) * CANVAS.fps),
      })}
    />
  );
};
