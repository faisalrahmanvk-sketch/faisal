import React, {createContext, useContext} from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import words from './words.json';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/inter/800.css';
import '@fontsource/instrument-serif/400-italic.css';
import '@fontsource/noto-sans-malayalam/malayalam-500.css';
import '@fontsource/noto-sans-malayalam/malayalam-700.css';

const FPS = 30;
const BLUE = '#2459E8';
const BLUE_SOFT = '#DCE6FF';
const INK = '#0B0B0F';
const MUTED = '#6B7280';
const LINE = '#E3E7F0';
const SANS = 'Inter, sans-serif';
const SERIF = "'Instrument Serif', serif";
const MAL = "'Noto Sans Malayalam', Inter, sans-serif";

// ---------- timing (all in absolute seconds of the voice-over) ----------
type Wd = {w: string; s: number; e: number; scene: number; ph: number};
const SPEED = 1.25;
const WORDS = (words as Wd[]).map((x) => ({...x, s: x.s / SPEED, e: x.e / SPEED}));
const PHW: Wd[][] = [];
WORDS.forEach((x) => {
  (PHW[x.ph] = PHW[x.ph] || []).push(x);
});
const cue = (ph: number, k = 0) => PHW[ph][k].s;

const B = [0, 10.7, 21.65, 33.22, 43.65, 52.85, 59.16].map((x) => x / SPEED);
const F = B.map((s) => Math.round(s * FPS));
export const TOTAL_FRAMES = F[F.length - 1];

const Ctx = createContext(0);
const useT = () => (useCurrentFrame() + useContext(Ctx)) / FPS;
const ease = (t: number) => 1 - Math.pow(1 - t, 3);
const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
const useProg = (at: number, dur = 0.6) => ease(clamp01((useT() - at) / dur));

// ---------- primitives ----------
const Reveal: React.FC<{at: number; dy?: number; dx?: number; dur?: number; style?: React.CSSProperties; children: React.ReactNode}> = ({at, dy = 22, dx = 0, dur = 0.55, style, children}) => {
  const p = useProg(at, dur);
  return <div style={{opacity: p, transform: `translate(${(1 - p) * dx}px, ${(1 - p) * dy}px)`, ...style}}>{children}</div>;
};

/** hand-written reveal: the word is wiped in left → right */
const WriteOn: React.FC<{at: number; dur?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({at, dur = 0.7, children, style}) => {
  const p = useProg(at, dur);
  return <span style={{display: 'inline-block', clipPath: `inset(-20% ${(1 - p) * 102}% -20% 0)`, opacity: p > 0 ? 1 : 0, ...style}}>{children}</span>;
};

const Layer: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={720} height={1280} viewBox="0 0 720 1280" style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>{children}</svg>
);

/** a path that draws itself; optional soft fill appears after */
const Ink: React.FC<{d: string; at: number; dur?: number; stroke?: string; w?: number; fill?: string; dash?: boolean}> = ({d, at, dur = 0.8, stroke = INK, w = 3.5, fill, dash}) => {
  const p = useProg(at, dur);
  const fp = useProg(at + dur * 0.8, 0.4);
  if (p <= 0) return null;
  return (
    <>
      {fill && <path d={d} fill={fill} opacity={fp} stroke="none" />}
      {dash ? (
        <path d={d} fill="none" stroke={stroke} strokeWidth={w} strokeLinecap="round" strokeDasharray="9 11" opacity={p} />
      ) : (
        <path d={d} fill="none" stroke={stroke} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
      )}
    </>
  );
};

const Underline: React.FC<{x: number; y: number; w: number; at: number; dur?: number}> = ({x, y, w, at, dur = 0.6}) => (
  <Ink d={`M ${x} ${y} C ${x + w * 0.3} ${y - 7}, ${x + w * 0.6} ${y + 6}, ${x + w} ${y - 3}`} at={at} dur={dur} stroke={BLUE} w={4.5} />
);

const Spark: React.FC<{x: number; y: number; s?: number; at: number}> = ({x, y, s = 16, at}) => {
  const t = useT();
  if (t < at) return null;
  const k = 0.6 + 0.4 * Math.sin((t - at) * 5 + x);
  const a = s * k * Math.min(1, (t - at) * 4);
  return <path d={`M ${x} ${y - a} Q ${x} ${y} ${x + a} ${y} Q ${x} ${y} ${x} ${y + a} Q ${x} ${y} ${x - a} ${y} Q ${x} ${y} ${x} ${y - a} Z`} fill={BLUE} />;
};

