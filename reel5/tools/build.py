"""Generates index.html for reel 2 from audio/timeline.json (ElevenLabs line durations at 1.25x)."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = json.load(open(R/"audio"/"timeline.json"))["clips"]; _d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
L, RT = -262, 262
SCENES = [
 ("Debit Card","debitcard.png","Credit Card","creditcards.png",
  ["Debit Card:","നമ്മുടെ ബാങ്ക് അക്കൗണ്ടിലുള്ള","പൈസയാണ് ഇവിടെ നിന്ന്","നേരിട്ട് കുറയുന്നത്"],
  ["Credit Card:","ബാങ്ക് നമുക്ക് ഒരു","നിശ്ചിത തുക കടമായി","ഉപയോഗിക്കാൻ തരുന്നതാണ്","പിന്നീട് അത് തിരിച്ചടയ്ക്കണം"],"എന്താണ് വ്യത്യാസം?"),
 ("Instant Payment","qrpay.png","Monthly Bill","invoice.png",
  ["Debit Card:","പണം അക്കൗണ്ടിൽ നിന്ന്","ഉടനെ കുറയും"],
  ["Credit Card:","ഇപ്പോൾ പണം ചെലവാക്കാം,","ബിൽ പിന്നീട്","അടച്ചാൽ മതി"],"എന്താണ് വ്യത്യാസം?"),
 ("Bank Balance","phoneapp.png","Credit Limit","cardsbudget.png",
  ["Debit Card:","അക്കൗണ്ടിൽ എത്ര പണമുണ്ടോ","അത്രയും മാത്രമേ സാധാരണ","ഉപയോഗിക്കാൻ കഴിയൂ"],
  ["Credit Card:","ബാങ്ക് അനുവദിച്ച","credit limit വരെ","ഉപയോഗിക്കാം"],"എന്താണ് വ്യത്യാസം?"),
 ("Debit Card","debitcard.png","Credit Card","calc695.png",
  ["Debit Card:","സാധാരണ വാങ്ങലുകൾക്ക് പലിശയില്ല;","അക്കൗണ്ടിലുള്ള പണമാണ്","ഉപയോഗിക്കുന്നത്"],
  ["Credit Card:","Due date-ന് മുമ്പ്","മുഴുവൻ ബില്ലും അടച്ചില്ലെങ്കിൽ","പലിശയും മറ്റ് ചാർജുകളും വരാം"],"ഏതാണ് കൂടുതൽ ശ്രദ്ധിക്കേണ്ടത്?"),
]
h=[]; js=[]; cap=[]; poses=[]
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
def tool(id_, label, img, s, e, x, mv=None, pop_at=None):
    clip(f"t-{id_}", s, e, f'<div class="tool"><div id="t-{id_}-in" class="toolin"><div class="lbl">{html.escape(label)}</div><div class="logo photo"><img src="assets/{img}" alt="{html.escape(label)}"></div></div></div>', z=3)
    base = 0.92 if x else 1.18; p = s if pop_at is None else pop_at
    js.append(f'tl.fromTo("#t-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:{base},opacity:1,duration:0.4,ease:"back.out(1.8)"}},{p:.3f});')
    if mv: js.append(f'tl.to("#t-{id_}-in",{{x:0,scale:1.18,duration:0.45,ease:"power2.inOut"}},{mv:.3f});')
    js.append(f'tl.to("#t-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.3f});')
def caps(i, s, e, chunks):
    w = [max(len(c),4) for c in chunks]; tot = sum(w); t = s
    for k,c in enumerate(chunks):
        d = (e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t += d
nscenes = len(SCENES)
for si,(xl,xi,yl,yi,atx,btx,qtx) in enumerate(SCENES):
    i1,i2,q,a,b = tl[5*si:5*si+5]
    nxt = tl[5*si+5]["start"] if si < nscenes-1 else DUR
    s0 = 0.0 if si==0 else i1["start"]-0.1
    end = nxt-0.1 if si < nscenes-1 else CARD
    tool(f"x{si}", xl, xi, s0, b["start"]+0.05, L, mv=a["start"]-0.1, pop_at=(0.0 if si==0 else i1["start"]-0.03))
    tool(f"ya{si}", yl, yi, i2["start"]-0.03, a["start"]+0.1, RT)
    tool(f"yb{si}", yl, yi, b["start"]-0.03, end, 0)
    caps(si, s0, i2["start"], [f"ഇത് {xl}"]); caps(si, i2["start"], q["start"], [f"ഇത് {yl}"])
    caps(si, q["start"], a["start"], [qtx]); caps(si, a["start"], b["start"], atx); caps(si, b["start"], end, btx)
    poses += [(s0,i2["start"],"L"),(i2["start"],q["start"],"R"),(q["start"],a["start"],"T"),(a["start"],b["start"],"L"),(b["start"],end,"R")]
for i,(s,e,t) in enumerate(cap):
    clip(f"c{i}", s, e, f'<div class="cap"><span id="c{i}-in">{html.escape(t)}</span></div>', z=5)
    js.append(f'tl.fromTo("#c{i}-in",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.18,ease:"power2.out"}},{s:.3f});')
PF = {"L":"pose_pointL.png","R":"pose_pointR.png","T":"pose_think.png"}
for i,(s,e,p) in enumerate(poses):
    clip(f"p{i}", s, e, f'<img id="p{i}-in" class="pose{" think" if p=="T" else ""}" src="assets/{PF[p]}" alt="character">', z=2)
    js.append(f'tl.fromTo("#p{i}-in",{{y:0}},{{y:-9,duration:{(e-s)/2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{s:.3f});')
clip("endcard", CARD, DUR, '<img id="endcard-in" class="endimg" src="assets/endcard.png" alt="Follow fyze.ai">', z=6)
js.append(f'tl.fromTo("#endcard-in",{{opacity:0,scale:1.05}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.4)"}},{CARD});')
clip("wm", 0, CARD, '<div class="wm">@fyze.ai</div>', z=4)
CSS = open(R.parent/"reel"/"hf"/"tools"/"build.py", encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
CSS = CSS
CSS += """
.toolin{width:480px;gap:30px}
.logo.photo{width:440px;height:324px}
.logo.photo img{width:440px;height:324px;object-fit:cover;border-radius:30px;box-shadow:0 6px 22px rgba(0,0,0,.18)}
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
