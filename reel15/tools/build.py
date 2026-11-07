"""Reel 15: Emirates ID vs Aadhaar (scenes 1-3), UAE Pass vs DigiLocker (scenes 4-5). Photos on top, character below."""
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
S2=c(4)["start"]-0.1; S3=c(13)["start"]-0.1; S4=c(24)["start"]-0.1; S5=c(31)["start"]-0.1
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
pair("a", 0.0, S4+0.25, ("r","emirates.jpg","Emirates ID"), ("l","aadhaar.jpg","Aadhaar Card"), ST(1), ST(2))
hl("#ar","#al", ST(4))     # scene 2: Emirates ID highlighted, Aadhaar smaller
hl("#al","#ar", ST(13))    # scene 3: Aadhaar highlighted, Emirates ID smaller
pair("b", S4, CARD+0.1, ("r","uaepass.jpg","UAE Pass"), ("l","digilocker.jpg","DigiLocker"), ST(24), ST(25))
hl("#br","#bl", ST(27))
hl("#bl","#br", ST(31))   # scene 5: DigiLocker highlighted, UAE Pass smaller
# ---- captions (one block per sentence)
CAP={1:["ഇതാണ് Emirates ID."],2:["ഇതാണ് Aadhaar Card."],3:["എന്താണ് വ്യത്യാസം?"],4:["ആദ്യം Emirates ID","നോക്കാം."],
5:["UAE-യിൽ താമസിക്കുന്ന","എല്ലാവർക്കും ഇത്","നിർബന്ധമാണ്."],6:["Citizens ആയാലും","expats ആയാലും വേണം."],
7:["Bank account തുറക്കാനും","SIM എടുക്കാനും","hospital-ൽ പോകാനും","എല്ലാം Emirates ID വേണം."],
8:["Expats-ന്റെ Emirates ID","visa-യുമായി link ആണ്."],9:["Visa തീരുമ്പോൾ","ID-യും തീരും."],10:["Renew ചെയ്യാൻ","മറന്നാലോ?"],
11:["Expiry കഴിഞ്ഞ് 30 ദിവസം","കഴിഞ്ഞാൽ ദിവസം","20 Dirham വെച്ച് fine വരും."],12:["Maximum 1000 Dirham","വരെ പോകും!"],
13:["ഇനി നമ്മുടെ Aadhaar","നോക്കാം."],14:["ഇത് ഒരു 12 അക്ക","number ആണ്."],15:["Aadhaar എടുക്കാൻ","പൈസ ഒന്നും വേണ്ട,","free ആണ്."],
16:["Aadhaar number-ന്","expiry ഇല്ല."],17:["Emirates ID പോലെ","renew ചെയ്യേണ്ട","കാര്യവുമില്ല."],
18:["പക്ഷേ 10 വർഷം കൂടുമ്പോൾ","documents ഒന്ന് update ചെയ്യാൻ","UIDAI പറയുന്നുണ്ട്."],
19:["Centre-ൽ പോയി address","പോലെയുള്ള details","മാറ്റാൻ ₹75 ആണ്."],20:["Fingerprint, photo","മാറ്റാൻ ₹125."],
21:["ഒരു കാര്യം കൂടി","ശ്രദ്ധിക്കണം."],22:["Aadhaar citizenship","proof അല്ല."],23:["Identity proof","മാത്രമാണ്."],
24:["ഇനി ഇതാണ് UAE Pass."],25:["ഇതാണ് DigiLocker."],26:["എന്താണ് വ്യത്യാസം?"],27:["UAE Pass ഒരു","digital ID app ആണ്."],
28:["ഒരൊറ്റ login കൊണ്ട്","government services-ഉം","പല private services-ഉം","use ചെയ്യാം."],29:["Face വെച്ച്","login ചെയ്യാനും പറ്റും."],
30:["Documents digital ആയി","sign ചെയ്യാം,","ആ signature-ന്","legal value-ഉം ഉണ്ട്."],31:["ഇനി DigiLocker."],
32:["ഇത് നമ്മുടെ documents","സൂക്ഷിക്കാനുള്ള ഒരു","digital wallet ആണ്."],33:["Driving licence, RC,","marksheet ഒക്കെ","ഇതിൽ കിട്ടും."],
34:["Department നേരിട്ട്","issue ചെയ്യുന്ന documents","original-ന് തുല്യമാണ്."],35:["പക്ഷേ നമ്മൾ സ്വന്തമായി","scan ചെയ്ത് upload ചെയ്യുന്ന","documents-ന് ആ value","ഇല്ല!"]}
KEEP=[int(k["clip"][1:]) for k in json.load(open(R/"audio"/"timeline.json"))["clips"]]
CAP[21]=["ശ്രദ്ധിക്കണം"]
starts={}
for i,n in enumerate(KEEP): starts[n]=0.0 if i==0 else c(n)["start"]-0.05
ends={n:(starts[KEEP[i+1]] if i+1<len(KEEP) else CARD) for i,n in enumerate(KEEP)}
for n in KEEP: caps(starts[n], ends[n], CAP[n])
# ---- character poses per sentence
P={}
for n in range(1,36):
    P[n]="R" if n<=2-1 else None
pose_of={1:"R",2:"L",3:"T"}
for n in range(4,13): pose_of[n]="R"
pose_of[10]="T"
for n in range(13,24): pose_of[n]="L"
pose_of[22]="T"; pose_of[23]="T"
pose_of[24]="R"; pose_of[25]="L"; pose_of[26]="T"
for n in range(27,31): pose_of[n]="R"
for n in range(31,36): pose_of[n]="L"
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