/** short radiating tick lines (no circles) */
const Ticks: React.FC<{x: number; y: number; at: number; n?: number; r0?: number; r1?: number}> = ({x, y, at, n = 9, r0 = 60, r1 = 100}) => {
  const p = useProg(at, 0.5);
  if (p <= 0) return null;
  return (
    <g opacity={1 - clamp01((p - 0.7) / 0.3) * 0.0}>
      {Array.from({length: n}).map((_, i) => {
        const a = (i / n) * Math.PI * 2 - Math.PI / 2;
        return <line key={i} x1={x + Math.cos(a) * r0} y1={y + Math.sin(a) * r0} x2={x + Math.cos(a) * (r0 + (r1 - r0) * p)} y2={y + Math.sin(a) * (r0 + (r1 - r0) * p)} stroke={BLUE} strokeWidth={4} strokeLinecap="round" />;
      })}
    </g>
  );
};

// ---------- line icons (64×64 viewBox) ----------
const ICON: Record<string, string[]> = {
  pen: ['M10 54 L14 40 L40 14 L50 24 L24 50 Z', 'M34 20 L44 30', 'M10 54 L24 50'],
  bulb: ['M32 6 C18 6 12 18 17 29 C20 35 24 37 24 44 H40 C40 37 44 35 47 29 C52 18 46 6 32 6 Z', 'M25 51 H39', 'M28 58 H36'],
  code: ['M22 16 L7 32 L22 48', 'M42 16 L57 32 L42 48', 'M37 10 L27 54'],
  doc: ['M14 6 H38 L52 20 V58 H14 Z', 'M38 6 V20 H52', 'M22 32 H44', 'M22 42 H44', 'M22 51 H35'],
  calendar: ['M7 14 H57 V57 H7 Z', 'M7 27 H57', 'M20 6 V19', 'M44 6 V19'],
  building: ['M8 58 V12 H36 V58', 'M36 30 H56 V58', 'M4 58 H60', 'M16 22 H28', 'M16 32 H28', 'M16 42 H28', 'M43 40 H49', 'M43 49 H49'],
  question: ['M20 22 C20 8 44 8 44 22 C44 34 32 33 32 44', 'M32 55 V56'],
  check: ['M9 34 L26 50 L55 15'],
  star: ['M32 4 V60', 'M4 32 H60', 'M12 12 L52 52', 'M52 12 L12 52'],
};
const Icon: React.FC<{k: string; x: number; y: number; size: number; at: number; dur?: number; stroke?: string; fill?: string}> = ({k, x, y, size, at, dur = 0.8, stroke = INK, fill}) => (
  <g transform={`translate(${x},${y}) scale(${size / 64})`}>
    {ICON[k].map((d, i) => (
      <Ink key={i} d={d} at={at + i * dur * 0.25} dur={dur * 0.7} stroke={stroke} w={3.2 * (64 / size) * 0.9 + 1.2} fill={i === 0 ? fill : undefined} />
    ))}
  </g>
);

// ---------- frame furniture ----------
const Background: React.FC = () => (
  <AbsoluteFill style={{background: '#fff', backgroundImage: `linear-gradient(#EEF1F7 1px, transparent 1px), linear-gradient(90deg, #EEF1F7 1px, transparent 1px)`, backgroundSize: '36px 36px', backgroundPosition: '-1px -1px'}} />
);

const LABELS = ['INTRODUCTION', 'THE STORY', 'WHAT CAN YOU DO?', 'THE COMMON MISTAKE', 'WHAT YOU WILL LEARN', 'ENDING'];
const Header: React.FC<{idx: number}> = ({idx}) => {
  const p = useProg(B[idx] + 0.05, 0.5);
  return (
    <>
      <div style={{position: 'absolute', left: 36, top: 44, display: 'flex', alignItems: 'center', gap: 12, opacity: p, fontFamily: SANS, fontWeight: 700, fontSize: 16, letterSpacing: 2, color: INK}}>
        <div style={{width: 28, height: 28, borderRadius: 8, background: INK, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 15, letterSpacing: 0}}>{idx + 1}</div>
        {LABELS[idx]}
      </div>
      <Layer>
        <Ink d="M 36 92 H 684" at={B[idx] + 0.15} dur={0.6} stroke={LINE} w={2} />
      </Layer>
    </>
  );
};

