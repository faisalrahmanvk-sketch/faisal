"""Reel 7: each scene shows ChatGPT (left) and Google Search (right) groups (logo + icon) at the same time."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
LX, RX = -235, 235
h=[]; js=[]; cap=[]; poses=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def group(id_, s, e, x, logo, icon, big=False):
    ic = f'<img class="gicon" src="assets/{icon}" alt="">' if icon else ""
    clip(f"g-{id_}", s, e, f'<div class="gwrap"><div id="g-{id_}-in" class="grp{" big" if big else ""}"><img class="glogo" src="assets/{logo}" alt="">{ic}</div></div>', z=3)
    js.append(f'tl.fromTo("#g-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{max(0,s):.3f});')
    js.append(f'tl.to("#g-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.3f});')
def caps(s, e, chunks):
    w=[max(len(c),4) for c in chunks]; tot=sum(w); t=s
    for k,c in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t+=d
S1=("ChatGPT","chatgpt.png","Google Search","google.png")
# (left icon, right icon, x-chunks, y-chunks)
SC=[
 ("answer.png","links.png",["ChatGPT-ൽ ചോദിച്ചാൽ","വിവരങ്ങൾ ഒരു answer ആയി","കിട്ടും"],["Google Search-ൽ തിരഞ്ഞാൽ","ബന്ധപ്പെട്ട website links","കിട്ടും"]),
 ("create.png","search.png",["ChatGPT ഉപയോഗിച്ച്","captions, emails,","പുതിയ ideas ഒക്കെ ഉണ്ടാക്കാം"],["Google Search ഉപയോഗിച്ച്","websites, news, images","എന്നിവ കണ്ടെത്താം"]),
 ("answer.png","source.png",["ഒരു കാര്യം എളുപ്പത്തിൽ","മനസ്സിലാക്കാൻ","ChatGPT സഹായിക്കും"],["വിവരങ്ങളുടെ original source","പരിശോധിക്കാൻ","Google Search സഹായിക്കും"]),
]
starts=[0.0, tl["s2-x"]["start"]-0.1, tl["s3-x"]["start"]-0.1, tl["s4-x"]["start"]-0.1, CARD]
# ---- scene 1
i1,i2,q,a,b = [tl[k] for k in ("s1-i1","s1-i2","s1-q","s1-a","s1-b")]
end1=starts[1]-0.1
group("1l",0.0,end1,LX,"chatgpt.png",None,True); group("1r",i2["start"]-0.03,end1,RX,"google.png",None,True)
caps(0.0,i2["start"],["ഇത് ChatGPT"]); caps(i2["start"],q["start"],["ഇത് Google Search"]); caps(q["start"],a["start"],["എന്താണ് വ്യത്യാസം?"])
caps(a["start"],b["start"],["ChatGPT:","നമ്മുടെ ചോദ്യങ്ങൾക്ക്","മനസ്സിലാകുന്ന രീതിയിൽ","ഉത്തരം നൽകും"]); caps(b["start"],end1,["Google Search:","നമുക്ക് വേണ്ട വിവരങ്ങളുള്ള","websites","കണ്ടെത്തിത്തരും"])
poses += [(0.0,i2["start"],"L"),(i2["start"],q["start"],"R"),(q["start"],a["start"],"T"),(a["start"],b["start"],"L"),(b["start"],end1,"R")]
# ---- scenes 2-4
for n,(li,ri,xc,yc) in enumerate(SC, start=2):
    x,y=tl[f"s{n}-x"],tl[f"s{n}-y"]; s0=starts[n-1]; end=starts[n]-0.1 if n<4 else CARD
    group(f"{n}l",s0,end,LX,"chatgpt.png",li); group(f"{n}r",y["start"]-0.03,end,RX,"google.png",ri)
    caps(s0,y["start"],xc); caps(y["start"],end,yc)
    poses += [(s0,y["start"],"L"),(y["start"],end,"R")]
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
.grp{width:440px;display:flex;flex-direction:column;align-items:center;gap:16px}
.glogo{height:150px;width:auto;object-fit:contain;border-radius:24px}
.gicon{width:430px;height:260px;object-fit:contain}
.grp.big{margin-top:70px}
.grp.big .glogo{height:300px}
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
