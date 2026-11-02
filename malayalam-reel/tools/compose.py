"""compose.py timing  <voice_timing.json> <out_dir>        -> out_dir/timing.json
   compose.py audio   <voice.wav> <voice_timing.json> <out_dir> -> out_dir/final_audio.wav (voice + sfx)
"""
import sys, json, subprocess, wave
import numpy as np

SR = 44100
OFF = 0.45                      # voice starts this long after the first frame
SKIP = {11, 14, 15, 16, 17, 20}  # scenes cut from the edit (no narration / no meaning)
G = 0.0                         # no silence inserted any more
ES = [0, 2.6, 4.6, 7.6, 11.6, 20.2, 26, 32.2, 34.6, 36.6, 38, 41, 42.4, 44.2, 48.2, 50.2, 52.2, 54.4, 56.2, 60.2, 64.4, 66.4, 70.2, 74.2, 76.8]
LS = [0, 4.5, 7, 11, 15, 19, 22, 25, 28, 31, 33, 38, 41, 44, 55, 59.5, 65, 69, 73, 76, 81.5]


def timing(vt, out):
    V = json.load(open(vt)); L = {l['line']: l for l in V['lines']}
    cstarts = {}
    for c in V['clauses']: cstarts.setdefault(c['line'], []).append(c['start'])
    split = 1e9

    def vt2video(t): return t + OFF + (G if t >= split else 0)

    def map_en(t):
        i = max(k for k in range(20) if LS[k] <= t); ln = i + 1
        f = (t - LS[i]) / (LS[i + 1] - LS[i]); a, b = L[ln]['start'], L[ln]['end']
        nt = a + f * (b - a)
        near = min(cstarts[ln], key=lambda c: abs(c - nt))
        return near if abs(near - nt) < 0.7 else nt

    starts = []
    for k, t in enumerate(ES):
        if k == 0: starts.append(0.0)
        elif k in SKIP: starts.append(None)
        elif k == 18: starts.append(vt2video(L[15]['start']) - 0.12)
        elif k == 13: starts.append(vt2video(L[14]['start']) - 0.12)
        elif k == 12: starts.append(vt2video(L[13]['start']) - 0.12)
        else: starts.append(vt2video(map_en(t)) - 0.12)
    prev = 0.0
    for k in range(len(starts)):                         # monotonic, min 0.9 s for kept scenes
        if starts[k] is None: continue
        starts[k] = max(starts[k], prev + (0.9 if k else 0)); prev = starts[k]
    end = V['duration'] + OFF + 1.2
    nxt = end; scenes = [None] * len(starts)
    for k in range(len(starts) - 1, -1, -1):             # skipped scenes collapse onto the next kept one
        if starts[k] is None: scenes[k] = {'s': nxt, 'e': nxt, 'skip': True}
        else: scenes[k] = {'s': starts[k], 'e': nxt}; nxt = starts[k]
    json.dump({'scenes': scenes, 'duration': end, 'voice_offset': OFF, 'split': split, 'gap': G}, open(f'{out}/timing.json', 'w'), indent=1)
    print('duration %.1f' % end); print(' '.join('%d:%.1f' % (k, s['s']) for k, s in enumerate(scenes)))


def synth(name, expr, dur, post=''):
    p = f'/tmp/sfx_{name}.wav'
    src = expr if expr.startswith('anoisesrc') else f"aevalsrc='{expr}':d={dur}:s={SR}"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', src, '-af', post or 'anull', '-ac', '1', '-ar', str(SR), '-t', str(dur), p], check=True)
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; w.close()
    return a / max(1e-6, np.abs(a).max())


def audio(voice, vt, out):
    T = json.load(open(f'{out}/timing.json')); ev = json.load(open(f'{out}/events.json'))
    w = wave.open(voice); v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; w.close()
    sp = int(T['split'] * SR)
    voice_t = np.concatenate([np.zeros(int(OFF * SR)), v[:sp], np.zeros(int(G * SR)), v[sp:]])
    total = int(T['duration'] * SR); mix = np.zeros(total, dtype=np.float32); mix[:min(total, len(voice_t))] = voice_t[:total] * 0.95
    cw = wave.open(f'{out}/click.wav'); ck = np.frombuffer(cw.readframes(cw.getnframes()), dtype=np.int16).astype(np.float32) / 32768; cw.close(); ck = ck / max(1e-6, np.abs(ck).max())
    seen = {}; keep = []
    for e in sorted(ev, key=lambda e: e['t']):
        if e['type'] == 'pop':
            n = seen.get(e['scene'], 0)
            if n >= 2: continue
            seen[e['scene']] = n + 1; e = dict(e, type='click')
        keep.append(e)
    ev = keep
    sfx = {
        'whoosh': (synth('whoosh', 'anoisesrc=d=0.6:c=pink:r=44100:a=0.9', 0.6, 'highpass=f=350,lowpass=f=5500,afade=t=in:d=0.28,afade=t=out:st=0.28:d=0.32'), 0.16),
        'click': (ck, 0.55),
        'ding': (synth('ding', '(sin(2*PI*1319*t)+0.5*sin(2*PI*1976*t)+0.25*sin(2*PI*2637*t))*exp(-t*4.5)', 1.2), 0.18),
    }
    last = T['scenes'][-1]['s']
    ev = ev + [{'t': last + 0.35, 'type': 'ding'}]
    for e in ev:
        a, g = sfx[e['type']]; i = int(max(0, e['t']) * SR)
        if e['type'] == 'whoosh': i = max(0, i - int(0.12 * SR))
        seg = a[:max(0, total - i)] * g; mix[i:i + len(seg)] += seg
    mix = np.clip(mix, -0.98, 0.98)
    p = f'{out}/final_audio_raw.wav'
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-af', 'loudnorm=I=-15:TP=-1.5:LRA=9', '-ar', '44100', f'{out}/final_audio.wav'], check=True)
    print('audio ok', len(ev), 'events')


if __name__ == '__main__':
    if sys.argv[1] == 'timing': timing(sys.argv[2], sys.argv[3])
    else: audio(sys.argv[2], sys.argv[3], sys.argv[4])
