import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/inter/800.css';
import '@fontsource/instrument-serif/400-italic.css';
import {Layer, DrawPath, DashedDraw, Ring, Underline, Ripples, Orbit, Burst, Sparkle, CheckRing, Wave, useProg, TypeBubble} from './Anim';

const FPS = 30;
const BLUE = '#2459E8';
const INK = '#0B0B0F';
const MUTED = '#6B7280';
const SANS = 'Inter, sans-serif';
const SERIF = "'Instrument Serif', serif";

// Scene boundaries (seconds) measured from the voice-over silences.
const B = [0, 10.7, 21.65, 36.95, 43.64, 52.85, 59.09];
const F = B.map((s) => Math.round(s * FPS));
export const TOTAL_FRAMES = F[F.length - 1];

type Side = 'left' | 'right' | 'center';
const POSE: Record<Side, {src: string; h: number; ar: number}> = {
  center: {src: 'chars/pose-center-thinking.png', h: 780, ar: 832 / 1920},
  left: {src: 'chars/pose-left.png', h: 660, ar: 1024 / 1536},
  right: {src: 'chars/pose-right.png', h: 660, ar: 1024 / 1536},
};

const useIn = (at: number, dur = 14) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [at * FPS, at * FPS + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)});
};

const Reveal: React.FC<{at: number; dx?: number; dy?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({at, dx = 0, dy = 28, children, style}) => {
  const p = useIn(at);
  return <div style={{opacity: p, transform: `translate(${(1 - p) * dx}px, ${(1 - p) * dy}px)`, ...style}}>{children}</div>;
};

const Background: React.FC = () => (
  <AbsoluteFill style={{background: '#FFFFFF', backgroundImage: 'radial-gradient(#D9DEE8 1.4px, transparent 1.4px)', backgroundSize: '32px 32px'}}>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 35%, rgba(255,255,255,0) 30%, rgba(255,255,255,0.85) 100%)'}} />
  </AbsoluteFill>
);

const Progress: React.FC<{idx: number}> = ({idx}) => (
  <div style={{position: 'absolute', top: 56, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 10, fontFamily: SANS, fontWeight: 600, fontSize: 18, color: MUTED}}>
    <span style={{marginRight: 6}}>{idx + 1}/6</span>
    {[0, 1, 2, 3, 4, 5].map((i) => (
      <div key={i} style={{width: i === idx ? 44 : 30, height: 16, borderRadius: 9, border: `2px solid ${i <= idx ? BLUE : '#CBD2E0'}`, background: i < idx ? BLUE : '#fff', position: 'relative'}}>
        {i === idx && <div style={{position: 'absolute', top: 1, left: 24, width: 10, height: 10, borderRadius: 5, background: BLUE}} />}
      </div>
    ))}
  </div>
);

const Character: React.FC<{side: Side}> = ({side}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = POSE[side];
  const w = p.h * p.ar;
  const s = spring({frame: frame - 2, fps, config: {damping: 16, stiffness: 120}});
  const float = Math.sin(frame / 18) * 5;
  const left = side === 'left' ? 4 : side === 'right' ? 720 - w - 4 : (720 - w) / 2;
  return (
    <div style={{position: 'absolute', left, bottom: 14 - (1 - s) * 80 - float, width: w, height: p.h, opacity: s, filter: 'drop-shadow(0 18px 22px rgba(20,30,70,0.18))'}}>
      <Img src={staticFile(p.src)} style={{width: '100%', height: '100%'}} />
    </div>
  );
};

const Title: React.FC<{a?: string; b: string; at?: number; align?: 'left' | 'right' | 'center'; size?: number}> = ({a, b, at = 0.3, align = 'center', size = 92}) => (
  <Reveal at={at} style={{textAlign: align, lineHeight: 1.0}}>
    {a && <div style={{fontFamily: SANS, fontWeight: 800, fontSize: size * 0.8, color: INK, letterSpacing: -1}}>{a}</div>}
    <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: size, color: BLUE, marginTop: 4}}>{b}</div>
  </Reveal>
);

// Layout helper: text column on the side opposite the character.
const Opp: React.FC<{side: Side; children: React.ReactNode; top?: number}> = ({side, children, top = 150}) => (
  <div style={{position: 'absolute', top, left: side === 'left' ? 360 : 30, right: side === 'left' ? 30 : 360, display: 'flex', flexDirection: 'column', gap: 22, alignItems: side === 'left' ? 'flex-end' : 'flex-start'}}>{children}</div>
);

