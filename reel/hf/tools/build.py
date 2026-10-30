"""Generates index.html for the single-character tools Reel.
All times (s) come from ElevenLabs Scribe word timings of audio/voice.mp3."""
import html, json, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "index.html"
DUR = 65.6
CTA = 62.2

# (id, label, logo asset or None for text tile, tile text, start, end, slot x, move-to-centre time)
L, R, C = -262, 262, 0
TOOLS = [
 ("chatgpt","ChatGPT","chatgpt.png",None, 0.0, 7.7, L, 3.9),
 ("claude-a","Claude","claude.png",None, 1.6, 3.9, R, None),
 ("claude-b","Claude","claude.png",None, 7.7,12.9, C, None),
 ("gemini","Gemini","gemini.png",None, 12.9,20.9, L,16.6),
 ("perplexity-a","Perplexity","perplexity.png",None, 14.1,16.6, R,None),
 ("perplexity-b","Perplexity","perplexity.png",None, 20.9,24.7, C,None),
 ("nano","Nano Banana","nanobanana.png",None, 24.7,34.4, L,29.4),
 ("gptimg-a","GPT image 2.0",None,"GPT Image 2.0", 26.2,29.4, R,None),
 ("gptimg-b","GPT image 2.0",None,"GPT Image 2.0", 34.4,41.8, C,None),
 ("kling","Kling",None,"Kling AI", 41.8,55.5, L,46.2),
 ("seedance-a","Seedance 2.5",None,"Seedance 2.5", 43.0,46.2, R,None),
 ("seedance-b","Seedance 2.5",None,"Seedance 2.5", 55.5,CTA, C,None),
]
CUES = [
 (0.0,1.6,"ഇത് ChatGPT"),(1.6,2.7,"ഇത് Claude"),(2.7,3.9,"എന്താണ് വ്യത്യാസം?"),
 (3.9,5.5,"ChatGPT എല്ലാ കാര്യത്തിനും"),(5.5,6.6,"ഉപയോഗിക്കാവുന്ന ഒരു"),(6.6,7.7,"all round tool ആണ്"),
 (7.7,9.4,"Claude deep ആയി ചിന്തിച്ച്"),(9.4,11.05,"കൂടുതൽ കൃത്യവും വിശദവുമായ"),(11.05,12.9,"ഉത്തരങ്ങൾ നൽകുന്നതിലാണ് ശക്തൻ"),
 (12.9,14.1,"ഇത് Gemini"),(14.1,15.4,"ഇത് Perplexity"),(15.4,16.6,"എന്താണ് വ്യത്യാസം?"),
 (16.6,18.25,"Gemini നിങ്ങളുടെ Gmail,"),(18.25,19.2,"Docs, Drive"),(19.2,20.25,"എന്നിവയുമായി നേരിട്ട്"),(20.25,20.9,"പ്രവർത്തിക്കും"),
 (20.9,22.55,"Perplexity source ലിങ്കുകൾ"),(22.55,23.62,"ഉൾപ്പെടെ research ചെയ്ത"),(23.62,24.7,"ഉത്തരങ്ങൾ നൽകും"),
 (24.7,26.2,"ഇത് Nano Banana"),(26.2,28.2,"ഇത് GPT Image 2.0"),(28.2,29.4,"എന്താണ് വ്യത്യാസം?"),
 (29.4,30.95,"Nano Banana പ്രധാനമായും"),(30.95,31.95,"image editing നും"),(31.95,33.2,"image manipulation നും"),(33.2,34.4,"ആണ് കൂടുതൽ ഉപയോഗിക്കുന്നത്"),
 (34.4,35.8,"GPT Image 2.0"),(35.8,37.0,"cinematic look ഓടെയും"),(37.0,38.3,"high quality rendering ഓടെയും"),(38.3,39.35,"professional images"),(39.35,40.5,"സൃഷ്ടിക്കാൻ മികച്ച"),(40.5,41.8,"AI image model ആണ്"),
 (41.8,43.0,"ഇത് Kling"),(43.0,45.1,"ഇത് Seedance 2.5"),(45.1,46.2,"എന്താണ് വ്യത്യാസം?"),
 (46.2,47.88,"Kling realistic motion ഉം"),(47.88,49.1,"cinematic look ഉം നൽകുന്ന"),(49.1,51.0,"മികച്ച AI video model ആണ്"),
 (51.0,52.65,"ഇപ്പോൾ ഇതിലൂടെ പരമാവധി"),(52.65,53.8,"പതിനഞ്ച് second വരെയുള്ള"),(53.8,55.5,"video കളാണ് create ചെയ്യാൻ പറ്റുന്നത്"),
 (55.5,57.0,"Seedance 2.5"),(57.0,58.55,"കൂടുതൽ realistic lighting ഉം"),(58.55,59.6,"texture ഉം നൽകും"),(59.6,60.6,"ഒറ്റ shot ന്റെ"),(60.6,CTA,"visual quality യിലാണ് ഇതിന്റെ ശക്തി"),
]
POSES = [(0,1.6,"L"),(1.6,2.7,"R"),(2.7,3.9,"T"),(3.9,7.7,"L"),(7.7,12.9,"R"),(12.9,14.1,"L"),(14.1,15.4,"R"),(15.4,16.6,"T"),
 (16.6,20.9,"L"),(20.9,24.7,"R"),(24.7,26.2,"L"),(26.2,28.2,"R"),(28.2,29.4,"T"),(29.4,34.4,"L"),(34.4,41.8,"R"),
 (41.8,43.0,"L"),(43.0,45.1,"R"),(45.1,46.2,"T"),(46.2,55.5,"L"),(55.5,CTA,"R")]
