import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';

const FPS = 30;
export const BLUE = '#2459E8';
const ease = (t: number) => 1 - Math.pow(1 - t, 3);

/** eased 0..1 progress between `at` and `at + dur` seconds (scene-relative) */
export const useProg = (at: number, dur = 0.8) => {
  const f = useCurrentFrame();
  return interpolate(f, [at * FPS, (at + dur) * FPS], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
};

export const Layer: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={720} height={1280} viewBox="0 0 720 1280" style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
    {children}
  </svg>
);

/** A path that draws itself. */
export const DrawPath: React.FC<{d: string; at: number; dur?: number; color?: string; w?: number; dashed?: boolean; arrow?: boolean; opacity?: number}> = ({d, at, dur = 0.9, color = BLUE, w = 4, dashed, opacity = 1}) => {
  const p = useProg(at, dur);
  if (p <= 0) return null;
  return dashed ? (
    <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeDasharray="10 12" opacity={opacity} style={{clipPath: undefined}} pathLength={1} strokeDashoffset={0} mask={undefined} />
  ) : (
    <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" opacity={opacity} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
  );
};

/** Dashed line that draws by revealing through a solid mask-like dash trick. */
export const DashedDraw: React.FC<{d: string; at: number; dur?: number; color?: string; w?: number; len?: number}> = ({d, at, dur = 0.9, color = BLUE, w = 4, len = 400}) => {
  const p = useProg(at, dur);
  const f = useCurrentFrame();
  if (p <= 0) return null;
  const id = `m${d.length}${at}`.replace(/\./g, '_');
  return (
    <>
      <defs>
        <mask id={id} maskUnits="userSpaceOnUse" x={-100} y={-100} width={1000} height={1500}>
          <path d={d} fill="none" stroke="#fff" strokeWidth={w + 8} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
        </mask>
      </defs>
      <g mask={`url(#${id})`}>
        <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeDasharray="10 12" strokeDashoffset={-f * 0.6} />
      </g>
      {len ? null : null}
    </>
  );
};

export const Ring: React.FC<{cx: number; cy: number; r: number; at: number; dur?: number; color?: string; w?: number; dashed?: boolean}> = ({cx, cy, r, at, dur = 1.1, color = BLUE, w = 4, dashed}) => {
  const p = useProg(at, dur);
  if (p <= 0) return null;
  const d = `M ${cx} ${cy - r} A ${r} ${r} 0 1 1 ${cx - 0.01} ${cy - r}`;
  return dashed ? <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeDasharray="6 12" opacity={p * 0.5} /> : <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />;
};

/** Hand-drawn wavy underline that draws left → right. */
export const Underline: React.FC<{x: number; y: number; w: number; at: number; dur?: number; color?: string}> = ({x, y, w, at, dur = 0.8, color = BLUE}) => {
  const d = `M ${x} ${y} C ${x + w * 0.25} ${y - 9}, ${x + w * 0.5} ${y + 7}, ${x + w * 0.75} ${y - 5} S ${x + w * 0.95} ${y + 3}, ${x + w} ${y - 4}`;
  return <DrawPath d={d} at={at} dur={dur} color={color} w={5} />;
};

/** Expanding ripple circles that loop. */
export const Ripples: React.FC<{cx: number; cy: number; max?: number; n?: number; at?: number; color?: string}> = ({cx, cy, max = 320, n = 3, at = 0, color = BLUE}) => {
  const f = useCurrentFrame();
  const t = f - at * FPS;
  if (t < 0) return null;
  return (
    <>
      {Array.from({length: n}).map((_, i) => {
        const cyc = 120;
        const q = ((t + (i * cyc) / n) % cyc) / cyc;
        return <circle key={i} cx={cx} cy={cy} r={40 + q * max} fill="none" stroke={color} strokeWidth={3} opacity={(1 - q) * 0.35} />;
      })}
    </>
  );
};

/** Dots orbiting a centre. */
export const Orbit: React.FC<{cx: number; cy: number; r: number; at?: number; n?: number; speed?: number; color?: string; showRing?: boolean}> = ({cx, cy, r, at = 0, n = 3, speed = 0.02, color = BLUE, showRing = true}) => {
  const f = useCurrentFrame();
  const t = f - at * FPS;
  if (t < 0) return null;
  const appear = Math.min(1, t / 15);
  return (
    <g opacity={appear}>
      {showRing && <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeOpacity={0.25} strokeWidth={2} strokeDasharray="4 10" />}
      {Array.from({length: n}).map((_, i) => {
        const a = t * speed + (i * Math.PI * 2) / n;
        return <circle key={i} cx={cx + Math.cos(a) * r} cy={cy + Math.sin(a) * r} r={i === 0 ? 9 : 6} fill={color} />;
      })}
    </g>
  );
};

