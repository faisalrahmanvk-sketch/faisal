"""Reel 11 (CV with Claude): one long take cut at sentence pauses into 15 chunks, sped up, placed with scene gaps."""
import subprocess, json, pathlib, os
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
SRC = os.environ.get("REEL_SRC","/root/.claude/uploads/7f783ea4-d946-5fec-9df1-3b3266bc0edf/0fb74d9f-Cvvvvv.mp3")
SPEED = float(os.environ.get("REEL_SPEED","1.45"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
# speech chunks (start,end) in the source file, one per sentence (found from the >=0.4 s pauses)
CH=[(0,3.879),(4.41,6.527),(7.22,11.907),(12.375,15.772),(16.197,21.059),(21.499,25.02),(25.5,27.809),(28.413,31.222),
    (31.66,38.426),(38.863,42.451),(42.973,49.782),(50.176,51.619),(52.09,60.533),(61.023,65.17),(65.657,67.2)]
# gap after each chunk (seconds): scene change 0.5, same scene 0.22, mid-sentence pause 0.30
GAP=[0.22,0.5,0.22,0.5,0.22,0.5,0.22,0.5,0.5,0.5,0.5,0.30,0.5,0.22,0.0]
t=0.35; tl=[]; parts=[]
for i,((a,b),g) in enumerate(zip(CH,GAP),1):
    out=A/"proc"/f"c{i}.wav"
    run(["-i",SRC,"-af",f"atrim=start={max(0,a-0.12)}:end={b+0.12},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)])
    d=dur(out); tl.append({"clip":f"c{i}","start":round(t,3),"end":round(t+d,3)}); parts.append((out,t)); t+=d+g
total=round(t,2); ins=[]; fl=[]
for i,(p,st) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
card=round(tl[-1]["end"]+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(R/"tools"/"dur.json","w"))
print("total",total,"card",card); [print(c) for c in tl]
