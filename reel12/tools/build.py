"""Reel 12: Dubai Bus vs KSRTC - follows the script's scene directions (look right/left/front, highlight, CTA)."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]; clicks=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def caps(s, e, chunks):
    w=[max(len(c),4) for c in chunks]; tot=sum(w); t=s
    for k,c in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t+=d
c=lambda n: tl[f"c{n}"]
S2=c(4)["start"]-0.1; S3=c(7)["start"]-0.1; S4=CARD       # scene starts (scene 1 = 0)
# ---- two photo tiles: KSRTC left, Dubai Bus right (script: Dubai pops right, KSRTC pops left)
def tile(id_, side, photo, label):
    return f'<div id="{id_}" class="tile {side}"><div class="tl">{html.escape(label)}</div><img src="assets/{photo}" alt="{html.escape(label)}"></div>'
clip("tiles", 0, S4, tile("tk","l","ksrtc.jpg","KSRTC")+tile("td","r","dubai.jpg","Dubai Bus"), z=3)
t_d=c(1)["start"]-0.03; t_k=c(2)["start"]-0.03
js.append(f'gsap.set("#tk,#td",{{opacity:0}});')
js.append(f'tl.fromTo("#td",{{x:120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_d:.3f});')
js.append(f'tl.fromTo("#tk",{{x:-120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_k:.3f});')
clicks += [round(t_d+0.02,3), round(t_k+0.02,3)]
# highlight: scene 2 -> Dubai, scene 3 -> KSRTC (other one dims)
def hl(on, off, at):
    js.append(f'tl.to("{on}",{{scale:1.07,opacity:1,duration:0.35,ease:"power2.out"}},{at:.3f});')
    js.append(f'tl.to("{off}",{{scale:0.9,opacity:0.45,duration:0.35,ease:"power2.out"}},{at:.3f});')
hl("#td","#tk",S2); hl("#tk","#td",S3)
js.append(f'tl.to("#tiles",{{opacity:0,duration:0.25}},{S4-0.05:.3f});')
# ---- captions
caps(0.0,c(2)["start"],["ഇതാണ് Dubai Bus."]); caps(c(2)["start"],c(3)["start"],["ഇതാണ് KSRTC."]); caps(c(3)["start"],S2,["എന്താണ് വ്യത്യാസം?"])
caps(S2,S3,["Dubai Bus, RTA","നിയന്ത്രിക്കുന്ന ഒരു","public transport service ആണ്.","ഇവിടെ Nol Card ഉപയോഗിച്ച്","യാത്ര ചെയ്യാം.","AC ബസുകളും","നിശ്ചിത bus stops-ഉം","real-time route information-ഉം","ഇതിന്റെ പ്രത്യേകതകളാണ്"])
caps(S3,S4,["KSRTC എന്ന് പറയുന്നത്","Kerala State Road","Transport Corporation ആണ്.","കേരളത്തിലെ നഗരങ്ങളെയും","ഗ്രാമങ്ങളെയും ബന്ധിപ്പിക്കുന്ന","public transport service ആണിത്.","Ordinary മുതൽ","Super Fast, long-distance","services വരെ ഇതിലുണ്ട്"])
# ---- poses: R (looks right at Dubai), L (looks left at KSRTC), think = front / camera
poses += [(0.0,c(2)["start"],"R"),(c(2)["start"],c(3)["start"],"L"),(c(3)["start"],S2,"T"),(S2,S3,"R"),(S3,S4,"L")]
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
.tile{position:absolute;top:215px;width:470px;text-align:center}
.tile.l{left:45px}.tile.r{left:565px}
.tl{font-weight:800;font-size:46px;margin-bottom:12px;letter-spacing:-0.5px}
.tile img{width:470px;height:350px;object-fit:cover;border-radius:28px;box-shadow:0 12px 34px rgba(0,0,0,.22);display:block}
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
(R/"index.html").write_text(doc_, encoding="utf-8"); print("wrote", len(doc_), "caps", len(cap), "poses", len(poses), "clicks", len(clicks))
