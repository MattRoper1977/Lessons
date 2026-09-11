#!/usr/bin/env python3
"""S1-M K2: measure inputs in the actual named deployed Pages archive."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, importlib.util, json, os, tarfile, urllib.request, zipfile
from urllib.parse import urlsplit

REPO='MattRoper1977/Lessons'
RUN=34586602323
ARTIFACT=10194069928
SOURCE='8c7d3e9e4c24faf48c13f5d73bb70226703a7c12'
PUBLISHER='7072a5605e795b1c872f843f04f2403a8880c409'
DIGEST='sha256:c57add0a1a3275246c26910f5cad001f028f97c8ef0bcac93565855ba3da0210'

def require(condition,message):
    if not condition: raise ValueError(message)

class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        require(newurl.startswith('https://'),'Artifact redirect must remain HTTPS')
        out=super().redirect_request(req,fp,code,msg,headers,newurl)
        if out is not None and urlsplit(req.full_url).netloc!=urlsplit(newurl).netloc:
            out.remove_header('Authorization')
        return out

def open_api(route):
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+route,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','User-Agent':'S1-M-published-input-proof'})
    return urllib.request.build_opener(Redirect()).open(req,timeout=45)

def api(route):
    with open_api(route) as r:return json.load(r)

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--lessons',type=Path,required=True);parser.add_argument('--publisher',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    run=api('/actions/runs/'+str(RUN));jobs=api('/actions/runs/'+str(RUN)+'/jobs?per_page=100');artifact=api('/actions/artifacts/'+str(ARTIFACT))
    require(run['head_sha']==SOURCE and run['status']=='completed' and run['conclusion']=='success','Wrong source run')
    require(any(x['sha']==PUBLISHER for x in run['referenced_workflows']),'Wrong publisher')
    require(any(j['name']=='publication / deploy' and j['conclusion']=='success' for j in jobs['jobs']),'No successful deploy job')
    require(artifact['id']==ARTIFACT and not artifact['expired'] and artifact['digest']==DIGEST and artifact['workflow_run']['id']==RUN,'Wrong or expired archive')
    out=a.output;out.mkdir(parents=True,exist_ok=True)
    archive=out/'pages.zip';digest=hashlib.sha256();size=0
    with open_api('/actions/artifacts/'+str(ARTIFACT)+'/zip') as r,archive.open('wb') as target:
        while chunk:=r.read(1024*1024):
            size+=len(chunk);require(size<=1_000_000_000,'Unexpected archive size');digest.update(chunk);target.write(chunk)
    require('sha256:'+digest.hexdigest()==DIGEST and size==artifact['size_in_bytes'],'Archive bytes not verified')
    g=module('s1m_generator',a.lessons/'tools/ux2/resource_sizes.py')
    source_inputs=g.paths(a.lessons)
    wanted=set(source_inputs)|{'resources.json','data/companion-packs.json','data/resource-sizes.json','assets/catalogue/hub.js'}
    root=out/'published';actual={};metadata={}
    with zipfile.ZipFile(archive) as z:
        require(z.namelist()==['artifact.tar'],'Unexpected Pages ZIP members')
        with z.open('artifact.tar') as stream,tarfile.open(fileobj=stream,mode='r|') as tar:
            for member in tar:
                rel=member.name.removeprefix('./');p=PurePosixPath(rel)
                require(not p.is_absolute() and '..' not in p.parts,'Unsafe archive path')
                require(not member.issym() and not member.islnk(),'Linked archive input')
                if not member.isfile():continue
                with tar.extractfile(member) as handle:data=handle.read()
                actual[rel]=hashlib.sha256(data).hexdigest();metadata[rel]={'sha256':actual[rel],'size_in_bytes':len(data)}
                if rel in wanted:
                    require(p.name!='REGISTER.md','No REGISTER write')
                    target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    require(wanted<=set(actual),'Missing selected archive input')
    published_inputs=g.paths(root)
    require(set(source_inputs)==set(published_inputs),'Aligned source and published input sets differ')
    require(len(published_inputs)==1463,'Aligned published set is not 1463')
    adm=module('active_admission',a.publisher/'domain-split/education_publication_admission.py')
    registry=adm.load_registry(a.publisher/'domain-split/education-publication-admission.json')
    baseline=adm.verify_tree_census(actual,'education-lessons',registry)
    rules=registry['trees']['education-lessons']
    rows=[]
    for rel in published_inputs:
        covered=rel in rules and actual[rel] in adm.admitted(rules[rel])
        rows.append({'path':rel,'covered':covered,'rule':rules.get(rel),'published_sha256':actual[rel],'published_bytes':metadata[rel]['size_in_bytes']})
    counts={'covered':sum(r['covered'] for r in rows),'uncovered':sum(not r['covered'] for r in rows),'pattern_only':0,'undetermined':0}
    print('K2 covered / uncovered / pattern-only / undetermined: '+str(counts['covered'])+' / '+str(counts['uncovered'])+' / 0 / 0')
    (out/'K2_INPUT_COVERAGE.json').write_text(json.dumps({'counts':counts,'rows':rows,'run':RUN,'artifact':artifact,'actual_archive_sha256':digest.hexdigest(),'baseline_admission':baseline},indent=2)+'\n')
    require(counts['uncovered']==0,'K2 STOP: uncovered inputs')
    chosen=published_inputs[0];target=root/chosen;original=target.read_bytes()
    try:
        changed=bytes([original[0]^1])+original[1:];target.write_bytes(changed)
        planted=dict(actual);planted[chosen]=hashlib.sha256(target.read_bytes()).hexdigest()
        fired=False
        try:adm.verify_tree_census(planted,'education-lessons',registry)
        except ValueError as error:
            require('CHANGED education-lessons/'+chosen in str(error),'Admission did not name the changed input')
            reason=str(error);fired=True
        require(fired,'K2 STOP: one-byte input control did not fire')
    finally:target.write_bytes(original)
    adm.verify_tree_census(actual,'education-lessons',registry)
    print('K2 one-byte control FIRED on '+chosen+'; restored admission passes.')
    derived=g.derive(root)
    (out/'ALIGNED_PUBLISHED_TABLE.json').write_text(g.serialise(derived))
    (out/'PUBLISHED_FILE_CENSUS.json').write_text(json.dumps(actual,indent=2)+'\n')
    (out/'K2_CONTROL.json').write_text(json.dumps({'path':chosen,'fired':fired,'reason':reason,'restored':True,'derived_count':len(derived['sizes']),'missing':derived['missing'],'derived_sha256':hashlib.sha256(g.serialise(derived).encode()).hexdigest()},indent=2)+'\n')
    print('Aligned published derivation: '+str(len(derived['sizes']))+' sizes; '+str(len(derived['missing']))+' missing; '+hashlib.sha256(g.serialise(derived).encode()).hexdigest())
    archive.unlink()
    print('K2 actual-published-input coverage established.')

if __name__=='__main__':main()
