"""Voice + one click when the Follow card appears (reference videos muted) -> audio/mix.mp3"""
import json, wave, pathlib, numpy as np, subprocess, os
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"; SR=44100
_d=json.load(open(R/"tools"/"dur.json")); DUR=float(_d["dur"]); CARD=float(_d["card"])
w=wave.open(str(A/"voice_all.wav")); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
VG=float(os.environ.get("REEL_VOICE_GAIN","1.75"))
n=int(DUR*SR); v=np.zeros(n); v[:min(n,len(x))]=x[:n]
w2=wave.open(str(A/"click.wav")); ck=np.frombuffer(w2.readframes(w2.getnframes()),dtype=np.int16).astype(float)/32768
sfx=np.zeros(n); i0=int(CARD*SR); sfx[i0:i0+len(ck)]=ck[:max(0,n-i0)]*0.8      # click as the Follow card appears (only SFX in the video)
mix=np.tanh(v*VG+sfx*0.6); pcm=(mix*32767).astype(np.int16)
wv=wave.open(str(A/"mix.wav"),"wb"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(pcm.tobytes()); wv.close()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(A/"mix.wav"),"-b:a","192k",str(A/"mix.mp3")],check=True)
print("mix ok",DUR,"peak",float(abs(mix).max()))
