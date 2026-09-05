"""Rebuild the supplemental GROW resources; never modify existing lesson files."""
from pathlib import Path
from html import escape as esc
import argparse, json, shutil, hashlib

HERE=Path(__file__).resolve().parent
H=lambda value:esc(str(value),quote=True)

def paragraphs(items):
    return ''.join('<p>'+H(text)+'</p>' for text in items)

def answer(text,label='Reveal a worked explanation after an attempt'):
    return '<details class="answer"><summary>'+H(label)+'</summary><p>'+H(text)+'</p></details>'

def table(activity):
    rows=activity.get('table')
    if not rows:return ''
    result='<div class="table-wrap" tabindex="0" role="region" aria-label="Activity data table"><table><caption>'+H(activity['table_caption'])+'</caption><thead><tr>'
    result+=''.join('<th scope="col">'+H(cell)+'</th>' for cell in rows[0])+'</tr></thead><tbody>'
    for row in rows[1:]:
        result+='<tr>'+''.join(('<th scope="row">'+H(cell)+'</th>') if i==0 else '<td>'+H(cell)+'</td>' for i,cell in enumerate(row))+'</tr>'
    return result+'</tbody></table></div>'

def render(c,lessons):
    video=c['video'];activity=c['activity'];stem=c['id'].lower()
    notice='<p class="notice">'+H(c['evidence_note'])+'</p>'
    period_links=''.join('<a '+('aria-current="page" ' if other['id']==c['id'] else '')+'href="'+H(other['id'])+'.html">'+H(other['day'])+' resources</a>' for other in lessons if other['week']==c['week'])
    media=''
    if video.get('local_file'):
        media='<video controls preload="none" playsinline poster="'+H(video['poster'])+'" aria-label="'+H(video['title'])+'"><source src="'+H(video['local_file'])+'" type="video/mp4"><p>Your browser cannot play this clip. Use the still scenario below.</p></video><p class="small">Optional local clip. Play only when ready; the question and still scenario also work without playback.</p>'
    else:
        media='<p><a class="button" href="'+H(video['url'])+'" target="_blank" rel="noopener noreferrer">Open NASA’s Moon rotation resource</a></p><p class="small">This optional link needs the internet and opens a new tab. The same question is available in the local model below.</p>'
    figure='<figure><img src="'+H(c['image'])+'" alt="'+H(c['image_alt'])+'" loading="lazy" width="1440" height="675"><figcaption>'+H(c['model_caption'])+'</figcaption></figure>'
    fallback='<figure><img src="'+H(video['fallback_image'])+'" alt="'+H(video['fallback_alt'])+'" loading="lazy"><figcaption>'+H(video['fallback_caption'])+'</figcaption></figure>'
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H(c['title'])} · GROW Science resources · Made by Matt</title><meta name="description" content="{H(c['objective'])} Shared tasks, printable worksheets and models for GROW Science Week {c['week']}."><link rel="stylesheet" href="resource.css"><script src="resource.js" defer></script></head>
<body><a class="sr-only" href="#main">Skip to resources</a><header><div class="wrap"><nav class="topnav" aria-label="Resource navigation"><a href="../{H(Path(c['online_path']).name)}">Return to the lesson</a><a href="../../../index.html?subject=Science">Browse Science</a></nav><div class="hero"><p class="eyebrow">Made by Matt · GROW Science · Week {c['week']}</p><h1>{H(c['title'])}</h1><p class="objective">{H(c['objective'])}</p><p class="schedule">{H(c['day'])} · {H(c['time'])}</p></div></div></header>
<main id="main" class="wrap"><nav class="period-nav" aria-label="Choose the teaching period">{period_links}</nav><p class="intro">Choose one task, model or clip within the current lesson stage. These resources support the existing two separate 40-minute lessons; they do not add another lesson or extra time.</p>
<div class="print-title"><h1>Week {c['week']} · {H(c['day'])}: {H(c['title'])}</h1><p>Name: ____________________ Date: ______________</p></div>
<div class="downloads"><a class="button" href="{H(c['worksheet_pdf'])}">Worksheet PDF</a></div>
<div class="print-actions js-only"><button class="button secondary" type="button" data-print-task>Print this shared task</button><label><input type="checkbox" data-print-answers> Include worked explanation when printing</label></div>
<div class="resource-layout"><div><section class="panel task" aria-labelledby="task-title"><p class="eyebrow">We Do · think together</p><h2 id="task-title">{H(activity['title'])}</h2><p class="prompt">{H(activity['prompt'])}</p>{notice}{table(activity)}<ol class="choices">{''.join('<li>'+H(item)+'</li>' for item in activity['items'])}</ol><p>Discuss, point, draw, write or dictate a first explanation. Choose one example first; extend only if there is time.</p><label for="{stem}-first">Our first reason</label><textarea id="{stem}-first" rows="3" placeholder="Keep a first idea here, or give it aloud."></textarea>{answer(activity['answer'])}<label for="{stem}-repair">One change to our explanation</label><textarea id="{stem}-repair" rows="2"></textarea><details class="support"><summary>Give a smaller support cue</summary><p>{H(c['support'])}</p></details><p class="small browser-note">Writing stays in this open page only. It is not saved or sent. Copy any record you want to keep before leaving.</p></section>
<section class="panel independent" aria-labelledby="independent-title"><p class="eyebrow">Apply it</p><h2 id="independent-title">Use the current workshop</h2><p>{H(c['independent'])}</p>{answer(c['model_answer'],'Teacher model · compare with the pupil’s evidence')}</section></div>
<aside><section class="panel model" aria-labelledby="model-title"><p class="eyebrow">I Do · explain and model</p><h2 id="model-title">Look, explain, check</h2>{figure}{paragraphs(c['model'])}<details><summary>Connect the ideas</summary>{paragraphs(c['connect'])}</details><details class="answer"><summary>Quick check</summary><p>{H(c['starter'])}</p><details class="answer"><summary>Check the explanation</summary><p>{H(c['starter_answer'])}</p></details></details></section>
<section class="panel media" aria-labelledby="video-title"><p class="eyebrow">Optional clip or still</p><h2 id="video-title">{H(video['title'])}</h2><p><strong>Question:</strong> {H(video['prompt'])}</p>{media}<h3>The same science without video</h3>{fallback}<p>{H(video['fallback_text'])}</p>{answer(video['answer'],'Teacher explanation for the video or still scenario')}<p class="small">Use a short extract or the still scenario in place of part of the modelling time. A video or model is not evidence that pupils completed a practical.</p></section>
<section class="panel teacher"><h2>For the adult</h2><details><summary>Preparation and a likely misconception</summary><p>{H(c['prep'])}</p><p><strong>Watch for:</strong> {H(c['trap'])}</p></details><details><summary>Exit question and model answer</summary><p>{H(c['exit_question'])}</p>{answer(c['exit_answer'])}</details></section></aside></div></main>
<footer><div class="wrap"><p><strong>Made by Matt · Learn • Build • Explore</strong></p><p class="small">{H(c['source_note'])}</p><a href="../{H(Path(c['online_path']).name)}">Return to the original two-period lesson</a></div></footer></body></html>
'''

def build(root):
    lessons=json.loads((HERE/'CONTENT.json').read_text())
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    dest=root/'Science_Teesside/Grow/resources';dest.mkdir(parents=True,exist_ok=True)
    for asset in manifest['dependencies']:
        p=dest/asset['target']
        assert p.is_file(),f'Missing dependency: {p}'
        assert hashlib.sha256(p.read_bytes()).hexdigest()==asset['sha256'],f'Changed dependency: {p}'
    for name in ['resource.css','resource.js']:shutil.copyfile(HERE/name,dest/name)
    for c in lessons:(dest/(c['id']+'.html')).write_text(render(c,lessons),encoding='utf-8')
    return {'pages':len(lessons),'dependencies':len(manifest['dependencies']),'output':str(dest)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=HERE.parents[1]);args=ap.parse_args()
    print(json.dumps(build(args.root),ensure_ascii=False))