/** Malayalam caption, one word at a time, exactly on the spoken word */
const Caption: React.FC<{scene: number}> = ({scene}) => {
  const t = useT();
  const phs = PHW.map((p, i) => ({i, p})).filter((x) => x.p[0].scene === scene);
  let cur = -1;
  for (const x of phs) if (t >= x.p[0].s - 0.08) cur = x.i;
  if (cur < 0) return null;
  const p = PHW[cur];
  const next = PHW[cur + 1] && PHW[cur + 1][0].scene === scene ? PHW[cur + 1][0].s : Infinity;
  if (t > p[p.length - 1].e + 0.9 && next === Infinity) return null;
  return (
    <div style={{position: 'absolute', left: 36, right: 36, top: 112, textAlign: 'center', fontFamily: MAL, fontWeight: 500, fontSize: 31, lineHeight: 1.55, color: INK}}>
      {p.map((wd, i) => {
        const a = ease(clamp01((t - wd.s) / 0.18));
        const active = t >= wd.s && t < wd.e + 0.08;
        const latin = /^[A-Za-z0-9]/.test(wd.w);
        return (
          <span key={i} style={{display: 'inline-block', margin: '0 6px', opacity: a, transform: `translateY(${(1 - a) * 10}px)`, filter: `blur(${(1 - a) * 4}px)`, color: active ? BLUE : INK, fontFamily: latin ? SANS : MAL, fontWeight: active ? 700 : 500, borderBottom: `3.5px solid ${active ? BLUE : 'transparent'}`, lineHeight: 1.35}}>
            {wd.w}
          </span>
        );
      })}
    </div>
  );
};

// ---------- character ----------
type Side = 'left' | 'right' | 'center';
const POSE: Record<Side, {src: string; h: number; ar: number}> = {
  center: {src: 'chars/pose-center-thinking.png', h: 720, ar: 832 / 1920},
  left: {src: 'chars/pose-left.png', h: 640, ar: 1024 / 1536},
  right: {src: 'chars/pose-right.png', h: 640, ar: 1024 / 1536},
};
const Character: React.FC<{side: Side}> = ({side}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = POSE[side];
  const w = p.h * p.ar;
  const s = spring({frame: frame - 2, fps, config: {damping: 16, stiffness: 120}});
  const float = Math.sin(frame / 18) * 4;
  const left = side === 'left' ? 6 : side === 'right' ? 720 - w - 6 : (720 - w) / 2;
  return (
    <div style={{position: 'absolute', left, bottom: 10 - (1 - s) * 70 - float, width: w, height: p.h, opacity: s}}>
      <Img src={staticFile(p.src)} style={{width: '100%', height: '100%'}} />
    </div>
  );
};

// ---------- headline helpers ----------
const Bold: React.FC<{children: React.ReactNode; size?: number}> = ({children, size = 60}) => (
  <span style={{fontFamily: SANS, fontWeight: 700, fontSize: size, color: INK, letterSpacing: -1}}>{children}</span>
);
const Ital: React.FC<{children: React.ReactNode; size?: number}> = ({children, size = 84}) => (
  <span style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: size, color: BLUE, letterSpacing: -0.5}}>{children}</span>
);

// ================= SCENES =================
const Win: React.FC<{x: number; y: number; at: number; stroke: string; fill?: string; label: string; labelColor: string; star?: boolean}> = ({x, y, at, stroke, fill, label, labelColor, star}) => (
  <g transform={`translate(${x},${y})`}>
    <Ink d="M14 0 H136 Q150 0 150 14 V106 Q150 120 136 120 H14 Q0 120 0 106 V14 Q0 0 14 0 Z" at={at} dur={0.7} stroke={stroke} fill={fill} w={3.5} />
    <Ink d="M0 26 H150" at={at + 0.2} dur={0.4} stroke={stroke} w={3} />
    <Ink d="M16 50 H104" at={at + 0.4} dur={0.4} stroke={stroke} w={3.5} />
    <Ink d="M16 68 H128" at={at + 0.5} dur={0.4} stroke={stroke} w={3.5} />
    <Ink d="M16 86 H84" at={at + 0.6} dur={0.4} stroke={stroke} w={3.5} />
    {star && (
      <g transform="translate(112,86) scale(0.34)">
        {ICON.star.map((d, i) => <Ink key={i} d={d} at={at + 0.9 + i * 0.1} dur={0.4} stroke={BLUE} w={6} />)}
      </g>
    )}
    <text x={75} y={152} textAnchor="middle" fontFamily={SANS} fontWeight={700} fontSize={24} fill={labelColor} opacity={useProg(at + 0.4, 0.4)}>{label}</text>
  </g>
);

