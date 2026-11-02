"""compose.py timing  <voice_timing.json> <out_dir>        -> out_dir/timing.json
   compose.py audio   <voice.wav> <voice_timing.json> <out_dir> -> out_dir/final_audio.wav (voice + sfx)
"""
import sys, json, subprocess, wave
import numpy as np

SR = 44100
OFF = 0.45                      # voice starts this long after the first frame
GAPS = [1.0, 1.0, 1.2]          # three silent beats ("most important line / inspired / your edits")
PAD = 0.2
G = PAD + sum(GAPS) + PAD       # total silence inserted into the voice
ES = [0, 2.6, 4.6, 7.6, 11.6, 20.2, 26, 32.2, 34.6, 36.6, 38, 41, 42.4, 44.2, 48.2, 50.2, 52.2, 54.4, 56.2, 60.2, 64.4, 66.4, 70.2, 74.2, 76.8]
LS = [0, 4.5, 7, 11, 15, 19, 22, 25, 28, 31, 33, 38, 41, 44, 55, 59.5, 65, 69, 73, 76, 81.5]


def timing(vt, out):
    V = json.load(open(vt)); L = {l['line']: l for l in V['lines']}
    cstarts = {}
    for c in V['clauses']: cstarts.setdefault(c['line'], []).append(c['start'])
    split = L[14]['end'] + 0.1

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
        elif 14 <= k <= 16: starts.append(None)
        elif k == 17: starts.append(vt2video(L[15]['start']) - 0.1)
        elif k == 13: starts.append(vt2video(L[14]['start']) - 0.1)
        else: starts.append(vt2video(map_en(t)) - 0.12)
    g0 = L[14]['end'] + OFF + 0.1 + PAD
    starts[14] = g0; starts[15] = g0 + GAPS[0]; starts[16] = g0 + GAPS[0] + GAPS[1]
    for k in range(1, len(starts)):                      # keep monotonic, min 0.9 s
        starts[k] = max(starts[k], starts[k - 1] + (0.9 if k not in (14, 15, 16) else 0))
    end = V['duration'] + OFF + G + 1.6
    scenes = [{'s': starts[k], 'e': (starts[k + 1] if k + 1 < len(starts) else end)} for k in range(len(starts))]
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
    sfx = {
        'whoosh': (synth('whoosh', 'anoisesrc=d=0.6:c=pink:r=44100:a=0.9', 0.6, 'highpass=f=350,lowpass=f=5500,afade=t=in:d=0.28,afade=t=out:st=0.28:d=0.32'), 0.16),
        'pop': (synth('pop', 'sin(2*PI*(380+1100*exp(-t*38))*t)*exp(-t*26)', 0.2), 0.20),
        'click': (synth('click', '(random(0)-0.5)*exp(-t*160)+0.6*sin(2*PI*1800*t)*exp(-t*90)', 0.08, 'highpass=f=900'), 0.30),
        'ding': (synth('ding', '(sin(2*PI*1319*t)+0.5*sin(2*PI*1976*t)+0.25*sin(2*PI*2637*t))*exp(-t*4.5)', 1.2), 0.18),
    }
    last = T['scenes'][-1]['s']
    ev = ev + [{'t': last + 0.35, 'type': 'ding'}, {'t': T['scenes'][17]['s'] + 0.05, 'type': 'ding'}]
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
