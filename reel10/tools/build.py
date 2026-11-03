"""Reel 9: Midjourney / Nano Banana / ChatGPT Images - alternating logos, quick-speciality finale."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def group(id_, s, e, x, logo, label, chip=None):
    lb = f'<div class="glbl">{html.escape(label)}</div>' if label else '<div class="glbl">&nbsp;</div>'
    cp = f'<div class="chip">{html.escape(chip)}</div>' if chip else ""
    clip(f"g-{id_}", s, e, f'<div class="gwrap"><div id="g-{id_}-in" class="grp big">{lb}<img class="glogo" src="assets/{logo}" alt="{html.escape(label or logo)} logo">{cp}</div></div>', z=3)
    js.append(f'tl.fromTo("#g-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{max(0,s):.3f});')
    js.append(f'tl.to("#g-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.3f});')
def caps(s, e, chunks):
    w=[max(len(c),4) for c in chunks]; tot=sum(w); t=s
    for k,c in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t+=d
i1,i2,q = tl["s1-i1"],tl["s1-i2"],tl["s1-q"]; j1,j2,q2 = tl["s4-i1"],tl["s4-i2"],tl["s4-q"]
st=[0.0, tl["s2"]["start"]-0.1, tl["s3"]["start"]-0.1, tl["s4-i1"]["start"]-0.1, tl["s5"]["start"]-0.1, tl["s6"]["start"]-0.1, tl["s7"]["start"]-0.1, CARD]
# scene 1: Sora + Kling
group("1l",0.0,st[1],-250,"sora.png","Sora"); group("1r",i2["start"]-0.03,st[1],250,"kling.png","Kling")
caps(0.0,i2["start"],["ഇത് Sora"]); caps(i2["start"],q["start"],["ഇത് Kling"]); caps(q["start"],st[1],["എന്താണ് വ്യത്യാസം?"])
poses += [(0.0,i2["start"],"L"),(i2["start"],q["start"],"R"),(q["start"],st[1],"T")]
# scenes 2,3
for n,logo,label,pose,chunks in [(2,"sora.png","Sora","L",["Sora ഉപയോഗിച്ച്","text prompt കൊടുത്ത്","AI videos create ചെയ്യാം."]),
    (3,"kling.png","Kling","R",["Kling-ന്റെ speciality","realistic movements-ഉം","cinematic video shots-ഉം","create ചെയ്യാൻ","കഴിയുന്നതാണ്"])]:
    s,e=st[n-1],st[n]; group(str(n),tl[f"s{n}"]["start"]-0.03,e,0,logo,label); caps(s,e,chunks); poses.append((s,e,pose))
# scene 4: Runway + Veo 3
group("4l",st[3],st[4],-250,"runway.png","Runway"); group("4r",j2["start"]-0.03,st[4],250,"veo.png","Veo 3")
caps(st[3],j2["start"],["ഇത് Runway"]); caps(j2["start"],q2["start"],["ഇത് Veo 3"]); caps(q2["start"],st[4],["എന്താണ് വ്യത്യാസം?"])
poses += [(st[3],j2["start"],"L"),(j2["start"],q2["start"],"R"),(q2["start"],st[4],"T")]
# scenes 5,6
for n,logo,label,pose,chunks in [(5,"runway.png","Runway","L",["Runway ഉപയോഗിച്ച്","AI videos create ചെയ്യാനും","existing videos","edit ചെയ്യാനും കഴിയും"]),
    (6,"veo.png","Veo 3","R",["Veo 3-യുടെ പ്രത്യേകത","video-ക്കൊപ്പം","sound effects-ഉം","dialogues-ഉം generate","ചെയ്യാൻ കഴിയും എന്നതാണ്"])]:
    s,e=st[n-1],st[n]; group(str(n),tl[f"s{n}"]["start"]-0.03,e,0,logo,label); caps(s,e,chunks); poses.append((s,e,pose))
# scene 7: all four logos together
s,e=st[6],st[7]; c7=tl["s7"]
tiles="".join(f'<div id="t7-{k}" class="tile"><img class="tlogo" src="assets/{lg}" alt="{lb} logo"><div class="tlbl">{lb}</div></div>' for k,(lg,lb) in enumerate([("sora.png","Sora"),("kling.png","Kling"),("runway.png","Runway"),("veo.png","Veo 3")]))
clip("g-7", s, e, f'<div class="grid4">{tiles}</div>', z=3)
for k in range(4):
    js.append(f'tl.fromTo("#t7-{k}",{{scale:0.3,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{c7["start"]-0.03+k*0.28:.3f});')
js.append(f'tl.to("#g-7",{{opacity:0,duration:0.2}},{e-0.22:.3f});')
caps(s,e,["ഈ നാല് AI video tools-ന്റെയും","specialities അറിയാൻ","ഈ വീഡിയോ future reference-ന്","save ചെയ്തുവെച്ചോ!"]); poses.append((s,e,"T"))
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
CSS = open(R.parent/"reel"/"hf"/"tools"/"build.py", encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
CSS += """
.gwrap{position:absolute;left:0;top:215px;width:1080px;height:520px;display:flex;justify-content:center}
.grp{width:520px;display:flex;flex-direction:column;align-items:center;gap:14px}
.grp.big{margin-top:24px}
.glbl{font-weight:700;font-size:46px;letter-spacing:-0.5px;white-space:nowrap}
.glogo{height:250px;max-width:460px;width:auto;object-fit:contain;border-radius:30px}
.grid4{position:absolute;left:90px;top:170px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:34px 40px}
.tile{display:flex;flex-direction:column;align-items:center;gap:10px}
.tlogo{height:170px;max-width:300px;width:auto;object-fit:contain;border-radius:24px}
.tlbl{font-weight:700;font-size:38px}
.chip{margin-top:4px;padding:6px 26px;border-radius:30px;background:#eef3ff;color:#2330c9;font-weight:700;font-size:34px;white-space:nowrap}
"""
doc = f"""<!doctype html>
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
(R/"index.html").write_text(doc, encoding="utf-8"); print("wrote", len(doc), "caps", len(cap), "poses", len(poses))
