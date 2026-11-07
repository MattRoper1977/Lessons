/* Virtual Chemistry Lab PRO Spatial v0.3 — release/ -> staging/ as a stated
 * list of transforms.
 *
 * Same discipline as tools/fieldops: every transform is an exact-string swap
 * that MUST match exactly once, or it throws. Drop all of them and the builder
 * hands back release byte for byte, so nothing can hide in the shipped file.
 *
 * V0 FREEZE, honoured throughout: the qualitative reaction engine and its
 * observation strings, the pH model, the deterministic mystery hash, the
 * sequencing teaching copy, the safety banner and the 40-minute arc are not
 * edited. Where a repair needs a string that does not exist yet, a NEW one is
 * added on a NEW code path and declared — no frozen string is rewritten.
 *
 * Usage: node build.mjs [--drop=X1a,X2 ...] [--out=staging]
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.env.VCL_ROOT || path.dirname(new URL(import.meta.url).pathname);
const DROP = new Set(
  (process.argv.find(a => a.startsWith('--drop=')) || '').replace('--drop=', '')
    .split(',').filter(Boolean));
const OUT = (process.argv.find(a => a.startsWith('--out=')) || '--out=staging').slice(6);
const FILE = 'Virtual_Chemistry_Lab_PRO_Spatial_v0_3.html';

let src = fs.readFileSync(path.join(ROOT, 'release', FILE), 'utf8');
const applied = [];

function swap(id, from, to) {
  if (DROP.has(id)) { applied.push(`${id} DROPPED`); return; }
  const n = src.split(from).length - 1;
  if (n !== 1) throw new Error(`${id}: expected exactly 1 occurrence, found ${n}\n  ${from.slice(0, 140)}`);
  src = src.replace(from, to);
  applied.push(id);
}

/* =====================================================================
 * V1 — the bench rewards the procedure it teaches against.  MERGE-BLOCKER.
 *
 * microResolve rebuilds the well from an ORDER-INDEPENDENT ion pool on every
 * drop and the sequencing check is presence-only: drop("reagent_hno3") > 0.
 * Silver nitrate first, then nitric acid, gives a byte-identical clean
 * positive to doing it correctly, with no warning at all.
 *
 * The model is untouched. Only the predicate changes: the acidification must
 * come BEFORE the silver or barium in w.drops, which is already an ordered
 * array. Every existing observation and warning string is reused verbatim; the
 * one new string is for the case that currently has no words at all — a
 * precipitate formed out of sequence — and it is chemically the honest thing
 * to say, because carbonate, sulfite and hydroxide precipitate with silver too.
 * ===================================================================== */
swap('X1a',
  `const nitric=drop("reagent_hno3")>0,silver=drop("reagent_agno3")>0;if(silver){if(has("CO3")&&!nitric){w.ppt={name:"silver carbonate interference",formula:"Ag₂CO₃",colour:"#e7d66b"};w.observation="A pale yellow carbonate interference forms because the sample was not acidified with nitric acid first.";w.warnings.push("Acidify a fresh portion with nitric acid before adding silver nitrate.");}
    else if(nitric&&has("Cl")){w.ppt={name:"silver chloride",formula:"AgCl",colour:"#f7f7f4"};w.observation="A white silver chloride precipitate forms.";}
    else if(nitric&&has("Br")){w.ppt={name:"silver bromide",formula:"AgBr",colour:"#f1e5aa"};w.observation="A cream silver bromide precipitate forms.";}
    else if(nitric&&has("I")){w.ppt={name:"silver iodide",formula:"AgI",colour:"#e8c93f"};w.observation="A yellow silver iodide precipitate forms.";}
    else if(!nitric)w.warnings.push("The halide test should use a fresh portion acidified with dilute nitric acid before silver nitrate is added.");}`,
  `const nitric=acidFirst("reagent_hno3","reagent_agno3"),silver=drop("reagent_agno3")>0;if(silver){if(has("CO3")&&!nitric){w.ppt={name:"silver carbonate interference",formula:"Ag₂CO₃",colour:"#e7d66b"};w.observation="A pale yellow carbonate interference forms because the sample was not acidified with nitric acid first.";w.warnings.push("Acidify a fresh portion with nitric acid before adding silver nitrate.");}
    else if(nitric&&has("Cl")){w.ppt={name:"silver chloride",formula:"AgCl",colour:"#f7f7f4"};w.observation="A white silver chloride precipitate forms.";}
    else if(nitric&&has("Br")){w.ppt={name:"silver bromide",formula:"AgBr",colour:"#f1e5aa"};w.observation="A cream silver bromide precipitate forms.";}
    else if(nitric&&has("I")){w.ppt={name:"silver iodide",formula:"AgI",colour:"#e8c93f"};w.observation="A yellow silver iodide precipitate forms.";}
    else if(!nitric){if(has("Cl")||has("Br")||has("I")){w.ppt={name:"unacidified silver precipitate",formula:"Ag⁺ + unacidified sample",colour:"#ece9df"};w.observation="A pale precipitate forms, but the silver nitrate went in before the nitric acid. Carbonate, sulfite and hydroxide precipitate with silver as well, so an unacidified result cannot be read as a halide test.";}w.warnings.push("The halide test should use a fresh portion acidified with dilute nitric acid before silver nitrate is added.");}}`);

