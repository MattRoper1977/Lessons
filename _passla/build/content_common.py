# -*- coding: utf-8 -*-
"""Shared content helpers for the LAUNCH ASDAN short-course strands (Careers, Living
Independently, Vocational, Community & Enterprise). PEQ has its own module.

Short-course strands bank the ASDAN short course + AQA UAS. Per the claims census they
do NOT claim a PEQ unit as a per-lesson bank (that was GROW's drift); any PEQ skill
contribution is surfaced only at hub/tracker level, by Binder code."""

_POS = [(29,43,134),(36,107,120),(380,43,169),(387,107,155)]

def ilm(center_icon, center_label, four_labels, bottom, col):
    """Authored illuminator: labelled badges dock onto a central card.
    icon+label+colour, horizontal labels, no layout transforms (brief §5)."""
    cards=""
    for i,(x,y,w) in enumerate(_POS):
        cards += (f'<g class="pop" style="animation-delay:{0.3+i*0.7}s">'
                  f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{col}"/>'
                  f'<text x="{x+w/2}" y="{y+17}" text-anchor="middle" font-size="9.5" fill="#fff">{four_labels[i]}</text></g>')
    links=('<path class="draw" style="animation-delay:0.6s" d="M160 56 L208 70" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>'
           '<path class="draw" style="animation-delay:1.3s" d="M160 120 L208 118" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>'
           '<path class="draw" style="animation-delay:2.0s" d="M400 56 L352 70" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>'
           '<path class="draw" style="animation-delay:2.7s" d="M400 120 L352 118" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 560 190" aria-hidden="true">'
            f'<rect x="210" y="34" width="140" height="126" rx="14" fill="#fff" stroke="{col}" stroke-width="4"/>'
            f'<circle cx="280" cy="78" r="24" fill="{col}"/>'
            f'<text x="280" y="88" text-anchor="middle" font-size="20" fill="#fff">{center_icon}</text>'
            f'<text x="280" y="126" text-anchor="middle" font-size="11" fill="{col}">{center_label}</text>'
            f'{cards}{links}'
            f'<text x="280" y="184" text-anchor="middle" font-size="11" fill="{col}">{bottom}</text></svg>')

def make_base(strand_key, folder, prefix, product_line, tag_strand):
    """Return a _base(week, title_short, banks, **kw) factory bound to one strand."""
    subtitle = "LAUNCH Pathway · ASDAN Studio · " + product_line
    def _base(week, title_short, banks, **kw):
        safe = title_short.replace(' ','_').replace('&','and').replace('/','_').replace("'","")
        d = dict(
            strand_key=strand_key, folder=folder, week=week, weeks_total=6,
            filename=f"{prefix}_W{week}_{safe}.html",
            title_short=title_short,
            title_full=f"LAUNCH ASDAN · {product_line} W{week} · {title_short}",
            tag_lesson=f"ASDAN Studio · {tag_strand} · Week {week} of 6",
            subtitle=subtitle,
            sow_strip=f"Progress SoW · LAUNCH ASDAN Aut 1 · 2026–27 · {product_line} · Week {week}",
            banks=banks,
            witness={"header": f"LAUNCH ASDAN W{week} · {title_short}"},
        )
        d.update(kw)
        return d
    return _base
