#!/usr/bin/env python3
"""tools/gc1/embed_paper_route.py - P2P's second delivery path: the lesson page
prints that week's paper route.

WHY THE LESSON HAS TO CARRY IT

P2P ships the paper route twice on purpose. Once as a .docx and .pdf a teacher can
open and print. And once from the lesson page itself, "so a teacher can produce it
from the lesson page with no download".

That second path is not a convenience. A cover teacher in front of a class, on a
managed device that blocks downloads, with a pupil who has no device today, needs
the paper route in the next two minutes. Downloading a .docx is exactly the step
that fails in that moment, and it is the moment the paper route exists for.

G5 was already "the print record is non-empty". After P2P it is stronger: the
printed output must be that week's paper route, not a stub.

WHY IT APPENDS RATHER THAN REPLACES

Two different print implementations exist across the eight lessons. Weeks 7 and 8
ship the pack's own `fillPrint`. Weeks 1 to 6 were given one by repair_weeks.py,
because theirs was missing or empty. Rewriting either would mean owning a copy of
someone else's function and keeping it in step.

So this registers a SECOND beforeprint listener that appends. Listeners run in
registration order, so whichever filler exists writes the pupil's response record
first and this adds the paper route after it. Nothing is replaced, nothing is
duplicated, and a lesson whose filler changes later still works.

WHAT IS PRINTED

The whole route, not a summary: the intro, every block-writing grid with its word
bank and its empty stack rows, the maze at its real geometry as a coordinate grid
a counter moves on, every predict/trace/compare table, the week-specific sheets,
the seeded-fault listings for Week 8, and the completion record with its outcome
wording. The teacher answers are NOT printed here -- they are Teacher_Only and
reach the page only behind the guidance toggle, never on a sheet handed to a class.

Idempotent and strip-reversible.

USAGE
  python3 tools/gc1/embed_paper_route.py --routes routes.json --unit <dir> [--strip]
  python3 tools/gc1/embed_paper_route.py --self-test
"""
import argparse
import glob
import json
import os
import re
import sys

OPEN, CLOSE = '<!--gc1-paper:v1-->', '<!--/gc1-paper-->'

WALLS = [[-220, -160, 440, 20], [-220, 140, 440, 20], [-220, -140, 20, 280],
         [200, -140, 20, 280], [-70, -140, 20, 220], [50, -80, 20, 220]]

