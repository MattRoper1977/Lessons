#!/usr/bin/env python3
"""TL-2 Part B: publish Town Life. Exact-match edits, asserted counts, idempotent."""
import json, re, shutil, hashlib
from pathlib import Path

SCR   = Path("/tmp/claude-0/-home-user-Lessons/91716126-0bef-5b42-b826-d86d99576965/scratchpad")
SITE  = Path("/workspace/mattroper1977.github.io")
GAMES = Path("/workspace/games")

HREF  = "/townlife/"
TITLE = "NEW · Town Life"          # NEW marker ON (B2 default)
PLAIN = "Town Life"
HUE   = "#2FA8A4"
ART   = "/assets/cards/town-life.svg"
ICON  = "\U0001F3D8"                    # 🏘
TAG   = "Sandbox"                        # reuse existing vocabulary; no new mint
GENRE = "Sandbox & Creative"
FEELS = ["long-haul", "thinky"]
DESC  = ("A whole town to live in. Claim a plot, furnish a home and wire its electrical grid, buy and "
         "upgrade businesses, tune a car, and take any of seven roles — Resident, Courier, Paramedic, "
         "Officer, Builder, Mayor or Mischief. Day and night, weather, police patrols, a civic budget the "
         "town votes on, and a save that keeps everything between visits. One file, no install, offline.")

log = []
def note(x): log.append(x); print("  " + x)

# ---------------- 1. runtime placement: /townlife/index.html ----------------
dest = SITE / "townlife" / "index.html"
dest.parent.mkdir(parents=True, exist_ok=True)
src = SCR / "build" / "v102.html"
shutil.copyfile(src, dest)
rt_sha = hashlib.sha256(dest.read_bytes()).hexdigest()
note(f"placed {dest.relative_to(SITE)}  {dest.stat().st_size} B  sha256 {rt_sha[:16]}")
assert rt_sha == "3605124fda9387c71fc1a7c02091d1110f5d82363ec7788de4ea90757d6e38da"
note("placed bytes are byte-identical to the gated v1.0.2 runtime")

