# CHECKS_E2 · BUILD

Edition: v2 · 25 Sep 2026. Files are prepared for review; nothing has been landed. Browser checks remain a separate step.

## Results

| Check | Result |
| --- | --- |
| Lessons | 7 |
| Hinge surfaces matching HINGE.json | 56/56 |
| Arrival routes / question instances | 21 / 84 |
| Four-question arrival surfaces matching the page | 35/35 |
| Delivered PDFs / pages | 35 / 98 |
| Approved mark and foot licence on PDF pages | 98/98 |
| Word files: title, creator, theme and licence | 15/15 |
| Decks: mark, creator, theme, title and licence | 7/7 |
| Deck slides: v2 licence and own-week brandline | 149/149 |
| Hinge correct letters | A: 2, B: 2, C: 1, D: 2 |
| Parallel correct letters | A: 2, B: 2, C: 2, D: 1 |
| Wrong-option diagnoses | 42 distinct within their question |
| Misconceptions with their own corrections | 14 |
| Content/structure validation failures | 0 |
| Layout overflow findings in deck validation | 0 |

The eight hinge surfaces are lesson page, TA pop-up, TA markdown, TA PDF, teacher Word, teacher PDF, slide notes and planner row. LOOP and P18 check lines use the same question. Hinge answers remain in staff/reveal content.

## Removed-content checks

| Targeted removal or correction | Remaining hits in scoped RE content |
| --- | --- |
| Repeated fictional-case arrival instruction and answer | 0 |
| Empty previous-lesson reminder label | 0 |
| Previous-learning preamble in W02–W07 | 0 |
| Exposed word-definition arrival line in W02–W07 | 0 |
| Cord safety line in RE lessons and RE visitor kit row | 0 |
| Remembered-person card and model lead | 0 |
| Personal visitor death-belief question | 0 |
| Named celebrant and private family details | 0 |
| Unqualified Muslim and Christian practice statements | 0 |
| Personal memory and personal late-friend dilemma prompts | 0 |
| Joint exile wording for Rama and Sita | 0 |
| Specified filler distractors and duplicated within-question diagnoses | 0 |
| Process names, review-process wording and redaction wording on RE pages | 0 |
| Scripture references with missing colons | 0 |

The public scan covers the delivered RE HTML, PDF text, Word/deck text and metadata, TA briefs, transcripts, SVGs and lesson JSON. The shared planners and kit retain unrelated subjects exactly as required; their existing Science lesson names and Science cord controls are outside the RE removal scope.

## Preservation and scope

The three E v1 pack archive hashes match the supplied bases. Across E2, 329 lesson style blocks are unchanged apart from the edition text; 105 main runtime script blocks are byte-identical. Lesson configuration and the old generic-arrival adapter change only where F1–F3 require it. All 45 Word files preserve their accepted header, style, settings and numbering parts. All 21 native decks retain their accepted geometry and pass package, layout and import checks; the receipt hashes match the delivered bytes.

Nineteen model videos and forty of the forty-two SVG/PNG picture files remain byte-identical. BUILD W03 and W06 videos change for F3; GROW W03 SVG/PNG and its embedded deck image change for F3. Approved mark image bytes are retained.

Only 42 planner cells change: the stage and TA cells for the 21 RE lessons. Other planner cells and workbook styling remain unchanged. The kit changes five safety cells: the RE visitor row, the scissors row and three highlighter rows. No-flame wording remains on light rows. Return-week planners and the accepted start-page bundle are not resent.

Pack-level START_HERE.html, Review_record.html, Sources_and_checks.html and pathway START_HERE.html are excluded. Lesson-local source pages remain. UNIT_RATIONALE HTML and Word are included. No pupil data is included.

## Video safe area

| Video | Seconds | Frames checked | Content bounds x0,y0,x1,y1 | 5% margin | Embedded bytes | Audio |
| --- | --- | --- | --- | --- | --- | --- |
| BUILD_RE_A2_W03 | 36.0 | 360 | [65, 41, 1167, 675] | PASS; 0 failed frames | Identical | Silent |
| BUILD_RE_A2_W06 | 36.0 | 360 | [65, 41, 1195, 675] | PASS; 0 failed frames | Identical | Silent |

