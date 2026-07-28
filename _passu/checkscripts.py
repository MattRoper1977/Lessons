import re,subprocess,sys,pathlib,os
root=pathlib.Path('.')
html=[p for p in root.rglob('*.html') if '.git' not in p.parts]
scriptpat=re.compile(r'<script\b([^>]*)>(.*?)</script>', re.S|re.I)
srcpat=re.compile(r'\bsrc\s*=', re.I)
typemod=re.compile(r'type\s*=\s*["\']module', re.I)
bad=[]; nchecked=0; nfiles=0
tmp='_passu/_s.js'
for p in html:
    txt=p.read_text(errors='replace')
    blocks=scriptpat.findall(txt)
    fset=False
    for i,(attrs,body) in enumerate(blocks):
        if srcpat.search(attrs): continue      # external
        if not body.strip(): continue
        # skip json/template scripts
        if re.search(r'type\s*=\s*["\'](application/json|text/template|text/html)', attrs, re.I): continue
        nchecked+=1; fset=True
        open(tmp,'w').write(body)
        cmd=['node','--check']
        if typemod.search(attrs): cmd=['node','--input-type=module','--check']
        r=subprocess.run(['node','--check',tmp],capture_output=True,text=True)
        if r.returncode!=0:
            bad.append((str(p),i,r.stderr.strip().split('\n')[0][:200]))
    if fset: nfiles+=1
print(f'files with inline scripts: {nfiles}; inline blocks checked: {nchecked}')
print(f'SYNTAX ERRORS: {len(bad)}')
for b in bad[:80]: print('  ',b)
