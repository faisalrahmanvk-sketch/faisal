"""Reel 4: trim each ElevenLabs line, split the two-app intro at its pause, speed up, concatenate with gaps; write timeline.json."""
import subprocess, json, pathlib, os, re
A = pathlib.Path(__file__).resolve().parent.parent / "audio"
SPEED = float(os.environ.get("REEL_SPEED","1.35"))
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
(A/"proc").mkdir(exist_ok=True)
def prep(name):
    out=A/"proc"/f"{name}.wav"; run(["-i",str(A/f"{name}.mp3"),"-af",f"{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)]); return out
def split_intro(name):
    raw=A/"proc"/f"{name}_raw.wav"; run(["-i",str(A/f"{name}.mp3"),"-af",TRIM,"-ar","44100","-ac","1",str(raw)])
    r=subprocess.run(["ffmpeg","-i",str(raw),"-af","silencedetect=n=-38dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
    gaps=[(e-s,(s+e)/2) for s,e in zip(st,en) if s>0.2]
    assert gaps, f"no pause found in {name}"
    mid=max(gaps)[1]; total=dur(raw); print(name,"split at",round(mid,2),"of",round(total,2))
    outs=[]
    for k,(a,b) in enumerate([(0,mid),(mid,total)]):
        o=A/"proc"/f"{name}_{k+1}.wav"
        run(["-i",str(raw),"-af",f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(o)]); outs.append(o)
    return outs
t=0.35; tl=[]; parts=[]
def place(label,p,gap):
    global t
    d=dur(p); tl.append({"clip":label,"start":round(t,3),"end":round(t+d,3)}); parts.append((p,t)); t+=d+gap
for s in (1,2,3,4):
    i1,i2=split_intro(f"s{s}-intro")
    place(f"s{s}-i1",i1,0.14); place(f"s{s}-i2",i2,0.14)
    place("q",prep("s1-q" if s%2 else "s2-q"),0.26)
    place(f"s{s}-a",prep(f"s{s}-a"),0.22); place(f"s{s}-b",prep(f"s{s}-b"),0.55)
total=round(t,2); ins=[]; fl=[]
for i,(p,st) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
last=tl[-1]["end"]; card=round(last+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(pathlib.Path(__file__).parent/"dur.json","w"))
print("total",total,"card",card)
for c in tl: print(c)
