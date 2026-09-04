"""Award-only print presentation, generated wholly from the authored spec."""
from html import escape
from lxml import html as lh


def rebuild_print(tree, plan, content, trace):
    pk = content.get('print', {})
    title = escape(content['title'])
    heading = escape(f"{plan['family']} · Week {plan['ruledWeek']} · {content.get('slot', '')}")
    rows = ''.join('<tr><th scope="row">' + escape(row) + '</th><td class="award-response"></td>'
                   '<td class="award-locator"></td></tr>' for row in pk.get('focusRows', []))
    tiers = ''.join('<div class="print-route"><h3>' + escape(label) + '</h3><p>' + escape(text)
                    + '</p></div>' for label,text in zip(content.get('tierLadder', []), pk.get('tiers', [])))
    checks = ''.join('<li>' + escape(item) + '</li>' for item in pk.get('checks', []))
    figures = ''.join(pk.get('figures', []))
    sequence = ' · '.join(escape(section) for section in pk.get('sections', []))
    html = f'''<section class="print-pack printpack award-print" aria-label="Printable lesson pack">
      <section class="print-page">
        <div class="running-head">{heading}</div><h1>{title}</h1>
        <p><b>Award evidence:</b> {escape(trace)}</p>
        <p><b>Objective:</b> {escape(content['objective'])}</p>
        <h2>My evidence record</h2><p>{escape(pk.get('intro',''))}</p><p>{sequence}</p>
        <table><thead><tr><th>Evidence focus</th><th>My words or response</th><th>File and page, slide or time</th></tr></thead>
        <tbody>{rows}</tbody></table>
        <div class="award-print-figures">{figures}</div>
        <p>Name or learner code: ____________________ Date: ____________________</p>
      </section>
      <section class="print-page">
        <div class="running-head">{heading}</div><h1>{title}</h1>
        <h2>Choose the support you need</h2>{tiers}
        <h2>Check the evidence</h2><ol>{checks}</ol>
        <h2>My review or next step</h2><div class="award-review-space"></div>
        <p>For a recorded response, write the actual file name and page, slide or timecode.</p>
      </section>
    </section>'''
    packs = tree.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]')
    new = lh.fragment_fromstring(html)
    if packs:
        packs[0].addprevious(new)
        for pack in packs:
            pack.getparent().remove(pack)
    else:
        tree.xpath('//body')[0].append(new)
    style=lh.Element('style',id='award-print-layout')
    style.text='''
      @media screen {
        [data-mbm-guide]{display:none!important}
        #taOverlay [data-mbm-guide]{display:block!important}
        #taOverlay .overlay-card{max-height:calc(100vh - 36px);overflow:auto;width:min(700px,100%)}
        body.calm .slide{box-shadow:none}
        body.calm *,body.calm *::before,body.calm *::after{animation:none!important;transition:none!important}
        body.teacher-freeze *,body.teacher-freeze *::before,body.teacher-freeze *::after{animation-play-state:paused!important;transition:none!important}
      }
      @media print {
        .award-print .print-page{box-sizing:border-box;padding:4mm;min-height:0}
        .award-print table{width:100%;border-collapse:collapse;table-layout:fixed}
        .award-print th,.award-print td{border:1px solid #777;padding:2mm;vertical-align:top;font-size:9pt}
        .award-print th:first-child{width:34%}.award-print th:last-child{width:23%}
        .award-print td.award-response{height:18mm}
        .award-print-figures svg{display:block;width:100%;max-height:34mm;margin:2mm 0}
        .award-print .print-route{padding:2mm;margin:2mm 0}
        .award-print h3{font-size:11pt;margin:0}
        .award-print .award-review-space{height:35mm;border:1px solid #777}
      }
    '''
    tree.xpath('//head')[0].append(style)


def replace_runtime(tree, content, runtime):
    """Only new award decks receive this runtime; legacy decks stay reproducible."""
    titles = tree.xpath('//head/title')
    title = titles[0] if titles else lh.Element('title')
    if not titles:
        tree.xpath('//head')[0].append(title)
    title.text = content['title']
    for node in tree.xpath('//script|//style|//button'):
        legacy_guide = node.get('id') in ('n6m-guide-js', 'n6m-guide-css')
        legacy_runtime = node.tag == 'script' and 'querySelectorAll("main.deck>.slide")' in (node.text or '')
        if legacy_guide or legacy_runtime or node.get('data-n6m-guide-control') or 'n6m-guide-btn' in (node.get('class') or '').split():
            node.getparent().remove(node)
    for node in tree.xpath('//comment()'):
        if 'n6m-guide' in (node.text or ''):
            node.getparent().remove(node)
    script = lh.Element('script', {'data-award-chassis': ''})
    script.text = runtime
    tree.xpath('//body')[0].append(script)
