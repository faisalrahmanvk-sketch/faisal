"""Reel 19 (Sheikh Mohammed vs Sheikh Mohamed, Ruler vs President): one 78.8 s take cut into its 25 sentences at the sentence-end pauses."""
import subprocess, json, pathlib, os, re
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
SRC = "/root/.claude/uploads/7f783ea4-d946-5fec-9df1-3b3266bc0edf/66a2f26d-ElevenLabs_2026-11-08T16_44_58_Abhilash_S_-_Fun_Encouraging_Friend_pvc_s50_sim75_v4.mp3"
SPEED = float(os.environ.get("REEL_SPEED","1.3"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
r=subprocess.run(["ffmpeg","-i",SRC,"-af","silencedetect=n=-36dB:d=0.1","-f","null","-"],capture_output=True,text=True).stderr
m=re.search(r"Duration: \d+:(\d+):([\d.]+)",r); T=60*int(m.group(1))+float(m.group(2))
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
# sentence-end pauses (commas / colons inside a sentence at 6.9, 65.9, 73.4, 75.7 are not listed)
ENDS=[1.6,3.7,5.2,8.8,12.2,14.3,16.8,20.7,26.1,29.6,32.1,34.5,37.2,40.5,43.7,45.2,46.8,48.1,51.7,55.2,58.0,63.3,68.8,72.3]
CH=[]; a=0.0
for tgt in ENDS:
    k=min(range(len(st)),key=lambda i:abs(st[i]-tgt)); assert abs(st[k]-tgt)<0.25,(tgt,st[k])
    CH.append((a,st[k])); a=en[k]
CH.append((a,T-0.05)); assert len(CH)==25
SC={3,9,15,18,22}; SHORT={1,2,16,17}
t=0.35; tl=[]; parts=[]
for k,(a_,b_) in enumerate(CH,1):
    g=0.55 if k in SC else (0.14 if k in SHORT else 0.25)
    if k==25: g=0.0
    out=A/"proc"/f"c{k}.wav"
    run(["-i",SRC,"-af",f"atrim=start={max(0,a_-0.12)}:end={b_+0.12},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)])
    d=dur(out); tl.append({"clip":f"c{k}","start":round(t,3),"end":round(t+d,3)}); parts.append((out,t)); t+=d+g
total=round(t,2); ins=[]; fl=[]
for i,(p,s_) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(s_*1000)}|{int(s_*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl},open(A/"timeline.json","w"),indent=1)
card=round(tl[-1]["end"]+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(R/"tools"/"dur.json","w"))
print("total",total,"card",card)
