"""Reel 8: Claude vs ChatGPT - logos alternate scene by scene, final comparison board."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def group(id_, s, e, x, logo, label):
    clip(f"g-{id_}", s, e, f'<div class="gwrap"><div id="g-{id_}-in" class="grp big"><div class="glbl">{html.escape(label)}</div><img class="glogo" src="assets/{logo}" alt="{html.escape(label)} logo"></div></div>', z=3)
    js.append(f'tl.fromTo("#g-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{max(0,s):.3f});')
    js.append(f'tl.to("#g-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.3f});')
def caps(s, e, chunks):
    w=[max(len(c),4) for c in chunks]; tot=sum(w); t=s
    for k,c in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t+=d
i1,i2,q = tl["s1-i1"],tl["s1-i2"],tl["s1-q"]
st=[0.0, tl["s2"]["start"]-0.1, tl["s3"]["start"]-0.1, tl["s4"]["start"]-0.1, tl["s5"]["start"]-0.1, tl["s6"]["start"]-0.1, CARD]
# scene 1: Claude + ChatGPT together
group("1l",0.0,st[1],-250,"claude.png","Claude"); group("1r",i2["start"]-0.03,st[1],250,"chatgpt.png","ChatGPT")
caps(0.0,i2["start"],["ഇത് Claude"]); caps(i2["start"],q["start"],["ഇത് ChatGPT"]); caps(q["start"],st[1],["എന്താണ് വ്യത്യാസം?"])
poses += [(0.0,i2["start"],"L"),(i2["start"],q["start"],"R"),(q["start"],st[1],"T")]
# scenes 2-5: one logo at a time
SC=[(2,"chatgpt.png","ChatGPT","R",["ChatGPT ഉപയോഗിച്ച്","image create ചെയ്യാനും,","voice വഴി സംസാരിക്കാനും,","web search ചെയ്യാനും പറ്റും"]),
    (3,"claude.png","Claude","L",["Claude ആണെങ്കിൽ","long documents വായിക്കാനും,","detailed writing ചെയ്യാനും,","coding ചെയ്യാനും നല്ലതാണ്"]),
    (4,"chatgpt.png","ChatGPT","R",["ChatGPT-യുടെ മറ്റൊരു പ്രത്യേകത,","പലതരം AI tools","ഒരേ platform-ൽ","ഉപയോഗിക്കാം എന്നതാണ്"]),
    (5,"claude.png","Claude","L",["Claude-ന്റെ ഒരു പ്രത്യേകത,","വലിയ documents analyze ചെയ്യാനും","complex information","മനസ്സിലാക്കാൻ സഹായിക്കുന്നു എന്നതാണ്"])]
for n,logo,label,pose,chunks in SC:
    s,e=st[n-1],st[n]
    group(str(n),tl[f"s{n}"]["start"]-0.03,e,0,logo,label); caps(s,e,chunks); poses.append((s,e,pose))
# scene 6: comparison board
s6=st[5]
clip("fin", s6, CARD, '''<div class="fin"><div id="fin-logos" class="finlogos"><img class="flogo" src="assets/claude.png" alt="Claude"><img class="flogo" src="assets/chatgpt.png" alt="ChatGPT"></div>
<div id="fin-cols" class="cols"><div class="col"><h3>CLAUDE</h3><p>Writing</p><p>Long documents</p><p>Coding &amp; Analysis</p></div><div class="col"><h3>CHATGPT</h3><p>Image Creation</p><p>Voice</p><p>Web Search</p></div></div>
<div class="note">ഇവ രണ്ടിനും പല കഴിവുകളും ഒരുപോലെയുണ്ട്. Features plan അനുസരിച്ച് മാറാം.</div></div>''', z=3)
t6=tl["s6"]["start"]-0.03
js.append(f'tl.fromTo("#fin-logos",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{t6:.3f});')
js.append(f'tl.fromTo("#fin-cols",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power2.out"}},{t6+0.35:.3f});')
js.append(f'tl.to("#fin-cols",{{opacity:0,duration:0.2}},{CARD-0.22:.3f}); tl.to("#fin-logos",{{opacity:0,duration:0.2}},{CARD-0.22:.3f});')
caps(s6,CARD,["ഇനി Claude-ന്റെയും","ChatGPT-യുടെയും വ്യത്യാസം","മറക്കണ്ട.","Future reference-ന്","ഈ വീഡിയോ save ചെയ്തുവെച്ചോ!"]); poses.append((s6,CARD,"L"))
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
.grp{width:520px;display:flex;flex-direction:column;align-items:center;gap:18px}
.grp.big{margin-top:30px}
.glbl{font-weight:700;font-size:46px;letter-spacing:-0.5px;white-space:nowrap}
.glogo{height:270px;width:auto;object-fit:contain;border-radius:36px}
.fin{position:absolute;left:0;top:200px;width:1080px;text-align:center}
.finlogos{display:flex;justify-content:center;gap:150px}
.flogo{height:125px;width:auto;border-radius:26px}
.cols{display:flex;justify-content:center;gap:30px;margin-top:20px}
.col{width:480px}
.col h3{font-weight:800;font-size:44px;margin-bottom:4px}
.col p{font-weight:700;font-size:38px;color:#222;margin:4px 0}
.note{margin-top:10px;font-weight:700;font-size:25px;color:#777}
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