swap('X1b',
  `const hcl=drop("reagent_hcl")>0,barium=drop("reagent_bacl2")>0;if(barium&&hcl&&has("SO4")){w.ppt={name:"barium sulfate",formula:"BaSO₄",colour:"#fafaf7"};w.observation="A dense white barium sulfate precipitate forms.";}else if(barium&&!hcl)w.warnings.push("For the sulfate test, acidify a fresh portion with dilute hydrochloric acid before adding barium chloride.");`,
  `const hcl=acidFirst("reagent_hcl","reagent_bacl2"),barium=drop("reagent_bacl2")>0;if(barium&&hcl&&has("SO4")){w.ppt={name:"barium sulfate",formula:"BaSO₄",colour:"#fafaf7"};w.observation="A dense white barium sulfate precipitate forms.";}else if(barium&&!hcl){if(has("SO4")){w.ppt={name:"unacidified barium precipitate",formula:"Ba²⁺ + unacidified sample",colour:"#f2f1ec"};w.observation="A white precipitate forms, but the barium chloride went in before the hydrochloric acid. Carbonate and sulfite give white barium precipitates too, so an unacidified result cannot be read as a sulfate test.";}w.warnings.push("For the sulfate test, acidify a fresh portion with dilute hydrochloric acid before adding barium chloride.");}`);

/* the predicate itself: index of first acid drop must precede index of first
   test-reagent drop. Presence alone is what the release build checked. */
swap('X1c',
  `  w.ppt=null;w.observation="Clear solution; no characteristic change.";const has=k=>(pool[k]||0)>1e-10,drop=k=>(counts[k]||0);`,
  `  w.ppt=null;w.observation="Clear solution; no characteristic change.";const has=k=>(pool[k]||0)>1e-10,drop=k=>(counts[k]||0);
  const acidFirst=(acid,test)=>{const ia=w.drops.indexOf(acid),it=w.drops.indexOf(test);return ia>=0&&(it<0||ia<it);};`);

/* =====================================================================
 * V2 — the pupil's name is in the URL and the label says it is not.
 *      MERGE-BLOCKER.
 *
 * The field is captioned "Name for print/export only". syncHash() base64url-
 * encodes the whole of state, state.pupil included, into location.hash on
 * every action, and Share copies location.href.
 *
 * pupil is excluded from the serialiser, which makes the existing caption
 * true. notes is KEPT, deliberately: this app has zero localStorage, so the
 * hash is its only persistence and dropping notes would destroy a pupil's
 * written conclusion on reload. The Share help card is corrected instead, so
 * nothing on screen misdescribes what the link carries.
 * ===================================================================== */
swap('X2a',
  `  const copy=JSON.parse(JSON.stringify(state));copy.version="0.3";`,
  `  const copy=JSON.parse(JSON.stringify(state));copy.version="0.3";
  /* THE URL CARRIES THE SETUP. IT NEVER CARRIES THE PUPIL'S WORK.
     Out: the name, the evidence note, the written answers. (v0.4's drawing
     strokes belong in this list too when this diff is re-applied there.)
     Retained: bench, apparatus, sample codes, teacher fault injection —
     everything Share exists to hand over.
     Share hands the URL out. A teacher sharing a bench setup would otherwise be
     shipping whichever pupil's answers were last typed. */
  delete copy.pupil; delete copy.notes; delete copy.phaseAnswers;`);
/* Export JSON must carry everything the URL now refuses to: the name, the
   evidence note and the written answers. The caption tells a pupil to use Print
   or Export JSON before closing the tab, so those two paths are the only place
   the work survives — a serialiser fix that quietly emptied them would turn that
   instruction into a lie. Caught twice by the same control: once for the name,
   and again for the answers when the ruling widened what leaves the URL. */
