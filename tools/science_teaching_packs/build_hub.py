"""Render the additive public Science download shelf from reviewed manifests."""
from pathlib import Path
from html import escape as E
import json

ROOT = Path(__file__).resolve().parents[2]
PACKS = ROOT / 'Science_Teesside/Teaching_Packs'


def size(value):
    return f'{value / 1_000_000:.1f} MB' if value >= 1_000_000 else f'{max(1, round(value / 1000))} KB'


def link(pathway, item, label):
    return f'<a class="download" href="{E(pathway + "/" + item["file"], quote=True)}" download>{E(label)} <small>({size(item["bytes"])})</small></a>'


def build():
    sections = []
    bindings = {}
    for pathway in ('BUILD', 'GROW'):
        directory = PACKS / pathway
        source = json.loads((directory / 'SOURCE_MANIFEST.json').read_text())
        archives = json.loads((directory / 'DOWNLOAD_INDEX.json').read_text())['archives']
        guide = 'START_HERE.pdf' if (directory/'START_HERE.pdf').is_file() else next(directory.glob('*Teaching_Guide.pdf')).name
        assert len(source['lessons']) == 10
        whole = next(x for x in archives if len(x['lessonIds']) == 10)
        weeks = []
        for week in range(3, 8):
            lessons = [x for x in source['lessons'] if x['week'] == week]
            assert {x['id'] for x in lessons} == {f'W{week}A', f'W{week}B'}
            weekly = next(x for x in archives if set(x['lessonIds']) == {r['id'] for r in lessons})
            cards = []
            for lesson in lessons:
                bindings[lesson['source']['repoPath']] = f'Teaching_Packs/#{pathway.lower()}-week-{week}'
                archive = next(x for x in archives if x['lessonIds'] == [lesson['id']])
                files = sorted(lesson['files'], key=lambda x: ({'Teaching slides':0, 'Pupil materials':1, 'Teacher guidance and answers':2, 'Experiment recording':3}.get(x['role'],4), x['format'] != 'PPTX', x['format']))
                file_links = ''.join('<li>' + link(pathway, f, f['role'] + ' · ' + f['format']) + '</li>' for f in files)
                cards.append(f'''<article class="lesson" id="{pathway.lower()}-{lesson['id'].lower()}"><p class="eyebrow">Lesson {E(lesson['part'])} · 40 minutes</p><h4>{E(lesson['title'])}</h4><p><a href="{E(lesson['htmlUrl'],quote=True)}">Open the matching classroom lesson →</a></p><ul class="files">{file_links}</ul><p>{link(pathway, archive, 'All files for this lesson · ZIP')}</p></article>''')
            weeks.append(f'''<details class="week" id="{pathway.lower()}-week-{week}" open><summary>Week {week} <span>Two lessons</span></summary><p>{link(pathway, weekly, f'Week {week} pack · ZIP')}</p><div class="lesson-grid">{''.join(cards)}</div></details>''')
        sections.append(f'''<section class="pathway {pathway.lower()}" id="{pathway.lower()}"><p class="eyebrow">Autumn 1 · Weeks 3–7</p><h2>{pathway} Science</h2><p>Ten 40-minute lessons. Edit the PowerPoints and Word resources, or use the ready-to-print PDFs.</p><div class="pack-actions">{link(pathway, whole, 'Download all ten lessons · ZIP')}<a class="download" href="{pathway}/{guide}">Read the pack guide · PDF</a></div><nav class="week-links" aria-label="{pathway} weeks">{''.join(f'<a href="#{pathway.lower()}-week-{w}">Week {w}</a>' for w in range(3,8))}</nav>{''.join(weeks)}</section>''')
    output = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BUILD and GROW Science teaching downloads — Made by Matt</title><meta name="description" content="Download editable BUILD and GROW Science PowerPoints, pupil resources and teacher guides for Autumn 1 Weeks 3–7."><link rel="stylesheet" href="packs.css"><link rel="stylesheet" href="../../assets/mbm-platform.css"><script>try{var t=localStorage.getItem('mbm_reading_theme');if(t&&t!=='cream')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script></head><body data-mbm-audience="teachers"><a class="skip" href="#main">Skip to teaching downloads</a><main id="main"><nav aria-label="Breadcrumb"><a href="/">Learning home</a> / <a href="../">Science by term</a></nav><header class="hero"><p class="eyebrow">Ready for your classroom</p><h1>Science teaching packs</h1><p class="lead">Editable lessons, accessible pupil resources and clear teacher guidance for BUILD and GROW.</p><nav class="pack-actions" aria-label="Choose a pathway"><a class="download" href="#build">BUILD Science</a><a class="download" href="#grow">GROW Science</a><a class="download" href="../?pathway=LAUNCH">Browse LAUNCH Science</a></nav><p class="scope">These packs cover the ten taught lessons in Autumn 1 Weeks 3–7. Weeks 1–2 baseline assessment and Week 8 enrichment are separate. The existing classroom lessons and other teaching versions remain available.</p><p class="revision">Updated 6 September 2026 · Original Made by Matt teaching resources. BUILD draws on the current website sequence and the supplied Year 3 topic materials; publisher slides and worksheets are not redistributed.</p></header>''' + ''.join(sections) + '''</main><footer class="footer"><p>Made by Matt · Learn • Build • Explore</p><a href="../">Back to all Science lessons</a></footer><script defer src="../../assets/mbm-theme.js"></script><script>function showWeek(){var e=document.getElementById(location.hash.slice(1));if(e){var d=e.closest('details');if(d)d.open=true;}}addEventListener('hashchange',showWeek);showWeek();</script></body></html>'''
    (PACKS / 'index.html').write_text(output)
    (ROOT / 'assets/catalogue/science-download-bindings.json').write_text(json.dumps(bindings, indent=2) + '\n')
    print(f'Built 20 teaching download entries, bound to {len(bindings)} existing weekly routes.')


if __name__ == '__main__':
    build()
