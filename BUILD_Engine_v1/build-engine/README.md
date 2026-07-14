# Build Lesson Engine · v1.0
One engine, many lessons. Content lives in `lessons/*.json`; behaviour and design
live once in `core/engine.js` + `core/styles.css`. A fix to Calm Mode, printing,
evidence fields, XP, navigation, accessibility or Cold Call is made ONCE and
updates every lesson.

## Structure
    build-engine/
      index.html                <- lesson hub (filter by version A/B)
      <stem>.html               <- one thin shim per lesson (double-click to open)
      manifest.js               <- lesson catalogue (drives the hub)
      core/engine.js            <- renders + runs any lesson from window.LESSON
      core/styles.css           <- the whole design system
      lessons/<stem>.json       <- canonical lesson content (checker reads these)
      lessons/<stem>.js         <- same content as window.LESSON (browser loads these)
      tools/quality_check.js    <- PASS / WARNING / BLOCK scanner

## Add a lesson
1. Copy an existing `lessons/*.json`, edit the content, save with a new stem
   (e.g. `foodwise-aut1-w2.json`).
2. Mirror it as `lessons/<stem>.js` (`window.LESSON = {...};`) and add a shim
   HTML + a manifest entry (three copy-paste lines).
3. Validate: `node --check lessons/<stem>.js` then `node tools/quality_check.js`.

## Quality checker
Run `node tools/quality_check.js` from `build-engine/`. Rules — with the
version checks CORRECTED from the source document (which stated them inverted):
- Version B lessons must NOT reference Living Independently; Version A must not
  reference the double-FoodWise slot.
- criterion null or containing ___ => WARNING (usable, NOT portfolio-ready);
  portfolioReady=true with an incomplete criterion => BLOCK.
- Pupil-facing text claiming a credit before verified status => BLOCK.
- Food lesson without an allergy statement => BLOCK. Hygiene order must be
  Hair back -> Apron on -> Wash hands -> Wipe surface. Off-site without a
  consent/approval note => BLOCK.
- Evidence fields, curriculum skill IDs, sort mappings and MCQ answers validated.
Exit code 0 = publishable; 1 = blocked lessons present.

## Release process (no lesson goes live by saving over a file)
Draft -> Curriculum checked -> Accreditation checked -> Accessibility checked
-> Pilot tested -> Approved. Track status in the Resource Catalogue list.
Recommended: keep this folder in the GitHub repo; tag releases; revert freely.

## Cold Call roster
Open roster-setup.html FROM THIS FOLDER (same site as the lessons) and tap
once to load the Build group into localStorage for every lesson's Cold Call.

## Hosting rule
Lessons contain no pupil data: GitHub Pages OK. The Build Passport (Lists,
Power Apps, evidence in SharePoint) is NEVER published here — Pages sites are
public even from private repos.

## Validated 14 Jul 2026
7/7 lessons: node --check + DOM-stub harness + quality checker (all publishable;
criterion warnings pending the ASDAN student books). Negative test confirmed the
checker BLOCKS version, safety, accreditation and data violations.
