"""Synthesize upbeat BGM + SFX (pop/boom/whoosh) and mix with the voice. All times from timeline.json."""
import json, wave, pathlib, numpy as np, subprocess
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"; SR = 44100
tl = json.load(open(A/"timeline.json")); clips = {}
for c in tl["clips"]: clips.setdefault(c["clip"], c)   # first occurrence
_d = json.load(open(R/"tools"/"dur.json")); DUR = float(_d["dur"]); CARD = float(_d["card"])
rng = np.random.default_rng(7)
N = int(DUR*SR)+SR; t_ = lambda d: np.arange(int(d*SR))/SR
def add(buf, x, at, g=1.0):
    i = int(at*SR); x = x[:max(0,len(buf)-i)]
    if i < len(buf): buf[i:i+len(x)] += x*g
def click():
    w=wave.open(str(A/'click.wav')); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768; return x
def pop(): t=t_(0.16); return np.sin(2*np.pi*(380+1500*t)*t)*np.exp(-t*34)
def boom():
    t=t_(0.9); k=np.sin(2*np.pi*(95*np.exp(-t*3.2)+38)*t)*np.exp(-t*4.2); n=rng.standard_normal(len(t))*np.exp(-t*30)*0.25
    return (k+n)
def whoosh():
    t=t_(0.55); n=rng.standard_normal(len(t)); k=np.ones(60)/60; lp=np.convolve(n,k,"same"); hp=n-np.convolve(n,np.ones(6)/6,"same")
    env=np.sin(np.pi*np.clip(t/0.55,0,1))**2; return (0.55*lp*6+0.35*hp)*env*0.5
def hat(): t=t_(0.07); n=rng.standard_normal(len(t)); return (n-np.convolve(n,np.ones(4)/4,"same"))*np.exp(-t*70)*0.5
def kick(): t=t_(0.28); return np.sin(2*np.pi*(52+110*np.exp(-t*22))*t)*np.exp(-t*11)
def bass(f,d=0.22): t=t_(d); w=np.sign(np.sin(2*np.pi*f*t))*0.35+np.sin(2*np.pi*f*t)*0.65; return w*np.exp(-t*7)*np.minimum(1,t*200)
def stab(freqs,d=0.18):
    t=t_(d); w=sum(np.sign(np.sin(2*np.pi*f*t)) for f in freqs)/len(freqs); return w*np.exp(-t*14)*0.25*np.minimum(1,t*300)
# ---- BGM: 124 bpm, Am-F-C-G, 4 on the floor + offbeat hat + 8th bass + stabs
bpm=124; beat=60/bpm; bgm=np.zeros(N)
roots=[55.0,43.65,65.41,49.0]; chords=[[220,261.6,329.6],[174.6,220,261.6],[261.6,329.6,392],[196,246.9,293.7]]
nbars=int(DUR/(4*beat))+2
for b in range(nbars):
    r=roots[b%4]; ch=chords[b%4]; t0=b*4*beat
    for k in range(4):
        add(bgm,kick(),t0+k*beat,0.9); add(bgm,hat(),t0+k*beat+beat/2,0.6)
        for e in range(2): add(bgm,bass(r*(2 if (k*2+e)%4==3 else 1)),t0+k*beat+e*beat/2,0.8)
    for s_ in (0.75,1.5,2.5,3.25): add(bgm,stab(ch),t0+s_*beat,0.8)
# duck BGM under voice
v=np.zeros(N); w=wave.open(str(A/"voice_all.wav")); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768; v[:len(x)]=x[:N]
env=np.convolve(np.abs(v),np.ones(int(0.12*SR))/int(0.12*SR),"same"); env=np.convolve((env>0.015).astype(float),np.ones(int(0.25*SR))/int(0.25*SR),"same")
bgm*= (1-0.6*np.clip(env,0,1))*0.20
# ---- SFX events
sfx=np.zeros(N); scenes=[1,2,3,4]
for s in scenes:
    i1,i2,a,b=[clips[f"s{s}-{k}"] for k in("i1","i2","a","b")]
    t0 = 0.0 if s==1 else i1["start"]-0.12
    add(sfx,click(),t0+0.05 if s==1 else i1["start"]-0.03,0.8); add(sfx,click(),i2["start"]-0.03,0.8)
    add(sfx,click(),b["start"]-0.03,0.8)
add(sfx,click(),CARD,1.0)   # follow card: uploaded click only
mix=v+sfx*0.6   # BGM removed on request; mix=np.tanh(mix*1.1)*0.92
mix=mix[:int(DUR*SR)]
pcm=(mix*32767).astype(np.int16); wv=wave.open(str(A/"mix.wav"),"wb"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(pcm.tobytes()); wv.close()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(A/"mix.wav"),"-b:a","192k",str(A/"mix.mp3")],check=True)
print("mix ok",DUR)
