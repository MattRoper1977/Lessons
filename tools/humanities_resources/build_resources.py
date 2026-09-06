"""Publish the final reviewed Humanities/RE cover content without rewriting lessons.

Run with an output Lessons root and the preserved, reviewed native pack ZIP.
Every native download is copied byte-for-byte; this does not rebuild Office/PDF files.
"""
from pathlib import Path
from html import escape
import argparse
import hashlib
import json
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
DEST = Path('Humanities_Teesside/David_Cover_Autumn1_W3-W7')
PATHWAYS = ('BUILD', 'GROW', 'LAUNCH')
NATIVE_ROOT = 'David_Humanities_RE_OneDrive_Pack/'
PHASES = ['Arrive', 'Read the source', 'Watch a model', 'Choose', 'Check', 'Your evidence', 'Improve', 'Reflect']
MINUTES = [3, 5, 5, 4, 3, 12, 5, 3]
H = lambda value: escape(str(value), quote=True)


def archive_name(pathway):
    return f'David_{pathway}_Humanities_RE_Pack.zip'


def create_pathway_archives(dest, native_zip, source_manifest):
    """Repackage original native bytes; never edit the Office/PDF members."""
    member_bytes = {}
    with zipfile.ZipFile(native_zip) as original:
        names = original.namelist()
        assert len(names) == len(set(names)) == 132, 'Original member set'
        for name in names:
            assert name.startswith(NATIVE_ROOT) and not original.getinfo(name).is_dir()
            rel = name.removeprefix(NATIVE_ROOT)
            assert rel and not Path(rel).is_absolute() and '..' not in Path(rel).parts
            member_bytes[rel] = original.read(name)
    shared = {name for name in member_bytes if '/' not in name}
    assert shared == {'START_HERE_David_Humanities_RE.docx', 'START_HERE_David_Humanities_RE.pdf'}
    assert all(name in shared or name.split('/')[0] in PATHWAYS for name in member_bytes)
    members = {
        'schema': 'humanities-native-members-v1',
        'source_archive_sha256': source_manifest['native_pack_sha256'],
        'source_archive_root': NATIVE_ROOT,
        'shared_members': sorted(shared),
        'members': [{'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)} for name, data in sorted(member_bytes.items())],
    }
    manifest_bytes = (json.dumps(members, ensure_ascii=False, indent=2) + '\n').encode()
    pinned = source_manifest.get('native_member_manifest_sha256')
    assert pinned and hashlib.sha256(manifest_bytes).hexdigest() == pinned, 'Original native member manifest changed'
    assert (HERE / 'ORIGINAL_MEMBER_MANIFEST.json').read_bytes() == manifest_bytes
    archives = []
    for pathway in PATHWAYS:
        selected = sorted(name for name in member_bytes if name.startswith(pathway + '/') or name in shared)
        target = dest / archive_name(pathway)
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
            for name in selected:
                info = zipfile.ZipInfo(NATIVE_ROOT + name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                output.writestr(info, member_bytes[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        data = target.read_bytes()
        assert len(data) < 10_000_000, 'Pathway archive exceeds the upload budget'
        archives.append({'pathway': pathway, 'filename': target.name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'members': selected})
    return archives


def paras(items):
    return ''.join('<p>'+H(item)+'</p>' for item in items)


def listing(items):
    return '<ol>'+''.join('<li>'+H(item)+'</li>' for item in items)+'</ol>'


def native_paths(c):
    prefix=f'downloads/{c["lane"]}/Week_{c["week"]}/'
    return {'slides':prefix+c['id']+'.pptx', 'pupil':prefix+c['id']+'_Pupil_Sheets.pdf',
            'teacher':prefix+f'{c["lane"]}_W{c["week"]}_David_Plan_and_Answers.pdf'}


def header(title, description, lane=''):
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H(title)} · Made by Matt</title><meta name="description" content="{H(description)}"><link rel="stylesheet" href="resource.css"><script src="resource.js" defer></script></head>
<body class="{H(lane.lower())}"><a class="skip" href="#main">Skip to the lesson</a><header class="site-header"><div class="wrap topbar"><a class="brand" href="../../index.html?subject=Humanities%20%26%20RE">Made by Matt <span>Humanities &amp; RE</span></a><nav aria-label="Main navigation"><a href="index.html">Cover lessons</a><a href="../../index.html?subject=Humanities%20%26%20RE">Lesson hub</a></nav></div></header>'''


def stage(index, content, extra=''):
    return f'<section class="stage {extra}" id="stage-{index+1}" aria-labelledby="stage-title-{index+1}" data-stage="{index}" data-minutes="{MINUTES[index]}"><p class="eyebrow">Stage {index+1} of 8 · {MINUTES[index]} minutes</p><h2 id="stage-title-{index+1}" tabindex="-1">{PHASES[index]}</h2>{content}</section>'


def source_board(label, lines, extra=''):
    return '<div class="source-board '+extra+'"><p class="source-label">'+H(label)+'</p>'+paras(lines)+'</div>'


def render(c, lessons, mapping):
    paths=native_paths(c)
    peers=[x for x in lessons if x['lane']==c['lane'] and x['subject']==c['subject']]
    adjacent=''.join(f'<a href="{H(x["id"])}.html"'+(' aria-current="page"' if x['id']==c['id'] else '')+f'>Week {x["week"]}</a>' for x in peers)
    route_links=''.join('<li><a href="../../'+H(item['path'].removeprefix('Humanities_Teesside/'))+'">'+('Full Humanities lesson' if '_HUM_' in item['path'] else 'Full RE lesson')+'</a></li>' for item in mapping['existing_routes'])
    # Resource page -> parent Humanities_Teesside -> lane directory.
    route_links=route_links.replace('href="../../','href="../')
    re_board=''
    if c.get('re_source_lines'):
        re_board='<h3>Beliefs and values</h3><p>'+H(c['re_objective'])+'</p>'+source_board(c['re_source_label'],c['re_source_lines'],'re-source')
    response_fields=''.join(f'<label for="response-{i}">Response {i}</label><textarea id="response-{i}" rows="3"></textarea>' for i in range(1,len(c['task'])+1))
    supported='Point to one match. Say or show why it fits.' if c['lane']=='BUILD' else 'Add evidence, improve a link, or mark a claim you cannot support.'
    intro=H(c['access']) if c.get('access') else 'Think, point, speak, draw or write. You may pass or ask for a quiet start. An adult may scribe your own words.'
    stages=[
        stage(0,'<p class="large">'+H(c['objective'])+'</p><p>'+intro+'</p>'),
        stage(1,source_board(c['source_label'],c['source_lines'])),
        stage(2,listing(c['model'])+'<p class="prompt">Point to the detail that supports the answer.</p>'),
        stage(3,'<fieldset class="decision"><legend>'+H(c['hinge']['question'])+'</legend>'+''.join(f'<label><input type="radio" name="hinge" value="{chr(65+i)}"><span>{H(choice)}</span></label>' for i,choice in enumerate(c['hinge']['choices']))+'</fieldset><p class="prompt">Choose first. Give a reason before checking.</p>'),
        stage(4,'<details class="answer"><summary>Reveal the deciding clue</summary><p class="answer-letter">'+H(c['hinge']['answer'])+'</p><p>'+H(c['hinge']['reason'])+'</p></details><p>Keep your first choice. If you change it, say what changed your mind.</p>'),
        stage(5,re_board+'<h3>Your tasks</h3>'+listing(c['task'])+response_fields+'<p class="small response-note">Writing stays in this open page only. It is not saved or sent. Copy what you want to keep before leaving.</p>'),
        stage(6,'<p class="large">Check your answer against the source. Show the detail you used.</p><p>'+H(supported)+'</p><label for="improvement">One change or one question</label><textarea id="improvement" rows="3"></textarea><p>Keep your first attempt visible.</p>'),
        stage(7,'<p class="large">'+H(c['exit'])+'</p><label for="take-forward">One thing I can explain, and one next step</label><textarea id="take-forward" rows="3"></textarea>')
    ]
    source_links=''.join('<li><a href="'+H(url)+'" target="_blank" rel="noopener noreferrer">'+H(url.split('/')[2])+' · source '+str(i+1)+'</a></li>' for i,url in enumerate(c['source_refs']))
    integrated='<p class="notice">One integrated 40-minute cover period: retain both the Humanities and RE responses. The beliefs-and-values source board is part of the independent task, with no extra lesson time.</p>' if c['lane']=='LAUNCH' else ''
    return header(c['title'],c['objective'],c['lane'])+f'''
<main id="main" class="wrap"><section class="lesson-intro"><p class="eyebrow">{H(c['lane'])} pathway · {H(c['subject'])} · Autumn 1 · Week {c['week']}</p><h1>{H(c['title'])}</h1><p>Cover lesson · 40 minutes</p><p class="small">{H(c['slot'])}. Match the week to the school calendar before teaching.</p>{integrated}<nav class="week-nav" aria-label="Choose a week">{adjacent}</nav><div class="downloads"><a class="button" href="{H(paths['pupil'])}">Pupil sheets PDF</a><a class="button secondary" href="{H(paths['slides'])}" download>Editable PowerPoint</a><a class="button secondary" href="{H(paths['teacher'])}">Teacher plan &amp; answers PDF</a></div></section>
<div class="lesson-deck" data-lesson-deck>{''.join(stages)}</div><nav class="stage-nav" aria-label="Lesson stage navigation" hidden><button type="button" data-prev>← Previous</button><label for="stage-select" class="sr-only">Choose a stage</label><select id="stage-select">{''.join(f'<option value="{i}">{i+1}. {phase}</option>' for i,phase in enumerate(PHASES))}</select><button type="button" data-next>Next →</button><p class="stage-status" aria-live="polite" aria-atomic="true"></p></nav>
<aside class="teacher-guide"><h2>Teacher guidance</h2><details><summary>Preparation, access and misconceptions</summary><p>{H(c['prep'])}</p><p>{intro}</p><p><strong>Watch for:</strong> {H(c['misconception'])}</p><p class="small">Use the matching pupil sheets for any map, table or writing frame named in these tasks.</p></details><details class="answer teacher-answers"><summary>Teacher key · task answers</summary>{listing(c['answers'])}</details><details><summary>School plan and source references</summary><p>{H(c['sow'])}</p><p>These cover activities use the reviewed source cards and tasks from David’s matching download pack. They are a teaching version of the existing slots, with no additional coverage or qualification credit claimed.</p><ul>{route_links}</ul><p>Optional original-source links need the internet; the labelled teaching cards above are available offline.</p><ul>{source_links}</ul></details></aside></main><footer class="wrap"><a href="index.html">All Humanities &amp; RE cover lessons</a><p class="small">Pupil writing is kept only in the current page. The printable PDFs include the planned response spaces.</p></footer></body></html>\n'''


def render_index(lessons):
    groups=[]
    for lane in ['BUILD','GROW','LAUNCH']:
        cards=[]
        for c in [x for x in lessons if x['lane']==lane]:
            cards.append(f'<article class="lesson-card {lane.lower()}"><p class="eyebrow">Week {c["week"]} · {H(c["subject"])}</p><h3><a href="{H(c["id"])}.html">{H(c["title"])}</a></h3><p>{H(c["objective"])}</p><p class="small">40 minutes · pupil sheets · editable slides</p><a class="button" href="{H(c["id"])}.html">Open cover lesson</a></article>')
        note='Five integrated Humanities/RE periods, one each week.' if lane=='LAUNCH' else 'Humanities and RE have separate 40-minute periods each week.'
        groups.append(f'<section id="{lane.lower()}" class="pathway-section"><h2>{lane}</h2><p>{note}</p><div class="lesson-grid">{"".join(cards)}</div></section>')
    pack_links=''.join(f'<a class="button" href="{archive_name(lane)}" download>Download {lane} pack</a>' for lane in PATHWAYS)
    return header('Humanities & RE cover lessons','25 prepared cover periods for Autumn 1, Weeks 3–7, with pupil sheets and editable PowerPoints.')+'''<main id="main" class="wrap"><section class="lesson-intro"><p class="eyebrow">Ready to teach · Autumn 1 · Weeks 3–7</p><h1>Humanities &amp; RE teaching packs</h1><p class="large">Choose a pathway, then the week and subject. Each cover period has a complete teaching sequence, pupil sheets and an editable PowerPoint.</p><nav class="week-nav" aria-label="Choose a pathway"><a href="#build">BUILD</a><a href="#grow">GROW</a><a href="#launch">LAUNCH</a></nav><div class="downloads">'''+pack_links+'''<a class="button secondary" href="downloads/START_HERE_David_Humanities_RE.pdf">Read the teaching guide</a></div><p class="small">Each pathway pack includes the editable PowerPoints, Word teaching plans and pupil sheets, printable PDFs and starting guide for all five weeks. Download and extract your pack for teaching without an internet connection. The cover weeks are undated until matched to the school calendar.</p></section>'''+''.join(groups)+'''</main><footer class="wrap"><a href="../../index.html?subject=Humanities%20%26%20RE">Browse all Humanities &amp; RE lessons</a></footer></body></html>\n'''


def build(root, native_zip):
    content_bytes=(HERE/'CONTENT.json').read_bytes()
    lessons=json.loads(content_bytes)
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    assert hashlib.sha256(content_bytes).hexdigest()==manifest['content_sha256'],'Final reviewed content changed'
    assert hashlib.sha256(native_zip.read_bytes()).hexdigest()==manifest['native_pack_sha256'],'Native pack changed'
    assert len(lessons)==25 and sum(MINUTES)==40
    dest=root/DEST;dest.mkdir(parents=True,exist_ok=True)
    manifest_by_id={c['id']:c for c in manifest['records']}
    wanted={'START_HERE_David_Humanities_RE.pdf'}
    for c in lessons:
        wanted.update(path.removeprefix('downloads/') for path in native_paths(c).values())
    dependencies=[]
    with zipfile.ZipFile(native_zip) as z:
        for rel in sorted(wanted):
            data=z.read('David_Humanities_RE_OneDrive_Pack/'+rel)
            target=dest/'downloads'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            dependencies.append({'path':target.relative_to(root).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    archives = create_pathway_archives(dest, native_zip, manifest)
    for archive in archives:
        dependencies.append({'path': (DEST / archive['filename']).as_posix(), 'sha256': archive['sha256'], 'bytes': archive['bytes']})
    old_candidate = dest / native_zip.name
    if old_candidate.exists():
        assert old_candidate.resolve() != native_zip.resolve(), 'Never remove the preserved original pack'
        assert hashlib.sha256(old_candidate.read_bytes()).hexdigest() == manifest['native_pack_sha256']
        old_candidate.unlink()
    for name in ['resource.css','resource.js']:shutil.copyfile(HERE/name,dest/name)
    for c in lessons:(dest/(c['id']+'.html')).write_text(render(c,lessons,manifest_by_id[c['id']]),encoding='utf-8')
    (dest/'index.html').write_text(render_index(lessons),encoding='utf-8')
    (HERE/'DOWNLOAD_MANIFEST.json').write_text(json.dumps({'dependencies':dependencies, 'archives': archives},ensure_ascii=False,indent=2)+'\n')
    return {'cover_pages':len(lessons),'native_downloads':len(wanted),'pathway_archives':len(archives),'original_members_preserved':132,'existing_mapped_routes':sum(len(x['existing_routes']) for x in manifest['records']),'root':str(dest)}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=HERE.parents[1]);p.add_argument('--native-zip',type=Path,required=True);args=p.parse_args()
    print(json.dumps(build(args.root,args.native_zip)))
