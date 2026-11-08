"""Reel 18 (Emirates vs Etihad, flydubai vs Air Arabia): one 100.8 s take cut into its 31 sentences at the sentence-end pauses."""
import subprocess, json, pathlib, os, re
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
SRC = "/root/.claude/uploads/7f783ea4-d946-5fec-9df1-3b3266bc0edf/de148e5c-ElevenLabs_2026-11-08T10_40_47_Abhilash_S_-_Fun_Encouraging_Friend_pvc_s50_sim75_v4.mp3"
SPEED = float(os.environ.get("REEL_SPEED","1.3"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
r=subprocess.run(["ffmpeg","-i",SRC,"-af","silencedetect=n=-36dB:d=0.1","-f","null","-"],capture_output=True,text=True).stderr
m=re.search(r"Duration: \d+:(\d+):([\d.]+)",r); T=60*int(m.group(1))+float(m.group(2))
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
# sentence-end pauses (commas inside a sentence at 21.9, 27.5, 31.1, 49.2, 59.5, 81.1 are not listed)
ENDS=[1.3,2.8,4.2,6.6,8.8,12.3,15.3,23.1,26.4,29.1,34.0,37.6,42.3,45.8,51.3,53.1,54.7,55.9,58.1,64.2,67.1,69.5,72.9,76.8,79.4,84.1,87.4,88.8,92.2,95.0]
CH=[]; a=0.0
for tgt in ENDS:
    k=min(range(len(st)),key=lambda i:abs(st[i]-tgt)); assert abs(st[k]-tgt)<0.25,(tgt,st[k])
    CH.append((a,st[k])); a=en[k]
CH.append((a,T-0.05)); assert len(CH)==31
SC={3,9,15,18,24}; SHORT={1,2,16,17}
t=0.35; tl=[]; parts=[]
for k,(a_,b_) in enumerate(CH,1):
    g=0.55 if k in SC else (0.14 if k in SHORT else 0.25)
    if k==31: g=0.0
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