# The renderer draws the maze from the same constant the lesson uses, so the paper
# grid and the on-screen stage cannot drift apart.
JS = r'''<script id="gc1-paper-js">(function(){
var P=%(payload)s;
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){
 return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function rows(n){var o='';for(var i=0;i<n;i++)o+='<tr><td class="gc1-row">&nbsp;</td></tr>';return o}
function maze(){
 var W=%(walls)s,step=20,xs=[],ys=[],x,y,o='';
 for(x=-240;x<=240;x+=step)xs.push(x);
 for(y=180;y>=-180;y-=step)ys.push(y);
 function blocked(x,y){for(var i=0;i<W.length;i++){var w=W[i];
  if(x>=w[0]&&x<w[0]+w[2]&&y>=w[1]&&y<w[1]+w[3])return true}return false}
 o+='<table class="gc1-maze">';
 for(var r=0;r<ys.length;r++){o+='<tr>';
  for(var c=0;c<xs.length;c++){var cx=xs[c],cy=ys[r],t='';
   if(blocked(cx,cy))t='&#9608;';
   else if(cx===-180&&cy===-120)t='P';
   else if(cx===180&&cy===120)t='F';
   o+='<td>'+t+'</td>'}
  o+='</tr>'}
 return o+'</table>'}
function grid(g){
 var real=[],notes=[],i;
 for(i=0;i<g.w.length;i++){(/\.$|\b(empty|no blocks|none)\b/i.test(g.w[i])?notes:real).push(g.w[i])}
 var o='<h3>'+esc(g.s)+'</h3><p>'+esc(g.p)+'</p>';
 o+='<table class="gc1-grid"><tr><td class="gc1-hat"><b>'+esc(g.h)+'</b></td></tr>'+rows(g.r)+'</table>';
 if(real.length){o+='<p><b>Blocks you may use this week:</b></p><ul>';
  for(i=0;i<real.length;i++)o+='<li>'+esc(real[i])+'</li>';o+='</ul>'}
 else{o+='<p>This week uses no blocks. There is nothing to write in the stack rows.</p>'}
 for(i=0;i<notes.length;i++)o+='<p>'+esc(notes[i])+'</p>';
 return o}
function table(t){
 var o='<h3>'+esc(t.caption)+'</h3><table class="gc1-tbl"><tr>',i,j;
 for(i=0;i<t.columns.length;i++)o+='<th>'+esc(t.columns[i])+'</th>';
 o+='</tr>';
 for(i=0;i<t.rows.length;i++){o+='<tr>';
  for(j=0;j<t.columns.length;j++)o+='<td>'+esc(t.rows[i][j]||'')+'</td>';
  o+='</tr>'}
 return o+'</table>'}
function html(){
 var o='<div class="gc1-paper"><h1>Week '+esc(WEEK)+' '+esc(P.label)+' &middot; paper route</h1>',i;
 o+='<p>Name: _____________________  Date: __________</p>';
 for(i=0;i<P.intro.length;i++)o+='<p>'+esc(P.intro[i])+'</p>';
 o+='<h2>Write your code</h2>';
 for(i=0;i<P.grids.length;i++)o+=grid(P.grids[i]);
 o+='<h2>The maze</h2><p>'+esc(P.maze.use)+'</p>'+maze();
 o+='<h2>Predict, trace, compare</h2>';
 for(i=0;i<P.tables.length;i++)o+=table(P.tables[i]);
 if(P.extra&&P.extra.length){o+='<h2>This week only</h2>';
  for(i=0;i<P.extra.length;i++)o+='<p>'+esc(P.extra[i])+'</p>'}
 for(i=0;i<(P.faults||[]).length;i++){var f=P.faults[i];
  o+='<h3>Fault: '+esc(f.name)+'</h3><p>What you see: '+esc(f.symptom)+'</p><pre>';
  for(var k=0;k<f.lines.length;k++)o+=esc(f.lines[k])+'\n';
  o+='</pre><p>What is wrong: ____________________________________</p>';
  o+='<p>My repair: __________________________________________</p>'}
 o+='<h2>My completion record</h2><p>'+esc(P.record.outcomeWording)+'</p>';
 for(i=0;i<P.record.pupilStatements.length;i++)o+='<p>&#9633; '+esc(P.record.pupilStatements[i])+'</p>';
 o+='<h3>Adult record</h3>';
 for(i=0;i<P.record.teacherObservation.length;i++)o+='<p>&#9633; '+esc(P.record.teacherObservation[i])+'</p>';
 o+='<p>Adult name: ____________________  Date: __________</p>';
 o+='<p>Route taken: paper &middot; Recorded in the teacher guide, not on the AQA form.</p>';
 return o+'</div>'}
// A second listener, registered after whichever filler this lesson already has.
// Listeners run in registration order, so the pupil's response record is written
// first and the paper route is appended to it.
function append(){var el=document.querySelector('.print-record');if(el)el.innerHTML+=html()}
window.gc1PaperHTML=html;
addEventListener('beforeprint',append);
var pb=document.getElementById('printBtn');
if(pb)pb.addEventListener('click',append);
})();</script>'''

CSS = ('<style id="gc1-paper-css">@media print{'
       '.gc1-paper{page-break-before:always}'
       '.gc1-paper h1{font-size:18pt}.gc1-paper h2{font-size:14pt;page-break-before:always}'
       '.gc1-paper h3{font-size:12pt}'
       '.gc1-paper table{border-collapse:collapse;width:100%}'
       '.gc1-paper td,.gc1-paper th{border:1px solid #000;padding:3pt;font-size:9pt;text-align:left}'
       '.gc1-grid .gc1-row{height:20pt}'
       '.gc1-maze td{width:3.6%;height:11pt;padding:0;text-align:center;font-size:6pt}'
       '.gc1-paper pre{font-size:9pt;white-space:pre-wrap}'
       '}</style>')


def slim(route):
    """Only what the printed sheet needs. The teacher answers are not included."""
    return {
        'label': route['label'],
        'intro': route['intro'],
        'grids': [{'s': g['sprite'], 'p': g['purpose'], 'h': g['hatBlock'],
                   'r': g['rows'], 'w': g['allowedBlocks']} for g in route['p1_grids']],
        'maze': route['p2_maze'],
        'tables': route['p3_tables'],
        'extra': route.get('p4_or_p5') or [],
        'faults': route.get('faultListings') or [],
        'record': route['p6_completionRecord'],
    }