Both rendered videos are 1280 × 720 at 10 fps. The required safe rectangle is x = 64…1216, y = 36…684. Every decoded frame was compared with the background to measure the caption box, text and drawing extent. BUILD W03 also required a render because its original model caption repeated the inaccurate exile wording.

## Correct letters and option lengths

Words are counted with apostrophes and hyphens inside a word; punctuation alone is not a word. Main and parallel questions are listed separately.

| Lesson | Question | Correct | A words | B words | C words | D words |
| --- | --- | --- | --- | --- | --- | --- |
| BUILD_RE_A2_W01 | main | A | 7 | 7 | 7 | 7 |
| BUILD_RE_A2_W01 | parallel | D | 7 | 7 | 7 | 7 |
| BUILD_RE_A2_W02 | main | C | 7 | 7 | 7 | 7 |
| BUILD_RE_A2_W02 | parallel | B | 7 | 7 | 7 | 7 |
| BUILD_RE_A2_W03 | main | D | 12 | 12 | 8 | 11 |
| BUILD_RE_A2_W03 | parallel | A | 3 | 3 | 3 | 3 |
| BUILD_RE_A2_W04 | main | B | 8 | 8 | 8 | 8 |
| BUILD_RE_A2_W04 | parallel | A | 9 | 9 | 9 | 9 |
| BUILD_RE_A2_W05 | main | A | 7 | 8 | 7 | 7 |
| BUILD_RE_A2_W05 | parallel | C | 8 | 7 | 7 | 8 |
| BUILD_RE_A2_W06 | main | B | 9 | 9 | 9 | 9 |
| BUILD_RE_A2_W06 | parallel | C | 9 | 9 | 9 | 9 |
| BUILD_RE_A2_W07 | main | D | 7 | 7 | 7 | 7 |
| BUILD_RE_A2_W07 | parallel | B | 7 | 7 | 7 | 7 |

The correct option is uniquely longest in 0 of 14 questions. The correct letters do not follow the former repeating four-letter cycle.

## Arrival questions, help and answers

Each lesson has its own four retrieval targets. Supported offers choices; Standard uses the retrieval prompts; Stretch asks for a reason or accurate example, with supporting detail on questions 3 and 4. The page keeps each answer hidden until its own reveal button is used. The printed arrival, Word pupil pack, pupil PDF and slides use the Standard questions and their help; staff notes carry the answers.

### BUILD W01 · A festival of light: Diwali