const Card: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div style={{background: '#fff', border: '1.5px solid #E3E7F0', borderRadius: 22, boxShadow: '0 12px 30px rgba(30,50,110,0.10)', ...style}}>{children}</div>
);

const Icon: React.FC<{k: 'pen' | 'bulb' | 'code' | 'file' | 'q' | 'check'; color?: string}> = ({k, color = BLUE}) => {
  const p = {fill: 'none', stroke: color, strokeWidth: 2.2, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  return (
    <svg width="46" height="46" viewBox="0 0 24 24">
      {k === 'pen' && <path {...p} d="M4 20l4-1 11-11-3-3L5 16l-1 4zM14 6l3 3" />}
      {k === 'bulb' && <path {...p} d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z" />}
      {k === 'code' && <path {...p} d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16" />}
      {k === 'file' && <path {...p} d="M6 3h8l5 5v13H6zM14 3v5h5M9 13h7M9 17h7" />}
      {k === 'q' && <path {...p} d="M9 9a3 3 0 116 0c0 2-3 2-3 4M12 17v.5" />}
      {k === 'check' && <path {...p} d="M5 12l5 5 9-10" />}
    </svg>
  );
};

// ---------- Scenes ----------
const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Layer>
        <Ripples cx={360} cy={880} max={300} at={0.4} />
        <Ring cx={360} cy={880} r={300} at={0.6} dur={1.4} dashed />
        <Orbit cx={360} cy={880} r={300} at={1.5} n={3} speed={0.015} showRing={false} />
        <Underline x={170} y={496} w={380} at={1.6} />
        <Sparkle x={90} y={200} at={1.0} /><Sparkle x={640} y={260} s={22} at={1.4} /><Sparkle x={600} y={560} at={2.0} /><Sparkle x={110} y={600} s={20} at={2.4} />
        <DashedDraw d="M 178 729 C 270 590, 470 610, 556 776" at={7.0} dur={1.1} />
        <circle cx={556} cy={776} r={7} fill={BLUE} opacity={useProg(8.0, 0.2)} />
      </Layer>
      <div style={{position: 'absolute', top: 150, left: 0, right: 0}}>
        <Title a="MEET" b="CLAUDE" size={150} />
      </div>
      <Reveal at={1.0} style={{position: 'absolute', top: 440, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 34, letterSpacing: 4, color: INK}}>
        ANOTHER POWERFUL AI
      </Reveal>
      <TypeBubble at={0.5} text="Using ChatGPT?" style={{left: 24, top: 600}} size={24} hideAfter={6.5} />
      <TypeBubble at={3.6} text="another AI exists…" style={{right: 24, top: 640}} size={24} hideAfter={6.5} dark />
      <Reveal at={0.8} dx={-40} dy={0} style={{position: 'absolute', left: 30, top: 700}}>
        <Card style={{padding: '14px 26px', fontFamily: SANS, fontWeight: 600, fontSize: 28, color: MUTED}}>ChatGPT</Card>
      </Reveal>
      <Reveal at={6.7} dx={40} dy={0} style={{position: 'absolute', right: 30, top: 780}}>
        <Card style={{padding: '14px 26px', fontFamily: SANS, fontWeight: 700, fontSize: 28, color: '#fff', background: BLUE, border: 'none', transform: `scale(${1 + 0.03 * Math.sin(frame / 8)})`}}>Claude</Card>
      </Reveal>
    </>
  );
};

const Scene2: React.FC = () => (
  <>
  <Layer>
    <Underline x={385} y={252} w={300} at={0.9} />
    <DashedDraw d="M 540 640 L 540 1190" at={3.2} dur={1.8} />
    {[720, 900, 1080].map((y, i) => (
      <g key={y} opacity={useProg(3.6 + i * 0.9, 0.3)}>
        <circle cx={540} cy={y} r={18} fill="#fff" stroke={BLUE} strokeWidth={5} />
        <circle cx={540} cy={y} r={7} fill={BLUE} />
      </g>
    ))}
    <Ripples cx={540} cy={1080} max={120} n={2} at={5.4} />
    <Ring cx={540} cy={1080} r={44} at={5.4} dur={0.8} w={4} />
    <Sparkle x={660} y={760} at={4.4} /><Sparkle x={420} y={980} s={20} at={5.0} /><Sparkle x={650} y={1130} s={14} at={6.0} />
    <Orbit cx={540} cy={470} r={165} at={3.0} n={2} speed={0.02} />
  </Layer>
  <TypeBubble at={3.8} text="Use AI" style={{left: 580, top: 698}} size={22} />
  <TypeBubble at={4.8} text="Do more" style={{left: 580, top: 878}} size={22} />
  <TypeBubble at={5.8} text="Easily" style={{left: 580, top: 1058}} size={22} dark />
  <Opp side="left">
    <Title b="ANTHROPIC" at={0.3} align="right" size={76} />
    <Reveal at={1.2} style={{fontFamily: SANS, fontWeight: 700, fontSize: 30, letterSpacing: 3, color: INK, textAlign: 'right'}}>FOUNDED IN 2021</Reveal>
    <Reveal at={2.2} dx={40} style={{marginTop: 30}}>
      <Card style={{padding: '30px 34px', width: 300, textAlign: 'center'}}>
        <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 16, letterSpacing: 3, color: MUTED}}>FOUNDED</div>
        <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 120, color: BLUE, lineHeight: 1.05}}>2021</div>
        <div style={{height: 4, background: '#E3E7F0', borderRadius: 2, marginTop: 14}}>
          <div style={{height: 4, width: `${useIn(3, 60) * 100}%`, background: BLUE, borderRadius: 2}} />
        </div>
      </Card>
    </Reveal>
  </Opp>
  </>
);

