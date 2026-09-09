"""Exact, accessible SVG rendition of the shared 1000 x 560 scientific diagram spec."""
from html import escape
import re

def esc(v): return escape(str(v),quote=True)
def num(v): return f'{float(v):g}'
def render_svg(visual, uid='diagram'):
    uid=re.sub(r'[^A-Za-z0-9_-]','_',str(uid))
    w=visual.get('width',1000); h=visual.get('height',560)
    title=visual.get('title','Scientific diagram')
    desc=visual.get('description',title)
    items=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {num(w)} {num(h)}" width="{num(w)}" height="{num(h)}" role="img" aria-labelledby="{uid}-title {uid}-desc"><title id="{uid}-title">{esc(title)}</title><desc id="{uid}-desc">{esc(desc)}</desc><defs><marker id="{uid}-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0 0 L9 4.5 L0 9 Z" fill="#1F2937"/></marker></defs>']
    for ei,el in enumerate(visual.get('elements',[])):
        kind=el.get('type'); x=el.get('x',0); y=el.get('y',0)
        fill=el.get('fill','none'); stroke=el.get('stroke','none'); sw=el.get('strokeWidth',2)
        common=f'fill="{esc(fill)}" stroke="{esc(stroke)}" stroke-width="{num(sw)}"'
        if kind=='rect':
            items.append(f'<rect x="{num(x)}" y="{num(y)}" width="{num(el.get("w",0))}" height="{num(el.get("h",0))}" {common}/>')
        elif kind=='ellipse':
            ew=el.get('w',0); eh=el.get('h',0)
            items.append(f'<ellipse cx="{num(x+ew/2)}" cy="{num(y+eh/2)}" rx="{num(ew/2)}" ry="{num(eh/2)}" {common}/>')
        elif kind=='line':
            marker=''
            if el.get('arrow'):
                mid=f'{uid}-arrow-{ei}'
                items.append(f'<defs><marker id="{mid}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0 0 L9 4.5 L0 9 Z" fill="{esc(stroke)}"/></marker></defs>')
                marker=f' marker-end="url(#{mid})"'
            items.append(f'<line x1="{num(x)}" y1="{num(y)}" x2="{num(el.get("x2",x))}" y2="{num(el.get("y2",y))}" {common}{marker}/>')
        elif kind=='text':
            size=el.get('size',24); lines=str(el.get('text','')).split('\n'); align=el.get('align','left')
            anchor={'left':'start','center':'middle','right':'end'}.get(align,'start')
            tx=x+(el.get('w',0)/2 if align=='center' else el.get('w',0) if align=='right' else 0)
            # Coordinates represent the upper-left of a text box; SVG uses a baseline.
            ty=y+size
            spans=''.join(f'<tspan x="{num(tx)}" y="{num(ty+i*size*1.2)}">{esc(line)}</tspan>' for i,line in enumerate(lines))
            items.append(f'<text font-family="Segoe UI, Arial, sans-serif" font-size="{num(size)}" font-weight="{700 if el.get("bold") else 400}" text-anchor="{anchor}" fill="{esc(el.get("color","#1F2937"))}">{spans}</text>')
        else: raise ValueError(f'Unknown visual element: {kind}')
    items.append('</svg>')
    return ''.join(items)
