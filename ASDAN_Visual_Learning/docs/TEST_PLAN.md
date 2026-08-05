# ASDAN visual-learning test plan

## Gate order

Run each gate as its own command and check the exit code before moving to the next. Do not combine a verification and the action it gates into one shell expression.

## 1. Toolkit integrity

```bash
python3 ASDAN_Visual_Learning/build_payloads.py --check
python3 ASDAN_Visual_Learning/check.py
node --check ASDAN_Visual_Learning/asdan-visual-learning.js
python3 -m py_compile   ASDAN_Visual_Learning/build_payloads.py   ASDAN_Visual_Learning/check.py   ASDAN_Visual_Learning/integrate.py   ASDAN_Visual_Learning/browser_test.py
```

Expected:

- 85 payloads;
- BUILD 37, GROW 18, LAUNCH 30;
- all 14 subsection counts;
- 85 valid accessible SVGs;
- zero prohibited storage, upload, media-capture or network APIs;
- no free-text evidence input;
- every LAUNCH payload has the structured locator;
- every GROW/LAUNCH activity has a prediction;
- every GROW/LAUNCH model requires at least two runs.

## 2. Generate the exact source patch

```bash
python3 ASDAN_Visual_Learning/integrate.py   --repo .   --patch-out /tmp/asdan-visual-source-integration.patch   --json-report /tmp/asdan-visual-source-integration.json

git apply --stat /tmp/asdan-visual-source-integration.patch
git apply --check /tmp/asdan-visual-source-integration.patch
git diff --check
```

Review the complete patch. Expected direct source scope:

- 6 shared source files;
- 6 standalone BUILD D&T lessons;
- no hub, scheme, printable pack, witness, tracker or qualification record.

## 3. Apply locally and materialise BUILD

```bash
git apply /tmp/asdan-visual-source-integration.patch

python3 BUILD_ASDAN/_framework/apply_framework.py

python3 ASDAN_Visual_Learning/integrate.py   --repo .   --check   --expect-build-materialized
```

Expected:

- exact current blocks in BUILD, GROW and LAUNCH shared sources;
- exact owned inline blocks in six D&T lessons;
- one materialised marker pair in all 31 BUILD ASDAN decks;
- idempotent second check.

## 4. Existing BUILD framework gates

Run the estate-owned commands documented in `BUILD_ASDAN/_framework/README.md`:

```bash
python3 BUILD_ASDAN/_framework/qa_check.py
node BUILD_ASDAN/_framework/smoke_test.js BUILD_ASDAN/*/[A-Z]*.html
node BUILD_ASDAN/_framework/label_rest_check.js BUILD_ASDAN/*/[A-Z]*.html
node BUILD_ASDAN/_framework/contrast_check.js --manifest BUILD_ASDAN/*/[A-Z]*.html
```

Compare the contrast manifest rather than accepting a regenerated file merely because it exists.

The content-integrity gate must prove that lesson content outside owned framework blocks remains byte-identical.

## 5. Toolkit browser gate

```bash
python3 ASDAN_Visual_Learning/browser_test.py   --repo .   --evidence-dir /tmp/asdan-visual-browser-evidence
```

Test at:

- 1440 × 900;
- 1024 × 768;
- 390 × 844;
- reduced motion.

For every one of the 85 lessons:

- panel mounts once;
- no page error or console error;
- panel fits its container without horizontal overflow;
- every native control is reachable;
- reset clears temporary state;
- static mode retains all meaning;
- print does not include transient panel controls.

## 6. Pathway behaviour

### BUILD

For each activity family:

- completion is possible by click/keyboard without dragging;
- corrective guidance identifies the relationship;
- completion opens the explanation;
- independent task mode is visible;
- screen rehearsal is explicitly separated from real evidence.

### GROW

- activity controls remain locked until a prediction is selected;
- finite model creates a frozen first result;
- the second valid result changes exactly one variable;
- changing zero or multiple variables does not count;
- comparison remains visible;
- independent transfer is not a copy of the model.

### LAUNCH

- activity controls remain locked until prediction;
- completing the activity alone keeps the explanation locked;
- the three structured locator groups become available;
- “not yet available” and “not yet located” remain selectable;
- all three choices unlock the explanation;
- the panel receives the temporary `data-asdan-opened-by` marker;
- no grade, level, criterion achievement or evidence state appears;
- teacher/assessor/access route remains visible.

## 7. Existing lesson regression

Representative tests in every subsection:

- Previous/Next navigation;
- keyboard navigation;
- timer start, pause and reset;
- authored matching and card activities;
- answer reveal;
- WAGOLL;
- teacher/TA controls;
- cold call where present;
- Calm Mode;
- supported/standard/stretch routes;
- print packs and witness surfaces;
- HUD where present;
- lesson completion overlays;
- mobile controls.

The new panel must not intercept background controls when it is not active.

## 8. D&T and vocational safety gate

The six Community Upcycling decks and all practical vocational lessons require human review against:

- the school’s current risk assessments;
- actual equipment, guarding and extraction;
- trained-adult supervision;
- material and allergy information;
- off-site and partner approvals;
- the exact practical method intended.

An HSE page or visual model informs observation; it does not authorise the practical.

## 9. Claims, data and safeguarding gate

Read and apply the current repository versions of:

- `quality/LUNDY_ASDAN_ACCEPTANCE_GATES.md`;
- `quality/LUNDY_ASDAN_DATA_FIREWALL.md`;
- `quality/toolkits/CLAIMS_REGISTER.md`;
- `quality/SEMH_PEDAGOGY_STANDARD.md`;
- `quality/SAFEGUARDING_CONTENT_GATE.md`.

Check:

- no real personal document;
- no disclosure field;
- no invented audience or witness;
- no guessed mapping;
- no automated evidence state;
- no upload or retained record;
- no pupil-facing artefact derived from an unapproved third-party pack.

## 10. Reverse and rollback

Before commit:

```bash
git apply --check --reverse /tmp/asdan-visual-source-integration.patch
```

For rollback through the generator:

```bash
python3 ASDAN_Visual_Learning/integrate.py --repo . --strip
python3 BUILD_ASDAN/_framework/apply_framework.py
```

Then rerun content integrity and `git diff --check`.

## Withheld close stamp

Do not report the complete estate as passed unless gates 1–9 have run on the exact current checkout. The standalone pack’s own validation is evidence about the pack, not about a future integrated repository.