swap('X2d',
  `const payload={schema:"virtual-chem-lab-evidence/0.3",exportedAt:nowISO(),state:serialisableState()};`,
  `const payload={schema:"virtual-chem-lab-evidence/0.3",exportedAt:nowISO(),state:{...serialisableState(),pupil:state.pupil,notes:state.notes,phaseAnswers:state.phaseAnswers}};`);

/* V3, second lever: a well's colour, ppt, pH, observation, warnings, pool and
   counts are ALL derived from its drops by microResolve. Encoding them costs
   2,753 characters of a 4,763-character payload and tells the URL nothing the
   drops do not. The state model is unchanged — they are recomputed on load. */
swap('X3c',
  `  copy.spatial.snapHint=null;copy.spatial.pouring=null;copy.spatial.examSVG="";return copy;`,
  `  copy.spatial.snapHint=null;copy.spatial.pouring=null;copy.spatial.examSVG="";
  /* wells become bare ordered drop lists: id and name are positional constants,
     and everything else microResolve computes. Events lose their timestamp
     (never displayed), carry the well INDEX rather than its name, and the
     reagent KEY rather than its display name. Nothing a teacher can see is
     dropped — all of it is rebuilt on load. */
  copy.micro.wells=copy.micro.wells.map(w=>w.drops.slice());
  copy.micro.events=copy.micro.events.map(e=>[MICRO_WELL_NAMES.indexOf(e.well),microKeyByName()[e.reagent]||e.reagent]);
  return copy;`);
swap('X3e',
  `function makeMicroState(){`,
  `const MICRO_WELL_NAMES=["A1","A2","A3","A4","B1","B2","B3","B4","C1","C2","C3","C4"];
/* LAZY, and deliberately so. The first cut of this was an IIFE const, which
   evaluated here — 400 lines ABOVE where microSamples is declared — and died in
   its temporal dead zone. Same trap the estate has hit three times before. */
let _microKeyByName=null;
function microKeyByName(){if(!_microKeyByName){_microKeyByName={};for(const [k,v] of Object.entries({...microSamples,...microReagents}))_microKeyByName[v.name]=k;}return _microKeyByName;}
function makeMicroState(){`);
swap('X3d',
  `    state.version="0.3";state.rates.running=false;state.rates.activeRun=null;`,
  `    /* rebuild the wells and the event log from what was encoded. Accepts both
       the compact form and the whole-tree form an older link carries. */
    {const fresh2=makeMicroState();
     state.micro.wells=fresh2.wells.map((base,i)=>{
       const enc=(state.micro.wells||[])[i];
       const drops=Array.isArray(enc)?enc:(enc&&Array.isArray(enc.drops)?enc.drops:[]);
       const w=Object.assign({},base,(enc&&!Array.isArray(enc))?enc:{},{drops,warnings:[]});
       if(drops.length)microResolve(w);
       return w;});
     /* The event log stores the observation AT THAT MOMENT, not the well's
        final state — three drops into one well are three different rows on the
        release build. Assigning the final observation to all of them looked
        right and quietly flattened the evidence table, so the logged drops are
        replayed instead. The scratch well is seeded with whatever drops predate
        the logged window, so a session longer than the 60-entry cap still
        replays exactly rather than approximately. */
     const compact=(state.micro.events||[]).filter(Array.isArray);
     if(compact.length){
       const scratch=makeMicroState().wells;
       const loggedPerWell={};for(const [wi] of compact)loggedPerWell[wi]=(loggedPerWell[wi]||0)+1;
       for(const wi of Object.keys(loggedPerWell)){
         const full=state.micro.wells[wi]?state.micro.wells[wi].drops:[];
         const pre=full.slice(0,Math.max(0,full.length-loggedPerWell[wi]));
         scratch[wi].drops=pre.slice();if(pre.length)microResolve(scratch[wi]);
       }
       const replayed=[];
       for(const [wi,key] of compact.slice().reverse()){
         const w=scratch[wi];if(!w)continue;
         w.drops.push(key);microResolve(w);
         replayed.push({at:0,well:w.name,reagent:(microCatalogue(key)||{}).name||key,observation:w.observation});
       }
       state.micro.events=replayed.reverse();
     }else{
       state.micro.events=(state.micro.events||[]).map(e=>e.observation?e:{...e,observation:(state.micro.wells.find(x=>x.name===e.well)||{}).observation||""});
     }}
    state.version="0.3";state.rates.running=false;state.rates.activeRun=null;`);

