"""Reel 15 (Emirates ID vs Aadhaar, UAE Pass vs DigiLocker): one 103 s take cut into its 35 sentences (pauses >= 0.335 s)."""
import subprocess, json, pathlib, os, re
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
SRC = "/root/.claude/uploads/7f783ea4-d946-5fec-9df1-3b3266bc0edf/2747ddfd-ElevenLabs_2026-11-07T07_06_23_Abhilash_S_-_Fun_Encouraging_Friend_pvc_s50_sim75_v4.mp3"
SPEED = float(os.environ.get("REEL_SPEED","1.3"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
r=subprocess.run(["ffmpeg","-i",SRC,"-af","silencedetect=n=-36dB:d=0.12","-f","null","-"],capture_output=True,text=True).stderr
T=float(re.search(r"Duration: \d+:(\d+):([\d.]+)",r).group(2))+60*int(re.search(r"Duration: \d+:(\d+):([\d.]+)",r).group(1))
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
TH=float(os.environ.get("REEL_TH","0.335")); SKIP=[83.0]            # 83.0 = comma pause inside one sentence
CH=[]; a=0.0
for s,e in zip(st,en):
    if (e-s)>=TH and not any(abs(s-k)<0.3 for k in SKIP): CH.append((a,s)); a=e
CH.append((a,T-0.1))
assert len(CH)==35, f"expected 35 sentences, got {len(CH)}"
# revised script: dropped old s10-s12 (renew/fine lines) and s19-s20 (Centre fee lines)
DROP={10,11,12,19,20}; KEEP=[k for k in range(1,36) if k not in DROP]
# gap after sentence k (1-based): scene change 0.55 after s3, s12, s23, s26(question->explanation), s30 ; 0.14 for short intro lines
SC={3,9,23,26,30}; SHORT={1,2,24,25}
t=0.35; tl=[]; parts=[]
for idx,k in enumerate(KEEP):
    a_,b_=CH[k-1]; g=0.55 if k in SC else (0.14 if k in SHORT else 0.25)
    if idx==len(KEEP)-1: g=0.0
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
print("total",total,"card",card,"sentences",len(KEEP))
