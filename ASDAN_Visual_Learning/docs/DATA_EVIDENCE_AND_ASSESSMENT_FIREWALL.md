# ASDAN data, evidence and assessment firewall

## Status

This toolkit is a **visual rehearsal layer**. It is not an upload workflow, portfolio studio, evidence register, assessment engine, moderation tool or certification system.

It follows the repository’s existing ASDAN-specific data and acceptance rules. Those source files remain authoritative.

## Prohibited data

The toolkit must never ask for, capture, infer, store or transmit:

- full pupil names or contact details;
- diagnoses, support needs, disclosures or safeguarding information;
- real bank statements, benefits letters, bills, payslips, account balances or banking-app screens;
- medical, identity, tenancy or other personal documents;
- an identifiable audience member or unapproved photograph, video or audio;
- a fabricated partner response, witness statement, performance or audience record;
- an adult-written reflection presented as the pupil’s meaning.

Fictional examples must be clearly fictional. Real personal documents are replaced by produced exemplars.

## Prohibited assessment actions

The toolkit must never:

- select or assign a qualification level;
- infer a criterion code;
- guess a unit mapping;
- mark a criterion achieved;
- create a grade or score that looks like one;
- move an item through evidence states;
- claim moderation, verification, certification or qualification completion;
- issue a portfolio next step from an automated result;
- treat screen completion as evidence.

Where a mapping is unknown, the correct wording is **not yet mapped**.

## Technical controls

The core JavaScript contains no use of:

- `localStorage`;
- `sessionStorage`;
- IndexedDB;
- cookies;
- `fetch`, XMLHttpRequest, WebSocket or beacon;
- camera, microphone or media-device APIs;
- clipboard write;
- file upload;
- geolocation;
- free-text evidence capture.

All state exists only in the current page’s DOM and memory. Reloading resets it.

## LAUNCH structured evidence locator

After a LAUNCH investigation, pupils choose one option in each group.

### What exists?

- Real task, product or action exists.
- Authentic observation, calculation or decision exists.
- Authentic feedback or witness evidence exists.
- Evidence is not yet available.

### Where is it?

- Lesson sheet or physical work.
- Authorised photo or record.
- Witness or feedback record.
- Not yet located.

### What is the next authorised route?

- Teacher or assessor review.
- Responsible-adult safety or permission check.
- Complete one authentic addition.
- Use the approved access or reasonable-adjustment route.

The locator does not label the item’s evidence state. It simply rehearses where the pupil and adult should look next.

## Visible pupil notice

Every panel displays:

> Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.

## Teacher and access route

Every panel displays that teacher, TA, assessor, responsible-adult, safety and reasonable-adjustment routes remain authoritative. The visual activity cannot approve a risk, permission, level, criterion or qualification outcome.

## Temporary provenance

When an explanation opens, the panel may receive a temporary DOM attribute. For LAUNCH it is:

```html
data-asdan-opened-by="completed activity and selected structured evidence-locator route"
```

This records how the interface opened. It is not a receipt, evidence state, learner record or upload. It disappears on reload.

## Safeguarding boundary

If a disclosure or data hazard appears during a curation, reflection, witness or audience conversation, the lesson task stops and the concern leaves the ordinary evidence workflow entirely through the setting’s DSL route. It must not be copied into the visual panel, portfolio caption, witness statement or temporary queue.

## Review checks

Before any commit or deployment:

- scan the toolkit and generated source patch for prohibited APIs;
- confirm no text input, upload or capture control exists;
- inspect all money/admin examples for fictional data;
- inspect audience/project lessons for invented responses;
- confirm “not yet” options remain available;
- confirm the explanation is not described as assessment;
- confirm all real evidence actions route to an authorised adult/process;
- run the repository’s current safeguarding and claims checks.
