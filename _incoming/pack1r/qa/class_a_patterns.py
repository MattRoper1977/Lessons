"""Pattern/function list ported from _passhumd5/scan_class_a.py; module never run or imported."""
import re
URLISH = re.compile(r'(https?://\S+|www\.\S+|\S+\.(?:html|pdf|docx|pptx|png|svg|mp4|csv|xlsx)\b|[\w./-]*/[\w./-]+)')
def spans(text):
    return [(m.start(), m.end()) for m in URLISH.finditer(text)]
def inside(pos, sp):
    return any(a <= pos < b for a, b in sp)

# house spellings that must be CAPITALISED (flag the lower-case form mid-sentence)
CAP = {'diwali':'Diwali','hanukkah':'Hanukkah','holocaust':'Holocaust','bible':'Bible',
       'gospel':'Gospel','humanist':'Humanist','humanism':'Humanism','hajj':'Hajj',
       'torah':'Torah','makkah':'Makkah'}
# house spellings that must be LOWER-CASE (flag the capitalised form mid-sentence)
LOW = {'Salah':'salah','Wudu':'wudu','Zakat':'zakat','Ihram':'ihram',
       'Gurdwara':'gurdwara','Langar':'langar'}
# always wrong, any case position
ALWAYS = [(re.compile(r'\bMecca\b'),'Makkah'), (re.compile(r'\bKaaba\b'),'Ka‘bah'),
          (re.compile(r"\bKa'bah\b"),'Ka‘bah'), (re.compile(r'\bQuran\b'),'Qur’an'),
          (re.compile(r'\bKoran\b'),'Qur’an'), (re.compile(r"\bQur'an\b"),'Qur’an'),
          (re.compile(r'\bbar mitzvah\b'),'Bar Mitzvah'), (re.compile(r'\bbat mitzvah\b'),'Bat Mitzvah'),
          (re.compile(r'\bRubert Adolphus 21\b'),'Rubert Adolphus 24')]

# a/an by SOUND
VOWEL_SOUND_INITIALISM = set('AEFHILMNORSX')      # letters read with a leading vowel sound
CONSONANT_SOUND_WORDS = ('one','once','uniform','union','unique','unit','united','universal',
                         'university','use','used','useful','usefulness','user','usual','usually',
                         'utility','european','ewe','ufo')
VOWEL_SOUND_WORDS = ('hour','honest','honestly','honour','honourable','heir','heirloom')

TEMPLATE = re.compile(r'(lorem ipsum|\bTODO\b|\bTBC\b|\bFIXME\b|\bplaceholder\b|\bundefined\b|'
                      r'\bNaN\b|review copy|\{\{[^}]+\}\}|<%[^%]*%>)', re.I)
PERSONAL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]{2,}|(?<!\d)(?:\+44|0)\d{9,10}(?!\d)|'
                      r'[A-Za-z]:\\Users\\|/home/[a-z]+/|/Users/[a-z]+/')

def article_wrong(art, word):
    w = word.lower().split('-')[0]   # D7: 'one-page' is judged on 'one'
    if w in CONSONANT_SOUND_WORDS: return art == 'an'
    if w in VOWEL_SOUND_WORDS:     return art == 'a'
    if word.isupper() and len(word) <= 5:            # initialism: judge by first letter's sound
        return (art == 'a') if word[0] in VOWEL_SOUND_INITIALISM else (art == 'an')
    starts_vowel = w[0] in 'aeiou'
    return (art == 'a' and starts_vowel) or (art == 'an' and not starts_vowel)

def findings_for(text):
    sp = spans(text); out = []
    for m in re.finditer(r'\bmeans:?\s+([A-Z])(\w*)', text):
        if inside(m.start(), sp): continue
        word = m.group(1) + m.group(2)
        if word in ('God','Allah','Jesus','Muhammad','Torah','Bible','Gospel','Qur','Makkah','Hajj',
                    'Diwali','Hanukkah','Humanist','Humanism','Holocaust','Guru','Britain','British',
                    'England','Christian','Christians','Muslim','Muslims','Jewish','Sikh','Hindu',
                    'Buddhist','Europe','European','Teesside','Middlesbrough','Jesus','Israel'):
            continue
        out.append(('broken-join-after-means', m.group(0),
                    m.group(0).replace(word, word[0].lower() + word[1:], 1)))
    for m in re.finditer(r'(?:(?<=^)|(?<=\s))(a|an|A|An)\s+([A-Za-z][\w-]*)', text):
        if inside(m.start(), sp): continue
        # D6: a bare capital 'A' is a LABEL here (option A, Evidence card A, 'Choose A or B'),
        # never the indefinite article. Only the lower-case forms are articles.
        # D6 (final): a bare capital 'A' in this corpus is always a LABEL -- option A,
        # Evidence card A, 'Choose A or B', 'item A and'. Checking it produced 576
        # false positives and zero true ones, so only the lower-case articles are judged.
        if m.group(1) in ('A', 'An'): continue
        if article_wrong(m.group(1).lower(), m.group(2)):
            right = 'an' if m.group(1).lower() == 'a' else 'a'
            if m.group(1)[0].isupper(): right = right.capitalize()
            out.append(('article-a-an', m.group(0), f'{right} {m.group(2)}'))
    for m in re.finditer(r'\.\.(?!\.)', text):
        if inside(m.start(), sp): continue
        seg = text[max(0, m.start()-4):m.end()+4]
        if '...' in text[max(0, m.start()-2):m.end()+2]: continue   # D8: an ellipsis is not a doubled stop
        out.append(('doubled-full-stop', seg, None))
    for rx, right in ALWAYS:
        for m in rx.finditer(text):
            if not inside(m.start(), sp): out.append(('house-spelling', m.group(0), right))
    for m in re.finditer(r'\b\w+\b', text):
        w = m.group(0)
        if inside(m.start(), sp): continue
        before = text[:m.start()].rstrip()
        mid = m.start() > 0 and before[-1:] not in ('', '.', '!', '?', ':', '“', '"') \
              and not re.search(r'(?:^|\s)[A-Z]$', before)   # D9: '... A Salah' is a labelled card title
        if not mid: continue
        if w.lower() in CAP and w[0].islower():
            out.append(('house-capitalisation', w, CAP[w.lower()]))
        elif w in LOW:
            out.append(('house-lowercase', w, LOW[w]))
    for m in TEMPLATE.finditer(text):
        if not inside(m.start(), sp): out.append(('template-residue', m.group(0), None))
    for m in PERSONAL.finditer(text):
        out.append(('personal-data-or-path', m.group(0), None))
    return out
