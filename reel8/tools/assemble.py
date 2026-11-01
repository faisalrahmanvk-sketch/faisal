"""Reel 7: scene 1 = intro (split) + question + two explanations; scenes 2-4 = one two-sentence clip split at its pause."""
import subprocess, json, pathlib, os, re
A = pathlib.Path(__file__).resolve().parent.parent / "audio"
SPEED = float(os.environ.get("REEL_SPEED","1.45"))
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
(A/"proc").mkdir(exist_ok=True)
def prep(name):
    out=A/"proc"/f"{name}.wav"; run(["-i",str(A/f"{name}.mp3"),"-af",f"{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)]); return out
def split2(name, min_start=0.4):
    raw=A/"proc"/f"{name}_raw.wav"; run(["-i",str(A/f"{name}.mp3"),"-af",TRIM,"-ar","44100","-ac","1",str(raw)])
    r=subprocess.run(["ffmpeg","-i",str(raw),"-af","silencedetect=n=-38dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; du=[float(x) for x in re.findall(r"silence_duration: ([\d.]+)",r)]
    total=dur(raw); gaps=[(d,s+d/2) for s,d in zip(st,du) if s>min_start and s+d<total-0.3]
    assert gaps, f"no pause in {name}"
    mid=max(gaps)[1]; print(name,"split at",round(mid,2),"of",round(total,2),"| gaps",[(round(g[0],2),round(g[1],2)) for g in sorted(gaps,reverse=True)[:3]])
    outs=[]
    for k,(a,b) in enumerate([(0,mid),(mid,total)]):
        o=A/"proc"/f"{name}_{k+1}.wav"
        run(["-i",str(raw),"-af",f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(o)]); outs.append(o)
    return outs
t=0.35; tl=[]; parts=[]
def place(label,p,gap):
    global t
    d=dur(p); tl.append({"clip":label,"start":round(t,3),"end":round(t+d,3)}); parts.append((p,t)); t+=d+gap
i1,i2=split2("s1-intro")
place("s1-i1",i1,0.14); place("s1-i2",i2,0.14); place("s1-q",prep("s1-q"),0.55)
for s in (2,3,4,5,6):
    place(f"s{s}",prep(f"s{s}"),0.55)
total=round(t,2); ins=[]; fl=[]
for i,(p,st) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
last=tl[-1]["end"]; card=round(last+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(pathlib.Path(__file__).parent/"dur.json","w"))
print("total",total,"card",card)
for c in tl: print(c)
