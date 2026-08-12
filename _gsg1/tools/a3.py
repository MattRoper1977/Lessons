#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 A3 — prose graft, sentence level, on the LIVE files.

Each entry states WHY the carrier changed. Two kinds only:

  QUARRIED  a pack sentence states the same content in a simpler carrier, so
            the pack's carrier replaces the live one (this is the A3 licence).
  MINE      a carrier this pass introduced in Phase A is itself too heavy.
            Holding my own additions to the same standard as the live prose.

NOT done here: anywhere the pack simplified by DELETING content, the live
content stays and the sentence is left alone. Protected vocabulary survives
verbatim in every replacement below.
"""
import re, os, sys, glob

LIVE = "/home/user/Lessons/Science_Teesside/Grow/v3_40min"

EDITS = [
 # ---------------------------------------------------------------- MINE ----
 # 38 words, FK 14.14, the hardest pupil-facing sentence in the whole suite
 # after Phase A - and it was mine. Same four routes, five short carriers.
 ("MINE",
  "<b>If writing is the barrier:</b> say it and an adult scribes your exact words · "
  "point to what changed and say it aloud · record it in the school’s own workflow · "
  "draw it and caption it in one spoken sentence. "
  "The line is never removed, and the route never lowers the Science.",
  "<b>If writing is hard:</b> say it, and an adult writes down your exact words. "
  "Or point to what changed and say it aloud. "
  "Or draw it and give it one spoken caption. "
  "Or record it in the school’s own workflow. "
  "The line always stays. The route changes how you answer, not the Science."),

 # ------------------------------------------------------------ QUARRIED ----
 # pack: "The adult is audience, not verifier." - a shorter carrier for the
 # same ruling. The 'no adult initial' framing is kept word for word.
 ("QUARRIED",
  "<b>No adult initial is required.</b> The adult is the audience for this line, not "
  "its signatory. There is no signature, initial, tick or receipt mark — the line is "
  "closed by being written and received.",
  "<b>No adult initial is required.</b> The adult is audience for this line, not "
  "verifier. There is no signature, initial, tick or receipt mark. "
  "The line closes when it is written and received."),

 # ---------------------------------------------------------------- MINE ----
 ("MINE",
  "Nothing here is right or wrong yet, and nothing is marked, scored or stored. "
  "A prediction is worth having even when it turns out differently — that is what "
  "makes the test worth running.",
  "Nothing here is right or wrong yet. Nothing is marked, scored or stored. "
  "A prediction still counts when it turns out differently. "
  "That is what makes the test worth running."),

 # ---------------------------------------------------------------- MINE ----
 ("MINE",
  "<b>TA fade route:</b> model the word, then prompt for it, then wait for it — drop "
  "a step as soon as the pupil no longer needs it.",
  "<b>TA fade route:</b> model the word. Then prompt for it. Then wait for it. "
  "Drop a step as soon as the pupil no longer needs it."),

 # ---------------------------------------------------------------- MINE ----
 ("MINE",
  "<b>Non-reading route:</b> point to it, say it, show it, or have an adult scribe "
  "your exact words.",
  "<b>Non-reading route:</b> point to it, say it, or show it. "
  "An adult can write down your exact words."),

 # ------------------------------------------------------------ QUARRIED ----
 # live: 17 words, one clause with a four-item list. The pack states the same
 # evidence rule in two short carriers. Content identical, nothing dropped.
 ("QUARRIED",
  "A photo is not proof by itself — pair it with the pupil’s decision, explanation, "
  "result or evaluation.",
  "A photo on its own is not proof. Add what the pupil decided, explained, "
  "found or judged."),
]


def main():
    files = sorted(glob.glob(os.path.join(LIVE, "SCI_G_*.html")))
    tally = {}
    for p in files:
        s = open(p, encoding="utf-8").read()
        orig = s
        for kind, old, new in EDITS:
            if old in s:
                n = s.count(old)
                s = s.replace(old, new)
                tally[kind] = tally.get(kind, 0) + n
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        print("%-44s %s" % (os.path.basename(p),
                            "edited" if s != orig else "UNCHANGED"))
    print("\nreplacements applied by kind:", tally)


if __name__ == "__main__":
    main()
