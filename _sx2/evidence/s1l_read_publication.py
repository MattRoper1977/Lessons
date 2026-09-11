#!/usr/bin/env python3
"""Read the already-deployed Pages archive for S1-L; never build or deploy."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
import argparse,hashlib,json,os,tarfile,urllib.request,zipfile
from urllib.parse import urlsplit

REPO='MattRoper1977/Lessons'
RUN=34586602323
ARTIFACT=10194069928
SOURCE='8c7d3e9e4c24faf48c13f5d73bb70226703a7c12'
PUBLISHER='7072a5605e795b1c872f843f04f2403a8880c409'
ARCHIVE_DIGEST='sha256:c57add0a1a3275246c26910f5cad001f028f97c8ef0bcac93565855ba3da0210'

def require(ok,message):
    if not ok: raise ValueError(message)

def sha(data):return hashlib.sha256(data).hexdigest()

def check_paths(paths):
    require(len(paths)==31 and len(set(paths))==31,'Expected the preserved 31 distinct paths')
    for p in paths:
        require(str(PurePosixPath(p))==p and not p.startswith('/') and '..' not in PurePosixPath(p).parts and p.endswith('.html'),'Invalid preserved path')

def check_binding(run,jobs,artifact):
    require(run['id']==RUN and run['head_sha']==SOURCE and run['conclusion']=='success' and run['status']=='completed','Publication is not the successful named source run')
    require(any(w['sha']==PUBLISHER for w in run['referenced_workflows']),'Wrong publisher')
    require(any(j['name']=='publication / deploy' and j['status']=='completed' and j['conclusion']=='success' for j in jobs['jobs']),'Deploy job did not succeed')
    require(artifact['id']==ARTIFACT and artifact['name']=='github-pages' and not artifact['expired'],'Wrong or expired artifact')
    require(artifact['workflow_run']['id']==RUN and artifact['workflow_run']['head_sha']==SOURCE,'Artifact is not bound to source/run')
    require(artifact['digest']==ARCHIVE_DIGEST,'Artifact metadata digest differs from the recorded deployed archive')

def check_digest(actual,expected):require(actual==expected,'Downloaded artifact digest mismatch')

def check_members(wanted,found):require(set(wanted)<=set(found),'Published archive is missing requested paths: '+str(sorted(set(wanted)-set(found))))

class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        require(newurl.startswith('https://'),'Artifact redirect must remain HTTPS')
        result=super().redirect_request(req,fp,code,msg,headers,newurl)
        if result is not None and urlsplit(req.full_url).netloc!=urlsplit(newurl).netloc:
            result.remove_header('Authorization')
        return result

def open_api(route):
    token=os.environ['GH_TOKEN']
    request=urllib.request.Request('https://api.github.com/repos/'+REPO+route,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'S1-L-read-only-published-tree'})
    return urllib.request.build_opener(Redirect()).open(request,timeout=45)

def api(route):
    with open_api(route) as response:return json.load(response)

class Page(HTMLParser):
    def __init__(self):super().__init__();self.redirect_marker=False;self.canonical=[];self.links=[];self.robots=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='body' and 'data-game-moved' in a:self.redirect_marker=True
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='a':self.links.append({'id':a.get('id'),'href':a.get('href')})
        if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content'))

def self_test():
    run={'id':RUN,'head_sha':SOURCE,'conclusion':'success','status':'completed','referenced_workflows':[{'sha':PUBLISHER}]}
    jobs={'jobs':[{'name':'publication / deploy','status':'completed','conclusion':'success'}]}
    artifact={'id':ARTIFACT,'name':'github-pages','expired':False,'workflow_run':{'id':RUN,'head_sha':SOURCE},'digest':ARCHIVE_DIGEST}
    check_binding(run,jobs,artifact)
    paths=[f'page-{i}.html' for i in range(31)];check_paths(paths);check_members(paths,paths);check_digest('a','a')
    cases=[('missing census member',lambda:check_paths(paths[:-1])),('wrong source run',lambda:check_binding(dict(run,head_sha='0'*40),jobs,artifact)),('failed deploy job',lambda:check_binding(run,{'jobs':[]},artifact)),('expired artifact',lambda:check_binding(run,jobs,dict(artifact,expired=True))),('wrong archive bytes',lambda:check_digest('b','a')),('missing archived route',lambda:check_members(paths,paths[:-1]))]
    for name,call in cases:
        fired=False
        try:call()
        except ValueError:fired=True
        require(fired,'Control did not fire: '+name);print('FIRED '+name)
    print('RESTORED valid provenance and complete member set PASS; 6/6 refusal controls fired')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--census',type=Path);parser.add_argument('--output',type=Path,default=Path('s1l-published-readback'));args=parser.parse_args()
    if args.self_test:self_test();return
    census=json.loads(args.census.read_text());paths=census['paths'];check_paths(paths)
    require(census['source_commit']=='c21532c8adfba0b7e941df7da7ec3f2a19142f20' and census['source_pr']==508,'Census provenance changed')
    run=api('/actions/runs/'+str(RUN));jobs=api('/actions/runs/'+str(RUN)+'/jobs?per_page=100');artifact=api('/actions/artifacts/'+str(ARTIFACT));check_binding(run,jobs,artifact)
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    archive=out.parent/'s1l-pages.zip';digest=hashlib.sha256();size=0
    print('Reading successful deploy archive',ARTIFACT,'for',SOURCE,flush=True)
    with open_api('/actions/artifacts/'+str(ARTIFACT)+'/zip') as response,archive.open('wb') as dest:
        while chunk:=response.read(1024*1024):
            size+=len(chunk);require(size<=1_000_000_000,'Unexpected archive size');digest.update(chunk);dest.write(chunk)
    check_digest('sha256:'+digest.hexdigest(),artifact['digest']);require(size==artifact['size_in_bytes'],'Archive byte length differs from metadata')
    wanted=set(paths)|{'data/resource-sizes.json','resources.json','data/companion-packs.json','subject.html','index.html','assets/catalogue/hub.js','assets/catalogue/catalogue.js'}
    found={};scanned=[];references=[]
    with zipfile.ZipFile(archive) as zip:
        members=zip.namelist();require(members==['artifact.tar'],'Unexpected Pages ZIP members')
        with zip.open('artifact.tar') as stream,tarfile.open(fileobj=stream,mode='r|') as tar:
            for member in tar:
                rel=member.name.removeprefix('./');path=PurePosixPath(rel)
                require(not path.is_absolute() and '..' not in path.parts,'Unsafe archive member')
                if not member.isfile():continue
                inspect=rel in wanted or path.suffix in {'.js','.mjs','.html','.htm'}
                if not inspect:continue
                with tar.extractfile(member) as handle:data=handle.read()
                scanned.append(rel)
                has_reference=b'resource-sizes' in data
                if has_reference:references.append(rel)
                if rel in wanted or has_reference or (path.suffix in {'.js','.mjs'} and rel.startswith('assets/')):
                    target=out/'published'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
                    found[rel]={'sha256':sha(data),'size_in_bytes':len(data)}
                    if rel in paths:
                        page=Page();page.feed(data.decode('utf-8'));found[rel].update({'redirect_marker':page.redirect_marker,'canonical':page.canonical,'links':page.links,'robots':page.robots})
    check_members(wanted,found)
    sizes=json.loads((out/'published/data/resource-sizes.json').read_text())
    rows=[{'path':rel,**found[rel],'size_row_present':rel in sizes['sizes'],'size_row_value':sizes['sizes'].get(rel)} for rel in paths]
    result={'source_commit':SOURCE,'publisher':PUBLISHER,'run':run,'jobs':jobs,'artifact':artifact,'downloaded_size':size,'downloaded_sha256':digest.hexdigest(),'census':census,'rows':rows,'extracted_files':found,'consumer_reference_files':references,'html_js_scanned':len(scanned),'all_scanned_paths':scanned,'table_metadata':{k:v for k,v in sizes.items() if k!='sizes'},'table_actual_entries':len(sizes['sizes'])}
    (out/'readback.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Verified archive SHA256:',digest.hexdigest())
    print('Read 31/31 published routes; redirects:',sum(x['redirect_marker'] for x in rows),'table rows present:',sum(x['size_row_present'] for x in rows))
    print('resource-sizes consumers:',json.dumps(references))
    print('Published table entries:',len(sizes['sizes']))
    archive.unlink()

if __name__=='__main__':main()
