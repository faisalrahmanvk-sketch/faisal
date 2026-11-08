"""Voice only (no sound effects, reference videos muted): soft-limited voice -> audio/mix.mp3"""
import json, wave, pathlib, numpy as np, subprocess, os
R = pathlib.Path(__file__).resolve().parent.parent; A = R/"audio"; SR=44100
DUR=float(json.load(open(R/"tools"/"dur.json"))["dur"])
w=wave.open(str(A/"voice_all.wav")); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
VG=float(os.environ.get("REEL_VOICE_GAIN","1.75"))
n=int(DUR*SR); v=np.zeros(n); v[:min(n,len(x))]=x[:n]
mix=np.tanh(v*VG); pcm=(mix*32767).astype(np.int16)
wv=wave.open(str(A/"mix.wav"),"wb"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(pcm.tobytes()); wv.close()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(A/"mix.wav"),"-b:a","192k",str(A/"mix.mp3")],check=True)
print("mix ok",DUR,"peak",float(abs(mix).max()))
