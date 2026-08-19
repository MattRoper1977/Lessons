import re,sys
def sheet(name, path):
    txt=open(path,encoding='utf-8').read()
    blocks=re.split(r'\n===== SHEET: ', txt)
    for b in blocks:
        if b.startswith(name): return b
    return None
for pw,f,sh in [("GROW","_sca1/inputs/GROW_SOW.txt","GROW Weekly - Autumn"),
                ("LAUNCH","_sca1/inputs/LAUNCH_SOW.txt","LAUNCH Weekly - Autumn")]:
    b=sheet(sh,f)
    print(f"\n########## {pw} :: {sh} ##########")
    if not b: print("  SHEET NOT FOUND"); continue
    lines=b.split('\n')
    # print rows whose text mentions science-y content, with their cell refs
    for ln in lines[1:]:
        if '\t' not in ln: continue
        cell,val=ln.split('\t',1)
        if re.match(r'^[A-Z]{1,2}\d+$',cell):
            print(f"  {cell:6s} {val[:150]}")
