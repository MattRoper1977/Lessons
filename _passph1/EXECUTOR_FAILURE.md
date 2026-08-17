# PH-1 Amendment 2 — unexpected executor failure before transport retirement

- The temporary workflow still existed, so the executor failed before its Phase 0d transport-retirement commit.
- No force-push, reset, merge or PR was performed.
- The tail of the executor output follows.

```text
Traceback (most recent call last):
  File "/tmp/ph1_amendment2_execute.py", line 2056, in <module>
    main()
  File "/tmp/ph1_amendment2_execute.py", line 1979, in main
    raise RuntimeError(f"production C7 re-check disagrees with committed census: {json.dumps(c7_actual, indent=2)}")
RuntimeError: production C7 re-check disagrees with committed census: {
  "delivering_project": [],
  "double_studio": [],
  "affirmative_l2_registration": [
    {
      "path": "GROW_ASDAN/PEQ/START_HERE.html",
      "window": " 4 \u00b7 Managing Myself Routines beat motivation Week 5 \u00b7 Solving Problems A method beats a panic Week 6 \u00b7 Present My Progress The term, out loud \ud83c\udfc5 Thu P4 \u00b7 banks ASDAN PEQ Level 1 \u2014 registration via UAS coordinator \u00b7 every lesson ends with Documentarian photo + annotation + witness tick. Stretch tier is written to L2 evidence standard. \u2190 Back to the GROW ASDAN hub"
    },
    {
      "path": "GROW_ASDAN/Scheme_and_Resources.html",
      "window": "annotation \u00b7 witness), full print pack off the title slide. Level decision: delivered at PEQ Level 1 per the 2026/27 Qualification Map (E3\u2013L1 only); the Stretch tier is written to L2 evidence standard so moving a flying pupil up is a registration decision, not a re-teach. Personal Effectiveness (PEQ Level 1) \u00b7 Thursday P4 ASDAN PEQ Level 1 Award (Entry 3 floor). Stretch tier written to L2 evidence standard throughout \u2014 pup"
    },
    {
      "path": "GROW_ASDAN/Scheme_and_Resources.html",
      "window": "g a flying pupil up is a registration decision, not a re-teach. Personal Effectiveness (PEQ Level 1) \u00b7 Thursday P4 ASDAN PEQ Level 1 Award (Entry 3 floor). Stretch tier written to L2 evidence standard throughout \u2014 pupils who fly can be registered for Level 2 units (UAS coordinator decision). Wk Lesson Core outcome Banks W1 Knowing Myself \u2014 Strengths, interests, starting points I can audit my strengths and interests with ev"
    },
    {
      "path": "GROW_ASDAN/GROW_ASDAN_Hub.html",
      "window": "; the Community Project and Enterprise both bank PEQ cross-unit project work evidence \u2014 plan phase this term, delivery in Aut 2. Weeks 7\u20138 = consolidation and portfolio audit. PEQ registration and level confirmation (L1 now, L2 units where earned) sit with the UAS/ASDAN coordinator."
    },
    {
      "path": "GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html",
      "window": "al Effectiveness \u00b7 Week 1 of 6 Knowing Myself GROW Pathway \u00b7 ASDAN Studio \u00b7 PEQ Level 1 (E3 floor \u00b7 L2 stretch) Progress SoW \u00b7 GROW ASDAN Aut 1 \u00b7 2026\u201327 \u00b7 PEQ Level 1 (E3 floor \u00b7 L2 stretch) \u00b7 Week 1 \ud83c\udfc5 Banks: ASDAN PEQ L1 baseline \u2014 core-skills audit (registration via UAS coordinator) Spark: You can't grow what you haven't measured. Success looks like I can audit my strengths and interests with evidence I can name a genuine area to develop "
    }
  ],
  "communication_10h": [],
  "not_both": []
}
```
