#!/usr/bin/env python3
"""RX3 P1b — reproducible patch for the Lumins Guardian tool-wheel on touch.

Usage: rx3_lumins_fix.py <in.html> <out.html> --variant {h2,h3,h4,final}
Every replacement must match exactly once or the script fails; nothing else in the file changes.
  h2    remove the pointer capture taken on pointerdown (hypothesis H2)
  h3    hold-menu state machine: lifting after the hold keeps the wheel open; a tap on a wedge selects it,
        a tap outside closes it; pointercancel keeps an open wheel open (hypothesis H3)
  h4    canvas touch-action: pinch-zoom (the browser stops claiming the one-finger drag as a scroll) (hypothesis H4)
  final h3 + h4
"""
import sys,argparse
ap=argparse.ArgumentParser();ap.add_argument('src');ap.add_argument('dst');ap.add_argument('--variant',required=True,choices=['h2','h3','h4','final'])
a=ap.parse_args();s=open(a.src,encoding='utf-8').read();n0=len(s)
def rep(old,new):
    global s
    c=s.count(old)
    if c!=1: sys.exit('expected exactly one match, found %d: %r'%(c,old[:80]))
    s=s.replace(old,new)
H2_OLD='pointerId=ev.pointerId;try{cv.setPointerCapture(ev.pointerId);}catch(e){}holdStart='
H2_NEW='pointerId=ev.pointerId;holdStart='
# --- H3: the state machine ---------------------------------------------------------------
UP_OLD='if(G.wheel){updateWheel(ev);var hot=G.wheel.hot,cell=G.wheel.cell;if(hot!==null){var sd=SKILLDEF[hot];if((G.skills[sd.id]|0)>0)useWorldTool(sd.id,cell.c,cell.r);else tip("None left");}closeToolWheel(true);holdStart=null;return;}'
UP_NEW='if(G.wheel){if(G.wheel.tap){holdStart=null;return;}updateWheel(ev);var hot=G.wheel.hot,cell=G.wheel.cell;if(hot!==null){var sd=SKILLDEF[hot];if((G.skills[sd.id]|0)>0)useWorldTool(sd.id,cell.c,cell.r);else tip("None left");closeToolWheel(true);}else{G.wheel.tap=true;G.preview=null;previewNote.classList.remove("show");tip("Tap a tool, or tap away to close");}holdStart=null;return;}'
DOWN_OLD='if(G.state!=="play"||G.mode==="edit")return;pointerId=ev.pointerId;'
DOWN_NEW='if(G.state!=="play"||G.mode==="edit")return;if(G.wheel&&G.wheel.tap){var wh=wheelHit(ev),wc=G.wheel.cell;if(wh!==null){var wsd=SKILLDEF[wh];if((G.skills[wsd.id]|0)>0)useWorldTool(wsd.id,wc.c,wc.r);else tip("None left");}closeToolWheel(true);holdStart=null;return;}pointerId=ev.pointerId;'
HIT_ANCHOR='function updateWheel(ev){'
HIT_NEW='function wheelHit(ev){if(!G.wheel)return null;var dx=ev.clientX-G.wheel.x,dy=ev.clientY-G.wheel.y,d=Math.hypot(dx,dy);if(d<=28||d>118)return null;var best=1e9,hot=null,pos=wheelPos();for(var i=0;i<pos.length;i++){var dd=Math.hypot(dx-pos[i][0],dy-pos[i][1]);if(dd<best){best=dd;hot=i;}}return hot;}\nfunction updateWheel(ev){'
MOVE_OLD='if(G.wheel)updateWheel(ev);else if(G.armed)'
MOVE_NEW='if(G.wheel){if(!G.wheel.tap)updateWheel(ev);}else if(G.armed)'
CANCEL_OLD='cv.addEventListener("pointercancel",function(){holdStart=null;closeToolWheel(true);});'
CANCEL_NEW='cv.addEventListener("pointercancel",function(){clearTimeout(holdTimer);holdRing.style.display="none";holdStart=null;if(G.wheel){G.wheel.tap=true;G.preview=null;previewNote.classList.remove("show");}else closeToolWheel(true);});'
# --- H4: the gesture stays with the game ---------------------------------------------------
H4_OLD='canvas#cv{border-color:rgba(91,217,255,.42);'
H4_NEW='canvas#cv{touch-action:pinch-zoom;border-color:rgba(91,217,255,.42);'
if a.variant=='h2': rep(H2_OLD,H2_NEW)
if a.variant in('h3','final'):
    rep(UP_OLD,UP_NEW);rep(DOWN_OLD,DOWN_NEW);rep(HIT_ANCHOR,HIT_NEW);rep(MOVE_OLD,MOVE_NEW);rep(CANCEL_OLD,CANCEL_NEW)
if a.variant in('h4','final'): rep(H4_OLD,H4_NEW)
open(a.dst,'w',encoding='utf-8').write(s)
print('variant',a.variant,'bytes',n0,'->',len(s),'delta',len(s)-n0)
