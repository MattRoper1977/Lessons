# A6 — GROW Supported route reading load

```
lesson                           FK before FK after w before w after    Δw%  vs 8.24
SCI_G_W3A_Friction_Explore            2.99     2.77       54      54  +0.0%  ok
SCI_G_W3B_Friction_Do                 6.15     6.15       47      47  +0.0%  ok
SCI_G_W4A_Mechanisms_Explore          5.56     5.56       47      47  +0.0%  ok
SCI_G_W4B_Mechanisms_Do               8.61     4.73       38      40  +5.3%  ok
SCI_G_W5A_Fair_Test_Explore           4.72     4.72       49      49  +0.0%  ok
SCI_G_W5B_Fair_Test_Do                3.89     3.89       48      48  +0.0%  ok
SCI_G_W6A_Earth_And_Planets_Explore      3.77     3.17       41      45  +9.8%  ok
SCI_G_W6B_Earth_And_Planets_Do        5.62     3.89       43      48 +11.6%  ok
SCI_G_W7A_The_Moon_Explore            5.06     5.06       47      47  +0.0%  ok
SCI_G_W7B_The_Moon_Do                 6.30     4.36       48      52  +8.3%  ok

pooled Supported route: FK 4.85 -> 4.06, words 462 -> 477

--- anti-gaming constraints ---
  word count within ±15% per lesson: PASS
  no Supported element lost:         PASS
  science vocabulary preserved:      PASS

--- four-element audit of every Supported route (state BEFORE any edit) ---
  SCI_G_W3A_Friction_Explore       all four present
  SCI_G_W3B_Friction_Do            MISSING: ['sentence stem']
  SCI_G_W4A_Mechanisms_Explore     MISSING: ['sentence stem']
  SCI_G_W4B_Mechanisms_Do          all four present
  SCI_G_W5A_Fair_Test_Explore      MISSING: ['sentence stem']
  SCI_G_W5B_Fair_Test_Do           MISSING: ['sentence stem']
  SCI_G_W6A_Earth_And_Planets_Explore MISSING: ['sentence stem']
  SCI_G_W6B_Earth_And_Planets_Do   MISSING: ['sentence stem']
  SCI_G_W7A_The_Moon_Explore       MISSING: ['word bank / visual support', 'sentence stem']
  SCI_G_W7B_The_Moon_Do            MISSING: ['word bank / visual support', 'sentence stem']

--- plain-text diff of every changed Supported block ---

  SCI_G_W3A_Friction_Explore.html  [arrival]
    -  Point or say: which force from last lesson can slow something moving through air or water?
    +  Point or say: what force do you already know that can slow a moving object down?
       FK 6.14 -> 5.40   words 16 -> 16

  SCI_G_W4B_Mechanisms_Do.html  [scaffold]
    -  Photo/diagram sequence + two labelled pivot positions + choice vocabulary: easier / harder / further / less far.
    +  Photo or diagram sequence. Two labelled pivot positions. Choice words: easier · harder · further · less far.
       FK 14.90 -> 5.05   words 13 -> 15

  SCI_G_W6A_Earth_And_Planets_Explore.html  [task]
    -  ◆ Use labelled cards + mnemonic strip + pre-drawn gravity arrow to complete.
    +  ◆ Use the labelled cards and the mnemonic strip. The gravity arrow is already drawn.
       FK 9.55 -> 5.68   words 10 -> 14

  SCI_G_W6B_Earth_And_Planets_Do.html  [task]
    -  ◆ Numbered planet cards + completed type key + teacher-supplied orbit arrows.
    +  ◆ Use the numbered planet cards. The type key and the orbit arrows are given.
       FK 10.21 -> 3.15   words 9 -> 14

  SCI_G_W7B_The_Moon_Do.html  [task]
    -  ◆ Four-position wheel with sunlight arrow already printed; pupil matches observer views.
    +  ◆ Use the four-position wheel. The sunlight arrow is already printed. Match what the observer sees.
       FK 11.23 -> 5.24   words 11 -> 15
```