const items3: {k: 'pen' | 'bulb' | 'code' | 'file'; t: string; cue: number}[] = [
  {k: 'pen', t: 'WRITE', cue: 3.4},
  {k: 'bulb', t: 'GENERATE IDEAS', cue: 4.6},
  {k: 'code', t: 'WRITE CODE', cue: 5.8},
  {k: 'file', t: 'ANALYSE FILES', cue: 7.6},
];
const Scene3: React.FC = () => {
  const frame = useCurrentFrame();
  const cy = [218, 345, 472, 599];
  const hub = {x: 520, y: 390};
  const ends = [[466, 360], [460, 382], [460, 402], [468, 424]];
  return (
    <>
    <Layer>
      <Ripples cx={hub.x} cy={hub.y} max={140} n={2} at={0.8} />
      <Ring cx={hub.x} cy={hub.y} r={100} at={0.6} dur={1.2} w={4} />
      <Orbit cx={hub.x} cy={hub.y} r={150} at={1.4} n={3} speed={0.022} />
      {items3.map((it, i) => (
        <DashedDraw key={it.t} d={`M 322 ${cy[i]} C 400 ${cy[i]}, 410 ${ends[i][1]}, ${ends[i][0]} ${ends[i][1]}`} at={it.cue} dur={0.7} />
      ))}
      <circle cx={hub.x} cy={hub.y} r={58 * useProg(0.9, 0.5)} fill={BLUE} />
      <g opacity={useProg(1.3, 0.4)} stroke="#fff" strokeWidth={6} strokeLinecap="round">
        {[0, 45, 90, 135].map((a) => (
          <line key={a} x1={hub.x - Math.cos((a * Math.PI) / 180) * 26} y1={hub.y - Math.sin((a * Math.PI) / 180) * 26} x2={hub.x + Math.cos((a * Math.PI) / 180) * 26} y2={hub.y + Math.sin((a * Math.PI) / 180) * 26} />
        ))}
      </g>
      <Burst cx={hub.x} cy={hub.y} at={7.6} r0={110} r1={190} />
    </Layer>
    <TypeBubble at={3.4} text="Write an email…" style={{left: 360, top: 566}} size={22} hideAfter={4.5} />
    <TypeBubble at={4.6} text="Give me ideas…" style={{left: 360, top: 566}} size={22} hideAfter={5.7} />
    <TypeBubble at={5.8} text="Write some code…" style={{left: 360, top: 566}} size={22} hideAfter={7.5} />
    <TypeBubble at={7.6} text="Summarise this file…" style={{left: 360, top: 566}} size={22} dark />
    <div style={{position: 'absolute', top: 170, left: 30, width: 290, display: 'flex', flexDirection: 'column', gap: 26}}>
      {items3.map((it, i) => {
        const on = frame >= it.cue * FPS;
        return (
          <Reveal key={it.t} at={0.4 + i * 0.25} dx={-60} dy={0}>
            <Card style={{padding: '24px 22px', display: 'flex', alignItems: 'center', gap: 16, background: on ? BLUE : '#fff', borderColor: on ? BLUE : '#E3E7F0'}}>
              <Icon k={it.k} color={on ? '#fff' : BLUE} />
              <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 25, color: on ? '#fff' : INK, lineHeight: 1.15}}>{it.t}</div>
            </Card>
          </Reveal>
        );
      })}
    </div>
    </>
  );
};

