"""Trim each ElevenLabs line, speed to 1.25x, concatenate with gaps; write timeline.json."""
import subprocess, json, pathlib
A = pathlib.Path(__file__).resolve().parent.parent / "audio"
SPEED = 1.25
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
def prep(name):
    out = A/"proc"/f"{name}.wav"; out.parent.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(A/f"{name}.mp3"),"-af",
      f"silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,atempo={SPEED}",
      "-ar","44100","-ac","1",str(out)],check=True)
    return out, dur(out)
# (clip file, clip key, gap after)
SEQ = []
for s in (1,2,3,4):
    SEQ += [(f"s{s}-i1",0.14),(f"s{s}-i2",0.14),("s1-q" if s%2 else "s2-q",0.26),(f"s{s}-a",0.22),(f"s{s}-b",0.55)]
t = 0.35; tl = []; parts = []
for name,gap in SEQ:
    p,d = prep(name); tl.append({"clip":name,"start":round(t,3),"end":round(t+d,3)}); parts.append((p,t)); t += d + gap
total = round(t,2)
ins=[]; fl=[]
for i,(p,st) in enumerate(parts):
    ins += ["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")],check=True)
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
print("total",total); [print(c) for c in tl]
