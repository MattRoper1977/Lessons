"""Static reference and content checks. This does not claim browser/print QA."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,json,hashlib
from lxml import html

HERE=Path(__file__).resolve().parent

def check(root):
    dest=root/'Science_Teesside/Grow/resources'
    lessons=json.loads((HERE/'CONTENT.json').read_text())
    sources=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    results=[]
    allowed_lesson_paths={root/c['online_path'] for c in lessons}
    nav_only={root/'index.html',*allowed_lesson_paths}
    for dependency in sources['dependencies']:
        p=dest/dependency['target']
        assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==dependency['sha256'],p
    for c in lessons:
        p=dest/(c['id']+'.html');d=html.fromstring(p.read_text());refs=0
        ids=d.xpath('//*[@id]/@id');assert len(ids)==len(set(ids)),(c['id'],'duplicate IDs')
        assert len(d.xpath('//h1'))==2 # screen heading and print-only task heading
        assert d.xpath('//html/@lang')==['en-GB']
        assert len(d.xpath('//nav[@aria-label="Choose the teaching period"]/a'))==2
        assert d.xpath('//a[@aria-current="page"]/@href')==[c['id']+'.html']
        for node in d.xpath('//img'):assert node.get('alt','').strip(),(c['id'],'empty image alternative')
        for node in d.xpath('//textarea'):assert d.xpath('//label[@for=$id]',id=node.get('id'))
        assert not d.xpath('//details[contains(@class,"answer")][@open]'),(c['id'],'premature answers')
        assert not d.xpath('//form|//iframe|//video[@autoplay]'),(c['id'],'unexpected transport or playback')
        for node in d.xpath('//*[@href or @src or @poster]'):
            for attr in ['href','src','poster']:
                val=node.get(attr)
                if not val:continue
                u=urlsplit(val)
                if u.scheme:
                    assert attr=='href' and u.scheme=='https' and u.netloc=='science.nasa.gov',(c['id'],val)
                    continue
                if not u.path:
                    assert u.fragment in ids,(c['id'],'missing fragment',val)
                    continue
                target=(p.parent/unquote(u.path)).resolve()
                assert target.is_relative_to(root.resolve()),(c['id'],'path escape',val)
                assert target.is_file() or (attr=='href' and target in nav_only),(c['id'],'missing reference',val)
                if not target.is_file():assert attr=='href'
                refs+=1
        text=' '.join(d.xpath('//text()'))
        assert c['activity']['prompt'] in text and c['activity']['answer'] in text
        assert c['video']['prompt'] in text and c['video']['fallback_text'] in text
        assert 'two separate 40-minute lessons' in text
        if c['id'] in ['GS_W3B','GS_W5B']:
            assert 'Invented teaching data' in text and 'not measurements made by this class' in text
            assert 'stopped sooner' not in text
        if c['week']==7:
            assert c['video']['fallback_image']=='assets/Moon_rotation_fallback.png'
        if c['week']==6:assert 'still itself cannot show movement' in text
        if c['week']==3:assert 'described scenario' in text
        results.append({'id':c['id'],'local_references':refs,'html_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    script=(dest/'resource.js').read_text()
    for prohibited in ['fetch(','XMLHttpRequest','localStorage','sessionStorage','sendBeacon']:assert prohibited not in script,prohibited
    css=(dest/'resource.css').read_text()
    for required in ['@media(max-width:740px)','@media print','prefers-reduced-motion','textarea','min-height:44px','body.print-answers']:
        assert required in css,required
    return {'result':'PASS','method':'Static DOM, referenced-file identities and explicit content assertions; not a browser rendering claim','pages':results,'source_dependencies':len(sources['dependencies']),'remaining':['Browser mobile/keyboard interactions','Browser print-pagination and visual review','Actual optional video playback','Integration and offline extracted-file acceptance']}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=HERE.parents[1]);ap.add_argument('--report',type=Path);a=ap.parse_args()
    result=check(a.root)
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':result['result'],'pages':len(result['pages']),'local_references':sum(r['local_references'] for r in result['pages']),'dependencies':result['source_dependencies']}))