const Logo: React.FC<{src: string; x: number; y: number; w: number; at: number; align?: 'left' | 'right'}> = ({src, x, y, w, at, align = 'left'}) => {
  const p = useProg(at, 0.6);
  return (
    <div style={{position: 'absolute', top: y, [align]: x, width: w, opacity: p > 0 ? 1 : 0, clipPath: `inset(-5% ${(1 - p) * 102}% -5% 0)`, mixBlendMode: 'multiply'} as React.CSSProperties}>
      <Img src={staticFile(src)} style={{width: '100%', display: 'block'}} />
    </div>
  );
};

const AppIcon: React.FC<{src: string; x: number; y: number; size: number; at: number; label: string; color: string; align: 'left' | 'right'}> = ({src, x, y, size, at, label, color, align}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const start = Math.round(at * FPS) - useContext(Ctx);
  const sp = spring({frame: frame - start, fps, config: {damping: 13, stiffness: 140}});
  return (
    <div style={{position: 'absolute', top: y, [align]: x, width: size, textAlign: 'center', opacity: frame >= start ? 1 : 0, transform: `scale(${sp})`}}>
      <Img src={staticFile(src)} style={{width: size, height: size, display: 'block', borderRadius: size * 0.22}} />
      <div style={{marginTop: 10, fontFamily: SANS, fontWeight: 700, fontSize: 26, color}}>{label}</div>
    </div>
  );
};

const Scene1: React.FC = () => {
  const t = useT();
  const tMeet = cue(3, 1);
  const move = ease(clamp01((t - tMeet) / 0.5));
  const subTop = 300 + move * 188;
  return (
    <>
      <Layer>
        <Ink d="M 100 600 C 190 548, 530 548, 620 600" at={cue(2, 4)} dur={1.0} stroke={BLUE} w={4} dash />
        <Ink d="M 604 580 L 624 604 L 596 610" at={cue(2, 4) + 0.9} dur={0.3} stroke={BLUE} w={4} />
        <Spark x={90} y={360} at={cue(3, 1) + 0.3} /><Spark x={640} y={380} s={22} at={cue(3, 1) + 0.5} />
      </Layer>
      <AppIcon src="logos/chatgpt-icon.png" x={36} y={610} size={130} at={cue(0, 1)} label="ChatGPT" color={MUTED} align="left" />
      <AppIcon src="logos/claude-icon.png" x={36} y={610} size={130} at={cue(3, 1)} label="Claude" color={BLUE} align="right" />
      <Reveal at={cue(2, 4)} style={{position: 'absolute', top: subTop, left: 0, right: 0, textAlign: 'center'}}>
        <Bold size={42}>Another </Bold><Ital size={58}>powerful AI</Ital>
      </Reveal>
      <div style={{position: 'absolute', top: 300, left: 0, right: 0, textAlign: 'center', lineHeight: 1.0}}>
        <Reveal at={tMeet}><Bold size={66}>Meet</Bold></Reveal>
        <div style={{marginTop: 2}}><WriteOn at={tMeet + 0.2} dur={0.8}><Ital size={100}>Claude.</Ital></WriteOn></div>
      </div>
    </>
  );
};

const Scene2: React.FC = () => (
  <>
    <Layer>
      <Icon k="calendar" x={316} y={330} size={92} at={cue(5, 0)} stroke={INK} fill={BLUE_SOFT} />
      <Icon k="building" x={540} y={650} size={120} at={cue(5, 2)} stroke={INK} fill={BLUE_SOFT} />
      <Ink d="M 470 1180 L 540 1130 L 580 1150 L 640 1060 L 690 1000" at={cue(6, 3)} dur={1.6} stroke={BLUE} w={6} />
      <Ink d="M 664 998 L 692 998 L 692 1026" at={cue(6, 3) + 1.5} dur={0.4} stroke={BLUE} w={6} />
      <Spark x={450} y={900} at={cue(6, 0)} /><Spark x={680} y={880} s={22} at={cue(6, 1)} /><Spark x={500} y={1040} s={14} at={cue(6, 4)} />
      <Ink d="M 470 1210 H 700" at={cue(6, 3) - 0.2} dur={0.6} stroke={LINE} w={3} />
    </Layer>
    <div style={{position: 'absolute', top: 300, left: 300, right: 36, textAlign: 'right', lineHeight: 1.0}}>
      <Reveal at={cue(5, 0)}><Bold size={52}>Founded in</Bold></Reveal>
      <div style={{marginTop: 4}}><WriteOn at={cue(5, 0) + 0.15} dur={0.8}><Ital size={120}>2021.</Ital></WriteOn></div>
    </div>
    <Logo src="logos/anthropic.png" x={36} y={480} w={330} at={cue(5, 2)} align="right" />
  </>
);

