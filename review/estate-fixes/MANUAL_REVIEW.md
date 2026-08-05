# Manual-review queue retained from the estate audit

These items are deliberately **not auto-patched** because placement, wording or
visual intent needs Matt/Claude review rather than an engineering guess.

## Orphan content after `</html>`

The following files contain teaching boxes appended after the document has
already closed. Browsers recover, but the intended slide/section is ambiguous.
Move each block into its intended lesson slide rather than merely hiding or
deleting it:

- `2 Physics 10/L1_Circuits_Symbols_Series_Parallel-1.html`
- `2 Physics 10/L2_Voltage_Current_Resistance-1.html`
- `2 Physics 10/L4_Wave_Properties_Definitions-1.html`
- `2 Physics 10/L5_Wave_Speed_Equation-1.html`
- `2 Physics 10/L6_Waves_Context_Reflection_Refraction-1.html`

`biology/Digestion_and_Absorption (1).html` is included in patch 0003 because the
orphaned memory trick has one unambiguous home: the Enzymes & Bile independent
work slide.

## Other structural HTML warnings

- `6 Art/Surrealism_Eye_Study_v5.html`: body closes while a `div` remains open.
- `Build/Slideshows/BUILD_HUM_W2_History_Detectives.html`: two malformed tag-name
  parse warnings near line 152.
- `primary/index.html`: two invalid comment sequences near line 10.

## Broad advisory backlog

The corrected audit records advisory—not release-blocking—warnings for:

- controls that may lack explicit accessible names;
- raw ampersands that HTML5 repairs but should be encoded as `&amp;`;
- six specialist/print pages without a viewport declaration;
- GitHub Pages API evidence endpoints returning permission/availability warnings.

The complete CSV/JSON evidence remains the source of truth. Do not mass-edit
pupil-facing files solely to reduce a warning count; group and render-review each
fix family.
