"""Reel 22: Dubai petrol vs Kerala petrol (scenes 1-3), E20 vs pure petrol (scenes 4-5), closing price board. Safe side margins."""
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
S2=c(4)["start"]-0.1; S3=c(9)["start"]-0.1; S4=c(14)["start"]-0.1; S5=c(23)["start"]-0.1; SB=c(27)["start"]-0.1   # SB = closing price summary
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
pair("a", 0.0, S4+0.25, ("r","dubai_pump.jpg","Dubai"), ("l","kerala_pump.jpg","Kerala"), ST(1), ST(2))
hl("#ar","#al", ST(4))      # scene 2: Dubai highlighted
hl("#al","#ar", ST(9))      # scene 3: Kerala highlighted
pair("b", S4, SB+0.25, ("r","e20.jpg","E20 Petrol"), ("l","xp100.jpg","Pure Petrol"), ST(14), ST(15))
hl("#br","#bl", ST(17))     # scene 4 explanation: E20 highlighted
hl("#bl","#br", ST(23))     # scene 5: pure petrol (XP100) highlighted
# ---- closing summary: photos removed, price board highlighted row by row
rows=[("Dubai","Special 95","₹104","#0a8f4a",ST(28)),("Kerala","E20 petrol","₹114","#d97757",ST(29)),("Pure petrol","XP100 premium","₹167","#e11d48",ST(30))]
board="".join(f'<div id="rw{i_}" class="row"><div class="rl"><b>{html.escape(a_)}</b><span>{html.escape(b_)}</span></div><div class="rp" style="color:{col}">{html.escape(p_)}</div></div>' for i_,(a_,b_,p_,col,_) in enumerate(rows))
clip("board", SB, DUR+0.1, f'<div class="board"><div class="bt">Price per litre</div>{board}</div>', z=3)
js.append(f'gsap.set("#rw0,#rw1,#rw2",{{opacity:0}});')
for i_,(a_,b_,p_,col,t_) in enumerate(rows):
    js.append(f'tl.fromTo("#rw{i_}",{{x:60,scale:0.9,opacity:0}},{{x:0,scale:1,opacity:1,duration:0.45,ease:"back.out(1.6)"}},{t_:.3f});')
    if i_<2: js.append(f'tl.to("#rw{i_}",{{scale:0.94,opacity:0.55,duration:0.3}},{rows[i_+1][4]:.3f});')
    clicks.append(round(t_+0.02,3))
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Dubai Petrol."],2:["ഇതാണ് Kerala Petrol."],3:["എന്താണ് വ്യത്യാസം?"],
4:["Dubai-യിൽ എല്ലാ മാസവും","ഒന്നാം തീയതി","petrol വില മാറും."],5:["Global oil വില അനുസരിച്ചാണ്","ഇത് തീരുമാനിക്കുന്നത്."],
6:["ഈ November-ൽ Special 95 petrol-ന്","ഒരു litre-ന്","4 Dirham 4 fils ആണ്."],7:["നമ്മുടെ പൈസയിൽ","ഏകദേശം 104 രൂപ."],
8:["കഴിഞ്ഞ മാസത്തേക്കാൾ","വില കുറഞ്ഞു!"],
9:["നമ്മുടെ Kerala-യിൽ ഇന്ന് Kochi-യിൽ","petrol-ന് ഒരു litre-ന് ഏകദേശം","113 രൂപ 50 പൈസയാണ്."],
10:["Thiruvananthapuram-ൽ","115 രൂപയ്ക്ക് മുകളിൽ."],11:["അതായത് Dubai-യേക്കാൾ litre-ന്","10 രൂപയോളം കൂടുതൽ."],
12:["പക്ഷേ ഒരു","twist ഉണ്ട്!"],13:["നമ്മൾ നാട്ടിൽ അടിക്കുന്നത്","100% petrol അല്ല!"],
14:["ഇതാണ് E20 Petrol."],15:["ഇതാണ് Pure Petrol."],16:["എന്താണ് വ്യത്യാസം?"],
17:["നാട്ടിലെ സാധാരണ pump-ൽ","കിട്ടുന്നത് E20 ആണ്."],18:["അതായത് ഒരു litre-ൽ","20 ശതമാനം വരെ","ethanol ഉണ്ട്."],
19:["ഈ ethanol കരിമ്പിൽ നിന്നും","ചോളത്തിൽ നിന്നുമാണ്","ഉണ്ടാക്കുന്നത്."],
20:["Ethanol ചേർത്താൽ","വില കുറയും എന്നാണ്","പലരും കരുതുന്നത്."],
21:["പക്ഷേ ഒരു litre ethanol-ന്","ഏകദേശം 72 രൂപ","government കൊടുക്കുന്നുണ്ട്."],
22:["അതുകൊണ്ട് E20-ക്ക്","വില കുറയില്ല എന്നാണ്","government പറയുന്നത്."],
23:["അപ്പോ ethanol ഇല്ലാത്ത","pure petrol വേണമെങ്കിലോ?"],24:["സാധാരണ pump-ൽ","കിട്ടില്ല."],
25:["XP100 പോലുള്ള","premium petrol വാങ്ങണം."],
26:["അതിന് metro cities-ൽ","ഒരു litre-ന്","167 മുതൽ 170 രൂപ വരെയാണ് വില!"],
27:["ചുരുക്കി പറഞ്ഞാൽ,"],28:["Dubai-യിൽ 104 രൂപ,"],29:["നാട്ടിൽ E20-ക്ക് 114 രൂപ,"],
30:["pure petrol വേണമെങ്കിൽ","167 രൂപ!"]}
KEEP=list(range(1,31))
starts={}
for i_,n in enumerate(KEEP): starts[n]=0.0 if i_==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i_+1]] if i_+1<len(KEEP) else CARD) for i_,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses (first item = right, second = left)
pose_of={n:"R" for n in range(1,31)}
pose_of[2]="L"; pose_of[3]="T"
for n in range(9,14): pose_of[n]="L"          # Kerala (left)
pose_of[15]="L"; pose_of[16]="T"
for n in range(23,27): pose_of[n]="L"         # pure petrol / XP100 (left)
for n in range(27,31): pose_of[n]="T"         # closing summary: facing the camera
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
.tile{position:absolute;top:215px;width:400px;text-align:center}
.tile.l{left:110px}.tile.r{left:570px}
.tl{font-weight:800;font-size:38px;margin-bottom:12px;letter-spacing:-0.5px;white-space:nowrap}
.tile img{width:400px;height:298px;object-fit:cover;border-radius:26px;box-shadow:0 12px 34px rgba(0,0,0,.22);border:2px solid #e5e7eb;display:block}
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
