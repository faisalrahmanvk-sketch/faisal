"""Reel 12 (Dubai Bus vs KSRTC): one take cut at pauses into 10 chunks (closing follow line removed), sped up and placed with scene gaps."""
import subprocess, json, pathlib, os
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
U="/root/.claude/uploads/7f783ea4-d946-5fec-9df1-3b3266bc0edf/"
S1=os.environ.get("REEL_SRC1",U+"16a0a71b-Bus.mp3"); S2=os.environ.get("REEL_SRC2",U+"9c938fde-Bus_2.mp3")
SPEED = float(os.environ.get("REEL_SPEED","1.45"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
P1=[(0,1.44),(1.95,3.34),(3.92,4.75),(5.38,9.48),(10.0,12.29),(12.75,19.64),(20.26,21.51),(21.97,26.86),(27.27,31.79),(32.31,37.3)]
G1=[0.14,0.14,0.55,0.22,0.22,0.55,0.30,0.22,0.22,0.9]
# part 2 (Nol Card vs Bus Conductor): trailing extra speech after 27.36 is not used
P2=[(0,1.26),(1.72,2.71),(3.3,4.2),(4.78,10.21),(10.62,14.37),(14.79,18.2),(18.63,27.36)]
G2=[0.14,0.14,0.55,0.22,0.22,0.55,0.0]
CH=[(S1,a,b,g,f"c{k}") for k,((a,b),g) in enumerate(zip(P1,G1),1)]+[(S2,a,b,g,f"d{k}") for k,((a,b),g) in enumerate(zip(P2,G2),1)]
t=0.35; tl=[]; parts=[]
for (src,a,b,g,name) in CH:
    out=A/"proc"/f"{name}.wav"
    run(["-i",src,"-af",f"atrim=start={max(0,a-0.12)}:end={b+0.12},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)])
    d=dur(out); tl.append({"clip":name,"start":round(t,3),"end":round(t+d,3)}); parts.append((out,t)); t+=d+g
total=round(t,2); ins=[]; fl=[]
for i,(p,st) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
card=round(tl[-1]["end"]+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(R/"tools"/"dur.json","w"))
print("total",total,"card",card); [print(c) for c in tl]
