"""Reel 19: Sheikh Mohammed vs Sheikh Mohamed (scenes 1-3), Ruler vs President (scenes 4-5). Photos on top, highlight moves, character below."""
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
S2=c(4)["start"]-0.1; S3=c(10)["start"]-0.1; S4=c(16)["start"]-0.1; S5=c(23)["start"]-0.1
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
pair("a", 0.0, S4+0.25, ("r","mbr.jpg","Sheikh Mohammed"), ("l","mbz.jpg","Sheikh Mohamed"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Sheikh Mohammed bin Rashid highlighted
hl("#al","#ar", ST(10))     # scene 3: Sheikh Mohamed bin Zayed highlighted
pair("b", S4, CARD+0.1, ("r","uae_emirates_map.jpg","Ruler"), ("l","uae_flag_photo.jpg","President"), ST(16), ST(17))
hl("#br","#bl", ST(19))     # scene 4 explanation: Ruler (7 emirates map) highlighted
hl("#bl","#br", ST(23))     # scene 5: President (UAE flag) highlighted
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Sheikh Mohammed."],2:["ഇതാണ് Sheikh Mohamed."],3:["എന്താണ് വ്യത്യാസം?"],
4:["പേര് ഏകദേശം ഒന്നാണ്,","പക്ഷേ ആള് വേറെയാണ്!"],5:["ഇത് Sheikh Mohammed","bin Rashid Al Maktoum."],
6:["Dubai-യുടെ Ruler","ഇദ്ദേഹമാണ്."],7:["2006 മുതൽ","Dubai ഭരിക്കുന്നു."],
8:["UAE-യുടെ Vice President-ഉം","Prime Minister-ഉം","ഇദ്ദേഹം തന്നെയാണ്."],
9:["Burj Khalifa, Dubai Metro,","Dubai Mall ഒക്കെ വന്നത്","ഇദ്ദേഹത്തിന്റെ","ഭരണകാലത്താണ്."],
10:["ഇത് Sheikh Mohamed","bin Zayed Al Nahyan."],11:["UAE-യുടെ President","ഇദ്ദേഹമാണ്."],12:["Abu Dhabi-യുടെ Ruler-ഉം","ഇദ്ദേഹം തന്നെ."],
13:["2022-ൽ ആണ്","President ആയത്."],14:["UAE സ്ഥാപിച്ച","Sheikh Zayed-ന്റെ മകനാണ്."],
15:["UAE-യുടെ മൂന്നാമത്തെ","President-ഉം ഇദ്ദേഹമാണ്."],
16:["ഇതാണ് Ruler."],17:["ഇതാണ് President."],18:["എന്താണ് വ്യത്യാസം?"],
19:["UAE-യിലെ 7 emirates-നും","ഓരോ Ruler ഉണ്ട്."],20:["അതായത് UAE-യിൽ","ആകെ 7 Rulers."],
21:["Ruler എന്നാൽ ആ emirate","ഭരിക്കുന്ന ആൾ."],
22:["Dubai-യിൽ Al Maktoum","family-യും Abu Dhabi-യിൽ","Al Nahyan family-യുമാണ്","ഭരിക്കുന്നത്."],
23:["President ഒരു emirate-ന്റെ","മാത്രം അല്ല,","UAE എന്ന രാജ്യത്തിന്റെ","മുഴുവൻ തലവനാണ്."],
24:["ആ 7 Rulers ചേർന്നാണ്","President-നെ","തിരഞ്ഞെടുക്കുന്നത്."],
25:["ചുരുക്കി പറഞ്ഞാൽ:","Sheikh Mohammed","Dubai-യുടെ Ruler,","Sheikh Mohamed","UAE-യുടെ President!"]}
KEEP=list(range(1,26))
starts={}
for i_,n in enumerate(KEEP): starts[n]=0.0 if i_==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i_+1]] if i_+1<len(KEEP) else CARD) for i_,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses (first item = right, second = left)
pose_of={n:"R" for n in range(1,26)}
pose_of[2]="L"; pose_of[3]="T"
for n in range(10,16): pose_of[n]="L"         # Sheikh Mohamed (left)
pose_of[17]="L"; pose_of[18]="T"
for n in range(23,26): pose_of[n]="L"         # President = flag (left)
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
