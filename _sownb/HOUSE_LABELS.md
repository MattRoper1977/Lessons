# House labels

The house-vocabulary register for the g10 name gate, built 2026-09-02 (ORDER
VB-RUN12A, HOUSE_LABELS ruling) the same way as `_sownb/PLACES.md`: by grep of
the live lesson corpus (399 decks, pupil-facing text with scripts, styles, SVG
and keyed staff guidance removed) and of every workbook cell on the 2026-27
spine, using the pair regex the gate itself uses. 5,194 distinct capitalised
pairs were measured across 28,006 occurrences; the ones below are the estate's
own furniture, not people.

A capitalised pair whose words include any word listed here is a HOUSE-LABEL.
As with PLACES, every word of every bullet becomes a token, and **a pair that
resolves to HOUSE_LABELS or PLACES never holds a lesson** — the register is
estate-wide, and no deck is ever named in it.

Why the pairs arise at all: a heading, a tier name or a button label sits next
to the first word of the sentence after it, so the gate sees "Starter Today",
"Reset Make", "Glance Key". Those are two pieces of furniture touching, never a
first name and a surname.

## Tier names

- Supported
- Standard
- Stretch
- Entry
- Secure
- Reach
- Access
- Scaffold
- Scaffolding

## Slide-role and stage names

- Arrival Task
- Starter
- Independent Work
- Exit Ticket
- Knowledge Organiser
- Key Facts
- Key Word
- Key Idea
- Key Question
- Success Criteria
- Big Idea
- Retrieval Quiz
- Reference Zone
- Studio Time
- Glance
- Model
- Evidence
- Misconception
- Complete
- Witness
- Assessor
- Feedback Sheet
- Signature
- Date
- Role
- Task
- Work
- Ticket
- Organiser
- Facts
- Quiz

## Control-bar and print furniture

- Reveal Answers
- Cold Call
- Teacher Print Tools
- Previous
- Next
- Reset
- Resume
- Pause
- Start
- Print
- Pack
- Long Answer
- Multiple Choice
- Short Answer
- What Went Well
- Even Better If
- Freeze

## Loop names

- Lundy Loop
- Learning Loop
- Live Loop
- Evidence Loop
- Stable Space
- Space
- Voice
- Audience
- Influence
- Loop
- Wall

## Pathway and programme names

- Build
- Grow
- Launch
- Progress
- Community Project
- Living Independently
- Independent Living
- Personal Effectiveness
- Vocational
- Enrichment Award
- Trinity Arts Award
- Creative Arts
- Young Duke
- Junior Duke
- Combined Science
- White Rose

## Award levels and assessment furniture

Measured in the corpus as capitalised pairs the gate flagged ("Silver Art",
"Bronze Art", "Explore Art", "Teaching Rehearsal", "Candidate Needs"). These
are programme levels and assessment furniture, both classes the ruling names.

- Bronze
- Silver
- Gold
- Platinum
- Explore
- Discover
- Candidate
- Rehearsal
- Observable
- Criteria
- Portfolio
- Moderation
- Assessment
- Curriculum

## Event names

- Bonfire Night
- Black History Month
- Remembrance Day
- Remembrance
- Holocaust Memorial Day
- Safer Internet Day
- International Literacy Day
- World Book Day
- Science Week
- Carers Week
- Anti Bullying Week
- Diwali
- Christmas
- Easter
- Ramadan
- Eid
- Hanukkah

## Named by the ruling, not found in the corpus

Two bullets above are here because the RUN12-A ruling names them, not because
the grep found them. Measured on the tree at the time of writing, excluding
`.git` and `node_modules`:

| token | occurrences in the repository | live decks containing it |
|---|---|---|
| Learning Loop | 1 (this file) | 0 |
| Bonfire Night | 6 (all in `_sownb` prose) | 0 |

The estate's actual loop vocabulary is **Lundy Loop** (443 occurrences across
189 files), **Live Loop** (280 files, in the control bar and so outside
`main.deck`, which is why it produces no gate red today), **Live Lundy** (53
decks — the single largest unresolved pair in the estate) and **Art Lundy** (17
decks). Those resolve through this register already: every word of every bullet
is a token, so "Lundy" and "Loop" come from the "Lundy Loop" and "Live Loop"
bullets and carry the rest.

Registering an absent token resolves nothing and costs nothing, so both stay as
the ruling wrote them. They are listed here so no reader takes this file to be
wholly grep-derived when two of its bullets are not.

## Deliberately NOT registered

These were measured in the corpus and left out on purpose, because every word
of every bullet becomes a token and these words double as personal names or
would mask one:

- "Grace", "Mark", "May", "Will", "Art", "Sam", "Rose" — each occurs in house
  phrases ("White Rose", "Art Award") but each is also a given name. "White
  Rose" and "Creative Arts" are registered as whole phrases above; the bare
  words are not.
  Subject terminology such as "Carbon Dioxide", "Natural Selection", "Active
  Transport" is NOT house vocabulary and is not registered. It is measured
  residue: the RUN12-A ruling names tier, slide-role, loop, pathway and event
  vocabulary, and this register covers exactly those. A pair of subject terms
  still reads as UNRESOLVED to the gate, and the residue is reported per deck
  rather than silently resolved here. A ruling on subject terminology would be
  a separate register, not an extension of this one.

  (Written without a leading bullet on purpose. Every word of every BULLET
  becomes a register token, so a prose bullet in a register file registers its
  own prose -- this paragraph once registered "Subject", "terminology",
  "Carbon", "Dioxide", "Natural", "Selection", "Active" and "Transport", which
  is the exact opposite of what it says.)