const Item: React.FC<{y: number; at: number; icon: string; a: string; b?: string}> = ({y, at, icon, a, b}) => (
  <>
    <Layer><Icon k={icon} x={36} y={y + 8} size={52} at={at} stroke={INK} fill={BLUE_SOFT} /></Layer>
    <div style={{position: 'absolute', top: y, left: 108, whiteSpace: 'nowrap'}}>
      <Reveal at={at} dx={-24} dy={0}>
        <Bold size={44}>{a}</Bold>
        {b && <span style={{marginLeft: 14}}><Ital size={58}>{b}</Ital></span>}
      </Reveal>
    </div>
  </>
);

const Scene3: React.FC = () => {
  const items = [
    {icon: 'pen', a: 'Write', b: 'texts', at: cue(8, 0)},
    {icon: 'bulb', a: 'Generate', b: 'ideas', at: cue(9, 1)},
    {icon: 'code', a: 'Write', b: 'code', at: cue(10, 0)},
    {icon: 'doc', a: 'Analyse', b: 'files', at: cue(11, 1)},
  ];
  return (
    <>
      {items.map((it, i) => <Item key={i} y={300 + i * 92} {...it} />)}
      <Layer>
        {/* big drawing on the free right-top area, changes with each word */}
        <Big k="pen" at={items[0].at} until={items[1].at} />
        <Big k="bulb" at={items[1].at} until={items[2].at} />
        <Big k="code" at={items[2].at} until={items[3].at} />
        <Big k="doc" at={items[3].at} until={999} />
        <Spark x={420} y={310} at={items[0].at} /><Spark x={690} y={600} s={20} at={items[2].at} />
      </Layer>
    </>
  );
};
const Big: React.FC<{k: string; at: number; until: number}> = ({k, at, until}) => {
  const t = useT();
  if (t < at || t > until + 0.25) return null;
  const out = until === 999 ? 1 : 1 - clamp01((t - until) / 0.25);
  return (
    <g opacity={out}>
      <Icon k={k} x={470} y={310} size={190} at={at + 0.05} dur={1.0} stroke={INK} fill={BLUE_SOFT} />
    </g>
  );
};

const Scene4: React.FC = () => {
  const t = useT();
  const tGood = cue(16, 1);
  const q = 1 - clamp01((t - tGood) / 0.3);
  return (
    <>
      <div style={{position: 'absolute', top: 290, left: 300, right: 36, textAlign: 'right', lineHeight: 1.0}}>
        <Reveal at={cue(14, 0)}><Bold size={56}>Ask better</Bold></Reveal>
        <div style={{marginTop: 2}}><WriteOn at={cue(14, 0) + 0.2} dur={0.8}><Ital size={96}>questions.</Ital></WriteOn></div>
      </div>
      <div style={{position: 'absolute', top: 500, left: 300, right: 36, textAlign: 'right', lineHeight: 1.0}}>
        <Reveal at={tGood}><Bold size={56}>Get better</Bold></Reveal>
        <div style={{marginTop: 2}}><WriteOn at={tGood + 0.2} dur={0.8}><Ital size={96}>results.</Ital></WriteOn></div>
      </div>
      <Layer>
        <g opacity={q}>
          <Icon k="question" x={480} y={700} size={200} at={cue(13, 2)} stroke={INK} fill={BLUE_SOFT} />
          <Icon k="question" x={430} y={960} size={70} at={cue(14, 0)} stroke={BLUE} />
          <Icon k="question" x={620} y={980} size={80} at={cue(15, 0)} stroke={BLUE} />
        </g>
        <Icon k="check" x={470} y={720} size={220} at={tGood + 0.1} dur={0.9} stroke={BLUE} />
        <Ticks x={580} y={830} at={tGood + 0.9} n={10} r0={150} r1={200} />
        <Spark x={690} y={700} at={tGood + 1.0} /><Spark x={440} y={1010} s={20} at={tGood + 1.2} />
      </Layer>
    </>
  );
};