POSEFILE = {"L":"pose_pointL.png","R":"pose_pointR.png","T":"pose_think.png"}

h=[]; js=[]
def clip(id_, start, end, body, cls="", z=1, extra=""):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.2f}" data-duration="{end-start:.2f}" data-track-index="{z}" style="z-index:{z}" {extra}>{body}</div>')

for (id_,label,img,txt,s,e,x,mv) in TOOLS:
    logo = f'<img src="assets/{img}" alt="{html.escape(label)} logo">' if img else f'<div class="ph">{html.escape(txt)}</div>'
    clip(f"t-{id_}", s, e, f'<div class="tool"><div id="t-{id_}-in" class="toolin"><div class="lbl">{html.escape(label)}</div><div class="logo">{logo}</div></div></div>', z=3)
    base = 0.92 if x else 1.18
    js.append(f'tl.fromTo("#t-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:{base},opacity:1,duration:0.4,ease:"back.out(1.8)"}},{s});')
    if mv: js.append(f'tl.to("#t-{id_}-in",{{x:0,scale:1.18,duration:0.45,ease:"power2.inOut"}},{mv});')
    js.append(f'tl.to("#t-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.2f});')

for i,(s,e,t) in enumerate(CUES):
    clip(f"c{i}", s, e, f'<div class="cap"><span id="c{i}-in">{html.escape(t)}</span></div>', z=5)
    js.append(f'tl.fromTo("#c{i}-in",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.18,ease:"power2.out"}},{s});')

for i,(s,e,p) in enumerate(POSES):
    cls = "pose think" if p=="T" else "pose"
    clip(f"p{i}", s, e, f'<img id="p{i}-in" class="{cls}" src="assets/{POSEFILE[p]}" alt="character">', z=2)
    js.append(f'tl.fromTo("#p{i}-in",{{y:0}},{{y:-9,duration:{(e-s)/2:.2f},ease:"sine.inOut",yoyo:true,repeat:1}},{s});')

# End card: user's "Follow fyze.ai" image replaces the follow-for-more CTA and the Instagram card
clip("endcard", CTA, DUR, '<img id="endcard-in" class="endimg" src="assets/endcard.png" alt="Follow fyze.ai">', z=6)
js.append(f'tl.fromTo("#endcard-in",{{opacity:0,scale:1.05}},{{opacity:1,scale:1,duration:0.45,ease:"power2.out"}},{CTA});')
# small black username watermark under the character, hidden once the end card is up
clip("wm", 0, CTA, '<div class="wm">@fyze.ai</div>', z=4)

CSS = """
@font-face{font-family:"NotoMal";font-weight:800;src:url("assets/fonts/mal800.woff2") format("woff2")}
@font-face{font-family:"PopFz";font-weight:800;src:url("assets/fonts/pop800.woff2") format("woff2")}
@font-face{font-family:"PopFz";font-weight:700;src:url("assets/fonts/pop700.woff2") format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#fff}
#root{position:absolute;inset:0;background:#fff;font-family:"PopFz","NotoMal",sans-serif;color:#0b0b0b}
.tool{position:absolute;left:0;top:215px;width:1080px;height:520px;display:flex;justify-content:center}
.toolin{display:flex;flex-direction:column;align-items:center;gap:34px;width:360px}
.lbl{font-weight:700;font-size:46px;letter-spacing:-0.5px;white-space:nowrap}
.logo{width:300px;height:300px;display:flex;align-items:center;justify-content:center}
.logo img{width:300px;height:300px;object-fit:contain;border-radius:36px}
.ph{width:300px;height:300px;border-radius:66px;background:#f1f3f5;border:5px solid #e3e6ea;display:flex;align-items:center;justify-content:center;text-align:center;padding:26px;font-weight:800;font-size:54px;line-height:1.1}
.cap{position:absolute;left:60px;top:700px;width:960px;height:190px;display:flex;align-items:center;justify-content:center;text-align:center}
.cap span{display:block;font-weight:800;font-size:64px;line-height:1.28;letter-spacing:-0.5px}
.pose{position:absolute;left:50%;margin-left:-161px;top:985px;height:700px;width:auto}
.pose.think{margin-left:-123px}
.endimg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.wm{position:absolute;left:0;top:1722px;width:1080px;text-align:center;font-weight:700;font-size:38px;letter-spacing:0.5px;color:#000;opacity:0.7}
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
OUT.write_text(doc, encoding="utf-8")
print("wrote", OUT, len(doc))
