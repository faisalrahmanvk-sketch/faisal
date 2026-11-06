"""Reel 14: Golden Visa (right) vs Employment Visa (left); click + highlight on each mention (script: click sound)."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]; clicks=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def caps(s, e, chunks):
    w=[max(len(x),4) for x in chunks]; tot=sum(w); t=s
    for k,x in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, x)); t+=d
c=lambda n: tl[f"c{n}"]
def tile(id_, side, photo, label):
    return f'<div id="{id_}" class="tile {side}"><div class="tl">{html.escape(label)}</div><img src="assets/{photo}" alt="{html.escape(label)}"></div>'
S2=c(4)["start"]-0.1; S3=c(9)["start"]-0.1
clip("tiles", 0, CARD, tile("te","l","employment.jpg","Employment Visa")+tile("tg","r","golden.jpg","Golden Visa"), z=3)
t_g=c(1)["start"]-0.03; t_e=c(2)["start"]-0.03
js.append('gsap.set("#te,#tg",{opacity:0});')
js.append(f'tl.fromTo("#tg",{{x:120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_g:.3f});')
js.append(f'tl.fromTo("#te",{{x:-120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_e:.3f});')
clicks += [round(t_g+0.02,3), round(t_e+0.02,3)]
def hl(on, off, at):
    clicks.append(round(at+0.02,3))   # script: click sound at "Golden Visa" / "Employment Visa"
    js.append(f'tl.to("{on}",{{scale:1.07,opacity:1,duration:0.35,ease:"power2.out"}},{at:.3f});')
    js.append(f'tl.to("{off}",{{scale:0.9,opacity:0.45,duration:0.35,ease:"power2.out"}},{at:.3f});')
hl("#tg","#te",c(4)["start"]-0.03); hl("#te","#tg",c(9)["start"]-0.03)
js.append(f'tl.to("#tiles",{{opacity:0,duration:0.25}},{CARD-0.05:.3f});')
CAP={1:["ഇതാണ് Golden Visa."],2:["ഇതാണ് Employment Visa."],3:["എന്താണ് വ്യത്യാസം?"],4:["Golden Visa."],
 5:["ഇത് UAE നൽകുന്ന","ഒരു Long-Term Residency ആണ്."],
 6:["സാധാരണയായി 5 അല്ലെങ്കിൽ","10 വർഷത്തേക്കാണ് ലഭിക്കുന്നത്."],
 7:["ഇതിന്റെ ഏറ്റവും വലിയ പ്രത്യേകത,","ഒരു പ്രത്യേക Employer-ന്റെ","Sponsorship ആവശ്യമില്ല എന്നതാണ്."],
 8:["Investors, Entrepreneurs,","Skilled Professionals,","Outstanding Students തുടങ്ങി","നിശ്ചിത യോഗ്യതയുള്ള ആളുകൾക്ക്","ഇത് ലഭിക്കും."],
 9:["Employment Visa."],
 10:["UAE-യിലെ ഒരു കമ്പനിയിൽ","ജോലി ലഭിക്കുമ്പോൾ സാധാരണയായി","ആ Employer ആണ് നിങ്ങളുടെ","Work Permit-നും Residence Visa-ക്കും","വേണ്ട നടപടികൾ ചെയ്യുന്നത്."],
 11:["സാധാരണ Employment Residence Visa","രണ്ട് വർഷത്തേക്കാണ് ലഭിക്കുന്നത്."],
 12:["കാലാവധി കഴിഞ്ഞാൽ","നിയമപ്രകാരമുള്ള നടപടികളിലൂടെ","പുതുക്കാം."],
 13:["അതായത്, ഇവിടെ നിങ്ങളുടെ","Residency ഒരു Employer-ന്റെ","Sponsorship-മായി","ബന്ധപ്പെട്ടിരിക്കുന്നു."]}
starts=[0.0]+[c(n)["start"]-0.05 for n in range(2,14)]+[CARD]
for n in range(1,14): caps(starts[n-1], starts[n], CAP[n])
# poses: scene 1 R/L/T ; scene 2 R (Golden is on the right) ; scene 3 L (Employment is on the left)
poses += [(starts[0],starts[1],"R"),(starts[1],starts[2],"L"),(starts[2],S2,"T"),(S2,S3,"R"),(S3,CARD,"L")]
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
.tl{font-weight:800;font-size:42px;margin-bottom:12px;letter-spacing:-0.5px;white-space:nowrap}
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
(R/"index.html").write_text(doc_, encoding="utf-8"); print("wrote", len(doc_), "caps", len(cap), "clicks", len(clicks))