const Scene4: React.FC = () => {
  const fl = useCurrentFrame();
  const out = 1 - useProg(3.4, 0.4);
  const qs = [[640, 800, 80, 0], [600, 1000, 70, 1.3], [440, 1120, 80, 2.1]];
  return (
  <>
  <Layer>
    {qs.map(([x, y, sz, ph], i) => (
      <text key={i} x={x} y={y + Math.sin(fl / 10 + ph) * 10} fontFamily="Instrument Serif, serif" fontStyle="italic" fontSize={sz} fill={BLUE} opacity={useProg(0.9 + i * 0.4, 0.4) * out} transform={`rotate(${Math.sin(fl / 14 + ph) * 8} ${x} ${y})`}>?</text>
    ))}
    <CheckRing cx={540} cy={950} r={105} at={3.7} />
    <Burst cx={540} cy={950} at={4.6} r0={125} r1={210} />
    <Sparkle x={420} y={680} at={4.8} /><Sparkle x={670} y={780} s={20} at={5.0} />
  </Layer>
  <TypeBubble at={1.0} text="What to ask?" style={{left: 400, top: 760}} size={24} hideAfter={3.4} />
  <TypeBubble at={2.0} text="How to ask?" style={{left: 450, top: 850}} size={24} hideAfter={3.4} />
  <Opp side="left">
    <Reveal at={0.3} style={{textAlign: 'right'}}>
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 56, color: INK, lineHeight: 1.05}}>ASK BETTER</div>
      <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 84, color: BLUE, lineHeight: 1.0}}>QUESTIONS</div>
    </Reveal>
    <Reveal at={3.6} style={{textAlign: 'right', marginTop: 10}}>
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 56, color: INK, lineHeight: 1.05}}>GET BETTER</div>
      <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 84, color: BLUE, lineHeight: 1.0}}>RESULTS</div>
    </Reveal>
    <Reveal at={1.0} dx={40} style={{marginTop: 20}}>
      <Card style={{width: 300, padding: 24, display: 'flex', alignItems: 'center', gap: 16}}>
        <Icon k={useIn(3.6) > 0.5 ? 'check' : 'q'} />
        <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 22, color: INK}}>{useIn(3.6) > 0.5 ? 'Clear answer' : 'Vague answer?'}</div>
      </Card>
    </Reveal>
  </Opp>
  </>
  );
};

const Scene5: React.FC = () => {
  const rows = [
    {t: 'LEARN CLAUDE', at: 0.4},
    {t: 'STEP BY STEP', at: 3.2},
    {t: 'WORK SMARTER', at: 5.8},
  ];
  const arc = (a0: number, a1: number, r: number, cx: number, cy: number) => {
    const t = (a: number) => [cx + Math.cos(((a - 90) * Math.PI) / 180) * r, cy + Math.sin(((a - 90) * Math.PI) / 180) * r];
    const [x0, y0] = t(a0), [x1, y1] = t(a1);
    return `M ${x0} ${y0} A ${r} ${r} 0 0 1 ${x1} ${y1}`;
  };
  const hx = 535, hy = 400;
  return (
    <>
    <Layer>
      <circle cx={hx} cy={hy} r={110} fill="none" stroke="#E3E7F0" strokeWidth={14} />
      <DrawPath d={arc(2, 118, 110, hx, hy)} at={0.6} dur={0.9} w={14} />
      <DrawPath d={arc(122, 238, 110, hx, hy)} at={3.4} dur={0.9} w={14} />
      <DrawPath d={arc(242, 358, 110, hx, hy)} at={6.0} dur={0.9} w={14} />
      <Orbit cx={hx} cy={hy} r={160} at={1.0} n={2} speed={0.016} />
      <CheckRing cx={hx} cy={hy} r={52} at={6.9} />
      <Burst cx={hx} cy={hy} at={7.5} r0={130} r1={210} />
      <DashedDraw d="M 75 300 L 75 330" at={3.2} dur={0.3} />
      <DashedDraw d="M 75 424 L 75 458" at={5.8} dur={0.3} />
      <Sparkle x={380} y={230} at={1.2} /><Sparkle x={690} y={560} s={20} at={3.0} />
    </Layer>
    <TypeBubble at={0.8} text="Use Claude" style={{left: 440, top: 560}} size={22} hideAfter={3.3} />
    <TypeBubble at={3.6} text="Write prompts" style={{left: 430, top: 560}} size={22} hideAfter={5.9} />
    <TypeBubble at={6.2} text="Save time" style={{left: 450, top: 560}} size={22} dark />
    <div style={{position: 'absolute', top: 200, left: 30, width: 300, display: 'flex', flexDirection: 'column', gap: 34}}>
      {rows.map((r, i) => (
        <Reveal key={r.t} at={r.at} dx={-60} dy={0}>
          <Card style={{padding: '24px 22px', display: 'flex', alignItems: 'center', gap: 16}}>
            <div style={{width: 46, height: 46, borderRadius: 23, background: BLUE, color: '#fff', fontFamily: SANS, fontWeight: 800, fontSize: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>{i + 1}</div>
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 28, color: INK, lineHeight: 1.1}}>{r.t}</div>
          </Card>
        </Reveal>
      ))}
    </div>
    </>
  );
};

