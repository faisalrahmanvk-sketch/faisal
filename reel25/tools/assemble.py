"""Reel 25 (5 Malayali business groups: logo / founder / place): one 20 s take cut into its 15 phrases."""
import subprocess, json, pathlib, os, re
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
SRC = str(A/"full.mp3")
SPEED = float(os.environ.get("REEL_SPEED","1.3"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
r=subprocess.run(["ffmpeg","-i",SRC,"-af","silencedetect=n=-36dB:d=0.1","-f","null","-"],capture_output=True,text=True).stderr
m=re.search(r"Duration: \d+:(\d+):([\d.]+)",r); T=60*int(m.group(1))+float(m.group(2))
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
ENDS=[0.7,2.5,3.9,5.5,7.2,8.9,10.2,11.3,12.5,13.5,14.8,16.4,17.8,19.0]
CH=[]; a=0.0
for tgt in ENDS:
    k=min(range(len(st)),key=lambda i:abs(st[i]-tgt)); assert abs(st[k]-tgt)<0.25,(tgt,st[k])
    CH.append((a,st[k])); a=en[k]
CH.append((a,T-0.05)); assert len(CH)==15
t=0.3; tl=[]; parts=[]
for k,(a_,b_) in enumerate(CH,1):
    g=0.6 if k%3==0 else 0.18           # longer pause between companies
    if k==15: g=0.0
    out=A/"proc"/f"c{k}.wav"
    run(["-i",SRC,"-af",f"atrim=start={max(0,a_-0.1)}:end={b_+0.1},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)])
    d=dur(out); tl.append({"clip":f"c{k}","start":round(t,3),"end":round(t+d,3)}); parts.append((out,t)); t+=d+g
total=round(t,2); ins=[]; fl=[]
for i,(p,s_) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(s_*1000)}|{int(s_*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
card=round(tl[-1]["end"]+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(R/"tools"/"dur.json","w"))
print("total",total,"card",card)