swap('X2b',
  `<div class="help-card"><h3>Share</h3><p>Encodes the current bench, settings and logged evidence into the URL fragment. No account or server is required.</p></div>`,
  `<div class="help-card"><h3>Share</h3><p>Encodes the current bench, apparatus, settings and logged evidence into the URL fragment. Your name, your evidence note and your written answers are <strong>not</strong> included — a shared link carries the setup, never your work. Keep those with Print or Export JSON. No account or server is required.</p></div>`);
/* The honest version of the cost this ruling accepts: with no localStorage
   anywhere in this app, work that is not in the URL is not saved at all. The
   caption says so rather than letting a pupil discover it by reloading. */
swap('X2c',
  `      <label for="reflectionNotes">Evidence note / conclusion</label>`,
  `      <label for="reflectionNotes">Evidence note / conclusion <span style="font-weight:600;opacity:.75">— not saved and not shared. Use Print or Export JSON before you close this tab.</span></label>`);

/* =====================================================================
 * V3 — the state URL is already over the common ceiling.
 *
 * Measured on the release build: 3,814 characters on a fresh spatial bench.
 * 2,048 is still a real limit in link handlers, previews and QR paths, so
 * Share is least reliable exactly when there is something worth sharing.
 *
 * The state model is NOT changed. Only what gets encoded: keys whose value is
 * identical to initialState() are pruned, so untouched benches cost nothing.
 * initialState() is deterministic — no Math.random(), no Date.now() — which is
 * what makes the delta safe to rehydrate against.
 * ===================================================================== */
swap('X3a',
  `function syncHash(){
  try{const token=base64urlEncode(serialisableState());`,
  `/* Structure-preserving delta. Arrays are all-or-nothing: micro.wells must
   survive as 12 entries or loadHash's own guard replaces it wholesale. */
function pruneToDelta(cur,base){
  if(cur===null||typeof cur!=="object")return cur;
  if(Array.isArray(cur))return JSON.stringify(cur)===JSON.stringify(base)?undefined:cur;
  const out={};
  for(const k of Object.keys(cur)){
    const c=cur[k],b=(base&&typeof base==="object")?base[k]:undefined;
    if(JSON.stringify(c)===JSON.stringify(b))continue;
    const nested=(c&&typeof c==="object"&&!Array.isArray(c)&&b&&typeof b==="object"&&!Array.isArray(b))?pruneToDelta(c,b):c;
    if(nested===undefined)continue;
    if(nested&&typeof nested==="object"&&!Array.isArray(nested)&&Object.keys(nested).length===0)continue;
    out[k]=nested;
  }
  return out;
}
function hydrateDelta(delta,base){
  if(delta===null||typeof delta!=="object"||Array.isArray(delta))return delta;
  const out=Array.isArray(base)?base:{...(base&&typeof base==="object"?base:{})};
  for(const k of Object.keys(delta)){
    const d=delta[k],b=out[k];
    out[k]=(d&&typeof d==="object"&&!Array.isArray(d)&&b&&typeof b==="object"&&!Array.isArray(b))?hydrateDelta(d,b):d;
  }
  return out;
}
function baselineState(){
  /* the SAME reduction applied to a fresh state, so an untouched bench prunes
     to nothing. Comparing a reduced tree against an unreduced baseline is what
     made the first cut of this encode 567 characters on a fresh load. */
  const b=initialState();
  b.micro.wells=b.micro.wells.map(w=>w.drops.slice());
  b.micro.events=[];
  b.spatial.snapHint=null;b.spatial.pouring=null;b.spatial.examSVG="";
  b.rates.running=false;b.rates.activeRun=null;
  return b;
}
function syncHash(){
  try{const full=serialisableState();const delta=pruneToDelta(full,baselineState());delta.version=full.version;const token=base64urlEncode(delta);`);

/* X3b is deliberately absent. A hydrate-the-delta-against-a-fresh-state step
   was written here and the removal matrix reported it UNWATCHED: loadHash
   already merges every top-level branch it cares about as
   {...fresh.micro, ...incoming.micro}, so a one-level delta rehydrates without
   it. Rather than invent a control for a step that protects nothing, the step
   went. V3-roundtrip and V3-legacy both stay green without it, which is the
   evidence for that claim.
   The decode side that DOES matter is X3d, which rebuilds what the compact
   encoding stopped storing. */

