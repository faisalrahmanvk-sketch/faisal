"""Reel 16: Dubai vs UAE (scenes 1-3), Emirate vs State/Kerala (scenes 4-5). Photos on top, highlight moves, character below."""
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
ST=lambda n: c(n)["start"]-0.03
S2=c(4)["start"]-0.1; S3=c(9)["start"]-0.1; S4=c(14)["start"]-0.1; S5=c(23)["start"]-0.1
def pair(pfx, s, e, right, left, t_r, t_l):
    """right/left = (id, photo, label). Right pops at t_r, left at t_l."""
    def tile(i,side,img,lab): return f'<div id="{pfx}{i}" class="tile {side}"><div class="tl">{html.escape(lab)}</div><img src="assets/{img}" alt="{html.escape(lab)}"></div>'
    clip(f"pair-{pfx}", s, e, tile("r","r",right[1],right[2])+tile("l","l",left[1],left[2]), z=3)
    js.append(f'gsap.set("#{pfx}r,#{pfx}l",{{opacity:0}});')
    js.append(f'tl.fromTo("#{pfx}r",{{x:120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_r:.3f});')
    js.append(f'tl.fromTo("#{pfx}l",{{x:-120,scale:0.4,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_l:.3f});')
    js.append(f'tl.to("#pair-{pfx}",{{opacity:0,duration:0.2}},{e-0.22:.3f});')
    clicks.extend([round(t_r+0.02,3), round(t_l+0.02,3)])
def single(id_, img, s, e):
    clip(f"ph-{id_}", s, e, f'<div class="ph"><img id="ph-{id_}-in" src="assets/{img}" alt="{id_}"></div>', z=3)
    js.append(f'tl.fromTo("#ph-{id_}-in",{{scale:0.4,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:0.45,ease:"back.out(1.6)"}},{max(0,s):.3f});')
    js.append(f'tl.to("#ph-{id_}-in",{{opacity:0,scale:0.92,duration:0.2}},{e-0.22:.3f});')
    clicks.append(round(max(0,s)+0.02,3))
def hl(on, off, at):
    clicks.append(round(at+0.02,3))
    js.append(f'tl.to("{on}",{{scale:1.07,opacity:1,duration:0.35,ease:"power2.out"}},{at:.3f});')
    js.append(f'tl.to("{off}",{{scale:0.9,opacity:0.45,duration:0.35,ease:"power2.out"}},{at:.3f});')
# ---- visuals
pair("a", 0.0, S4+0.25, ("r","dubai.jpg","Dubai"), ("l","uae_map.jpg","UAE"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Dubai highlighted, UAE smaller
hl("#al","#ar", ST(9))      # scene 3: UAE map highlighted, Dubai smaller
pair("b", S4, CARD+0.1, ("r","emirate.jpg","Emirate"), ("l","kerala.jpg","State (Kerala)"), ST(14), ST(15))
hl("#br","#bl", ST(17))     # scene 4 explanation: Emirate highlighted
hl("#bl","#br", ST(23))     # scene 5: Kerala highlighted
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Dubai."],2:["ഇതാണ് UAE."],3:["എന്താണ് വ്യത്യാസം?"],
4:["Dubai ഒരു","രാജ്യമല്ല!"],5:["UAE-യിലെ 7 emirates-ൽ","ഒന്നാണ് Dubai."],6:["UAE-യിലെ ഏറ്റവും വലിയ","city-യും ഇതാണ്."],
7:["ഇപ്പോൾ ഏകദേശം","48 ലക്ഷം ആളുകൾ","Dubai-ൽ താമസിക്കുന്നുണ്ട്."],
8:["പക്ഷേ വലിപ്പം നോക്കിയാൽ","നമ്മുടെ Idukki district-നേക്കാൾ","കുറച്ച് ചെറുതാണ് Dubai!"],
9:["UAE എന്നാൽ","United Arab Emirates."],
10:["7 emirates ചേർന്ന","ഒരു രാജ്യമാണിത്:","Abu Dhabi, Dubai,","Sharjah, Ajman,","Umm Al Quwain,","Ras Al Khaimah, Fujairah."],
11:["1971 December 2-നാണ്","UAE രൂപീകരിച്ചത്."],12:["UAE-യുടെ capital","Dubai അല്ല,","Abu Dhabi ആണ്!"],
13:["വലിപ്പത്തിൽ UAE-ക്ക്","നമ്മുടെ Kerala-യുടെ","ഏകദേശം ഇരട്ടിയുണ്ട്."],
14:["ഇതാണ് Emirate."],15:["ഇതാണ് നമ്മുടെ State."],16:["എന്താണ് വ്യത്യാസം?"],
17:["ഓരോ emirate-നും","സ്വന്തമായി ഒരു","ruler ഉണ്ട്."],
18:["ആ ruler-നെ ആരും","vote ചെയ്ത് തിരഞ്ഞെടുക്കുന്നതല്ല,","family വഴി കൈമാറി","വരുന്നതാണ്."],
19:["7 emirates-ന്റെയും","rulers ചേർന്നതാണ്","Federal Supreme Council."],
20:["അവരാണ് UAE-യുടെ","President-നെ","തിരഞ്ഞെടുക്കുന്നത്."],
21:["ഓരോ emirate-നും സ്വന്തമായി","നിയമങ്ങൾ ഉണ്ടാക്കാൻ","അധികാരമുണ്ട്."],
22:["അതുകൊണ്ടാണ് Dubai-യിലെയും","Sharjah-യിലെയും rules ചിലപ്പോൾ","വ്യത്യസ്തമായിരിക്കുന്നത്."],
23:["Kerala India-യിലെ","ഒരു state ആണ്."],24:["1956 November 1-നാണ്","Kerala രൂപീകരിച്ചത്."],25:["ഇവിടെ ruler ഇല്ല."],
26:["നമ്മൾ vote ചെയ്ത്","MLA-മാരെ തിരഞ്ഞെടുക്കും,","അവരിൽ നിന്നാണ്","Chief Minister വരുന്നത്."],
27:["അതാണ് ഏറ്റവും","വലിയ വ്യത്യാസം:"],28:["Emirate-ൽ ruler,","Kerala-യിൽ നമ്മൾ തിരഞ്ഞെടുക്കുന്ന","government!"]}
KEEP=list(range(1,29))
starts={}
for i_,n in enumerate(KEEP): starts[n]=0.0 if i_==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i_+1]] if i_+1<len(KEEP) else CARD) for i_,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses (first item = right, second = left)
pose_of={}
for n in range(1,29): pose_of[n]="R"
pose_of[2]="L"; pose_of[3]="T"
for n in range(9,14): pose_of[n]="L"          # UAE map is on the left
pose_of[15]="L"; pose_of[16]="T"
for n in range(23,29): pose_of[n]="L"         # Kerala is on the left
seg=[]; cur=None
for n in KEEP:
    if cur and cur[2]==pose_of[n]: cur[1]=ends[n]
    else: cur=[starts[n],ends[n],pose_of[n]]; seg.append(cur)
poses=[tuple(x) for x in seg]
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
.tile img{width:470px;height:350px;object-fit:cover;border-radius:28px;box-shadow:0 12px 34px rgba(0,0,0,.22);border:2px solid #e5e7eb;display:block}
.ph{position:absolute;left:120px;top:80px;width:840px;height:630px}
.ph img{width:840px;height:630px;object-fit:cover;border-radius:34px;box-shadow:0 16px 44px rgba(0,0,0,.25);border:2px solid #e5e7eb;display:block}
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
