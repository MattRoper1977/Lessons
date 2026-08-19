#!/usr/bin/env node
// ECA-1 Track B — British English scan. PROSE stream only (CODE = script/style contents
// exempt by construction; the exemption universe = every <script>/<style> block in the
// scanned files). Reports word + 60-char context per hit for human classification.
const fs = require('fs');
const { execSync } = require('child_process');
const { splitCode, visibleText } = require('./lib');

// US form → expected UK form. Word-boundary, case-insensitive; proper-noun and
// verbatim-quote hits are classified by the reader, not auto-fixed.
const PAIRS = [
  ['organize', 'organise'], ['organizing', 'organising'], ['organized', 'organised'], ['organization', 'organisation'],
  ['recognize', 'recognise'], ['recognized', 'recognised'], ['realize', 'realise'], ['realized', 'realised'],
  ['emphasize', 'emphasise'], ['summarize', 'summarise'], ['analyze', 'analyse'], ['analyzed', 'analysed'],
  ['specialize', 'specialise'], ['specialized', 'specialised'], ['prioritize', 'prioritise'], ['prioritized', 'prioritised'],
  ['personalize', 'personalise'], ['personalized', 'personalised'], ['finalize', 'finalise'], ['finalized', 'finalised'],
  ['apologize', 'apologise'], ['criticize', 'criticise'], ['memorize', 'memorise'], ['visualize', 'visualise'],
  ['color', 'colour'], ['colors', 'colours'], ['colored', 'coloured'], ['colorful', 'colourful'],
  ['center', 'centre'], ['centers', 'centres'], ['centered', 'centred'],
  ['meter', 'metre'], ['meters', 'metres'], ['liter', 'litre'], ['liters', 'litres'],
  ['fiber', 'fibre'], ['theater', 'theatre'], ['behavior', 'behaviour'], ['behaviors', 'behaviours'],
  ['favorite', 'favourite'], ['favorites', 'favourites'], ['honor', 'honour'], ['labor', 'labour'],
  ['neighbor', 'neighbour'], ['neighbors', 'neighbours'], ['neighborhood', 'neighbourhood'],
  ['practicing', 'practising'], ['practiced', 'practised'],
  ['defense', 'defence'], ['offense', 'offence'], ['license', 'licence'],
  ['traveled', 'travelled'], ['traveling', 'travelling'], ['traveler', 'traveller'],
  ['modeling', 'modelling'], ['modeled', 'modelled'], ['labeled', 'labelled'], ['labeling', 'labelling'],
  ['jewelry', 'jewellery'], ['gray', 'grey'], ['mold', 'mould'], ['molds', 'moulds'], ['molding', 'moulding'],
  ['skillful', 'skilful'], ['fulfill', 'fulfil'], ['fulfillment', 'fulfilment'], ['enrollment', 'enrolment'],
  ['catalog', 'catalogue'], ['dialog', 'dialogue'], ['artifact', 'artefact'], ['artifacts', 'artefacts'],
  ['acknowledgment', 'acknowledgement'], ['judgment', 'judgement'], ['judgments', 'judgements'],
  ['math ', 'maths '], ['gotten', 'got'], ['vacation', 'holiday'], ['learned skill', 'learnt skill'],
  ['aluminum', 'aluminium'], ['gasoline', 'petrol'], ['sidewalk', 'pavement'], ['fall term', 'autumn term'],
];

const files = process.argv.length > 2 ? process.argv.slice(2) :
  execSync("git ls-files '*.html'", { encoding: 'utf8' }).trim().split('\n')
    .filter(f => /^(BUILD_ASDAN|GROW_ASDAN|LAUNCH_ASDAN|Art_Teesside|Humanities_Teesside)\//.test(f)
      || /^(Build|Grow|Launch)\/Slideshows\/[A-Z]+_(DT|HUM)_/.test(f));

let hits = 0;
for (const f of files) {
  const { prose } = splitCode(fs.readFileSync(f, 'utf8'));
  const text = visibleText(prose);
  for (const [us, uk] of PAIRS) {
    const re = new RegExp('\\b' + us.replace(/ $/, '\\b ') + (us.endsWith(' ') ? '' : '\\b'), 'gi');
    let m;
    while ((m = re.exec(text)) !== null) {
      const ctx = text.slice(Math.max(0, m.index - 45), m.index + us.length + 45).trim();
      console.log(`${f}\t${us}->${uk}\t…${ctx}…`);
      hits++;
    }
  }
}
console.error(`ukscan: ${hits} hits over ${files.length} files`);
