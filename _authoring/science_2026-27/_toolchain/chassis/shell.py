"""Portable renderer for Matt's recovered classic slideshow chassis.

render_shell(d, slides_html, print_html, inline_js='') -> standalone HTML string.

Required d: id, title, pathway (BUILD/GROW/LAUNCH), subject (Science/Humanities/Art/ASDAN).
Optional d: word_help and staff (trusted, authored HTML); extra_css (content widgets only),
logo_data_uri (verified original asset only), menu_href (local review menu), stages.

Root supplies complete .slide elements in slides_html and .print-section elements in
print_html. Runtime supports data-title, data-type, data-timer, data-teacher and
 data-stage-index. It exposes mbmShowSlide(index) plus the classic function names.
Style files are literal source copies; access.css adds sizing/accessibility rules.
"""
from pathlib import Path
import html,json,re
from html.parser import HTMLParser

class _SlideCounter(HTMLParser):
 def __init__(self):
  super().__init__();self.count=0
 def handle_starttag(self,tag,attrs):
  if 'slide' in dict(attrs).get('class','').split():self.count+=1

def count_slides(value):
 parser=_SlideCounter();parser.feed(value);return parser.count
HERE=Path(__file__).resolve().parent

def esc(value): return html.escape(str(value),quote=True)
def safe_json(value): return json.dumps(value,ensure_ascii=False).replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
def print_tools():
 return '<div class="classic-print-tools">'+''.join(f'<button type="button" data-action="print" data-level="{name}">{glyph} {name.title()} pack</button>' for name,glyph in [('supported','◆'),('standard','▲'),('stretch','★')])+'</div>'
def _words(d):
 if isinstance(d.get('word_help'),str): return d['word_help']
 terms=d.get('vocabulary') or []
 return '<dl class="classic-word-list">'+''.join('<dt>'+esc(item.get('term',''))+'</dt><dd>'+esc(item.get('meaning',''))+'</dd>' for item in terms)+'</dl>'
def _dialog(identifier,title,body,staff=False):
 return f'<dialog id="{identifier}" class="classic-dialog" aria-labelledby="{identifier}-title"'+(' data-audience="staff"' if staff else '')+f'><div class="v4-modal"><h2 id="{identifier}-title">{title}</h2>{body}<div class="v4-modal-footer"><button type="button" data-action="close">Close</button></div></div></dialog>'

