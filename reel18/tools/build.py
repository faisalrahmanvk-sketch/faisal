"""Reel 18: Emirates vs Etihad (scenes 1-3), flydubai vs Air Arabia (scenes 4-5). Photos on top, highlight moves, character below."""
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
S2=c(4)["start"]-0.1; S3=c(10)["start"]-0.1; S4=c(16)["start"]-0.1; S5=c(25)["start"]-0.1
def pair(pfx, s, e, right, left, t_r, t_l, overlay=None):
    """right/left = (id, photo, label). Right pops at t_r, left at t_l."""
    def tile(i,side,img,lab):
        ov = f'<img class="ov" id="{pfx}{i}-ov" src="assets/{overlay}" alt="">' if (overlay and i=="r") else ""
        return f'<div id="{pfx}{i}" class="tile {side}"><div class="tl">{html.escape(lab)}</div><div class="wrap"><img src="assets/{img}" alt="{html.escape(lab)}">{ov}</div></div>'
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
pair("a", 0.0, S4+0.25, ("r","emirates.jpg","Emirates"), ("l","etihad.jpg","Etihad"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Emirates highlighted, Etihad smaller
hl("#al","#ar", ST(10))     # scene 3: Etihad highlighted
pair("b", S4, CARD+0.1, ("r","flydubai.jpg","flydubai"), ("l","airarabia.jpg","Air Arabia"), ST(16), ST(17))
hl("#br","#bl", ST(21))     # scene 4: flydubai highlighted once its own facts start
hl("#bl","#br", ST(25))     # scene 5: Air Arabia highlighted
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Emirates."],2:["ഇതാണ് Etihad."],3:["എന്താണ് വ്യത്യാസം?"],
4:["Emirates Dubai-യുടെ","airline ആണ്."],5:["Dubai government ആണ്","ഇതിന്റെ owner."],6:["1985-ൽ ആണ്","Emirates തുടങ്ങിയത്."],
7:["Middle East-ലെ ഏറ്റവും","വലിയ airline-ഉം ഇതാണ്."],
8:["ലോകത്തിലെ ഏറ്റവും വലിയ","passenger plane ആയ A380","ഏറ്റവും കൂടുതൽ ഉള്ളതും","Emirates-ന്റെ കയ്യിലാണ്,","100-ൽ കൂടുതൽ!"],
9:["Dubai International Airport","ആണ് Emirates-ന്റെ base."],
10:["Etihad Abu Dhabi-യുടെ","airline ആണ്."],11:["2003-ൽ ആണ് തുടങ്ങിയത്,","അതായത് Emirates വന്ന്","18 വർഷം കഴിഞ്ഞ്."],
12:["Etihad എന്ന Arabic","വാക്കിന്റെ അർത്ഥം","'ഐക്യം' എന്നാണ്."],13:["UAE-യിലെ 7 emirates-ന്റെ","ഒരുമയാണ് ആ പേര്","കാണിക്കുന്നത്."],
14:["Abu Dhabi-യിലെ Zayed","International Airport","ആണ് base."],
15:["അപ്പോൾ ഒരേ രാജ്യത്തെ","രണ്ട് വലിയ airlines,","പക്ഷേ രണ്ട്","emirates-ന്റേതാണ്!"],
16:["ഇതാണ് flydubai."],17:["ഇതാണ് Air Arabia."],18:["എന്താണ് വ്യത്യാസം?"],
19:["രണ്ടും budget","airlines ആണ്."],20:["Ticket rate കുറവാണ്,","പക്ഷേ പല tickets-ലും","food-നും extra baggage-നും","വേറെ പൈസ കൊടുക്കണം."],
21:["flydubai-യും Dubai","government-ന്റെ airline ആണ്."],22:["Emirates-ന്റെ sister airline","എന്ന് പറയാം."],
23:["2009-ൽ ആയിരുന്നു","flydubai-യുടെ first flight."],24:["Dubai Airport-ലെ","Terminal 2-ൽ നിന്നാണ്","കൂടുതലും flights."],
25:["Air Arabia Sharjah-യുടെ","airline ആണ്."],26:["2003-ൽ തുടങ്ങി,","അതായത് flydubai-യേക്കാൾ","6 വർഷം മുമ്പ്."],
27:["UAE-യിലെ ആദ്യത്തെ","budget airline ഇതാണ്."],28:["ഒരു twist","കൂടി ഉണ്ട്!"],
29:["Air Arabia stock market-ൽ","list ചെയ്ത company ആണ്."],30:["അതായത് investors-ന്","ഇതിന്റെ shares വാങ്ങാം."],
31:["Sharjah കൂടാതെ","Abu Dhabi-യിൽ നിന്നും","Ras Al Khaimah-യിൽ നിന്നും","Air Arabia flights ഉണ്ട്."]}
KEEP=list(range(1,32))
starts={}
for i_,n in enumerate(KEEP): starts[n]=0.0 if i_==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i_+1]] if i_+1<len(KEEP) else CARD) for i_,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses (first item = right, second = left)
pose_of={n:"R" for n in range(1,32)}
pose_of[2]="L"; pose_of[3]="T"
for n in range(10,16): pose_of[n]="L"         # Etihad is on the left
pose_of[17]="L"; pose_of[18]="T"; pose_of[19]="T"; pose_of[20]="T"   # both planes: neutral
for n in range(25,32): pose_of[n]="L"         # Air Arabia is on the left
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
.wrap{position:relative}
.ov{position:absolute;left:0;top:0;opacity:0}
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