/** Radiating burst lines at a cue time. */
export const Burst: React.FC<{cx: number; cy: number; at: number; n?: number; r0?: number; r1?: number; color?: string}> = ({cx, cy, at, n = 12, r0 = 60, r1 = 130, color = BLUE}) => {
  const p = useProg(at, 0.7);
  if (p <= 0) return null;
  return (
    <g opacity={1 - Math.max(0, p - 0.6) / 0.4}>
      {Array.from({length: n}).map((_, i) => {
        const a = (i / n) * Math.PI * 2;
        const a0 = r0 + (r1 - r0) * p * 0.6;
        const a1 = r0 + (r1 - r0) * p;
        return <line key={i} x1={cx + Math.cos(a) * a0} y1={cy + Math.sin(a) * a0} x2={cx + Math.cos(a) * a1} y2={cy + Math.sin(a) * a1} stroke={color} strokeWidth={4} strokeLinecap="round" />;
      })}
    </g>
  );
};

/** Little 4-point sparkles twinkling at fixed spots. */
export const Sparkle: React.FC<{x: number; y: number; s?: number; at?: number; color?: string}> = ({x, y, s = 16, at = 0, color = BLUE}) => {
  const f = useCurrentFrame();
  const t = f - at * FPS;
  if (t < 0) return null;
  const k = 0.55 + 0.45 * Math.sin(t / 9 + x);
  const a = s * k;
  return <path d={`M ${x} ${y - a} Q ${x} ${y} ${x + a} ${y} Q ${x} ${y} ${x} ${y + a} Q ${x} ${y} ${x - a} ${y} Q ${x} ${y} ${x} ${y - a} Z`} fill={color} opacity={0.9} />;
};

/** Audio-style waveform bars. */
export const Wave: React.FC<{x: number; y: number; n?: number; gap?: number; at?: number; color?: string; h?: number}> = ({x, y, n = 14, gap = 12, at = 0, color = BLUE, h = 60}) => {
  const f = useCurrentFrame();
  const t = f - at * FPS;
  if (t < 0) return null;
  return (
    <>
      {Array.from({length: n}).map((_, i) => {
        const amp = (0.35 + 0.65 * Math.abs(Math.sin(t / 7 + i * 0.9))) * Math.min(1, t / 20);
        const bh = h * amp;
        return <rect key={i} x={x + i * gap} y={y - bh / 2} width={5} height={bh} rx={2.5} fill={color} opacity={0.85} />;
      })}
    </>
  );
};

/** Check mark that draws itself inside a ring. */
export const CheckRing: React.FC<{cx: number; cy: number; r: number; at: number}> = ({cx, cy, r, at}) => (
  <>
    <Ring cx={cx} cy={cy} r={r} at={at} dur={0.8} w={6} />
    <DrawPath d={`M ${cx - r * 0.38} ${cy + r * 0.02} L ${cx - r * 0.08} ${cy + r * 0.34} L ${cx + r * 0.42} ${cy - r * 0.3}`} at={at + 0.7} dur={0.5} w={9} />
  </>
);

/** Typewriter text with blinking cursor inside a pill/bubble. */
export const TypeBubble: React.FC<{at: number; text: string; style?: React.CSSProperties; size?: number; dark?: boolean; cps?: number; hideAfter?: number}> = ({at, text, style, size = 24, dark, cps = 16, hideAfter}) => {
  const f = useCurrentFrame();
  const t = (f - at * FPS) / FPS;
  if (t < 0) return null;
  const n = Math.min(text.length, Math.floor(t * cps));
  const done = n >= text.length;
  const cursor = !done || Math.floor(f / 14) % 2 === 0;
  const fade = hideAfter !== undefined ? 1 - interpolate(f, [hideAfter * FPS, hideAfter * FPS + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  const pop = Math.min(1, t / 0.25);
  return (
    <div style={{position: 'absolute', opacity: fade * pop, transform: `scale(${0.9 + 0.1 * pop})`, background: dark ? BLUE : '#fff', color: dark ? '#fff' : '#0B0B0F', border: dark ? 'none' : '1.5px solid #E3E7F0', borderRadius: 18, padding: '12px 20px', boxShadow: '0 10px 24px rgba(30,50,110,0.12)', fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: size, whiteSpace: 'nowrap', ...style}}>
      {text.slice(0, n)}
      <span style={{display: 'inline-block', width: 2.5, height: size * 0.95, background: dark ? '#fff' : BLUE, marginLeft: 3, verticalAlign: 'text-bottom', opacity: cursor ? 1 : 0}} />
    </div>
  );
};