# ---------------- 2. card art ----------------
card = SITE / "assets" / "cards" / "town-life.svg"
card.write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" width="640" height="360" role="img" aria-label="Town Life">
<rect width="640" height="360" fill="#101827"/>
<rect x="0" y="0" width="10" height="360" fill="{HUE}"/>
<g opacity=".38" fill="none" stroke="{HUE}" stroke-width="3">
<rect x="392" y="196" width="66" height="104" rx="4"/>
<rect x="470" y="152" width="78" height="148" rx="4"/>
<rect x="560" y="222" width="56" height="78" rx="4"/>
<path d="M392 196 l33 -30 l33 30"/><path d="M470 152 l39 -34 l39 34"/><path d="M560 222 l28 -26 l28 26"/>
</g>
<g opacity=".55" stroke="#ffc857" stroke-width="2.5" stroke-linecap="round">
<path d="M46 300 h548"/><path d="M120 300 v-14"/><path d="M300 300 v-14"/><path d="M480 300 v-14"/>
</g>
<text x="46" y="52" font-family="Poppins,Segoe UI,sans-serif" font-size="13" font-weight="800" letter-spacing="3.2" fill="#9E9CA8">MADE BY MATT</text>
<text font-family="Poppins,Segoe UI,sans-serif" font-size="46" font-weight="800" fill="#F6F1E4"><tspan x="46" y="186.0">Town Life</tspan></text>
<text x="46" y="224" font-family="Poppins,Segoe UI,sans-serif" font-size="15" font-weight="600" fill="#64d8d4">Seven roles · one town</text>
</svg>
""", encoding="utf-8")
note(f"wrote {card.relative_to(SITE)}  {card.stat().st_size} B")

# ---------------- 3. games.json: canonical (Games repo) then site mirror ----------------
entry = {"icon": ICON, "title": TITLE, "desc": DESC, "href": HREF,
         "tag": TAG, "hue": HUE, "featured": False, "hero": False, "art": ART}

for label, p in (("canonical (Games repo)", GAMES / "games.json"),
                 ("site mirror", SITE / "data" / "source-manifests" / "games.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    if any(g.get("href") == HREF for g in d["games"]):
        note(f"{label}: entry already present — skip"); continue
    before = len(d["games"])
    d["games"].insert(0, entry)          # newest first, as Emberwild sits first
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    heroes = [g["title"] for g in d["games"] if g.get("hero") is True]
    note(f"{label}: {before} -> {len(d['games'])} entries; heroes={len(heroes)} ({heroes[0] if heroes else '-'})")
    assert len(heroes) == 1

# ---------------- 4. TAXONOMY in games/index.html (genre + feels; no CURATION entry) ----------------
gi = SITE / "games" / "index.html"
t = gi.read_text(encoding="utf-8")
if f'href:"{HREF}"' in t:
    note("games/index.html: TAXONOMY entry already present — skip")
else:
    # scope strictly to the TAXONOMY array — '{href:"/voxel/",' also occurs in CURATION
    tm = re.search(r"var TAXONOMY\s*=\s*\[", t)
    ti = t.index("[", tm.end() - 1); d2 = 0
    for tj in range(ti, len(t)):
        if t[tj] == "[": d2 += 1
        elif t[tj] == "]":
            d2 -= 1
            if d2 == 0: break
    tax = t[ti:tj + 1]
    anchor = '{href:"/voxel/",'
    assert tax.count(anchor) == 1, ("anchor count inside TAXONOMY", tax.count(anchor))
    line = ('{href:"%s",%sgenre:"%s",feels:["%s","%s"]},\n  ' % (HREF, " " * 39, GENRE, FEELS[0], FEELS[1]))
    newtax = tax.replace(anchor, line + anchor, 1)
    t = t[:ti] + newtax + t[tj + 1:]
    gi.write_text(t, encoding="utf-8")
    note("games/index.html: TAXONOMY entry added (genre + feels only; no CURATION entry, so no take and not in TOP)")

# assert no curation entry for townlife
t = gi.read_text(encoding="utf-8")
cur = re.search(r"var CURATION\s*=\s*\[", t)
i = t.index("[", cur.end() - 1); depth = 0
for j in range(i, len(t)):
    if t[j] == "[": depth += 1
    elif t[j] == "]":
        depth -= 1
        if depth == 0: break
assert HREF not in t[i:j + 1], "townlife must NOT be in CURATION"
note("verified: /townlife/ absent from CURATION — no take, not in TOP (B2)")

# ---------------- 5. /for/pupils/ : STATIC page, so an explicit edit is required ----------------
pp = SITE / "for" / "pupils" / "index.html"
t = pp.read_text(encoding="utf-8")
if HREF in t:
    note("for/pupils: already present — skip")
else:
    sand = '<span class="mf-pupil-gname">Sandbox &amp; Creative</span><span class="mf-pupil-gnum">4 games</span>'
    assert t.count(sand) == 1, t.count(sand)
    t = t.replace(sand, sand.replace("4 games", "5 games"), 1)

    # insert the card as the last article of the Sandbox grid
    start = t.index('<span class="mf-pupil-gname">Sandbox &amp; Creative</span>')
    end = t.index("</div></details>", start)
    art_html = (
        f'<article class="mf-pupil-game"><a class="mf-media" href="{HREF}" aria-label="Play {PLAIN}">'
        f'<img data-mbm-real-visual src="{ART}" alt="{PLAIN} — a moment from play" width="640" height="360" '
        f'loading="lazy" decoding="async"></a><div class="mf-feature-copy"><h3>{PLAIN}</h3><p>{DESC}</p>'
        f'<a class="mf-text-link" href="{HREF}">Play {PLAIN}<span aria-hidden="true">→</span></a></div></article>'
    )
    t = t[:end] + art_html + t[end:]

    tot = 'All 52 games, grouped by what they are.'
    assert t.count(tot) == 1
    t = t.replace(tot, 'All 53 games, grouped by what they are.', 1)
    pp.write_text(t, encoding="utf-8")
    note("for/pupils: card inserted into Sandbox & Creative; group count 4->5; total 52->53")
    note("NOTE: this page is STATIC — it does NOT render from the genre record, contrary to B3/B4")

# ---------------- 6. post-state ----------------
pt = pp.read_text(encoding="utf-8")
arts = re.findall(r'<article class="mf-pupil-game">(.*?)</article>', pt, re.S)
hrefs = [re.search(r'<a class="mf-media" href="([^"]+)"', a).group(1) for a in arts]
from collections import Counter
c = Counter(hrefs)
twice = sorted(h for h, n in c.items() if n == 2)
gj = json.loads((GAMES / "games.json").read_text(encoding="utf-8"))
site_ = [g for g in gj["games"] if not g["href"].startswith("/Lessons/")]
less_ = [g for g in gj["games"] if g["href"].startswith("/Lessons/")]
print(json.dumps({
    "manifestEntries": len(gj["games"]),
    "siteServed": len(site_), "lessonsHosted": len(less_),
    "pupilCards": len(arts), "pupilDistinct": len(set(hrefs)),
    "paintedTwice": len(twice), "maxPaints": max(c.values()),
    "twiceSet": twice,
    "titlesWithNEW": [g["title"] for g in gj["games"] if "NEW" in g["title"]],
}, indent=1))
