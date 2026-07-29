import re, json, sys
sel=sys.argv[1]
d=json.load(open("_passq/tools/movers.json"))
def match(f):
    if sel=="art": return f.startswith("Art_Teesside")
    if sel=="hum": return "HUM" in f
    if sel=="rest": return not f.startswith("Art_Teesside") and "HUM" not in f and not f.startswith(("BUILD_ASDAN","GROW_ASDAN"))
files=sorted(x["file"] for x in d if match(x["file"]))
def vis(s):
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>',' ',s); s=s.replace('&amp;','&')
    return re.sub(r'\s+',' ',s).strip()
def region(s,rid,limit=2200):
    i=s.find(f'id="{rid}"')
    if i<0: return "(none)"
    j=s.find('id="print-',i+len(rid)+6)
    return vis(s[i:j if j>0 else i+limit])[:limit]
for f in files:
    s=open(f,encoding='utf-8').read()
    print("\n"+"="*88); print("FILE:",f)
    print("--KO--:",region(s,"print-ko"))
    print("--WEDO--:",region(s,"print-wedo",1500))
print("N=",len(files),file=sys.stderr)