/* =====================================================================
 * V4 — .drop-pill has no CSS rule at all.
 *
 * The class appears exactly once in the file, in the template. The pills are
 * joined with "" so they render as run-together text: "1x FeCl3 . 0.10 M1x
 * NaOH . 0.40 M". The look is derived from the .var-tag / chip idiom already
 * in the stylesheet rather than inventing a second visual language.
 * ===================================================================== */
swap('X4',
  `.var-tag{display:inline-flex;align-items:center;gap:6px;font-size:.68rem;font-weight:850;letter-spacing:.06em;text-transform:uppercase}`,
  `.drop-count-pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.drop-pill{display:inline-flex;align-items:center;padding:3px 9px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.04);font-size:.68rem;font-weight:750;line-height:1.5;white-space:nowrap}
.var-tag{display:inline-flex;align-items:center;gap:6px;font-size:.68rem;font-weight:850;letter-spacing:.06em;text-transform:uppercase}`);

/* =====================================================================
 * V5 — answer marking is negation-blind.  Option (a).
 *
 * "the glowing splint does not relight" was marked Correct: oxygen relights a
 * glowing splint. Every keyword item has that shape. Rather than guess at
 * negation, the keyword items stop claiming a verdict at all: they show the
 * model answer and say which ideas the learner's wording does and does not yet
 * mention. It cannot be wrong, which a keyword marker can always be.
 *
 * The items that compare a COMPUTED VALUE — the rate at 20 s, the concordant
 * titre, the concentration, the mystery identity — keep their verdict. Those
 * checks are arithmetic against state, not keyword presence, and downgrading
 * them would lose real marking. The order named six regexes; this covers
 * eight, because rates-0 and gastest-2 have the identical defect written a
 * different way. That widening is deliberate and declared.
 * ===================================================================== */
swap('X5a',
  `function checkPhase(i){
  const bench=state.bench,input=$(\`#phase-\${bench}-\${i}\`),fb=$(\`#phase-fb-\${bench}-\${i}\`);if(!input||!fb)return;
  const raw=input.value.trim(),low=raw.toLowerCase();state.phaseAnswers[bench][i]=raw;
  let ok=false,msg="";`,
  `/* Items whose check is keyword presence. Each carries the model answer (the
   wording the release build used when it thought the answer was right) and the
   ideas it looks for, so the feedback can say what is and is not mentioned
   without ever pronouncing a verdict. */
const PHASE_COMPARE={
  rates:{0:{model:"Higher concentration means more reacting particles per unit volume, so successful collisions occur more frequently.",
            ideas:[["the direction of the rate change",/(increase|faster|steep|greater|decrease|slower)/],
                   ["collision theory",/(collision|particle|frequency|successful)/]]}},
  titration:{0:{model:"Residual water would dilute the titrant and change its effective concentration.",
                ideas:[["dilution or concentration",/(dilut|concentr)/],["the water left inside the burette",/(water|contamin)/]]}},
  gastest:{0:{model:"Oxygen relights a glowing splint.",
              ideas:[["the glowing splint",/(glow|glowing)/],["what the splint does",/(relight|re-light|relights)/]]},
           2:{model:"State the gas, then the observation that identifies it: \\u201cThe gas is ___ because ___\\u201d.",
              ideas:[["a named gas",/(oxygen|hydrogen|carbon dioxide|chlorine|ammonia)/],
                     ["a reason",/(because|since|as )/],["the observed test result",/(splint|limewater|litmus|pop|relight|bleach|milky)/]]}},
  spatial:{0:{model:"Close the air hole for an easily visible yellow safety flame, which also reduces strike-back risk during ignition.",
              ideas:[["the air hole or collar",/(air ?hole|collar)/],["the closed / yellow safety flame",/(clos|yellow|safety)/],
                     ["why that is safer when lighting",/(strike|safe|visible|light)/]]},
           2:{model:"Simulated reasoning evidence is not proof of real handling and safety competence.",
              ideas:[["a real hands-on competence",/(hands|physical|manual|dexterity|real|competenc|chemical|glass|safety)/],
                     ["a limitation",/(cannot|not|doesn|limitation|but)/]]}},
  microscale:{0:{model:"Fe\\u00b3\\u207a gives a red-brown Fe(OH)\\u2083 precipitate with sodium hydroxide.",
                 ideas:[["the red-brown colour",/(red.?brown|brown)/],["iron(III) hydroxide",/(fe|iron|hydroxide|oh)/]]},
              2:{model:"Hydrochloric acid would introduce chloride ions and could create a false AgCl result; nitric acid does not add a tested halide.",
                 ideas:[["the chloride ion",/(chloride|cl-|cl\\u207b|chlor)/],
                        ["the false positive",/(false|interfer|precipitate|silver chloride|agcl)/],
                        ["nitric acid",/(nitric|nitrate)/]]}},
};
function comparePhase(bench,i,raw,fb){
  const spec=PHASE_COMPARE[bench]&&PHASE_COMPARE[bench][i];if(!spec)return false;
  const low=raw.toLowerCase();
  const hit=spec.ideas.filter(([,re])=>re.test(low)).map(([label])=>label);
  const missing=spec.ideas.filter(([,re])=>!re.test(low)).map(([label])=>label);
  fb.className="feedback";
  const parts=[];
  if(!raw)parts.push("Write an answer, then compare it with the model.");
  else{
    if(hit.length)parts.push("Your answer mentions "+hit.join(", ")+".");
    if(missing.length)parts.push("It does not yet mention "+missing.join(", ")+".");
    if(!missing.length)parts.push("It covers every idea the model answer uses \\u2014 read both and decide whether yours says the same thing.");
  }
  parts.push("Model answer: "+spec.model);
  fb.textContent=parts.join(" ");
  LabAudio.drop();
  return true;
}
function checkPhase(i){
  const bench=state.bench,input=$(\`#phase-\${bench}-\${i}\`),fb=$(\`#phase-fb-\${bench}-\${i}\`);if(!input||!fb)return;
  const raw=input.value.trim(),low=raw.toLowerCase();state.phaseAnswers[bench][i]=raw;
  if(comparePhase(bench,i,raw,fb)){syncHash();return;}
  let ok=false,msg="";`);

