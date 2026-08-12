#!/usr/bin/env python3
"""Flesch-Kincaid Grade instrument for GSG-1.

PROSE SELECTOR (stated, and applied identically to live and pack):
  INCLUDE : text nodes inside <p>, <li>, and <div class="...task-box...">
  EXCLUDE : <script>, <style>, <svg>, <title>, <button>, <option>, <textarea>,
            all <h1>-<h6> headings, every HTML attribute value,
            any JSON/JS island, and any resulting sentence that is
            ALL-CAPS or shorter than 5 words (fragments make FK meaningless).
Unit: Flesch-Kincaid Grade Level (US grade), per file, per surface.
"""
import re, sys, json

VOWELS = "aeiouy"


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    n = len(re.findall(r"[aeiouy]{1,2}", w))
    return max(1, n)


def strip_islands(s):
    for tag in ("script", "style", "svg", "title", "textarea", "button", "option"):
        s = re.sub(r"<%s\b.*?</%s>" % (tag, tag), " ", s, flags=re.S | re.I)
    s = re.sub(r"<h[1-6]\b.*?</h[1-6]>", " ", s, flags=re.S | re.I)
    return s


def prose_blocks(s):
    """Return prose text from <p>, <li>, and task-box divs."""
    s = strip_islands(s)
    out = []
    for m in re.finditer(r"<(p|li)\b[^>]*>(.*?)</\1>", s, flags=re.S | re.I):
        out.append(m.group(2))
    for m in re.finditer(
        r'<div\b[^>]*class="[^"]*task-box[^"]*"[^>]*>(.*?)</div>', s, flags=re.S | re.I
    ):
        out.append(m.group(1))
    txt = " ".join(out)
    txt = re.sub(r"<[^>]+>", " ", txt)                     # drop nested tags+attrs
    txt = (txt.replace("&amp;", "&").replace("&nbsp;", " ")
              .replace("&mdash;", "-").replace("&rsquo;", "'")
              .replace("&lt;", "<").replace("&gt;", ">"))
    txt = re.sub(r"&[a-z]+;", " ", txt)
    txt = re.sub(r"[‘’]", "'", txt)
    txt = re.sub(r"[“”]", '"', txt)
    txt = re.sub(r"[–—·→]", " ", txt)
    txt = re.sub(r"[^\x00-\x7f]", " ", txt)                # emoji, glyph markers
    txt = re.sub(r"\s+", " ", txt)
    return txt


def fk(text):
    raw = re.split(r"(?<=[.!?])\s+", text)
    sents = []
    for s in raw:
        s = s.strip()
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", s)
        if len(words) < 5:
            continue
        letters = re.sub(r"[^A-Za-z]", "", s)
        if letters and letters.upper() == letters:         # ALL-CAPS fragment
            continue
        sents.append(words)
    if not sents:
        return None, 0, 0
    nw = sum(len(w) for w in sents)
    ns = len(sents)
    nsy = sum(syllables(w) for ws in sents for w in ws)
    grade = 0.39 * (nw / ns) + 11.8 * (nsy / nw) - 15.59
    return round(grade, 2), nw, ns


def surface(s, dtype):
    """Extract one slide by data-type and return its prose."""
    m = re.search(
        r'<section class="slide"[^>]*data-type="%s".*?</section>' % dtype, s, flags=re.S
    )
    return prose_blocks(m.group(0)) if m else ""


if __name__ == "__main__":
    rows = []
    for path in sys.argv[1:]:
        s = open(path, encoding="utf-8").read()
        name = path.split("/")[-1]
        whole = fk(prose_blocks(s))
        row = {"file": name, "whole": whole[0], "words": whole[1], "sents": whole[2]}
        for d in ("arrival", "exit"):
            t = surface(s, d)
            row[d] = fk(t)[0] if t else None
        rows.append(row)
    print(json.dumps(rows, indent=1))
