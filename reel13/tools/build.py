"""Reel 13: photo 1 pops in, then swaps to photo 2; character at the bottom; Follow card at the end. No captions (no script supplied)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]; clicks=[]
import html
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
c=lambda n: tl[f"c{n}"]
def caps(s, e, chunks):
    w=[max(len(x),4) for x in chunks]; tot=sum(w); t=s
    for k,x in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, x)); t+=d
s2=c(2)["start"]-0.05
def photo(id_, src, s, e):
    clip(f"ph-{id_}", s, e, f'<div class="ph"><img id="ph-{id_}-in" src="assets/{src}" alt="Dubai Run"></div>', z=3)
    js.append(f'tl.fromTo("#ph-{id_}-in",{{scale:0.4,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:0.45,ease:"back.out(1.6)"}},{s:.3f});')
    clicks.append(round(s+0.02,3))
t_p1=c(1)["start"]+0.38*(c(1)["end"]-c(1)["start"])
photo("0","dfc.jpg",0.0,t_p1+0.15)
photo("1","run1.jpg",t_p1,s2+0.15)
photo("2","run2.jpg",s2,CARD)
js.append(f'tl.to("#ph-0-in",{{opacity:0,duration:0.15}},{t_p1:.3f});')
js.append(f'tl.to("#ph-1-in",{{opacity:0,duration:0.15}},{s2:.3f});')
js.append(f'tl.to("#ph-2-in",{{opacity:0,scale:0.92,duration:0.2}},{CARD-0.25:.3f});')
poses += [(0.0,s2,"R"),(s2,c(3)["start"]-0.05,"L"),(c(3)["start"]-0.05,CARD,"T")]
caps(0.0,s2,["2026 ദുബായ് റണ്ണിന്റെ","രജിസ്ട്രേഷൻ ഇപ്പോൾ","സ്റ്റാർട്ട് ചെയ്തിട്ടുണ്ട്!"])
caps(s2,c(3)["start"]-0.05,["ഇപ്പോൾ തന്നെ","രജിസ്റ്റർ ചെയ്യാം."])
caps(c(3)["start"]-0.05,CARD,["രജിസ്ട്രേഷൻ ലിങ്ക് വേണമെങ്കിൽ","കമന്റ് ബോക്സിൽ","“LINK” എന്ന് കമന്റ് ചെയ്യൂ.","ലിങ്ക് നിങ്ങൾക്ക്","ഷെയർ ചെയ്യാം!"])
for i,(s,e,t) in enumerate(cap):
    clip(f"c{i}", s, e, f'<div class="cap"><span id="c{i}-in">{html.escape(t)}</span></div>', z=5)
    js.append(f'tl.fromTo("#c{i}-in",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.18,ease:"power2.out"}},{s:.3f});')
PF={"L":"pose_pointL.png","R":"pose_pointR.png","T":"pose_think.png"}
for i,(s,e,p) in enumerate(poses):
    clip(f"p{i}", s, e, f'<img id="p{i}-in" class="pose{" think" if p=="T" else ""}" src="assets/{PF[p]}" alt="character">', z=2)
    js.append(f'tl.fromTo("#p{i}-in",{{y:0}},{{y:-9,duration:{(e-s)/2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{s:.3f});')
clip("endcard", CARD, DUR, '<img id="endcard-in" class="endimg" src="assets/endcard.png" alt="Follow fyze.ai">', z=6)
js.append(f'tl.fromTo("#endcard-in",{{opacity:0,scale:1.05}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.4)"}},{CARD});')
clip("wm", 0, CARD, '<div class="wm">@fyze.ai</div>', z=4)
json.dump(clicks, open(R/"tools"/"clicks.json","w"))
CSS = open(R.parent/"reel"/"hf"/"tools"/"build.py", encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
CSS += """
.ph{position:absolute;left:120px;top:80px;width:840px;height:630px}
.ph img{width:840px;height:630px;object-fit:cover;border-radius:34px;box-shadow:0 16px 44px rgba(0,0,0,.25);display:block}
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
(R/"index.html").write_text(doc_, encoding="utf-8"); print("wrote", len(doc_))
