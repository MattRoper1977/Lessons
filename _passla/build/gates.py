# -*- coding: utf-8 -*-
"""Gate runner for authored lesson files (brief §6). Run over a directory of .html.
Checks: node --check per inline <script>, jsdom boot, tag balance, print-section==15,
witness §4/§5, sentinel absence, banned/zero-count strings, _ccQuestions keys."""
import os, re, sys, subprocess, tempfile

SCRATCH = os.environ.get("LA_SCRATCH",
    "/tmp/claude-0/-home-user-mattroper1977-github-io/e2287189-7d70-5645-b759-366e023fea48/scratchpad")
NODE_MODULES = os.path.join(SCRATCH, "node_modules")
BOOT = os.path.join(os.path.dirname(__file__), "boot.js")

BANNED = ["ASDAN Studio · ASDAN Studio", "Delivering a Project", "ll-g:loop-mark"]
L2_BANNED = ["register at level 2","level 2 registration","l2 registration","registered for level 2",
             "banked at level 2","level 2 award","level 2 certificate","level 2 extended award"]
FOOD_BANNED = ["calorie","calories","kcal","weight loss","lose weight","slimming","diet plan","restrict"]

SLIDE_TITLES = ["Title","Arrival Task","Starter","I Do 1","We Do 1","I Do 2",
                "We Do 2","Independent Work","Lundy Loop","Exit Ticket"]

def scripts_of(html):
    return re.findall(r"<script>(.*?)</script>", html, re.S)

def check_file(path, food_sensitive=False):
    errs=[]
    html=open(path,encoding="utf-8").read()
    # 1. node --check each inline script block
    for i,js in enumerate(scripts_of(html)):
        with tempfile.NamedTemporaryFile("w",suffix=".js",delete=False,encoding="utf-8") as tf:
            tf.write(js); tmp=tf.name
        r=subprocess.run(["node","--check",tmp],capture_output=True,text=True)
        os.unlink(tmp)
        if r.returncode!=0:
            errs.append(f"node --check script[{i}] FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr else ''}")
    # 2. jsdom boot
    env=dict(os.environ, NODE_PATH=NODE_MODULES)
    r=subprocess.run(["node",BOOT,path],capture_output=True,text=True,env=env)
    if r.returncode!=0 or "BOOT-OK" not in r.stdout:
        errs.append("jsdom boot FAILED: "+(r.stderr.strip() or r.stdout.strip())[:400])
    # 3. tag balance (a coarse but useful check on the big structural tags)
    for tag in ["div","script","style","table","svg"]:
        o=len(re.findall(rf"<{tag}[\s>]",html)); c=len(re.findall(rf"</{tag}>",html))
        if o!=c: errs.append(f"tag imbalance <{tag}>: {o} open / {c} close")
    # 4. print-section count
    ps=html.count('class="print-section')
    if ps!=15: errs.append(f"print-section count {ps} != 15")
    # 5. witness §4/§5 present, §5 once (no on-screen leak)
    for s in ["4 &#183; Assessor declaration","5 &#183; Learner confirmation"]:
        if s not in html: errs.append(f"witness missing '{s}'")
    if html.count("Learner confirmation")!=1: errs.append("Learner confirmation not confined to print-area (count!=1)")
    # 6. sentinel absence
    if "ll-g:loop-mark" in html: errs.append("SENTINEL present (new file must not carry it)")
    # 7. banned + zero-count
    for b in BANNED:
        if b in html: errs.append(f"BANNED: {b}")
    low=html.lower()
    for b in L2_BANNED:
        if b in low: errs.append(f"L2 registration phrase: {b}")
    for pat in ["youtube.com","youtu.be","youtube-nocookie","ytimg"]:
        if pat in low: errs.append(f"YouTube marker: {pat}")
    if "\U0001f3ac" in html: errs.append("clapper emoji present")
    if food_sensitive:
        for b in FOOD_BANNED:
            if re.search(rf"\b{re.escape(b)}\b",low): errs.append(f"food restriction language: {b}")
    # 8. _ccQuestions keys == slide titles
    for t in SLIDE_TITLES:
        if f'"{t}":{{F:' not in html: errs.append(f"_ccQuestions missing key {t}")
    # 9. exactly 10 slides
    sl=html.count('class="slide"')+html.count('class="slide active"')
    if sl!=10: errs.append(f"slide count {sl} != 10")
    return errs

def run_dir(d, food_sensitive=False):
    files=sorted(f for f in os.listdir(d) if f.endswith(".html"))
    allok=True
    for f in files:
        errs=check_file(os.path.join(d,f), food_sensitive)
        if errs:
            allok=False
            print(f"FAIL {f}")
            for e in errs: print("   -",e)
        else:
            print(f"PASS {f}")
    return allok

if __name__=="__main__":
    d=sys.argv[1]
    fs = "--food" in sys.argv
    ok=run_dir(d, fs)
    sys.exit(0 if ok else 1)
