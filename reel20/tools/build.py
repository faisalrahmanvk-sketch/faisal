"""Reel 20: Normal AI video (RIGHT) vs Professional Creative AI video (LEFT). Original reference videos, muted; stills as paused previews."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; END = _d["end"]
h=[]; js=[]; cap=[]; poses=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def caps(s, e, chunks):
    w=[max(len(x),4) for x in chunks]; tot=sum(w); t=s
    for k,x in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, x)); t+=d
c=lambda n: tl[f"c{n}"]
S2s=c(4)["start"]-0.15; S2e=c(5)["end"]+0.25; S3s=c(6)["start"]-0.15; S3e=c(7)["end"]+0.3; S4s=c(8)["start"]-0.1
SM=0.6667                                   # small preview scale (450x800 element -> 300x533)
def media(tag, id_, src, still, s, e, z, side, extra=""):
    pass
# ---- paused previews (first frame of each ORIGINAL video): RIGHT = normal AI, LEFT = professional
RX,LX,TOP=600,30,70
def still(id_, src, x, origin, pop_at, end_at):
    h.append(f'<img id="{id_}" class="clip pv" src="assets/{src}" data-start="{pop_at:.3f}" data-duration="{end_at-pop_at:.3f}" data-track-index="3" style="z-index:3;left:{x}px;top:{TOP}px;transform-origin:{origin}" alt="">')
    js.append(f'tl.fromTo("#{id_}",{{scale:0.3,opacity:0}},{{scale:{SM},opacity:1,duration:0.45,ease:"back.out(1.6)"}},{pop_at:.3f});')
    js.append(f'tl.to("#{id_}",{{opacity:0,duration:0.3,ease:"power1.in"}},{end_at-0.32:.3f});')
still("pvR","normal_still.jpg",RX,"100% 0%",c(1)["start"]-0.03,S4s+0.4)
still("pvL","pro_still.jpg",LX,"0% 0%",c(2)["start"]-0.03,S4s+0.4)
# ---- the ORIGINAL videos, muted, enlarged only while they are being discussed
def video(id_, src, x, origin, s, e):
    h.append(f'<video id="{id_}" class="clip pv" src="assets/{src}" muted playsinline data-start="{s:.3f}" data-duration="{e-s:.3f}" data-media-start="0" data-track-index="4" style="z-index:4;left:{x}px;top:{TOP}px;transform-origin:{origin}"></video>')
    js.append(f'tl.fromTo("#{id_}",{{scale:{SM}}},{{scale:1,duration:0.55,ease:"power2.inOut"}},{s:.3f});')
    js.append(f'tl.to("#{id_}",{{scale:{SM},duration:0.5,ease:"power2.inOut"}},{e-0.52:.3f});')
video("vidR","normal_ai.mp4",RX,"100% 0%",S2s,S2e)   # scene 2: Normal AI video (RIGHT)
video("vidL","pro_ai.mp4",LX,"0% 0%",S3s,S3e)        # scene 3: Professional Creative AI video (LEFT)
# ---- final CTA: the Follow card (existing asset)
clip("cta", S4s+0.2, DUR, '<img id="cta-in" class="cta" src="assets/follow_card.png" alt="Follow / DM">', z=6)
js.append(f'tl.fromTo("#cta-in",{{opacity:0,scale:0.9,y:20}},{{opacity:1,scale:1,y:0,duration:0.5,ease:"back.out(1.5)"}},{S4s+0.2:.3f});')
# ---- subtitles (match the spoken Malayalam)
CAP={1:["ഇതാണ് സാധാരണ AI വീഡിയോ."],2:["ഇതാണ് Professional","Creative AI വീഡിയോ."],3:["എന്താണ് ഇവ തമ്മിലുള്ള","വ്യത്യാസം?"],
4:["സാധാരണ AI വീഡിയോകൾ","കൂടുതലായും Free AI Tools","ഉപയോഗിച്ച് തയ്യാറാക്കുന്ന","Entertainment Content ആണ്."],
5:["Likes, Shares, Reach,","Followers എന്നിവ","കൂട്ടാനാണ് പ്രധാനമായും","ഉപയോഗിക്കുന്നത്."],
6:["എന്നാൽ Creative AI","Advertisement എന്നത്","Premium Paid AI Tools","ഉപയോഗിച്ച് Professional","Creators തയ്യാറാക്കുന്ന","High-Quality Cinematic","വീഡിയോകളാണ്."],
7:["നിങ്ങളുടെ Products-ഉം","Services-ഉം ആകർഷകമായി","അവതരിപ്പിച്ച്","Brand Promotion-നും","Marketing-നും ഉപയോഗിക്കാം."],
8:["നിങ്ങളുടെ Brand-നും","ഇതുപോലെയുള്ള Creative AI","വീഡിയോകൾ വേണമെങ്കിൽ","ഇപ്പോൾ തന്നെ ഞങ്ങൾക്ക്","DM ചെയ്യൂ!"]}
starts={n:(0.0 if n==1 else c(n)["start"]-0.05) for n in range(1,9)}
ends={n:(starts[n+1] if n<8 else DUR) for n in range(1,9)}
for n in range(1,9): caps(starts[n], ends[n], CAP[n])
# ---- presenter: looks RIGHT for the normal AI video, LEFT for the professional one, camera for question + CTA
poses=[(starts[1],starts[2],"R"),(starts[2],starts[3],"L"),(starts[3],starts[4],"T"),(starts[4],starts[6],"R"),(starts[6],starts[8],"L"),(starts[8],DUR,"T")]
for i,(s,e,t) in enumerate(cap):
    clip(f"c{i}", s, e, f'<div class="cap"><span id="c{i}-in">{html.escape(t)}</span></div>', z=5)
    js.append(f'tl.fromTo("#c{i}-in",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.18,ease:"power2.out"}},{s:.3f});')
PF={"L":"pose_pointL.png","R":"pose_pointR.png","T":"pose_think.png"}
for i,(s,e,p) in enumerate(poses):
    clip(f"p{i}", s, e, f'<img id="p{i}-in" class="pose{" think" if p=="T" else ""}" src="assets/{PF[p]}" alt="presenter">', z=2)
    js.append(f'tl.fromTo("#p{i}-in",{{y:0}},{{y:-9,duration:{(e-s)/2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{s:.3f});')
clip("wm", 0, DUR, '<div class="wm">@fyze.ai</div>', z=4)
CSS = open(R.parent/"reel"/"hf"/"tools"/"build.py", encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
CSS += """
.cap{top:885px;height:130px}
.pose{top:1040px;height:650px}
.pv{position:absolute;width:450px;height:800px;object-fit:cover;border-radius:30px;box-shadow:0 18px 46px rgba(0,0,0,.30);background:#fff}
.cta{position:absolute;left:230px;top:150px;width:620px;height:auto;-webkit-mask-image:radial-gradient(ellipse 52% 52% at 50% 50%,#000 70%,transparent 100%);mask-image:radial-gradient(ellipse 52% 52% at 50% 50%,#000 70%,transparent 100%)}
"""
doc_ = f"""<!doctype html>
<html lang="ml"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(h)}
<audio id="voice" src="audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body></html>"""
(R/"index.html").write_text(doc_, encoding="utf-8"); print("wrote", len(doc_), "caps", len(cap), "dur", DUR, "S2",round(S2s,2),round(S2e,2),"S3",round(S3s,2),round(S3e,2),"S4",round(S4s,2))
