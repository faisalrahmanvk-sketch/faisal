"""Instagram carousel (1080x1350) - 'Create ATS-friendly CV with Claude' - same theme as reel 11."""
import pathlib, re, html
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE.parent/"tools"/"build.py").read_text(encoding="utf-8")
ns = {}
exec(src[src.index('B,O,G,RD,GR='):src.index("def svg(")].replace("f'",'f\''), ns)   # B,O,G.. + doc/lines + SVG dict
SVG = ns["SVG"]
def svg(key, text=None):
    inner = SVG[key]
    if key=="comment": inner += f'<text x="100" y="108" text-anchor="middle" font-family="PopFz, sans-serif" font-weight="800" font-size="{44 if len(text)<4 else 28}" fill="#2330c9">{text}</text>'
    return f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def icon(spec):
    key,label,*rest = spec
    art = f'<img src="assets/claude.png" alt="Claude">' if key=="claude" else svg(key, rest[0] if rest else None)
    return f'<div class="ic">{art}' + (f'<div class="il">{html.escape(label)}</div>' if label else '') + '</div>'
N=10
SL=[
 dict(kind="cover"),
 dict(kick="HOOK", title="Still paying for a CV in <o>2027</o>?", body="If yes, this one is for you!", icons=[("cv","Your CV"),("coin","Paying?")], pose="think", side="L"),
 dict(kick="THE PROBLEM", title="Companies want <g>ATS-friendly</g> CVs", body="But sending the same CV to every company doesn’t work.", icons=[("ats","ATS-friendly"),("nocv","Same CV"),("company","Every company")], pose="pointR", side="L"),
 dict(kick="WHY?", title="Every job is <o>different</o>", body="Each company’s job description and required skills are different, so tailor your CV for every job.", icons=[("jd","Job description"),("skills","Skills"),("scissors","Tailor CV")], pose="pointL", side="R"),
 dict(kick="THE FIX", title="Use <o>Claude AI</o>", body="Create a separate ATS-friendly CV for every job, in minutes.", icons=[("claude","Claude AI"),("ats","ATS-friendly CV")], pose="pointR", side="L"),
 dict(kick="STEP 1", title="Upload your <b>current CV</b>", body="No CV? Fill in a form with your education, experience, skills and personal details.", icons=[("upload","Upload CV"),("form","Or fill a form")], pose="pointL", side="R"),
 dict(kick="STEP 2", title="Paste my <o>prompt</o> into Claude", body="Copy the prompt I give you and paste it into Claude.", icons=[("copy","Copy prompt"),("claude","Paste in Claude")], pose="pointR", side="L"),
 dict(kick="STEP 3", title="Add the <b>job description</b>", body="Copy the job description and company name of the job you’re applying for, and paste them below the prompt.", icons=[("jd","Job description"),("company","Company name")], pose="pointL", side="R"),
 dict(kick="RESULT", title="A CV <g>tailored</g> to the job", body="Claude matches your experience with the job description and helps you build the right CV for that position.", icons=[("claude","Claude AI"),("ats","Tailored CV")], pose="pointR", side="L"),
 dict(kick="WANT THE PROMPT?", title="Comment <b>“CV”</b> or <o>“CLAUDE”</o>", body="and I’ll share the prompt with you!", icons=[], pose="pointL", side="R", last=True),
]
CSS = """
@font-face{font-family:"PopFz";font-weight:800;src:url("assets/fonts/pop800.woff2") format("woff2")}
@font-face{font-family:"PopFz";font-weight:700;src:url("assets/fonts/pop700.woff2") format("woff2")}
@font-face{font-family:"PopFz";font-weight:500;src:url("assets/fonts/pop500.woff2") format("woff2")}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#fff;font-family:"PopFz",sans-serif;position:relative;overflow:hidden;color:#0b0b14}
.glow{position:absolute;left:-250px;top:380px;width:1580px;height:1100px;background:radial-gradient(closest-side,#e6ecff,#fff 78%)}
.hd{position:absolute;left:70px;right:70px;top:48px;display:flex;justify-content:space-between;font-weight:700;font-size:34px;color:#475569}
.hd b{color:#2330c9;font-weight:800}
.kick{position:absolute;left:0;top:140px;width:1080px;display:flex;justify-content:center}
.kick span{background:#2330c9;color:#fff;font-weight:800;font-size:38px;padding:10px 38px;border-radius:50px;letter-spacing:1.5px}
.txt{position:absolute;left:70px;right:70px;top:240px;display:flex;flex-direction:column;align-items:center;gap:34px}
.ttl{width:100%;text-align:center;font-weight:800;font-size:96px;line-height:1.1;letter-spacing:-2px}
.ttl .o{color:#d97757}.ttl .g{color:#16a34a}.ttl b{color:#2330c9}
.bod{width:880px;text-align:center;font-weight:500;font-size:42px;line-height:1.4;color:#64748b}
.row{position:absolute;display:flex;justify-content:center;gap:34px;height:330px;align-items:flex-start}
.ic{width:230px;text-align:center}.ic svg,.ic img{width:230px;height:230px;object-fit:contain;display:block}
.ic img{border-radius:50px;box-shadow:0 18px 44px rgba(217,119,87,.3);padding:0}
.il{margin-top:12px;font-weight:700;font-size:30px;color:#1e293b;white-space:nowrap}
.char{position:absolute;bottom:60px;height:540px}
.wm{position:absolute;left:0;bottom:16px;width:1080px;text-align:center;font-weight:700;font-size:30px;color:#6b7280}
.halo{position:absolute;left:250px;top:740px;width:580px;height:580px;border-radius:50%;background:radial-gradient(closest-side,#c7d6ff,#e9efff 60%,rgba(255,255,255,0))}
.ring{position:absolute;left:200px;top:700px;width:680px;height:680px;border-radius:50%;border:4px dashed #bcc9f5}
.dt{position:absolute;border-radius:50%;display:block}
.sw{position:absolute;right:70px;bottom:22px;font-weight:800;font-size:32px;color:#2330c9}
.fol{position:absolute;left:0;width:1080px;display:flex;justify-content:center;top:760px}
.fol span{background:linear-gradient(180deg,#3b82f6,#2330c9);color:#fff;font-weight:800;font-size:44px;padding:16px 56px;border-radius:50px;box-shadow:0 14px 34px rgba(35,48,201,.35)}
"""
POSE={"pointL":"pose_pointL.png","pointR":"pose_pointR.png","think":"pose_think.png"}
def page(body): return f'<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div class="glow"></div>{body}</body></html>'
def hd(i): return f'<div class="hd"><span><b>@fyze.ai</b></span><span>{i:02d}/{N}</span></div>'
for i,s in enumerate(SL,1):
    if s.get("kind")=="cover":
        b = hd(i)+'<div class="kick"><span style="background:#16a34a">ATS-FRIENDLY</span></div>'
        b += '<div class="ttl" style="position:absolute;left:70px;width:940px;top:230px;font-size:138px;line-height:1.1">Create CV<br>with <span class="o">Claude</span></div>'
        b += '''<style>.cv{position:absolute;left:520px;top:690px;width:430px;height:540px;background:#fff;border-radius:32px;box-shadow:0 26px 70px rgba(35,48,201,.22),0 0 0 6px #2330c9;transform:rotate(5deg);padding:40px 36px}
.av{width:86px;height:86px;border-radius:50%;background:#93c5fd}.nm{position:absolute;left:140px;top:52px}.nm i{display:block;height:18px;border-radius:9px;background:#1e293b;width:180px;margin-bottom:12px}.nm i+i{height:12px;width:124px;background:#94a3b8}
.sec{margin-top:30px}.sec i{display:block;height:13px;border-radius:7px;background:#cbd5e1;margin-bottom:14px}.sec .h{background:#2330c9;width:116px;height:16px;margin-bottom:18px}
.chips{display:flex;gap:10px;margin-top:8px}.chips u{display:block;height:30px;width:84px;border-radius:15px;background:#dbeafe}
.ats{position:absolute;right:-24px;top:-28px;background:#16a34a;color:#fff;font-weight:800;font-size:36px;padding:10px 26px;border-radius:36px;box-shadow:0 10px 24px rgba(22,163,74,.4)}
.cl{position:absolute;left:760px;top:1030px;width:200px;height:200px;border-radius:46px;box-shadow:0 20px 46px rgba(217,119,87,.35);background:#fff}</style>
<div class="cv"><div class="ats">ATS ✓</div><div class="av"></div><div class="nm"><i></i><i></i></div>
<div class="sec"><i class="h"></i><i style="width:92%"></i><i style="width:78%"></i><i style="width:86%"></i></div>
<div class="sec"><i class="h"></i><i style="width:88%"></i><i style="width:70%"></i></div>
<div class="sec"><i class="h"></i><div class="chips"><u></u><u></u><u></u></div></div></div>
<img class="cl" src="assets/claude.png" alt="Claude">
<img class="char" style="left:30px;height:700px;bottom:70px" src="assets/pose_pointR.png" alt="">'''
        b += '<div class="sw">Swipe →</div>'
    else:
        b = hd(i)+f'<div class="kick"><span>{html.escape(s["kick"])}</span></div><div class="txt"><div class="ttl">{s["title"]}</div><div class="bod">{html.escape(s["body"])}</div></div>'
        left = s["side"]=="L"   # character side
        rowx = (330,1010) if left else (60,740)
        if s["icons"]: b += f'<div class="row" style="top:760px;left:{rowx[0]}px;width:{rowx[1]-rowx[0]}px">{"".join(icon(x) for x in s["icons"])}</div>'
        if s.get("last"):
            b += '<div class="halo"></div><div class="ring"></div><i class="dt" style="left:170px;top:820px;width:22px;height:22px;background:#d97757"></i><i class="dt" style="left:880px;top:780px;width:30px;height:30px;background:#16a34a"></i><i class="dt" style="left:230px;top:1130px;width:16px;height:16px;background:#2330c9"></i><i class="dt" style="left:860px;top:1100px;width:20px;height:20px;background:#fbbf24"></i>'
            b += f'<img class="char" style="left:50%;transform:translateX(-50%);height:575px;bottom:30px" src="assets/{POSE[s["pose"]]}" alt="">'
        else:
            b += f'<img class="char" style="{"left:20px" if left else "right:20px"}" src="assets/{POSE[s["pose"]]}" alt="">'
        if s.get("last"): b += '<div class="fol" style="top:800px"><span>Follow @fyze.ai</span></div>'
        else: b += '<div class="sw">Swipe →</div>'
    b += '<div class="wm">@fyze.ai</div>' if False else ""
    if not s.get('kind')=='cover': b += '<script>const t=document.querySelector(".txt").getBoundingClientRect().bottom,r=document.querySelector(".row"),f=document.querySelector(".fol");const av=1350-70-t;if(r)r.style.top=(t+Math.max(40,(av-330)/2))+"px";if(f)f.style.top=(t+40)+"px";</script>'
    (HERE/f"s{i:02d}.html").write_text(page(b), encoding="utf-8")
print("slides", len(SL))