/* the button stops saying "Check" where nothing is being checked */
swap('X5b',
  `        <button class="btn-primary" data-action="phase-check" data-phase="\${i}">Check</button>`,
  `        <button class="btn-primary" data-action="phase-check" data-phase="\${i}">\${(PHASE_COMPARE[bench]&&PHASE_COMPARE[bench][i])?"Compare":"Check"}</button>`);

/* =====================================================================
 * V6.4 — reduced motion: there is a CSS blanket rule but matchMedia is 0,
 * so the JS layer never knows. Ported from the shape Scrap Core v10 uses:
 * seed from the OS, keep an explicit user choice as the override.
 * ===================================================================== */
swap('X6c',
  `const initialState = () => ({
  version:"0.3",
  bench:"spatial",
  calm:false,`,
  `const SYSTEM_PREFERS_REDUCED_MOTION=(()=>{try{return !!(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches);}catch(e){return false;}})();
const initialState = () => ({
  version:"0.3",
  bench:"spatial",
  calm:SYSTEM_PREFERS_REDUCED_MOTION,`);

/* =====================================================================
 * V6.5 — accessible names.
 *
 * MEASURED, and it disagrees with the handover note's "3 controls with no
 * accessible name" depending on the predicate used:
 *   1 control has NO name of any kind          (#spatialMission)
 *   3 more have only a placeholder             (#phase-spatial-0/1/2 and the
 *                                               same three on every bench)
 * A placeholder is not an accessible name in every assistive technology and it
 * disappears as soon as the field has content, so all four are named here and
 * the predicate is stated rather than the number quoted loose.
 * ===================================================================== */
swap('X6d1',
  `<select id="spatialMission">`,
  `<select id="spatialMission" aria-label="Open spatial mission">`);
/* the gas-test identity select: missed by a first census that looked only at
   the default bench, found by one that switched through all five */
swap('X6d3',
  `        <select id="gasIdentity">`,
  `        <select id="gasIdentity" aria-label="Identify the unknown gas">`);
swap('X6d2',
  `        <input id="phase-\${bench}-\${i}" data-phase="\${i}" type="\${it.type}"`,
  `        <input id="phase-\${bench}-\${i}" data-phase="\${i}" aria-label="\${escapeHTML(it.title)}" type="\${it.type}"`);

fs.mkdirSync(path.join(ROOT, OUT), { recursive: true });
fs.writeFileSync(path.join(ROOT, OUT, FILE), src);
console.log(`built ${path.join(ROOT, OUT, FILE)}`);
for (const a of applied) console.log('  ' + a);
