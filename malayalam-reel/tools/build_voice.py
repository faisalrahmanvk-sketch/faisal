"""Tighten pauses + slightly speed up an ElevenLabs take, and align script clauses to it.

usage: build_voice.py take.mp3 take.sil out_dir [tempo] [gap]
  take.sil = output of: ffmpeg -i take.mp3 -af silencedetect=noise=-38dB:d=0.3 -f null -  (reduced to 'silence_start N'/'silence_end N' lines)
Writes out_dir/voice.wav and out_dir/voice_timing.json (clause + line start times on the NEW timeline).
"""
import re, sys, json, subprocess, wave
import numpy as np

take, silf, out = sys.argv[1], sys.argv[2], sys.argv[3]
tempo = float(sys.argv[4]) if len(sys.argv) > 4 else 1.08
GAP = float(sys.argv[5]) if len(sys.argv) > 5 else 0.28
SR = 44100
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', take, '-ac', '1', '-ar', str(SR), f'{out}/raw.wav'], check=True)
w = wave.open(f'{out}/raw.wav'); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32); w.close()
total = len(x) / SR

st, en = [], []
for l in open(silf):
    k, v = l.split(); (st if k == 'silence_start' else en).append(float(v))
segs, cur = [], 0.0
for i, s in enumerate(st):
    if s - cur > 0.15: segs.append((cur, s))
    cur = en[i] if i < len(en) else total
if total - cur > 0.15: segs.append((cur, total))

# script clauses (Malayalam column of script.md)
txt = open('/home/user/faisal/malayalam-reel/script.md').read()
rows = [r.split('|') for r in txt.splitlines() if r.startswith('| ') and r.split('|')[1].strip().replace('.', '').isdigit()]
cl, line_of = [], []
for li, c in enumerate(rows, 1):
    for p in [p for p in re.split(r'(?<=[,.:])\s+', c[3].strip()) if p.strip()]:
        cl.append(re.sub(r'[\s,.:"?!]', '', p)); line_of.append(li)
n, m = len(segs), len(cl)
dur = [b - a for a, b in segs]; ch = [len(c) for c in cl]
rate = sum(dur) / sum(ch)
INF = 1e18
dp = [[INF] * (m + 1) for _ in range(n + 1)]; bk = [[0] * (m + 1) for _ in range(n + 1)]; dp[0][0] = 0
for i in range(1, n + 1):
    for j in range(i, m + 1):
        for k in range(i - 1, j):
            c = sum(ch[k:j]); v = dp[i - 1][k] + (dur[i - 1] - rate * c) ** 2 / max(c, 1)
            if v < dp[i][j]: dp[i][j] = v; bk[i][j] = k
j, groups = m, []
for i in range(n, 0, -1): k = bk[i][j]; groups.append((k, j)); j = k
groups.reverse()

# build audio: speech segments joined by GAP seconds of silence
pieces, newstart, t = [], [], 0.0
for k, (a, b) in enumerate(segs):
    s0 = max(0, a - .03); s1 = min(total, b + .06)
    c = x[int(s0 * SR):int(s1 * SR)].copy(); f = int(.01 * SR); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
    newstart.append(t + (a - s0)); pieces.append(c); t += len(c) / SR
    if k < n - 1: pieces.append(np.zeros(int(GAP * SR), dtype=np.float32)); t += GAP
y = np.concatenate(pieces)
pre = f'{out}/voice_pre.wav'
w = wave.open(pre, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pre, '-af', f'atempo={tempo}', f'{out}/voice.wav'], check=True)

# clause times on the new timeline
clauses = []
for si, (a, b) in enumerate(groups):
    tot = sum(ch[a:b]); acc = 0
    for ci in range(a, b):
        s = newstart[si] + (acc / tot) * dur[si]; acc += ch[ci]; e = newstart[si] + (acc / tot) * dur[si]
        clauses.append({'clause': ci, 'line': line_of[ci], 'start': s / tempo, 'end': e / tempo})
lines = {}
for c in clauses:
    L = lines.setdefault(c['line'], {'line': c['line'], 'start': c['start'], 'end': c['end']}); L['end'] = c['end']
json.dump({'tempo': tempo, 'duration': t / tempo, 'lines': list(lines.values()), 'clauses': clauses}, open(f'{out}/voice_timing.json', 'w'), indent=1)
print('segments', n, 'clauses', m, 'duration %.1f' % (t / tempo))
for L in lines.values(): print(L['line'], '%.1f-%.1f' % (L['start'], L['end']))
