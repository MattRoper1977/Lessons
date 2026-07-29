"""
Shared readable-text extractor for the kit assertions. Standing rule 13.

WHY THIS EXISTS AND WHY IT IS NOT "STRIP THE SCRIPT TAGS".

Rule 13 as first stated says to exclude script blocks. Implemented literally that
would create a false negative larger than the one it fixes: in this estate most
pupil-facing prose lives INSIDE <script> -- _taBriefs, _pres fault cards, the
WEEKS array that builds every print pack, _wagollText. Excluding script blocks
would have hidden the TA brief that sets up an inking bench, which is the single
worst string in GROW W2.

So the rule is implemented as its intent rather than its letter:
  * <style> blocks are dropped entirely -- CSS is never read by a pupil, and
    "grid-template-columns" is where the phantom 16 `plate` hits came from.
  * inside <script>, only STRING LITERALS are kept -- '...', "...", `...`.
    Identifiers, keywords and property names are dropped. That keeps the prose
    and drops the code.
  * in markup, tags are removed and text kept; attribute VALUES are kept only for
    alt/title/aria-label, which a user can read. class/id/data-* are dropped.
  * HTML entities are decoded, so "&mdash;" does not become a word.
"""
import re, html

STYLE = re.compile(r'<style\b[^>]*>.*?</style>', re.S | re.I)
SCRIPT = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)
READABLE_ATTR = re.compile(r'\b(?:alt|title|aria-label)\s*=\s*"([^"]*)"', re.I)
STRINGS = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"|`((?:[^`\\]|\\.)*)`", re.S)
TAG = re.compile(r'<[^>]+>')


def readable(path):
    """Return only what a pupil or teacher can actually read, as one string."""
    raw = open(path, encoding='utf-8', errors='replace').read()
    raw = STYLE.sub(' ', raw)

    parts = []
    for m in SCRIPT.finditer(raw):
        for s in STRINGS.finditer(m.group(1)):
            lit = next(g for g in s.groups() if g is not None)
            # drop code-ish literals: selectors, CSS fragments, DOM constants,
            # camelCase identifiers. Keep anything that reads like prose.
            if re.search(r'[{};]', lit): continue
            if re.match(r'^[.#\[]', lit.strip()): continue
            if re.match(r'^[A-Z][A-Z0-9_]+$', lit.strip()): continue          # TEXTAREA
            if re.match(r"^[A-Za-z][A-Za-z0-9]*$", lit.strip()) and re.search(r'[a-z][A-Z]', lit):
                continue                                                       # progressBar
            if re.match(r'^[\w-]+:[\w#%.-]+$', lit.strip()): continue        # css decls
            t = lit.strip()
            # single hyphenated token with no space is a class/id, not prose
            if ' ' not in t and '-' in t and re.match(r'^[a-z0-9-]+$', t): continue
            # short all-lower single tokens are JSON data keys (maa, tkb, inh)
            if ' ' not in t and len(t) <= 4 and re.match(r'^[a-z]+[0-9]?$', t): continue
            parts.append(lit)
    markup = SCRIPT.sub(' ', raw)
    parts += READABLE_ATTR.findall(markup)
    parts.append(TAG.sub(' ', markup))

    text = html.unescape(' '.join(parts))
    text = text.replace('\\u2019', "'").replace('\\n', ' ').replace('\\', ' ')
    return re.sub(r'\s+', ' ', text)


WORD = re.compile(r"[a-z][a-z']{2,}")   # hyphens split; identifiers dissolve


def words(text):
    return WORD.findall(text.lower())
