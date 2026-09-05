"""Build the static Science shelf from reviewed additive catalogue metadata."""
from pathlib import Path
import collections, html, json, re
from lxml import html as lhtml
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[2]
DATA=json.loads((ROOT/'assets/catalogue/science-shelf.json').read_text())
E=html.escape
TERMS=list(DATA['terms'])
STYLES=list(DATA['styles'])
def natural(value):return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)',value)]
def card(row):
 title=re.sub(r'\s*[·—]\s*40 minutes\s*$','',row['title'])
 path=row['path'].removeprefix('Science_Teesside/')
 return f'''<article class="card t-{row['pathway']}" data-lesson-path="{E(row['path'],quote=True)}" data-term="{E(row['term'],quote=True)}" data-style="{E(row['style'],quote=True)}" data-pathway="{E(row['pathway'],quote=True)}"><p class="kind">{E(row['pathway'])} · Science</p><h4><a href="{E(path,quote=True)}">{E(title)}</a></h4><p>{E(DATA['styles'][row['style']])}</p><a class="go" href="{E(path,quote=True)}">Open lesson <span aria-hidden="true">→</span></a></article>'''
body=[]
for pathway in ['BUILD','GROW','LAUNCH']:
 rows=[r for r in DATA['lessons'] if r['pathway']==pathway]
 terms=[]
 for term in TERMS:
  trows=[r for r in rows if r['term']==term]
  if not trows:continue
  batches=[]
  for style in STYLES:
   for batch in sorted(set(r['batch'] for r in trows if r['style']==style)):
    selected=sorted([r for r in trows if r['style']==style and r['batch']==batch],key=lambda r:natural(r['path']))
    batches.append(f'<section class="catalogue-batch" data-style="{E(style)}"><h4>{E(batch)} <span data-batch-count>· {len(selected)} lessons</span></h4><div class="grid">'+''.join(card(r) for r in selected)+'</div></section>')
  terms.append(f'<section class="catalogue-term" data-term="{E(term)}"><h3>{E(DATA["terms"][term])} <span data-term-count>· {len(trows)} lessons</span></h3>'+''.join(batches)+'</section>')
 body.append(f'<details class="science-pathway l-{pathway}" data-pathway="{pathway}" open><summary><h2>{pathway}</h2><span data-pathway-count>{len(rows)} lessons</span><span class="chev" aria-hidden="true">▾</span></summary>'+''.join(terms)+'</details>')
term_options=''.join(f'<option value="{E(term)}">{E(label)}</option>' for term,label in DATA['terms'].items() if any(r['term']==term or term in r['terms'] for r in DATA['lessons']))
style_options=''.join(f'<option value="{E(style)}">{E(label)}</option>' for style,label in DATA['styles'].items() if any(r['style']==style for r in DATA['lessons']))
root_source=(ROOT/'index.html').read_text()
header=re.search(r'<header class="header mbm-site-header".*?</header>',root_source,re.S).group(0)
header_doc=lhtml.fromstring(header)
for link in list(header_doc.xpath('//a[@href]')):
 u=urlsplit(link.get('href'))
 if u.netloc in {'madebymatt-play.uk','www.madebymatt-play.uk'} or u.path.rstrip('/').lower()=='/games':link.drop_tree()
header=lhtml.tostring(header_doc,encoding='unicode')
# Reuse the actual Lesson Hub house styles and current header. Relative platform
# assets are addressed from this shelf's own directory, not from a new shell.
base_css=re.search(r'<style>(.*?)</style>',root_source,re.S).group(1)
output='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Science by pathway and term — Made by Matt</title><meta name="description" content="Find Science lessons by BUILD, GROW and LAUNCH pathway, term and teaching version. Recommended lessons, fuller Lundy Loop versions and earlier resources stay together.">
<meta name="theme-color" content="#161D3D"><link rel="icon" href="https://madebymatt.uk/favicon.svg">
<style>'''+base_css+'''</style><link rel="stylesheet" href="../assets/mbm-platform.css"><link rel="stylesheet" href="../assets/mbm-hub.css"><link rel="stylesheet" href="../assets/catalogue/catalogue.css"><link rel="stylesheet" href="../assets/catalogue/science-shelf.css">
<script>try{var theme=localStorage.getItem('mbm_reading_theme');if(theme&&theme!=='cream')document.documentElement.setAttribute('data-theme',theme)}catch(e){}</script>
</head><body class="mbm-hub mbm-hub-lessons" data-mbm-estate="lessons"><a class="skip" href="#main">Skip to Science lessons</a>'''+header+'''
<main id="main"><section class="hero"><div class="hero-in"><nav class="lesson-breadcrumb" aria-label="Breadcrumb"><a href="/">Learning home</a><a href="../">All lessons</a></nav><p class="eyebrow">Science</p><h1>Science <span>by term</span></h1><p class="lead">Choose your pathway and term, then choose a teaching version. The recommended LAUNCH Weeks 3–7 lessons bring the cover pack into the familiar classroom slides.</p></div></section>
<section class="catalogue-intro" aria-label="Choose a teaching version"><div class="catalogue-links"><a href="?pathway=LAUNCH&amp;term=Aut1&amp;style=recommended" data-shortcut="recommended">Recommended LAUNCH · Weeks 3–7</a><a href="?style=full-lundy" data-shortcut="full-lundy">Browse full Lundy Loop versions</a><a href="../">All subjects at the Lesson Hub →</a></div><p>Full Lundy Loop versions repeat Space, Voice, Audience and Influence prompts through the lesson. Current and earlier teaching series remain available alongside them.</p><p>The Wednesday osmosis lesson offers a planned practical or a clearly labelled sample-data alternative. Friday focuses on analysis; sample data does not count as completing a practical.</p></section>
<div class="toolbar" role="search" aria-label="Filter Science lessons"><label>Search<input id="science-search" type="search" placeholder="Try: osmosis, muscles, fossils…" autocomplete="off"></label><label>Pathway<select id="science-pathway"><option value="">All pathways</option><option value="BUILD">BUILD</option><option value="GROW">GROW</option><option value="LAUNCH">LAUNCH</option></select></label><label>Term<select id="science-term"><option value="">All terms</option>'''+term_options+'''</select></label><label>Teaching style<select id="science-style"><option value="">All teaching styles</option>'''+style_options+'''</select></label></div>
<div class="science-status"><p id="science-count" role="status" aria-live="polite" aria-atomic="true">'''+str(len(DATA['lessons']))+''' Science lessons</p><button type="button" id="science-clear">Clear filters</button></div><p id="science-empty" class="status" hidden>No matching lessons. Try a different term or clear the filters.</p>
<noscript><p class="status">All lessons are listed below. The filters need JavaScript; lesson links work without it.</p></noscript>
<div id="science-lessons">'''+''.join(body)+'''</div></main><footer class="footer"><div class="bar"><p>Made by Matt · Learn • Build • Explore</p><a href="../">Return to the Lesson Hub</a></div></footer>
<script src="../assets/catalogue/science-shelf.js"></script><script defer src="../assets/mbm-theme.js"></script><script defer src="../assets/mbm-platform.js"></script><script defer src="/hud.js"></script>
</body></html>
'''
(ROOT/'Science_Teesside/index.html').write_text(output)
print(f'Built static Science shelf with {len(DATA["lessons"])} lesson links and {len(body)} pathways.')
