"""Reel 28: one 74.8 s take. Every caption phrase (49) is aligned to the real pauses of the recording (DP), then the 25 sentences are cut/sped up.
Writes audio/timeline.json with per-sentence clips AND per-phrase caption times (so subtitles follow the voice)."""
import subprocess, json, pathlib, os, re, sys
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"
sys.path.insert(0, str(R/"tools")); from captions import CAP; from syl import syl
SRC = str(A/"full.mp3"); SPEED = float(os.environ.get("REEL_SPEED","1.3"))
TRIM = "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse"
def run(args): subprocess.run(["ffmpeg","-v","error","-y",*args],check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())
(A/"proc").mkdir(exist_ok=True)
r=subprocess.run(["ffmpeg","-i",SRC,"-af","silencedetect=n=-36dB:d=0.08","-f","null","-"],capture_output=True,text=True).stderr
m=re.search(r"Duration: \d+:(\d+):([\d.]+)",r); T=60*int(m.group(1))+float(m.group(2))
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
cand=[(s,e) for s,e in zip(st,en) if s>0.3 and e<T-0.3]
import math, itertools
first=[e for s,e in zip(st,en) if s<0.3]; t0=first[0] if first else 0.0
allsil=[(s,e) for s,e in zip(st,en)]
def speech_between(a,b):                      # speech time in [a,b] excluding every detected silence inside
    tot=b-a
    for s,e in allsil:
        lo=max(a,s); hi=min(b,e)
        if hi>lo: tot-=hi-lo
    return max(tot,0.05)
SN=sorted(CAP); SY=[syl(" ".join(CAP[n])) for n in SN]; R0=5.3
# ---- sentence boundaries: the 13 phrases are short words separated by clear pauses (12 pauses)
ENDS=[2.98,4.09,4.83,5.67,6.89,8.09,8.53,9.39,10.42,11.76,12.47,15.54]
bs=[]
for tgt in ENDS:
    k=min(range(len(allsil)),key=lambda i:abs(allsil[i][0]-tgt)); assert abs(allsil[k][0]-tgt)<0.1,(tgt,allsil[k]); bs.append(allsil[k])
sa=[t0]+[e for s,e in bs]; sb=[s for s,e in bs]+[T-0.12]
# ---- stage 2: caption phrases inside each sentence, placed on the internal pauses (>=0.06 s) that give the most natural phrase rates
ph={}                                          # sentence -> list of (start,end) per phrase
def time_at_speech(a_,b_,frac):                 # time where `frac` of the sentence's speech (silences excluded) has been spoken
    target=speech_between(a_,b_)*frac; lo,hi=a_,b_
    for _ in range(40):
        mid=(lo+hi)/2
        if speech_between(a_,mid)<target: lo=mid
        else: hi=mid
    return (lo+hi)/2
for n_,sn in enumerate(SN):
    txts=CAP[sn]; a_,b_=sa[n_],sb[n_]; w=[syl(t) for t in txts]
    if len(txts)==1: ph[sn]=[(a_,b_)]; continue
    ins=[(s,e) for s,e in allsil if s>a_+0.15 and e<b_-0.15 and e-s>=0.12]       # only real pauses may split phrases
    best=(1e9,None)
    for comb in itertools.combinations(range(len(ins)),len(txts)-1):
        pts=[a_]+[x for k in comb for x in (ins[k][0],ins[k][1])]+[b_]
        segs=[(pts[2*i],pts[2*i+1]) for i in range(len(txts))]
        rates=[w[i]/speech_between(*segs[i]) for i in range(len(txts))]
        if min(rates)<3.0 or max(rates)>8.5: continue
        cst=sum((math.log(r/R0))**2 for r in rates)
        if cst<best[0]: best=(cst,segs)
    if best[1]: ph[sn]=best[1]; continue
    tot=sum(w); cum=0; segs=[]; prev=a_                   # fallback: split by syllable share of the real speech time
    for i in range(len(txts)):
        cum+=w[i]; end=b_ if i==len(txts)-1 else time_at_speech(a_,b_,cum/tot)
        segs.append((prev,end)); prev=end
    ph[sn]=segs
SC={3,7,13,16,20,24}; SHORT={1,2,14,15}
t=0.35; tl=[]; chunks=[]; parts=[]
for n_,sn in enumerate(SN):
    a_,b_=sa[n_],sb[n_]
    out=A/"proc"/f"c{sn}.wav"
    run(["-i",SRC,"-af",f"atrim=start={max(0,a_-0.08)}:end={b_+0.08},asetpts=PTS-STARTPTS,{TRIM},atempo={SPEED}","-ar","44100","-ac","1",str(out)])
    d=dur(out); tl.append({"clip":f"c{sn}","start":round(t,3),"end":round(t+d,3)}); parts.append((out,t))
    for k,(ps,pe) in enumerate(ph[sn]):
        cs=t+max(0,(ps-a_))/SPEED; ce=t+min(d,(pe-a_)/SPEED)
        chunks.append({"sent":sn,"k":k,"start":round(cs,3),"end":round(ce,3)})
    g=0.5 if sn in SC else (0.18 if sn in SHORT else 0.25)
    if sn==SN[-1]: g=0.0
    t+=d+g
total=round(t,2); ins=[]; fl=[]
for i,(p,s_) in enumerate(parts):
    ins+=["-i",str(p)]; fl.append(f"[{i}:a]adelay={int(s_*1000)}|{int(s_*1000)}[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad=pad_dur=1[o]")
run([*ins,"-filter_complex",";".join(fl),"-map","[o]","-t",str(total),"-ar","44100",str(A/"voice_all.wav")])
json.dump({"total":total,"clips":tl,"chunks":chunks},open(A/"timeline.json","w"),indent=1)
card=round(tl[-1]["end"]+0.45,2); json.dump({"dur":round(card+2.5,2),"card":card},open(R/"tools"/"dur.json","w"))
print("total",total,"card",card)
print("sentence ends:",[round(x,1) for x in sb[:-1]])
