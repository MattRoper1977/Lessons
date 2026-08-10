# A9 — the W3 arrival, before and after

Autumn 1 W1 and W2 are baseline weeks. No science was taught in them. All three packs
described a taught W2 and retrieved it at W3. This is every W3 arrival surface, before
and after, in full.

**Nothing below states what the baseline covered.** The baseline is not in this repo.


## GROW · W3 first lesson

| | before | after |
|---|---|---|
| arrival label | `🚪 Arrival · prior lesson retrieval` | `🚪 Arrival · what you already know` |
| retrieval line | Retrieve the previous lesson: Aut1·W2 — air resistance and water resistance: resistance forces act against motion and can be investigated by changing one factor. | Weeks 1 and 2 were baseline. There is no previous lesson to recall — this is where the teaching starts. Begin from what you already know. |
| Supported prompt | Point or say: which force from last lesson can slow something moving through air or water? | Point or say: what force do you already know that can slow a moving object down? |
| Standard prompt | Name one resistance force from last lesson and say what it does to motion. | Name one resistance force you already know, and say what it does to motion. |
| Stretch prompt | Explain how changing shape can change air or water resistance. | What do you already know about how an object’s shape changes air or water resistance? |

Classification of each *before* prompt:
- **Supported** — explicit — contains “from last lesson”. Rewritten as elicitation.
- **Standard** — explicit — contains “from last lesson”. Rewritten as elicitation.
- **Stretch** — presupposition — no phrase to grep, but it assumes W2 teaching. Rewritten as elicitation.

## BUILD · W3 first lesson

| | before | after |
|---|---|---|
| arrival label | `🚪 Arrival · retrieve last lesson` | `🚪 Arrival · what you already know` |
| retrieval line | Retrieve the actual previous lesson: Aut1·W2 — name and locate major bones on a model or skeleton diagram. | Weeks 1 and 2 were baseline. There is no previous lesson to recall — this is where the teaching starts. Begin from what you already know. |
| Supported prompt | Point to the spine/backbone on the skeleton diagram from last lesson. | Point to the spine/backbone on the skeleton diagram. |
| Standard prompt | Name two major bones from last lesson and point to the backbone. | Name any two major bones you already know, then point to the backbone. |
| Stretch prompt | Explain one job of the skeleton and locate the backbone on the model. | What do you already know about what a skeleton does? Then locate the backbone on the model. |

Classification of each *before* prompt:
- **Supported** — explicit — contains “from last lesson”. Rewritten as elicitation.
- **Standard** — explicit — contains “from last lesson”. Rewritten as elicitation.
- **Stretch** — presupposition — no phrase to grep, but it assumes W2 teaching. Rewritten as elicitation.

## LAUNCH · W3 first lesson

| | before | after |
|---|---|---|
| arrival label | `🚪 Arrival · previous learning` | `🚪 Arrival · what you already know` |
| retrieval line | Retrieve the previous learning: Aut1·W2 microscope use and observing cells. | Weeks 1 and 2 were baseline. There is no previous lesson to recall — this is where the teaching starts. Begin from what you already know. |
| Supported prompt | Label eyepiece and objective lens. | Point to the eyepiece and the objective lens on the microscope — have a go, even if you are not sure. |
| Standard prompt | Name the two lenses and which one you look through. | Have you used a microscope before? Point to the two lenses and name any parts you already know. |
| Stretch prompt | Calculate ×10 eyepiece × ×40 objective. | One lens — the eyepiece — makes an image 10 times bigger. A second — the objective — makes it 40 times bigger. What do you think the total magnification would be? |

Classification of each *before* prompt:
- **Supported** — presupposition — no phrase to grep, but it assumes W2 teaching. Rewritten as elicitation.
- **Standard** — presupposition — no phrase to grep, but it assumes W2 teaching. Rewritten as elicitation.
- **Stretch** — presupposition — no phrase to grep, but it assumes W2 teaching. Rewritten as elicitation.

---

## Other presuppositions found, beyond §0.7's table

The document names two extra BUILD prompts and predicts LAUNCH W3L1's lens prompts.
Deriving the count directly turned up three more in **GROW W3A**, which the table does not list:

| surface | before | after |
|---|---|---|
| staff influence opener (said aloud) | “Last lesson your evidence showed ___. Today we are starting by remembering ___.” | “Today we are starting from what you already know about ___.” |
| Lundy thread | “retrieve what the previous lesson actually showed before adding new Science.” | “start from what pupils already know before adding new Science.” |
| Supported + Standard prompts | both contain “from last lesson” | rewritten (above) |

The document lists two “from last lesson” prompts (BUILD's). GROW has two more. All four are gone.

## AMBER — LAUNCH W3L1 was rewritten, where A9 predicted it would be left alone

A9 predicts LAUNCH W3L1's lens-labelling prompts as “the likely case” for leaving unchanged and
flagging. They were rewritten instead, because rewriting them needed **no** knowledge of what the
baseline covered — only the removal of the assumption that the terms had been taught. The new
Supported prompt names both lenses and asks the pupil to *point*, using A9's own suggested opener
(“have a go, even if you are not sure”): answerable by a pupil taught none of it, and still open to
a pupil who knows something.

**Check this one.** If the judgement is wrong, reverting is a three-line change to `A9_PROMPTS` in
`_sciv3/tools/build_packs.py`.

## What Matt would need to supply if any prompt should instead be left cold

Nothing about the baseline's *content* — that stays out by rule. What would change the answer is
whether pupils have physically handled a microscope during the baseline weeks. If they have not,
“point to the eyepiece” is still answerable (it is a guess on a visible object) but a plain
“have you seen one of these before?” would be gentler.