Retrieval sequence: Autumn 1 W07; Vocabulary retrieval; Autumn 1 W03; Autumn 1 W05.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: can meaning make a simple object special? | Recall the previous lesson; a clue is enough. Choose: Yes. Its meaning or purpose can matter more than its price. OR Its price alone. | Yes. Its meaning or purpose can matter more than its price. |
| 2 | Which meaning fits festival? | Choose: A special time when people celebrate OR A festival of lights celebrated by many Hindus, Sikhs and Jains. | A special time when people celebrate |
| 3 | Earlier learning (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Recall Autumn 1 W03; picture the source or activity. Choose: A volunteer greets him and shows him where to sit. OR A person checks his beliefs first. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Choose: Helping others. OR Owning matching objects. Stretch: add the detail that supports your answer. | Helping others. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: can meaning make a simple object special? | Recall the previous lesson; a clue is enough. | Yes. Its meaning or purpose can matter more than its price. |
| 2 | Which meaning fits festival? | Choose: A special time when people celebrate OR A festival of lights celebrated by many Hindus, Sikhs and Jains. | A special time when people celebrate |
| 3 | Earlier learning (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Recall Autumn 1 W03; picture the source or activity. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Helping others. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: can meaning make a simple object special? Give a reason or example. | Recall the previous lesson; a clue is enough. | Yes. Its meaning or purpose can matter more than its price. |
| 2 | Use festival in an accurate example. | Use the word in a relevant RE sentence and explain the example. | A special time when people celebrate Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Recall Autumn 1 W03; picture the source or activity. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Helping others. |

### BUILD W02 · Comparing light in celebrations

Retrieval sequence: Autumn 2 W01; Vocabulary retrieval; Autumn 1 W04; Autumn 1 W06.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What can the light of a diya stand for? | Recall the previous lesson; a clue is enough. Choose: Good overcoming evil, and hope. OR Everyone must have the same experience. | Good overcoming evil, and hope. |
| 2 | Which meaning fits compare? | Choose: To look for what is the same and what is different OR A Jewish festival of lights that lasts eight nights. | To look for what is the same and what is different |
| 3 | Earlier learning (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Recall Autumn 1 W04; picture the source or activity. Choose: So that fingers do not touch the handwritten scroll. OR To make the writing larger. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Choose: Every year on 21 September. OR Quiet thinking is always worship. Stretch: add the detail that supports your answer. | Every year on 21 September. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What can the light of a diya stand for? | Recall the previous lesson; a clue is enough. | Good overcoming evil, and hope. |
| 2 | Which meaning fits compare? | Choose: To look for what is the same and what is different OR A Jewish festival of lights that lasts eight nights. | To look for what is the same and what is different |
| 3 | Earlier learning (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Recall Autumn 1 W04; picture the source or activity. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Every year on 21 September. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What can the light of a diya stand for? Give a reason or example. | Recall the previous lesson; a clue is enough. | Good overcoming evil, and hope. |
| 2 | Use compare in an accurate example. | Use the word in a relevant RE sentence and explain the example. | To look for what is the same and what is different Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Recall Autumn 1 W04; picture the source or activity. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Every year on 21 September. |

### BUILD W03 · Retelling a festival story

Retrieval sequence: Autumn 2 W02; Vocabulary retrieval; Autumn 2 W01; Autumn 1 W02.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Name one thing Diwali and Hanukkah both use. | Recall the previous lesson; a clue is enough. Choose: Light. Both festivals use lamps or lights. OR Everyone must have the same experience. | Light. Both festivals use lamps or lights. |
| 2 | Which meaning fits sequence? | Choose: The order in which things happen OR To tell a story again in your own way. | The order in which things happen |
| 3 | Earlier learning (Autumn 2 W01): What can the light of a diya stand for? | Recall Autumn 2 W01; picture the source or activity. Choose: Good overcoming evil, and hope. OR Its price alone. Stretch: add the detail that supports your answer. | Good overcoming evil, and hope. |
| 4 | Last half-term (Autumn 1 W02): Where is a Torah scroll kept in a synagogue? | Think back to Autumn 1 W02; a word, action or source detail can help. Choose: In a special cupboard called the Ark. OR A shelf for coats. Stretch: add the detail that supports your answer. | In a special cupboard called the Ark. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Name one thing Diwali and Hanukkah both use. | Recall the previous lesson; a clue is enough. | Light. Both festivals use lamps or lights. |
| 2 | Which meaning fits sequence? | Choose: The order in which things happen OR To tell a story again in your own way. | The order in which things happen |
| 3 | Earlier learning (Autumn 2 W01): What can the light of a diya stand for? | Recall Autumn 2 W01; picture the source or activity. Stretch: add the detail that supports your answer. | Good overcoming evil, and hope. |
| 4 | Last half-term (Autumn 1 W02): Where is a Torah scroll kept in a synagogue? | Think back to Autumn 1 W02; a word, action or source detail can help. Stretch: add the detail that supports your answer. | In a special cupboard called the Ark. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Name one thing Diwali and Hanukkah both use. Give a reason or example. | Recall the previous lesson; a clue is enough. | Light. Both festivals use lamps or lights. |
| 2 | Use sequence in an accurate example. | Use the word in a relevant RE sentence and explain the example. | The order in which things happen Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 2 W01): What can the light of a diya stand for? | Recall Autumn 2 W01; picture the source or activity. Stretch: add the detail that supports your answer. | Good overcoming evil, and hope. |
| 4 | Last half-term (Autumn 1 W02): Where is a Torah scroll kept in a synagogue? | Think back to Autumn 1 W02; a word, action or source detail can help. Stretch: add the detail that supports your answer. | In a special cupboard called the Ark. |

### BUILD W04 · Taking part respectfully

Retrieval sequence: Autumn 2 W03; Vocabulary retrieval; Autumn 2 W02; Autumn 1 W03.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What do people do to welcome Rama and Sita home? | Recall the previous lesson; a clue is enough. Choose: They light rows of lamps. OR Everyone must have the same experience. | They light rows of lamps. |
| 2 | Which meaning fits celebration? | Choose: A way of marking a special time OR Showing devotion to God or gods. | A way of marking a special time |
| 3 | Earlier learning (Autumn 2 W02): Name one thing Diwali and Hanukkah both use. | Recall Autumn 2 W02; picture the source or activity. Choose: Light. Both festivals use lamps or lights. OR A shelf for coats. Stretch: add the detail that supports your answer. | Light. Both festivals use lamps or lights. |
| 4 | Last half-term (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Think back to Autumn 1 W03; a word, action or source detail can help. Choose: A volunteer greets him and shows him where to sit. OR A person checks his beliefs first. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What do people do to welcome Rama and Sita home? | Recall the previous lesson; a clue is enough. | They light rows of lamps. |
| 2 | Which meaning fits celebration? | Choose: A way of marking a special time OR Showing devotion to God or gods. | A way of marking a special time |
| 3 | Earlier learning (Autumn 2 W02): Name one thing Diwali and Hanukkah both use. | Recall Autumn 2 W02; picture the source or activity. Stretch: add the detail that supports your answer. | Light. Both festivals use lamps or lights. |
| 4 | Last half-term (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Think back to Autumn 1 W03; a word, action or source detail can help. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What do people do to welcome Rama and Sita home? Give a reason or example. | Recall the previous lesson; a clue is enough. | They light rows of lamps. |
| 2 | Use celebration in an accurate example. | Use the word in a relevant RE sentence and explain the example. | A way of marking a special time Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 2 W02): Name one thing Diwali and Hanukkah both use. | Recall Autumn 2 W02; picture the source or activity. Stretch: add the detail that supports your answer. | Light. Both festivals use lamps or lights. |
| 4 | Last half-term (Autumn 1 W03): What is one sign that Sam is welcome at the gurdwara? | Think back to Autumn 1 W03; a word, action or source detail can help. Stretch: add the detail that supports your answer. | A volunteer greets him and shows him where to sit. |

### BUILD W05 · Hope and remembrance

Retrieval sequence: Autumn 2 W04; Vocabulary retrieval; Autumn 2 W03; Autumn 1 W04.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Is making a rangoli-style pattern in class worship? | Recall the previous lesson; a clue is enough. Choose: No. It is learning about a celebration. OR Everyone must have the same experience. | No. It is learning about a celebration. |
| 2 | Which meaning fits hope? | Choose: Believing that something good can happen OR Taking time to remember people and events. | Believing that something good can happen |
| 3 | Earlier learning (Autumn 2 W03): What do people do to welcome Rama and Sita home? | Recall Autumn 2 W03; picture the source or activity. Choose: They light rows of lamps. OR A person checks his beliefs first. Stretch: add the detail that supports your answer. | They light rows of lamps. |
| 4 | Last half-term (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Think back to Autumn 1 W04; a word, action or source detail can help. Choose: So that fingers do not touch the handwritten scroll. OR To make the writing larger. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Is making a rangoli-style pattern in class worship? | Recall the previous lesson; a clue is enough. | No. It is learning about a celebration. |
| 2 | Which meaning fits hope? | Choose: Believing that something good can happen OR Taking time to remember people and events. | Believing that something good can happen |
| 3 | Earlier learning (Autumn 2 W03): What do people do to welcome Rama and Sita home? | Recall Autumn 2 W03; picture the source or activity. Stretch: add the detail that supports your answer. | They light rows of lamps. |
| 4 | Last half-term (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Think back to Autumn 1 W04; a word, action or source detail can help. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Is making a rangoli-style pattern in class worship? Give a reason or example. | Recall the previous lesson; a clue is enough. | No. It is learning about a celebration. |
| 2 | Use hope in an accurate example. | Use the word in a relevant RE sentence and explain the example. | Believing that something good can happen Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 2 W03): What do people do to welcome Rama and Sita home? | Recall Autumn 2 W03; picture the source or activity. Stretch: add the detail that supports your answer. | They light rows of lamps. |
| 4 | Last half-term (Autumn 1 W04): Why do readers often use a pointer with a Torah scroll? | Think back to Autumn 1 W04; a word, action or source detail can help. Stretch: add the detail that supports your answer. | So that fingers do not touch the handwritten scroll. |

### BUILD W06 · A big question

Retrieval sequence: Autumn 2 W05; Vocabulary retrieval; Autumn 2 W04; Autumn 1 W05.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What does the red poppy stand for? | Recall the previous lesson; a clue is enough. Choose: Remembrance and hope for a peaceful future. OR Everyone must have the same experience. | Remembrance and hope for a peaceful future. |
| 2 | Which meaning fits big question? | Choose: A question about life that has more than one answer OR Why you think something. | A question about life that has more than one answer |
| 3 | Earlier learning (Autumn 2 W04): Is making a rangoli-style pattern in class worship? | Recall Autumn 2 W04; picture the source or activity. Choose: No. It is learning about a celebration. OR To make the writing larger. Stretch: add the detail that supports your answer. | No. It is learning about a celebration. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Choose: Helping others. OR Owning matching objects. Stretch: add the detail that supports your answer. | Helping others. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What does the red poppy stand for? | Recall the previous lesson; a clue is enough. | Remembrance and hope for a peaceful future. |
| 2 | Which meaning fits big question? | Choose: A question about life that has more than one answer OR Why you think something. | A question about life that has more than one answer |
| 3 | Earlier learning (Autumn 2 W04): Is making a rangoli-style pattern in class worship? | Recall Autumn 2 W04; picture the source or activity. Stretch: add the detail that supports your answer. | No. It is learning about a celebration. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Helping others. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: What does the red poppy stand for? Give a reason or example. | Recall the previous lesson; a clue is enough. | Remembrance and hope for a peaceful future. |
| 2 | Use big question in an accurate example. | Use the word in a relevant RE sentence and explain the example. | A question about life that has more than one answer Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 2 W04): Is making a rangoli-style pattern in class worship? | Recall Autumn 2 W04; picture the source or activity. Stretch: add the detail that supports your answer. | No. It is learning about a celebration. |
| 4 | Last half-term (Autumn 1 W05): What value do Aisha and Tom share? | Think back to Autumn 1 W05; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Helping others. |

### BUILD W07 · Festival reflection and UAS evidence

Retrieval sequence: Autumn 2 W06; Vocabulary retrieval; Autumn 2 W05; Autumn 1 W06.

**Supported**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Which word joins an answer to its reason? | Recall the previous lesson; a clue is enough. Choose: Because. OR Everyone must have the same experience. | Because. |
| 2 | Which meaning fits reflection? | Choose: Looking back at what you have learned OR Work that shows what you know or can do. | Looking back at what you have learned |
| 3 | Earlier learning (Autumn 2 W05): What does the red poppy stand for? | Recall Autumn 2 W05; picture the source or activity. Choose: Remembrance and hope for a peaceful future. OR Owning matching objects. Stretch: add the detail that supports your answer. | Remembrance and hope for a peaceful future. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Choose: Every year on 21 September. OR Quiet thinking is always worship. Stretch: add the detail that supports your answer. | Every year on 21 September. |

**Standard**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Which word joins an answer to its reason? | Recall the previous lesson; a clue is enough. | Because. |
| 2 | Which meaning fits reflection? | Choose: Looking back at what you have learned OR Work that shows what you know or can do. | Looking back at what you have learned |
| 3 | Earlier learning (Autumn 2 W05): What does the red poppy stand for? | Recall Autumn 2 W05; picture the source or activity. Stretch: add the detail that supports your answer. | Remembrance and hope for a peaceful future. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Every year on 21 September. |

**Stretch**

| # | Question | Help | Reveal answer |
| --- | --- | --- | --- |
| 1 | Previous lesson: Which word joins an answer to its reason? Give a reason or example. | Recall the previous lesson; a clue is enough. | Because. |
| 2 | Use reflection in an accurate example. | Use the word in a relevant RE sentence and explain the example. | Looking back at what you have learned Accept an accurate RE example with an explanation. |
| 3 | Earlier learning (Autumn 2 W05): What does the red poppy stand for? | Recall Autumn 2 W05; picture the source or activity. Stretch: add the detail that supports your answer. | Remembrance and hope for a peaceful future. |
| 4 | Last half-term (Autumn 1 W06): When is the International Day of Peace? | Think back to Autumn 1 W06; a word, action or source detail can help. Stretch: add the detail that supports your answer. | Every year on 21 September. |

## Exit Q2 application replacements

| Lesson | Question | Answer guidance |
| --- | --- | --- |
| BUILD_RE_A2_W02 | A source says a family adds one Hanukkah light each night. What could the growing row help them remember? | It can help recall the tradition of the Temple oil lasting eight days; relate the growing row to that story. |
| BUILD_RE_A2_W03 | A retelling puts the welcome lamps before Sita is rescued. Which event needs moving, and why? | Move the welcome lamps after the rescue: the lamps welcome Rama and Sita home. |
| BUILD_RE_A2_W04 | A museum labels an unlit diya with its festival meaning. How does this help people learn? | It links an object to its meaning without asking the visitor to take part in worship. |

Other exit Q2 wording is retained.

## Source corrections

| Source | Claim checked | Link |
| --- | --- | --- |
| BBC Teach, Rama and Sita — story transcript | Rama is sent away; Sita and Lakshmana go with him. Ravana takes Sita; Hanuman and his army help. | https://teach.files.bbci.co.uk/schoolradio/assemblies/frameworks/diwali_the_story_of_rama_and_sita_transcript.pdf |
| SikhNet / Basics of Sikhi, Diwali and Bandi Chhor Divas | Diwali and Sikh Bandi Chhor Divas context. | https://sikhnet.com/stories/diwali-festival-light-bandi-chhor-divas |
| Victoria and Albert Museum, Diwali | Rangoli welcomes guests. Doorway location is also supported by the Hindu American Foundation source below. | https://www.vam.ac.uk/blog/museum-life/letsmakewednesdays-diwali |
| Imperial War Museums, definition of a war memorial | War memorials can include gardens, monuments and rolls of names. | https://www.iwm.org.uk/file-download/download/public/16908 |
| Imperial War Museums, Warrington Cenotaph | A listed memorial combines a stone cenotaph, benches and garden setting. | https://memorials.iwm.org.uk/memorial/18154 |
| UK Government, DCMS July 2026 update: Remembrance Sunday, 8 November 2026 | National confirmation of Remembrance Sunday, 8 November 2026. | https://www.gov.uk/government/publications/department-for-culture-media-and-sport-british-sign-language-bsl-5-year-plan-1-year-update-july-2026/british-sign-language-5-year-plan-department-for-culture-media-and-sport-1-year-update-july-2026-english-and-bsl-versions |
| Luke 6:31, New International Version, BibleGateway | Luke 6:31 NIV wording matches the quotation. | https://www.biblegateway.com/passage/?search=Luke+6%3A31&version=NIV |
| Royal British Legion, Armistice Day | 11 November Armistice Day and remembrance practice; current national link. | https://www.britishlegion.org.uk/get-involved/remembrance/armistice-day |
| Humanists UK, What happens at a Humanist naming ceremony | Humanist naming-ceremony practice; no real celebrant or family details are reproduced. | https://humanists.uk/ceremonies/namings/blog/what-happens-at-a-humanist-naming-ceremony/ |

Doorway placement: https://www.hinduamerican.org/blog/whats-the-meaning-behind-hindu-door-decorations . The V&A welcome claim was available in its indexed public result; its direct page returned an access restriction during retrieval. The other named replacements were checked against their public text.