def render_shell(d, slides_html, print_html, inline_js=''):
 pathway=str(d['pathway']).upper(); subject_label=str(d['subject']); lowered=subject_label.lower()
 if lowered.startswith('science') or any(x in lowered for x in ['biology','physics','chemistry']): subject='Science'
 elif lowered.startswith('humanit'): subject='Humanities'
 elif lowered.startswith('asdan'): subject='Asdan'
 elif re.search(r'\barts?\b',lowered): subject='Art'
 else: raise ValueError('Unknown classic donor subject: '+subject_label)
 if pathway not in ['BUILD','GROW','LAUNCH']:raise ValueError('Unknown pathway: '+pathway)
 key=pathway.lower()+'_'+subject.lower()
 donor_css=(HERE/'styles'/f'{key}.css').read_text()
 common_css=(HERE/'controls.css').read_text()
 access_css=(HERE/'access.css').read_text()
 runtime=(HERE/'controls.js').read_text()
 extra_css=str(d.get('extra_css',''))
 if '</style' in extra_css.lower(): raise ValueError('extra_css must be CSS only')
 manifest=json.loads((HERE/'chassis_manifest.json').read_text())
 donor=next(item for item in manifest['donors'] if item['family'].lower().replace(' ','_')==key)
 data={k:d[k] for k in ['id','title','objective','stages'] if k in d}
 staff=d.get('staff','<p>See the lesson teacher guidance.</p>')
 if not isinstance(staff,str):raise TypeError('d.staff must be trusted HTML')
 logo=str(d.get('logo_data_uri',''))
 if logo and not re.match(r'^data:image/(?:png|jpeg|webp|svg\+xml);base64,',logo):raise ValueError('Logo must be an embedded verified image')
 if logo:
  slides_html=re.sub(r'(<(?:section|div)\b[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*>)',lambda match:match.group(1)+f'<img class="classic-brand" src="{esc(logo)}" alt="Made by Matt">',slides_html,count=1)
 menu=''
 if d.get('menu_href'):menu=f'<a href="{esc(d["menu_href"])}">Lessons<span class="classic-menu-label"> menu</span></a>'
 ta='<div class="ta-section"><strong id="ta-current-title">Current stage</strong><p id="ta-current-text"></p></div>'+staff
 tools='<p>Choose a slide or a print route.</p><label class="classic-tools-label" for="slide-picker">Go to slide</label><select id="slide-picker"></select><h3>Teacher Print Tools</h3>'+print_tools()+'<button type="button" data-action="notes">Save my work</button><p>Your typed notes stay here while this page is open. Save them before closing or reloading.</p>'
 cold='<div class="cc-question" id="cold-call-question"></div><div class="scaffold-box"><p>Give thinking time. Invite a response by voice, pointing or showing work. A pupil can pass; check in privately when useful.</p></div>'
 pause='<div class="scaffold-box"><p>Take a quiet pause.</p><p>You can look away from the screen. Come back when you are ready.</p></div><p>The lesson and your work are still here. Close this box to return.</p>'
 return f'''<!DOCTYPE html>
<html lang="en-GB" class="pathway-{pathway.lower()}" data-chassis="classic-source" data-chassis-family="{esc(donor['family'])}">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="color-scheme" content="light">
<title>{esc(d['title'])} · {pathway} {esc(d['subject'])}</title>
<meta name="classic-donor" content="{esc(donor['donor'])}"><meta name="classic-donor-sha256" content="{donor['donor_sha256']}">
<style id="literal-classic-donor">{donor_css}</style>
<style id="literal-classic-controls">{common_css}</style>
<style id="standalone-access">{access_css}</style>
<style id="lesson-widgets">{extra_css}</style></head><body>
<div id="auto-timer" aria-label="Stage timer"><span id="auto-timer-icon" aria-hidden="true">⏱</span><span id="auto-timer-display">00:00</span><button class="at-btn" id="auto-timer-toggle" type="button" data-action="timer-toggle" aria-label="Start stage timer">▶</button><button class="at-btn" type="button" data-action="timer-reset" aria-label="Reset stage timer">↺</button></div>
<div class="classic-toolbar">{menu}<button type="button" class="ghost" data-action="words">Word help</button><button type="button" class="ghost" data-action="pause">Pause</button><button type="button" class="ghost" data-action="tools">Tools &amp; print</button></div>
<main class="slide-container" aria-label="{esc(d['title'])}">{slides_html}</main>
<div class="controls" aria-label="Lesson controls"><button type="button" id="previous-slide" data-action="previous">◀ Previous</button><button type="button" data-action="ta">🧑‍🏫 TA Brief</button><button type="button" data-action="cold-call">🎯 Cold Call</button><button type="button" id="next-slide" data-action="next">Next ▶</button></div>
<div class="progress-wrap" id="classic-progress" role="progressbar" aria-label="Lesson progress" aria-valuemin="1" aria-valuemax="{count_slides(slides_html)}" aria-valuenow="1"><div class="progress-bar" id="progressBar"></div></div><div class="progress-label" id="progressLabel" aria-live="polite">Slide 1</div><p class="classic-status" id="classic-status" role="status"></p>
{_dialog('ta-dialog','TA Brief',ta,True)}
{_dialog('word-dialog','Word help',_words(d))}
{_dialog('cold-call-dialog','Cold Call',cold,True)}
{_dialog('pause-dialog','Pause',pause)}
{_dialog('tools-dialog','Lesson tools',tools)}
<div id="print-area">{print_html}</div>
<script>window.CLASSIC_LESSON={safe_json(data)};</script>
<script>{runtime}</script>
<script>{inline_js}</script>
</body></html>'''
