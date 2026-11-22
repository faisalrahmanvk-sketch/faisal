"""Reel 30: Dubai Run vs Normal Race (scenes 1-3), Dubai Run vs Dubai Ride (scenes 4-6). Landscape photos are stacked (top/bottom) so they stay big and whole."""
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
def pair(pfx, s, e, right, left, t_r, t_l, overlay=None):
    """right/left = (id, photo, label). Right pops at t_r, left at t_l."""
    def tile(i,side,img,lab):
        ov = f'<img class="ov" id="{pfx}{i}-ov" src="assets/{overlay}" alt="">' if (overlay and i=="r") else ""
        return f'<div id="{pfx}{i}" class="tile {side}"><div class="tl">{html.escape(lab)}</div><div class="wrap"><img src="assets/{img}" alt="{html.escape(lab)}">{ov}</div></div>'
    clip(f"pair-{pfx}", s, e, tile("r","r",right[1],right[2])+tile("l","l",left[1],left[2]), z=3)
    js.append(f'gsap.set("#{pfx}r,#{pfx}l",{{opacity:0}});')
    js.append(f'tl.fromTo("#{pfx}r",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_r:.3f});')
    js.append(f'tl.fromTo("#{pfx}l",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.7)"}},{t_l:.3f});')
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
S4=c(14)["start"]-0.1
CH=json.load(open(R/"audio"/"timeline.json"))["chunks"]
ph18=[x for x in CH if x["sent"]==18][1]["start"]
# pair() "r" tile = TOP photo (Dubai Run, named first), "l" tile = BOTTOM photo
pair("a", 0.0, S4+0.02, ("r","dubai_run.jpg","Dubai Run"), ("l","normal_race.jpg","Normal Race"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Dubai Run
hl("#al","#ar", ST(9))      # scene 3: Normal Race
pair("b", S4, CARD+0.1, ("r","dubai_run.jpg","Dubai Run"), ("l","dubai_ride.jpg","Dubai Ride"), ST(14), ST(15))
hl("#br","#bl", ST(18))     # "Dubai Run-ൽ ഓടണം"
hl("#bl","#br", ph18-0.03)  # "Dubai Ride-ൽ cycle ചവിട്ടണം"
hl("#br","#bl", ST(19))     # 70,000 / 3 lakh / world's biggest free run -> Dubai Run
import sys; sys.path.insert(0,str(R/'tools')); from captions import CAP
_ch=json.load(open(R/"audio"/"timeline.json"))["chunks"]
for i_,ch_ in enumerate(_ch):                                   # one caption per phrase, timed to the voice
    s_=ch_["start"]+0.03; e_=(_ch[i_+1]["start"]+0.03) if i_+1<len(_ch) else CARD
    cap.append((s_, e_, CAP[ch_["sent"]][ch_["k"]]))
# ---- presenter poses: Fazza = right, Sheikh Mohammed = left, camera for the question and the birthday ending
pz={}
for n in (1,14): pz[n]="R"
for n in (2,15): pz[n]="L"
for n in (3,16,17,22,23,24,25): pz[n]="T"
for n in range(4,9): pz[n]="R"
for n in range(9,14): pz[n]="L"
pz[18]="R"
for n in (19,20,21): pz[n]="R"
poses=[]; prev=None
for n in range(1,26):
    s_=0.0 if n==1 else c(n)["start"]-0.05; e_=CARD if n==25 else c(n+1)["start"]-0.05
    if prev and prev[2]==pz[n]: prev[1]=e_
    else: prev=[s_,e_,pz[n]]; poses.append(prev)
poses=[tuple(x) for x in poses]
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
.tile{position:absolute;left:240px;width:600px;text-align:center}
.tile.r{top:70px}.tile.l{top:432px}
.tl{display:none}
.tile .wrap{width:600px;height:338px;display:flex;align-items:center;justify-content:center}
.tile img{width:600px;height:338px;max-width:none;max-height:none;object-fit:cover;border-radius:22px;box-shadow:0 12px 34px rgba(0,0,0,.22);display:block}
.cap{top:795px}.pose{top:1000px}
.wrap{position:relative}
.ov{position:absolute;left:0;top:0;opacity:0}
.ph{position:absolute;left:160px;top:90px;width:760px;height:570px}
.ph img{width:760px;height:570px;object-fit:cover;border-radius:30px;box-shadow:0 16px 44px rgba(0,0,0,.25);border:2px solid #e5e7eb;display:block}
.cap{left:120px;width:840px;top:795px}
.logos{position:relative;left:100px;top:60px;width:880px;display:flex;flex-wrap:wrap;justify-content:center;gap:18px 20px}
.lg{width:270px;height:200px;display:flex;align-items:center;justify-content:center}
.lg img{max-width:270px;max-height:200px;width:auto;height:auto;border-radius:18px;box-shadow:0 10px 26px rgba(0,0,0,.22)}
.grid{position:absolute;left:120px;top:50px;width:840px;display:grid;grid-template-columns:1fr 1fr;gap:20px 24px}
.gc{width:408px;height:296px;display:flex;align-items:center;justify-content:center}
.gc img{max-width:408px;max-height:296px;width:auto;height:auto;border-radius:20px;box-shadow:0 12px 30px rgba(0,0,0,.24);display:block}
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
