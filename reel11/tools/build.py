"""Reel 11: Claude AI ATS-friendly CV tutorial. Icons are inline SVG; one click per icon pop (clicks.json)."""
import html, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
tl = {c["clip"]: c for c in json.load(open(R/"audio"/"timeline.json"))["clips"]}
_d = json.load(open(R/"tools"/"dur.json")); DUR = _d["dur"]; CARD = _d["card"]
h=[]; js=[]; cap=[]; poses=[]; clicks=[]
B,O,G,RD,GR="#2330c9","#d97757","#16a34a","#e11d48","#64748b"
def doc(inner, stroke=B): return f'<rect x="45" y="20" width="110" height="150" rx="12" fill="#fff" stroke="{stroke}" stroke-width="8"/>{inner}'
def lines(y0,n,c="#cbd5e1"): return "".join(f'<rect x="62" y="{y0+i*20}" width="{76 if i%2==0 else 56}" height="9" rx="4" fill="{c}"/>' for i in range(n))
SVG={
 "cv": doc('<circle cx="100" cy="58" r="16" fill="#93c5fd"/>'+lines(88,4)),
 "coin": '<circle cx="100" cy="95" r="70" fill="#fbbf24" stroke="#d97706" stroke-width="8"/><circle cx="100" cy="95" r="52" fill="none" stroke="#d97706" stroke-width="5"/><text x="100" y="118" text-anchor="middle" font-family="PopFz, sans-serif" font-weight="800" font-size="70" fill="#b45309">&#8377;</text>',
 "ats": doc(lines(52,3)+'<circle cx="138" cy="150" r="34" fill="'+G+'"/><path d="M122 150 l12 13 l22 -26" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'+f'<rect x="58" y="30" width="54" height="26" rx="8" fill="{G}"/><text x="85" y="50" text-anchor="middle" font-family="PopFz, sans-serif" font-weight="800" font-size="20" fill="#fff">ATS</text>', G),
 "company": '<rect x="48" y="40" width="104" height="130" rx="8" fill="#e0e7ff" stroke="'+B+'" stroke-width="8"/>'+"".join(f'<rect x="{62+c*30}" y="{56+r*30}" width="16" height="16" rx="3" fill="{B}"/>' for r in range(3) for c in range(3))+'<rect x="88" y="132" width="24" height="38" fill="'+B+'"/>',
 "nocv": doc('<circle cx="100" cy="58" r="16" fill="#93c5fd"/>'+lines(88,4))+'<circle cx="148" cy="148" r="34" fill="'+RD+'"/><path d="M134 134 l28 28 M162 134 l-28 28" stroke="#fff" stroke-width="10" stroke-linecap="round"/>',
 "jd": '<rect x="48" y="30" width="104" height="140" rx="12" fill="#fff" stroke="'+B+'" stroke-width="8"/><rect x="78" y="18" width="44" height="26" rx="8" fill="'+B+'"/>'+lines(62,4)+f'<text x="100" y="150" text-anchor="middle" font-family="PopFz, sans-serif" font-weight="800" font-size="26" fill="{B}">JD</text>',
 "skills": '<rect x="40" y="30" width="120" height="140" rx="14" fill="#fff" stroke="'+B+'" stroke-width="8"/>'+"".join(f'<path d="M58 {62+i*38} l9 10 l17 -20" fill="none" stroke="{G}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><rect x="96" y="{56+i*38}" width="46" height="10" rx="5" fill="#cbd5e1"/>' for i in range(3)),
 "scissors": '<circle cx="62" cy="145" r="22" fill="none" stroke="'+RD+'" stroke-width="10"/><circle cx="138" cy="145" r="22" fill="none" stroke="'+RD+'" stroke-width="10"/><path d="M76 128 L138 28 M124 128 L62 28" stroke="'+GR+'" stroke-width="12" stroke-linecap="round"/>',
 "upload": '<path d="M52 128 a30 30 0 0 1 8 -58 a42 42 0 0 1 82 6 a28 28 0 0 1 -4 52 z" fill="#dbeafe" stroke="'+B+'" stroke-width="8" stroke-linejoin="round"/><path d="M100 150 V84 M72 108 L100 80 L128 108" fill="none" stroke="'+B+'" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>',
 "form": doc("".join(f'<rect x="62" y="{38+i*32}" width="76" height="20" rx="6" fill="#eff6ff" stroke="{B}" stroke-width="3"/>' for i in range(4))+f'<rect x="62" y="162" width="0" height="0"/>'),
 "prompt": '<path d="M30 40 h140 a14 14 0 0 1 14 14 v76 a14 14 0 0 1 -14 14 h-80 l-34 30 v-30 h-26 a14 14 0 0 1 -14 -14 v-76 a14 14 0 0 1 14 -14z" fill="#fff" stroke="'+O+'" stroke-width="8" stroke-linejoin="round"/>'+"".join(f'<rect x="52" y="{66+i*24}" width="{96 if i<2 else 52}" height="10" rx="5" fill="#fcd9ca"/>' for i in range(3)),
 "copy": '<rect x="62" y="40" width="96" height="124" rx="12" fill="#fff" stroke="'+B+'" stroke-width="8"/><rect x="36" y="22" width="96" height="124" rx="12" fill="#dbeafe" stroke="'+B+'" stroke-width="8"/>'+lines(54,4,"#93c5fd"),
 "comment": '<path d="M30 40 h140 a14 14 0 0 1 14 14 v76 a14 14 0 0 1 -14 14 h-80 l-34 30 v-30 h-26 a14 14 0 0 1 -14 -14 v-76 a14 14 0 0 1 14 -14z" fill="#fff" stroke="'+B+'" stroke-width="8" stroke-linejoin="round"/>',
 "plane": '<path d="M24 100 L176 30 L140 170 L98 126 Z" fill="#dbeafe" stroke="'+B+'" stroke-width="8" stroke-linejoin="round"/><path d="M98 126 L176 30 M98 126 L96 170 L120 146" fill="none" stroke="'+B+'" stroke-width="8" stroke-linejoin="round"/>',
}
def svg(key, text=None):
    inner=SVG[key]
    if key=="comment": inner+=f'<text x="100" y="108" text-anchor="middle" font-family="PopFz, sans-serif" font-weight="800" font-size="{44 if len(text)<4 else 28}" fill="{B}">{text}</text>'
    return f'<svg class="ico" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def clip(id_, s, e, body, cls="", z=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="{z}" style="z-index:{z}">{body}</div>')