const Scene6: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - 4.45 * FPS, fps, config: {damping: 12}});
  return (
    <>
      <Layer>
        <Ripples cx={360} cy={900} max={360} at={0.2} />
        <Ring cx={360} cy={900} r={310} at={0.5} dur={1.4} dashed />
        <Orbit cx={360} cy={900} r={310} at={1.2} n={3} speed={0.014} showRing={false} />
        <Burst cx={360} cy={430} at={4.45} n={16} r0={190} r1={300} />
        <Sparkle x={100} y={300} at={0.8} /><Sparkle x={640} y={340} s={22} at={1.2} /><Sparkle x={80} y={720} at={2.0} /><Sparkle x={650} y={700} s={20} at={2.4} />
      </Layer>
      <TypeBubble at={1.5} text="Use it right" style={{left: 24, top: 640}} size={22} />
      <TypeBubble at={5.2} text="Let’s go!" style={{right: 24, top: 640}} size={26} dark />
      <div style={{position: 'absolute', top: 150, left: 0, right: 0}}>
        <Title a="MASTER" b="CLAUDE" size={118} at={0.3} />
      </div>
      <div style={{position: 'absolute', top: 392, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: frame > 4.4 * FPS ? 1 : 0}}>
        <div style={{transform: `scale(${0.6 + 0.4 * s})`, background: BLUE, color: '#fff', fontFamily: SANS, fontWeight: 800, fontSize: 34, padding: '18px 40px', borderRadius: 18, boxShadow: '0 16px 34px rgba(36,89,232,0.35)'}}>LET’S GET STARTED</div>
      </div>
    </>
  );
};

const SCENES: {C: React.FC; side: Side}[] = [
  {C: Scene1, side: 'center'},
  {C: Scene2, side: 'left'},
  {C: Scene3, side: 'right'},
  {C: Scene4, side: 'left'},
  {C: Scene5, side: 'right'},
  {C: Scene6, side: 'center'},
];

const Wipe: React.FC = () => {
  const f = useCurrentFrame();
  const x = f < 8 ? interpolate(f, [0, 8], [-720, 0]) : interpolate(f, [8, 17], [0, 720], {extrapolateRight: 'clamp'});
  if (f > 17) return null;
  return <AbsoluteFill style={{background: BLUE, transform: `translateX(${x}px)`}} />;
};

export const ClaudeIntro: React.FC = () => (
  <AbsoluteFill style={{background: '#fff'}}>
    <Background />
    <Audio src={staticFile('audio/voiceover.mp3')} />
    {SCENES.map(({C, side}, i) => (
      <Sequence key={i} from={F[i]} durationInFrames={F[i + 1] - F[i]} name={`Scene ${i + 1}`}>
        <AbsoluteFill>
          <Progress idx={i} />
          <C />
          <Character side={side} />
          {i > 0 && <Wipe />}
        </AbsoluteFill>
      </Sequence>
    ))}
  </AbsoluteFill>
);
