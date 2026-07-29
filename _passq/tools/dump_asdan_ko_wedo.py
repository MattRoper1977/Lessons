import re, json, sys
d=json.load(open("_passq/tools/movers.json"))
files=[x["file"] for x in d if x["file"].startswith(("BUILD_ASDAN","GROW_ASDAN"))]
files.sort()
def vis(s):
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>',' ',s); s=s.replace('&amp;','&')
    return re.sub(r'\s+',' ',s).strip()
def region(s,rid,limit=2600):
    i=s.find(f'id="{rid}"')
    if i<0: return "(none)"
    j=s.find('id="print-',i+len(rid)+6)
    return vis(s[i:j if j>0 else i+limit])[:limit]
for f in files:
    s=open(f,encoding='utf-8').read()
    ko=region(s,"print-ko")
    wd=region(s,"print-wedo")
    print("\n"+"="*90)
    print("FILE:",f)
    print("--KO--:",ko)
    print("--WEDO--:",wd)
print("\nTOTAL FILES:",len(files),file=sys.stderr)