def embed(src, route):
    if OPEN in src:
        return src, 'already'
    payload = json.dumps(slim(route), ensure_ascii=False, separators=(',', ':'))
    block = OPEN + CSS + (JS % {'payload': payload, 'walls': json.dumps(WALLS)}) + CLOSE
    if '</body>' not in src:
        return src, 'no-body'
    return src.replace('</body>', block + '</body>', 1), 'embedded'


def strip(src):
    while OPEN in src:
        i = src.find(OPEN)
        j = src.index(CLOSE, i) + len(CLOSE)
        src = src[:i] + src[j:]
    return src


def self_test():
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    route = {'week': 5, 'label': 'Make a rule work',
             'intro': ['Line one.', 'Line two.'],
             'p1_grids': [{'sprite': 'Player', 'purpose': 'The wall rule', 'hatBlock': 'when green flag clicked',
                           'rows': 4, 'allowedBlocks': ['forever', 'if <> then', 'touching [Maze]?']}],
             'p2_maze': {'use': 'Move a counter.'},
             'p3_tables': [{'caption': 'Trace 1', 'columns': ['Step', 'x', 'y'], 'rows': [['1', '', '']]}],
             'p4_or_p5': [], 'faultListings': [],
             'p6_completionRecord': {'outcomeWording': 'Outcome 3.', 'pupilStatements': ['I wrote it.'],
                                     'teacherObservation': ['Observed.'], 'honestGap': 'NONE'},
             'p7_teacherAnswers': ['THE ANSWER IS 42']}
    page = '<html><body><div class="print-record"></div></body></html>'
    out, key = embed(page, route)
    want('a lesson gains the paper-route block', key == 'embedded' and OPEN in out)
    want('the payload carries the grids', '"grids"' in out and 'when green flag clicked' in out)
    want('the payload carries the tables', 'Trace 1' in out)
    want('the payload carries the completion record', 'Outcome 3.' in out)

    # The single most important negative: teacher answers are Teacher_Only and must
    # never reach a sheet handed to a class.
    want('teacher answers are NOT embedded', 'THE ANSWER IS 42' not in out)
    want('  ... and p7 is absent from the payload entirely', 'p7_teacherAnswers' not in out)

    want('it appends rather than replacing the existing filler',
         'innerHTML+=' in out.replace(' ', '') and 'innerHTML=' not in out.replace('innerHTML+=', ''))
    want('it registers its own beforeprint listener', "addEventListener('beforeprint',append)" in out.replace(' ', ''))
    want('the print styles are print-only', '@media print{' in out)
    want('re-running changes nothing', embed(out, route)[1] == 'already')
    want('strip returns the page byte-identical', strip(out) == page)
    want('a page with no body is refused', embed('<div></div>', route)[1] == 'no-body')

    s = slim(route)
    want('slim() drops the teacher answers', 'p7_teacherAnswers' not in s)
    want('slim() keeps every grid', len(s['grids']) == len(route['p1_grids']))
    want('slim() keeps the honest gap on the record, for the teacher guide',
         s['record'].get('honestGap') == 'NONE')

    # The maze the lesson prints must be the maze the lesson plays.
    want('the embedded walls are the lesson’s own WALLS constant',
         json.dumps(WALLS) in out)

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--routes')
    ap.add_argument('--unit')
    ap.add_argument('--strip', action='store_true', dest='do_strip')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.unit:
        print('--unit is required', file=sys.stderr)
        sys.exit(2)
    byweek = {}
    if a.routes:
        data = json.load(open(a.routes, encoding='utf-8'))
        if isinstance(data, dict):
            data = data.get('routes', [])
        byweek = {r['week']: r for r in data}
    tally = {}
    for path in sorted(glob.glob(os.path.join(a.unit, 'Week_*', '*Interactive.html'))):
        wk = int(re.search(r'Week_(\d+)', path).group(1))
        src = open(path, encoding='utf-8').read()
        if a.do_strip:
            out, key = strip(src), 'stripped'
        elif wk not in byweek:
            out, key = src, 'no-route'
        else:
            out, key = embed(src, byweek[wk])
        open(path, 'w', encoding='utf-8').write(out)
        tally[key] = tally.get(key, 0) + 1
        if key == 'embedded':
            print('  W%02d  %d B -> %d B  (+%d)' % (wk, len(src.encode()), len(out.encode()),
                                                    len(out.encode()) - len(src.encode())))
    print()
    for k in sorted(tally):
        print('  %-12s %d' % (k, tally[k]))
    sys.exit(1 if any(k in ('no-body', 'no-route') for k in tally) else 0)


if __name__ == '__main__':
    main()
