# PH-1 Amendment 2 — unexpected executor failure before transport retirement

- The temporary workflow still existed, so the executor failed before its Phase 0d transport-retirement commit.
- No force-push, reset, merge or PR was performed.
- The tail of the executor output follows.

```text
Traceback (most recent call last):
  File "/tmp/ph1_amendment2_execute.py", line 2055, in <module>
    main()
  File "/tmp/ph1_amendment2_execute.py", line 1978, in main
    raise RuntimeError(f"production C7 re-check disagrees with committed census: {json.dumps(c7_actual, indent=2)}")
RuntimeError: production C7 re-check disagrees with committed census: {
  "delivering_project": [],
  "double_studio": [],
  "affirmative_l2_registration": [
    {
      "path": "LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html",
      "window": "akes communication effective I can describe audience and purpose with examples I can give a range of examples of formal and informal communication Aspire \u00b7 explain WHY a choice of register works for a given audience \u2014 an L2 evidence standard. Teacher Print Tools \u2014 Week 2 \ud83d\udda8 Supported pack \ud83d\udda8 Standard pack \ud83d\udda8 Stretch pack Retrieval Quiz Arrival Task \u2013 What Do You Already Know? \ud83d\udc41\ufe0f Reveal Answers \ud83e\udd1d With su"
    },
    {
      "path": "LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html",
      "window": "annotation \u2610 witness \u2610 Independent Work \u2013 Stretch Task: Write two versions of the same message and describe, with examples, how audience and purpose changed your choices. Stretch (L2 standard): explain WHY a choice of register works for a given audience \u2014 an L2 evidence standard. Exit Ticket \u2013 Supported 1) You can outline what makes communication effective \u2014 true? Say one thing. 2) You can name a formal"
    },
    {
      "path": "GROW_ASDAN/Scheme_and_Resources.html",
      "window": "g a flying pupil up is a registration decision, not a re-teach. Personal Effectiveness (PEQ Level 1) \u00b7 Thursday P4 ASDAN PEQ Level 1 Award (Entry 3 floor). Stretch tier written to L2 evidence standard throughout \u2014 pupils who fly can be registered for Level 2 units (UAS coordinator decision). Wk Lesson Core outcome Banks W1 Knowing Myself \u2014 Strengths, interests, starting points I can audit my strengths and interests with ev"
    }
  ],
  "communication_10h": [],
  "not_both": []
}
```