const Scene5: React.FC = () => {
  const rows = [
    {at: cue(17, 2), a: 'Learn', b: 'Claude.'},
    {at: cue(19, 3), a: 'Work', b: 'smarter.'},
    {at: cue(20, 1), a: 'Step by', b: 'step.'},
  ];
  const stairs = [
    'M 440 560 H 500 V 500',
    'M 500 500 H 560 V 440',
    'M 560 440 H 620 V 380',
    'M 620 380 H 690 V 320',
  ];
  const sAt = [cue(17, 2) + 0.2, cue(18, 1), cue(19, 3), cue(20, 1)];
  return (
    <>
      {rows.map((r, i) => (
        <div key={i} style={{position: 'absolute', top: 290 + i * 115, left: 36, whiteSpace: 'nowrap', lineHeight: 1}}>
          <Reveal at={r.at} dx={-24} dy={0}><Bold size={52}>{r.a}</Bold><span style={{marginLeft: 16}}><WriteOn at={r.at + 0.15} dur={0.7}><Ital size={76}>{r.b}</Ital></WriteOn></span></Reveal>
        </div>
      ))}
      <Layer>
        {stairs.map((d, i) => <Ink key={i} d={d} at={sAt[i]} dur={0.7} stroke={INK} w={5} />)}
        <Ink d="M 690 320 V 260" at={cue(20, 2)} dur={0.4} stroke={BLUE} w={5} />
        <Ink d="M 690 262 L 650 278 L 690 294" at={cue(20, 2) + 0.35} dur={0.4} stroke={BLUE} w={5} fill={BLUE} />
        <Ink d="M 440 560 H 700" at={cue(17, 2)} dur={0.6} stroke={LINE} w={3} />
        <Spark x={430} y={400} at={cue(18, 0)} /><Spark x={560} y={300} s={20} at={cue(19, 1)} />
      </Layer>
    </>
  );
};

const Scene6: React.FC = () => (
  <>
    <div style={{position: 'absolute', top: 280, left: 0, right: 0, textAlign: 'center', lineHeight: 1}}>
      <Reveal at={cue(22, 2)}><Bold size={80}>Master</Bold></Reveal>
      <div style={{marginTop: 2}}><WriteOn at={cue(22, 2) + 0.2} dur={0.8}><Ital size={112}>Claude.</Ital></WriteOn></div>
    </div>
    <div style={{position: 'absolute', top: 470, left: 0, right: 0, textAlign: 'center'}}>
      <Reveal at={cue(23, 0)}><Bold size={46}>Let’s get <span style={{color: BLUE, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 400, fontSize: 62}}>started!</span></Bold></Reveal>
    </div>
    <Layer>
      <Underline x={140} y={540} w={440} at={cue(23, 1)} dur={0.8} />
      <Ticks x={360} y={420} at={cue(23, 2)} n={14} r0={210} r1={270} />
      <Spark x={90} y={330} at={cue(22, 2)} /><Spark x={640} y={350} s={24} at={cue(23, 0)} /><Spark x={110} y={600} at={cue(23, 1)} /><Spark x={630} y={590} s={18} at={cue(23, 2)} />
    </Layer>
  </>
);

const SCENES: {C: React.FC; side: Side}[] = [
  {C: Scene1, side: 'center'},
  {C: Scene2, side: 'left'},
  {C: Scene3, side: 'right'},
  {C: Scene4, side: 'left'},
  {C: Scene5, side: 'right'},
  {C: Scene6, side: 'center'},
];

const SceneFade: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 6, dur - 6, dur], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

export const ClaudeIntro: React.FC = () => (
  <AbsoluteFill style={{background: '#fff'}}>
    <Background />
    <Audio src={staticFile('audio/voiceover-1.25x.mp3')} />
    {SCENES.map(({C, side}, i) => (
      <Sequence key={i} from={F[i]} durationInFrames={F[i + 1] - F[i]} name={`Scene ${i + 1}`}>
        <Ctx.Provider value={F[i]}>
          <SceneFade dur={F[i + 1] - F[i]}>
            <Header idx={i} />
            <Caption scene={i + 1} />
            <C />
            <Character side={side} />
          </SceneFade>
        </Ctx.Provider>
      </Sequence>
    ))}
  </AbsoluteFill>
);