n_g=[0]
def pop(s, e, x, key, label, text=None, logo=None):
    n_g[0]+=1; id_=f"i{n_g[0]}"; s=max(0.0,s)
    art = f'<img class="glogo" src="assets/{logo}" alt="{html.escape(label)}">' if logo else svg(key,text)
    clip(f"g-{id_}", s, e, f'<div class="gwrap"><div id="g-{id_}-in" class="grp big"><div class="glbl">{html.escape(label)}</div>{art}</div></div>', z=3)
    js.append(f'tl.fromTo("#g-{id_}-in",{{x:{x},scale:0.35,opacity:0}},{{x:{x},scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{s:.3f});')
    js.append(f'tl.to("#g-{id_}-in",{{opacity:0,scale:0.85,duration:0.2,ease:"power1.in"}},{e-0.22:.3f});')
    clicks.append(round(s+0.02,3))
def caps(s, e, chunks):
    w=[max(len(c),4) for c in chunks]; tot=sum(w); t=s
    for k,c in enumerate(chunks):
        d=(e-s)*w[k]/tot; cap.append((t, t+d if k<len(chunks)-1 else e, c)); t+=d
c=lambda n: tl[f"c{n}"]
S=[0.0]+[c(n)["start"]-0.1 for n in (3,5,7,9,10,11,12,14)]+[CARD]      # scene starts (S1..S9) + end
def sc(n): return S[n-1], S[n]
# ---- scene 1 hook: CV + money
s,e=sc(1); pop(0.0,e,-250,"cv","CV"); pop(c(1)["start"]+1.5,e,250,"coin","Price")
caps(c(1)["start"]-0.35,c(2)["start"],["2027 ആയിട്ടും","നിങ്ങൾ CV ഉണ്ടാക്കാൻ","പൈസ കൊടുക്കുകയാണോ?"]); caps(c(2)["start"],e,["എങ്കിൽ ഈ വീഡിയോ","നിങ്ങൾക്കുള്ളതാണ്!"])
# ---- scene 2 problem
s,e=sc(2); pop(c(3)["start"]-0.03,c(4)["start"]-0.1,0,"ats","ATS-friendly CV"); pop(c(4)["start"]-0.03,e,-250,"nocv","One CV"); pop(c(4)["start"]+1.0,e,250,"company","All companies")
caps(s,c(4)["start"],["ഇന്നത്തെ പല കമ്പനികളും","ATS-friendly ആയിട്ടുള്ള","CV-കൾക്ക് പ്രാധാന്യം","കൊടുക്കുന്നുണ്ട്"]); caps(c(4)["start"],e,["പക്ഷേ ഒരു CV തന്നെ","എല്ലാ കമ്പനികൾക്കും","അയച്ചിട്ട് കാര്യമില്ല"])
# ---- scene 3 why
s,e=sc(3); pop(c(5)["start"]-0.03,c(6)["start"]-0.1,-250,"jd","Job Description"); pop(c(5)["start"]+1.9,c(6)["start"]-0.1,250,"skills","Skills"); pop(c(6)["start"]-0.03,e,0,"scissors","Tailor your CV")
caps(s,c(6)["start"],["കാരണം ഓരോ കമ്പനിയുടെ","job description-ഉം","ആവശ്യപ്പെടുന്ന skills-ഉം","വ്യത്യസ്തമായിരിക്കും"]); caps(c(6)["start"],e,["അതുകൊണ്ട് ഓരോ job-നും","അനുസരിച്ച് നിങ്ങളുടെ","CV tailor ചെയ്യണം"])
# ---- scene 4 introduce Claude
s,e=sc(4); pop(c(7)["start"]-0.03,c(8)["start"]-0.1,0,None,"Claude AI",logo="claude.png"); pop(c(8)["start"]-0.03,e,0,"ats","ATS-friendly CV")
caps(s,c(8)["start"],["ഇത് ചെയ്യാൻ നമുക്ക്","Claude AI ഉപയോഗിക്കാം"]); caps(c(8)["start"],e,["എങ്ങനെ ഓരോ job-നും","പ്രത്യേകം ATS-friendly CV","ഉണ്ടാക്കാമെന്ന് കാണിച്ചുതരാം"])
# ---- scene 5 step 1
s,e=sc(5); mid=c(9)["start"]+0.38*(c(9)["end"]-c(9)["start"])
pop(c(9)["start"]-0.03,mid,0,"upload","Step 1 · Upload CV"); pop(mid,e,0,"form","No CV? Fill the form")
caps(s,mid,["ആദ്യം നിങ്ങളുടെ","നിലവിലുള്ള CV upload ചെയ്യുക."]); caps(mid,e,["CV ഇല്ലെങ്കിൽ,","education, experience, skills,","personal details എന്നിവയുള്ള","form fill ചെയ്യുക"])
# ---- scene 6 step 2
s,e=sc(6); pop(c(10)["start"]-0.03,e,-250,"prompt","Step 2 · Prompt"); pop(c(10)["start"]+1.3,e,250,None,"Claude",logo="claude.png")
caps(s,e,["അതിനുശേഷം ഞാൻ തരുന്ന","prompt Claude-ൽ","copy-paste ചെയ്യുക"])
# ---- scene 7 step 3
s,e=sc(7); pop(c(11)["start"]-0.03,e,-250,"jd","Step 3 · Job Description"); pop(c(11)["start"]+1.9,e,250,"company","Company name")
caps(s,e,["ഇനി നിങ്ങൾ apply ചെയ്യാൻ","പോകുന്ന job-ന്റെ","description-ഉം company name-ഉം","copy ചെയ്ത് prompt-ന്റെ","താഴെ paste ചെയ്യുക"])
# ---- scene 8 result
s,e=sc(8); pop(c(12)["start"]-0.03,e,-250,None,"Claude",logo="claude.png"); pop(c(13)["start"]+0.6,e,250,"ats","Tailored CV")
caps(s,e,["ഇപ്പോൾ Claude","നിങ്ങളുടെ experience-ഉം","job description-ഉം match ചെയ്ത്,","ആ position-ന് അനുയോജ്യമായ","CV തയ്യാറാക്കാൻ സഹായിക്കും"])
# ---- scene 9 CTA
s,e=sc(9); pop(c(14)["start"]-0.03,c(15)["start"]-0.1,-250,"comment","Comment","CV"); pop(c(14)["start"]+1.5,c(15)["start"]-0.1,250,"comment","or","CLAUDE"); pop(c(15)["start"]-0.03,e,0,"plane","Prompt share")
caps(s,c(15)["start"],["ഈ prompt വേണമെങ്കിൽ","comment-ൽ ‘CV’ അല്ലെങ്കിൽ","‘CLAUDE’ എന്ന് എഴുതൂ"]); caps(c(15)["start"],e,["Prompt നിങ്ങളുമായി","share ചെയ്യാം!"])
# poses: alternate pointing, thinking on the "problem"/"result" lines
PS=["L","R","L","T","R","L","R","L","R","L","R","L","R","L"]
bounds=[(S[0],c(2)["start"]),(c(2)["start"],S[1]),(S[1],c(4)["start"]),(c(4)["start"],S[2]),(S[2],c(6)["start"]),(c(6)["start"],S[3]),(S[3],c(8)["start"]),(c(8)["start"],S[4]),(S[4],S[5]),(S[5],S[6]),(S[6],S[7]),(S[7],S[8]),(S[8],c(15)["start"]),(c(15)["start"],S[9])]
PS=["L","R","L","T","R","L","R","L","R","L","R","L","R","L"]
for (a,b),p in zip(bounds,PS): poses.append((a,b,p))
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
.gwrap{position:absolute;left:0;top:215px;width:1080px;height:520px;display:flex;justify-content:center}
.grp{width:520px;display:flex;flex-direction:column;align-items:center;gap:14px}
.grp.big{margin-top:24px}
.glbl{font-weight:700;font-size:40px;letter-spacing:-0.5px;white-space:nowrap}
.glogo{height:300px;max-width:460px;width:auto;object-fit:contain;border-radius:30px}
.ico{height:330px;width:330px}
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
