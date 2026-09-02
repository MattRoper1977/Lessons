#!/usr/bin/env bash
# VB run 11 battery for one deck on the classic chassis (v2). Usage: battery11.sh "<Family>" <deck> <prefix>
set -u; cd /home/user/Lessons
export RSH_CHROMIUM_PATH=/opt/pw-browsers/chromium FEB_CHROMIUM_PATH=/opt/pw-browsers/chromium CODEX_PRIMARY_RUNTIME_NODE_MODULES=/opt/node22/lib/node_modules
FAM="$1"; L="$2"; PX="$3"; EV=_sownb/vb/evidence/run11/decks; mkdir -p $EV
say(){ printf '  %-12s %s\n' "$1" "$2"; }
st(){ python3 -c "import json;d=json.load(open('$1'));print(d.get('status') or d.get('verdict'))" 2>/dev/null || echo ERR; }
node _sownb/feb/tools/render_measure.js candidate "$L" >/dev/null 2>&1; RC=$?
PDF=_sownb/rsh/output/candidate/candidate/candidate-a4.pdf
python3 _sownb/feb/tools/contact_sheets.py candidate >/dev/null 2>&1
say render "exit=$RC pdf=$( [ -s $PDF ] && echo present || echo MISSING )"
python3 _sownb/vb/tools/g16_v2.py --family "$FAM" --file "$L" --output $EV/${PX}_g16v2.json >/dev/null 2>&1; say g16v2 "$(st $EV/${PX}_g16v2.json)"
python3 _sownb/feb/tools/g18_content_floor.py "$L" _sownb/rsh/output/candidate/contact_metrics.json $EV/${PX}_g18feb.json >/dev/null 2>&1; say g18feb "$(st $EV/${PX}_g18feb.json)"
python3 _sownb/vb/tools/g18_v2_rebind.py --candidate "$L" --family "$FAM" --v1 $EV/${PX}_g18feb.json --output $EV/${PX}_g18.json >/dev/null 2>&1; say g18rebind "$(st $EV/${PX}_g18.json)"
python3 _sownb/feb/tools/g11_family_similarity.py --family "$FAM" --candidate "$L" --g18 $EV/${PX}_g18.json --output $EV/${PX}_g11.json >/dev/null 2>&1; say g11 "$(st $EV/${PX}_g11.json)"
python3 _sownb/feb/tools/g10_role_classification.py --file "$L" --output $EV/${PX}_g10.json >/dev/null 2>&1; say g10 "$(st $EV/${PX}_g10.json)"
node _sownb/feb/tools/g15_guidance_hidden.js "$L" $EV/${PX}_g15.json >/dev/null 2>&1; say g15 "$(st $EV/${PX}_g15.json)"
node _sownb/feb/tools/render_installation_gate.js "$L" $EV/${PX}_rig.json >/dev/null 2>&1; say rig "$(st $EV/${PX}_rig.json)"
python3 _sownb/feb/tools/g19_token_ownership.py --config _sownb/vb/G19_TOKEN_OWNERSHIP_v2.json --family "$FAM" --file "$L" --output $EV/${PX}_g19v2.json >/dev/null 2>&1; say g19v2 "$(st $EV/${PX}_g19v2.json)"
python3 _sownb/feb/tools/s24_print.py "$L" $PDF $EV/${PX}_s24.json >/dev/null 2>&1; say s24 "$(st $EV/${PX}_s24.json)"
python3 _sownb/feb/tools/running_heads_pdf.py $PDF $EV/${PX}_heads.json --expect "$FAM" >/dev/null 2>&1; say heads "$(st $EV/${PX}_heads.json)"
python3 _sownb/feb/tools/g21_trailing_sheet.py $PDF $EV/${PX}_g21.json >/dev/null 2>&1; say g21 "$(st $EV/${PX}_g21.json)"
python3 _sownb/vb/tools/g18_v2_family_floor.py --family "$FAM" --candidate "$L" --output $EV/${PX}_g18v2.json >/dev/null 2>&1; say g18v2 "$(python3 _sownb/vb/tools/g18_v2_family_floor.py --family "$FAM" --candidate "$L" 2>/dev/null | tail -1 | grep -o 'BINDING=[A-Z]*')"
python3 _sownb/vb/tools/g23_period_load.py --family "$FAM" --candidate "$L" --scope new --output $EV/${PX}_g23.json >/dev/null 2>&1; say g23 "$(python3 _sownb/vb/tools/g23_period_load.py --family "$FAM" --candidate "$L" --scope new 2>/dev/null | tail -1 | grep -o 'x[0-9.]* .*ceiling<=1.5 [A-Z]*')"
for g in g24 g25 g26; do python3 _sownb/vb/tools/${g}_*.py --scope=new "$L" > /tmp/$g.txt 2>&1; say $g "$(tail -1 /tmp/$g.txt | cut -c1-120)"; python3 - "$g" "$PX" "$L" <<'PY'
import json,sys
g,px,deck=sys.argv[1:4]
try: d=json.load(open(f'/tmp/{g}_last.json'))
except Exception: d={'status':'ERR'}
json.dump({'file':deck,'subject':f'{g} on the run-11 reshelled deck','rows':d},open(f'_sownb/vb/evidence/run11/decks/{px}_{g}.json','w'),indent=1)
PY
done
python3 - "$PX" "$L" "$PDF" <<'PY'
import json,sys,pymupdf
px,deck,pdf=sys.argv[1:4]
d=pymupdf.open(pdf); chars=sum(len(p.get_text().strip()) for p in d); blank=[i+1 for i,p in enumerate(d) if not p.get_text().strip()]
json.dump({'file':deck,'subject':'rendered pagination of the run-11 candidate (screen render to A4 by render_measure)','pages':d.page_count,'chars':chars,'blankPages':blank,'verdict':'PASS' if not blank else 'CHECK'},open(f'_sownb/vb/evidence/run11/decks/{px}_pagination.json','w'),indent=1)
print(f"  {'pagination':12} pages={d.page_count} chars={chars} blank={blank or 'none'}")
PY
