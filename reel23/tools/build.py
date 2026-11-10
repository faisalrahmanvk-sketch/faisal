"""Reel 23: Big Ticket vs Onam Bumper (scenes 1-3), Dubai Duty Free vs Kerala daily lottery (scenes 4-5). Safe side margins."""
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
S2=c(4)["start"]-0.1; S3=c(10)["start"]-0.1; S4=c(15)["start"]-0.1; S5=c(21)["start"]-0.1
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
pair("a", 0.0, S4+0.25, ("r","bigticket.jpg","Big Ticket"), ("l","onam.jpg","Onam Bumper"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Big Ticket highlighted
hl("#al","#ar", ST(10))     # scene 3: Onam Bumper highlighted
pair("b", S4, CARD+0.1, ("r","ddf.jpg","Dubai Duty Free"), ("l","kerala_lottery.jpg","Kerala Lottery"), ST(15), ST(16))
hl("#br","#bl", ST(18))     # scene 4 explanation: Dubai Duty Free highlighted
hl("#bl","#br", ST(21))     # scene 5: Kerala daily lottery highlighted
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Big Ticket."],2:["ഇതാണ് Onam Bumper."],3:["എന്താണ് വ്യത്യാസം?"],
4:["Big Ticket Dubai-യിലാണ്","എന്നാണ് പലരും","കരുതുന്നത്."],5:["പക്ഷേ ഇത്","Abu Dhabi-യിലാണ്!"],
6:["എല്ലാ മാസവും 3-ആം തീയതി","Abu Dhabi Airport-ൽ","വെച്ചാണ് draw."],
7:["ഒരു ticket-ന് 500 Dirham ആണ്,","അതായത് ഏകദേശം","12,800 രൂപ!"],
8:["grand prize","25 million Dirham ആണ്."],9:["നമ്മുടെ നാട്ടിലെ","ഏകദേശം 64 കോടി രൂപ!"],
10:["Onam Bumper നമ്മുടെ Kerala","government-ന്റെ lottery ആണ്."],11:["ഈ വർഷത്തെ ഒന്നാം സമ്മാനം","30 കോടി രൂപ ആയിരുന്നു."],
12:["Ticket-ന് 500 രൂപ","മാത്രം."],13:["പക്ഷേ ഒരു","twist ഉണ്ട്!"],
14:["10 ശതമാനം agent commission-ഉം","30 ശതമാനം tax-ഉം കഴിഞ്ഞാൽ","winner-ന്റെ കയ്യിൽ കിട്ടുന്നത്","ഏകദേശം 19 കോടി രൂപ","മാത്രമാണ്."],
15:["ഇതാണ് Dubai Duty Free","Millionaire."],16:["ഇതാണ് Kerala","Daily Lottery."],17:["എന്താണ് വ്യത്യാസം?"],
18:["Dubai Airport-ലാണ്","ഇത് നടക്കുന്നത്."],
19:["First Prize 1 million dollar,","അതായത് ഏകദേശം 9 കോടി","രൂപയിലധികം."],
20:["ഇതുവരെ 250-ലധികം Indians-ന്","ഈ 1 million dollar","അടിച്ചിട്ടുണ്ട്!"],
21:["നമ്മുടെ Kerala-ത്തിൽ","ദിവസവും lottery draw ഉണ്ട്."],22:["ഒരു ticket-ന്","50 രൂപ മാത്രം."],
23:["ഒന്നാം സമ്മാനം","1 കോടി രൂപ."],24:["Commission-ഉം tax-ഉം കഴിഞ്ഞാൽ","കയ്യിൽ കിട്ടുന്നത്","ഏകദേശം 63 ലക്ഷം."]}
KEEP=list(range(1,25))
starts={}
for i_,n in enumerate(KEEP): starts[n]=0.0 if i_==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i_+1]] if i_+1<len(KEEP) else CARD) for i_,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses (first item = right, second = left)
pose_of={n:"R" for n in range(1,25)}
pose_of[2]="L"; pose_of[3]="T"
for n in range(10,15): pose_of[n]="L"         # Onam Bumper (left)
pose_of[16]="L"; pose_of[17]="T"
for n in range(21,25): pose_of[n]="L"         # Kerala daily lottery (left)
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
clip("wm", 0, CARD, '<div class="wm">@fyze.ai</div>', z=4)
clip("endcard", CARD, DUR, '<img id="endcard-in" class="endimg" src="assets/endcard.png" alt="Follow fyze.ai">', z=7)
js.append(f'tl.fromTo("#endcard-in",{{opacity:0,scale:1.05}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.4)"}},{CARD});')
json.dump(clicks, open(R/"tools"/"clicks.json","w"))
CSS = open(R.parent/"reel"/"hf"/"tools"/"build.py", encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
CSS += """
/* SAFE MARGINS (approved): photos stay >=100px away from both edges so cropped / 16:9 / fit-to-phone uploads never cut them */
.tile{position:absolute;top:190px;width:430px;text-align:center}
.tile.l{left:95px}.tile.r{left:555px}
.tl{font-weight:800;font-size:42px;margin-bottom:12px;letter-spacing:-0.5px;white-space:nowrap}
.tile img{width:430px;height:350px;object-fit:cover;border-radius:26px;box-shadow:0 12px 34px rgba(0,0,0,.22);border:2px solid #e5e7eb;display:block}
.wrap{position:relative}
.ov{position:absolute;left:0;top:0;opacity:0}
.ph{position:absolute;left:160px;top:90px;width:760px;height:570px}
.ph img{width:760px;height:570px;object-fit:cover;border-radius:30px;box-shadow:0 16px 44px rgba(0,0,0,.25);border:2px solid #e5e7eb;display:block}
.cap{left:120px;width:840px}
.board{position:absolute;left:110px;top:70px;width:860px}
.bt{font-weight:800;font-size:40px;text-align:center;color:#475569;margin-bottom:14px}
.row{display:flex;align-items:center;justify-content:space-between;background:#fff;border:3px solid #e5e7eb;border-radius:30px;padding:12px 36px;margin-bottom:16px;box-shadow:0 14px 36px rgba(0,0,0,.14)}
.rl b{display:block;font-weight:800;font-size:46px;color:#0b0b14}
.rl span{font-weight:700;font-size:30px;color:#64748b}
.rp{font-weight:800;font-size:78px;letter-spacing:-2px}
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
