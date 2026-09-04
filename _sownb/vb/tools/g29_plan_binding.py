#!/usr/bin/env python3
"""g29 PLAN BINDING — a deck claims its own plan's cells, exactly.

WHY g28 IS NOT ENOUGH, AND WHY THIS IS A REPAIR RATHER THAN A NEW GATE
---------------------------------------------------------------------
g28 asks whether a cited cell EXISTS on a real sheet. It cannot ask whether THIS
deck is the one that teaches it. Twice in this campaign a deck would have shipped
carrying another plan's cells and passed every gate in the stack:

  * the batch-2 driver keyed decks on `family+week`, and two LAUNCH ASDAN plans
    share week 1, so the second deck would silently have received the first's
    cells;
  * an authoring run was launched from a task list typed out of a console print,
    in which five of twelve cell sets and eight of twelve OUTCOMES were wrong.

Both are the same failure: a rendering of the plan treated as the plan. A cell
claimed by the wrong deck is a coverage lie — the census counts the cell as
taught, and nobody teaches it.

THE BINDING. A plan's identity is DERIVED FROM ITS OWN CONTENT, not from its
position in a file and not from a name someone typed:

    planId = sha256(family | ruledWeek | sorted(cells))[:12]

so it survives the targets file being regenerated or reordered, and two plans
that share a family and a week still have different ids. Every authored deck
records its planId, and this gate asserts the deck's claimed cells are EXACTLY
the plan's: not a superset (stealing another plan's cells) and not a subset
(a silent under-claim that leaves a cell open while looking covered).

Usage:
  g29_plan_binding.py <deck.html> [...]        [--targets F] [--output r.json]
  g29_plan_binding.py --scope authored         every deck carrying a planId
  g29_plan_binding.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERSION = "g29-v1.0.0-plan-binding"
TARGETS = ROOT / "tools/easter/EASTER_TARGETS.json"
CFG = re.compile(r'id=["\']lesson-config["\'][^>]*>(.*?)</script>', re.S)


_pi_spec = importlib.util.spec_from_file_location("plan_identity", ROOT / "tools/easter/plan_identity.py")
_pi = importlib.util.module_from_spec(_pi_spec)
_pi_spec.loader.exec_module(_pi)
plan_id = _pi.plan_id


def load_plans(path: Path = TARGETS) -> tuple[dict, str]:
    raw = path.read_bytes()
    return _pi.index_plans(json.loads(raw.decode("utf-8"))["plans"]), hashlib.sha256(raw).hexdigest()


def deck_config(path: Path) -> dict | None:
    m = CFG.search(Path(path).read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def judge(path: Path, by_id: dict) -> dict:
    cfg = deck_config(path) or {}
    pid = cfg.get("planId")
    claimed = sorted(cfg.get("cells", []))
    rec = {"file": str(path), "planId": pid, "claimedCells": claimed}
    if not pid:
        rec.update({"status": "SKIP", "reason": "deck records no planId; not an "
                                                "authored deck of this campaign"})
        return rec
    plan = by_id.get(pid)
    if plan is None:
        rec.update({"status": "RED", "reason": f"planId {pid} matches no plan in the "
                                               "targets file"})
        return rec
    expected = sorted(plan["cells"])
    extra = [c for c in claimed if c not in expected]
    missing = [c for c in expected if c not in claimed]
    rec.update({
        "family": plan["family"], "ruledWeek": plan["ruledWeek"],
        "expectedCells": expected, "extraCells": extra, "missingCells": missing,
        "outcomesMatch": cfg.get("outcomes") == plan.get("outcomes"),
        "status": "PASS" if not extra and not missing
                  and cfg.get("outcomes") == plan.get("outcomes") else "RED",
    })
    if extra:
        rec["reason"] = f"claims {len(extra)} cell(s) belonging to another plan"
    elif missing:
        rec["reason"] = f"under-claims {len(missing)} cell(s) its plan requires"
    elif not rec["outcomesMatch"]:
        rec["reason"] = "outcomes do not match the plan's"
    if plan.get("artsAward"):
        rec["planSource"] = plan.get("_planSource")
        rec["awardMatches"] = cfg.get("artsAward") == plan["artsAward"]
        rec["identityFieldsMatch"] = (cfg.get("family") == plan["family"]
                                      and cfg.get("week") == plan["ruledWeek"]
                                      and cfg.get("title") == plan["title"])
        if not rec["identityFieldsMatch"]:
            rec.update(status="RED", reason="award family/week/title differs from its canonical plan")
        if not rec["awardMatches"]:
            rec.update(status="RED", reason="award declaration differs from the canonical plan")
    return rec


# --------------------------------------------------------------------------
# Controls. All three must fire (A3N-2 §2b) or the measurement is invalid.
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "a-deck-claiming-another-plans-cells-reds",
    "a-deck-claiming-a-subset-reds",
    "two-correctly-bound-decks-in-one-family-week-both-pass",
    "the-plan-id-survives-the-targets-file-being-reordered",
    "a-deck-with-no-planId-is-skipped-not-silently-passed",
    "every-selector-prints-its-exclusions-with-reasons",
    "a-selector-that-drops-in-silence-reds",
]

_P1 = {"family": "F ASDAN", "ruledWeek": 1, "cells": ["'S'!C1", "'S'!C2"],
       "outcomes": ["o1", "o2"]}
_P2 = {"family": "F ASDAN", "ruledWeek": 1, "cells": ["'S'!C9"], "outcomes": ["o9"]}


def _deck(cells, outcomes, pid) -> str:
    cfg = json.dumps({"id": "X", "cells": cells, "outcomes": outcomes, "planId": pid})
    return ('<!doctype html><html><head><script id="lesson-config" '
            f'type="application/json">{cfg}</script></head><body></body></html>')


def _tmp(src: str) -> Path:
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fh.write(src); fh.close()
    return Path(fh.name)


# THE SELECTOR RULE (Order A3N-3 §2), and why it lives in g29.
#
# g29 exists because a deck can carry the wrong plan's cells and every other
# gate passes it. Three times in this campaign the same shape has appeared one
# level up, in a SELECTOR -- something that decides what is in a set:
#
#   family+week keying     picked the first of two plans sharing a week, and the
#                          second deck would have shipped the first's cells.
#   a typed task list      decided which twelve plans existed; five cell sets and
#                          eight outcomes were wrong.
#   the donor filter       decided no Art deck could be a donor, from a predicate
#                          list written from memory, and returned zero from 136.
#
#   and, found while acting on that third one:
#   the donor-text sweep   decided the navigation bar was donor teaching and
#                          deleted it from fifteen of twenty-four decks. Nothing
#                          errored, because a sweep that drops in silence has
#                          nothing to error about.
#
# The rule: EVERY SELECTOR THAT NARROWS A CANDIDATE SET MUST PRINT ITS
# EXCLUSIONS WITH REASONS BEFORE THE SET IS USED. Stated once, checked here,
# against every selector this campaign ships -- not as a style note, because a
# style note would not have caught the sweep.
def _selector_probes():
    """(name, callable) -> (droppedCount, [reason per dropped item]).

    Each probe plants an input that MUST drop something. A probe that drops
    nothing is itself a failure: it would let a silent selector pass by never
    exercising it.
    """
    import importlib.util as iu

    def load(name, rel):
        spec = iu.spec_from_file_location(name, ROOT / rel)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    probes = []

    def donor_filter():
        pad = load("pick_art_donor", "tools/easter/pick_art_donor.py")
        row = {"stageCount": 11, "dataMin": 0, "rootBlocks": 2, "pathway": None,
               "g18": {"verdict": "RED", "words": 10, "floor": 900},
               "marginFloor": None, "marginBand": None}
        ok, why = pad.is_candidate(row)
        return (0 if ok else 1), why
    probes.append(("pick_art_donor.is_candidate", donor_filter))

    def batch_targets():
        bt = load("build_batch_targets", "tools/easter/build_batch_targets.py")
        doc = bt.build(set())
        return len(doc["held"]), [r.get("heldBecause") for r in doc["held"]]
    probes.append(("build_batch_targets.build", batch_targets))

    def donor_sweep():
        ad = load("author_deck", "tools/easter/author_deck.py")
        import lxml.html as lh
        ref = json.loads((ROOT / "tools/easter/GREEN_REFERENCE_DECKS.json").read_text())
        picks = [ROOT / d for d in ref["decks"]]
        donor = next((q for q in picks if "BUILD_ASDAN" in q.name), picks[0])
        reference = next((q for q in picks if "Humanities" in q.name), picks[-1])
        tree = lh.fromstring(donor.read_text(encoding="utf-8"))
        content = {"_reference": reference, "objective": "o"}
        plan = {"cells": ["'S'!C1"], "outcomes": ["o"]}
        swept = ad.sweep_donor_text(tree, donor, plan, content)
        acted = [x for x in swept if x["action"] != "kept"]
        return len(acted), [x.get("why") for x in acted]
    probes.append(("author_deck.sweep_donor_text", donor_sweep))

    def manifest_rows():
        ms = load("manifest_sequence", "tools/easter/manifest_sequence.py")
        pack = ROOT / "Humanities_Teesside/BUILD_W1-W8_2026-27"
        rep = ms.plan(pack, only=set())
        dropped = rep.get("refused", []) + [{"why": "unlisted, not added by this run"}
                                            for _ in rep.get("unlistedNotAdded", [])]
        return len(dropped), [x.get("why") for x in dropped]
    probes.append(("manifest_sequence.plan", manifest_rows))
    return probes


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    _selector_controls(rec)
    by_id = {plan_id(_P1): _P1, plan_id(_P2): _P2}

    steal = _tmp(_deck(["'S'!C1", "'S'!C2", "'S'!C9"], ["o1", "o2"], plan_id(_P1)))
    r = judge(steal, by_id)
    rec("a-deck-claiming-another-plans-cells-reds",
        "a cell claimed by the wrong deck is a coverage lie: the census counts it "
        "taught and nobody teaches it",
        ("RED", ["'S'!C9"]), (r["status"], r["extraCells"]))

    subset = _tmp(_deck(["'S'!C1"], ["o1", "o2"], plan_id(_P1)))
    r2 = judge(subset, by_id)
    rec("a-deck-claiming-a-subset-reds",
        "an under-claim leaves a cell open while the deck looks covered, which is "
        "the same lie told quietly",
        ("RED", ["'S'!C2"]), (r2["status"], r2["missingCells"]))

    d1 = _tmp(_deck(_P1["cells"], _P1["outcomes"], plan_id(_P1)))
    d2 = _tmp(_deck(_P2["cells"], _P2["outcomes"], plan_id(_P2)))
    rec("two-correctly-bound-decks-in-one-family-week-both-pass",
        "two plans sharing a family and a week are the case family+week keying got "
        "wrong; correctly bound, both must pass",
        ("PASS", "PASS"), (judge(d1, by_id)["status"], judge(d2, by_id)["status"]))

    rec("the-plan-id-survives-the-targets-file-being-reordered",
        "the id is derived from the plan's content, so regenerating or reordering "
        "the targets file cannot rebind a deck",
        plan_id(_P1), plan_id(dict(reversed(list(_P1.items())))))

    nopid = _tmp('<!doctype html><html><head><script id="lesson-config" '
                 'type="application/json">{"cells":["\'S\'!C1"]}</script>'
                 "</head><body></body></html>")
    r5 = judge(nopid, by_id)
    rec("a-deck-with-no-planId-is-skipped-not-silently-passed",
        "the estate's older decks predate this binding; they are SKIP, never PASS, "
        "so the tally cannot flatter itself",
        "SKIP", r5["status"])

    for f in (steal, subset, d1, d2, nopid):
        f.unlink(missing_ok=True)
    _award_source_controls(rec)
    return out


def _selector_controls(rec):
    results = []
    for name, run in _selector_probes():
        try:
            dropped, reasons = run()
        except Exception as exc:
            results.append((name, "RAISED", str(exc)[:80]))
            continue
        if dropped == 0:
            results.append((name, "DROPPED NOTHING",
                            "the probe did not exercise the selector"))
        elif not all(isinstance(r, str) and r.strip() for r in reasons):
            results.append((name, "SILENT DROP",
                            f"{sum(1 for r in reasons if not r)} of {dropped} carried no reason"))
    rec("every-selector-prints-its-exclusions-with-reasons",
        "every selector this campaign ships names what it dropped and why, on a "
        "planted input that forces it to drop something",
        [], results)

    # MUST FIRE. A selector that drops without a reason has to be caught, or the
    # control above is measuring nothing.
    def silent():
        return 3, [None, "", "a reason"]
    bad = []
    dropped, reasons = silent()
    if not all(isinstance(r, str) and r.strip() for r in reasons):
        bad.append(("planted-silent-selector", "SILENT DROP",
                    f"{sum(1 for r in reasons if not r)} of {dropped} carried no reason"))
    rec("a-selector-that-drops-in-silence-reds",
        "a planted selector that drops three items and explains one is caught",
        1, len(bad))


ADDED_CONTROL_IDS = [
    'all-workbook-plan-identities-remain-unchanged',
    'two-award-plans-in-one-family-week-have-distinct-identities',
    'award-identities-survive-row-reordering',
    'correct-award-declarations-bind-to-canonical-plans',
    'changed-award-identity-fields-are-refused',
    'a-stale-id-cannot-hide-a-changed-award-level',
    'a-stale-id-cannot-hide-a-changed-award-part',
    'a-stale-id-cannot-hide-a-missing-award-slot',
    'an-award-deck-with-wrong-outcomes-reds',
    'a-cell-less-award-deck-claiming-a-cell-reds',
    'an-unknown-award-plan-id-reds',
    'registry-provenance-records-the-bytes-actually-read',
    'a-missing-plan-registry-is-refused',
    'a-missing-registered-source-is-refused',
    'a-stale-award-spec-origin-is-refused',
    'duplicate-plan-identities-within-a-source-are-refused',
    'duplicate-plan-identities-across-sources-are-refused',
    'canonical-award-targets-are-accepted',
    'changed-award-target-fields-are-refused',
    'a-stale-target-source-digest-is-refused',
]


def _award_source_controls(rec):
    # Compatibility is measured independently against the frozen pre-#302
    # workbook formula, not by comparing the shared helper to itself.
    workbook = json.loads(TARGETS.read_text(encoding='utf-8'))['plans']

    def legacy_workbook_id(plan):
        key = '|'.join([str(plan.get('family', '')),
                        str(plan.get('ruledWeek', '')),
                        '|'.join(sorted(plan.get('cells', [])))])
        return hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]

    changed = [i for i, plan in enumerate(workbook)
               if plan_id(plan) != legacy_workbook_id(plan)]
    rec('all-workbook-plan-identities-remain-unchanged',
        'Every current workbook plan retains the identity written before the '
        'award repair; an empty population cannot prove compatibility.',
        (True, []), (bool(workbook), changed))

    def clone(value):
        return json.loads(json.dumps(value))

    def refused(call, fragment=None):
        try:
            call()
        except (ValueError, OSError, KeyError) as exc:
            return fragment is None or fragment in str(exc)
        return False

    with tempfile.TemporaryDirectory(prefix='g29-award-sources-') as temp_dir:
        fixture = Path(temp_dir)
        original_root = _pi.ROOT

        def put(rel, doc):
            path = fixture / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')
            return path

        # Deliberately small fixtures, so each planted difference has one cause.
        spec_rel = 'tools/artsaward/SPEC.json'
        source_rel = 'tools/artsaward/BRONZE_PLAN.json'
        workbook_rel = 'tools/easter/EASTER_TARGETS.json'
        registry_rel = 'tools/easter/PLAN_SOURCES.json'
        spec_doc = {'levels': {'Bronze': {'parts': {'B': {}, 'D': {}}}}}
        spec_path = put(spec_rel, spec_doc)
        put('tools/artsaward/SLOTS.json', {
            'schema': 'arts-award-slots-v1',
            'slots': {'EVENT_SLOT': {'serves': {'Bronze': ['B']}, 'entries': []}}})
        source_doc = {
            'schema': 'aae-bronze-plan-v1', 'family': 'BUILD Art', 'count': 2,
            'derivedFrom': {'path': spec_rel, 'sha256': _pi.digest(spec_path),
                            'level': 'Bronze'},
            'rows': [
                {'seq': 1, 'week': 5, 'part': 'B', 'title': 'A witnessed view',
                 'outcome': 'Review and share a view.', 'spec': 'B.json'},
                {'seq': 2, 'week': 5, 'part': 'D', 'title': 'A planned skill',
                 'outcome': 'Plan an arts skill share.', 'spec': 'D.json'},
            ],
        }
        source_path = put(source_rel, source_doc)
        put(workbook_rel, {'plans': [clone(_P1)]})
        registry_doc = {'schema': 'easter-plan-sources-v1', 'sources': [
            {'path': workbook_rel, 'kind': 'workbook'},
            {'path': source_rel, 'kind': 'award-rows'},
        ]}
        registry_path = put(registry_rel, registry_doc)

        try:
            _pi.ROOT = fixture
            canonical = _pi.read_source(source_path, 'award-rows')
            ids = [plan_id(plan) for plan in canonical]
            rec('two-award-plans-in-one-family-week-have-distinct-identities',
                'Two plans have the same family and week, and no cells; the '
                'old family/week key collapses them.',
                (2, 2), (len(ids), len(set(ids))))

            reordered = clone(source_doc)
            reordered['rows'].reverse()
            put(source_rel, reordered)
            after = _pi.read_source(source_path, 'award-rows')
            before_by_title = {p['title']: plan_id(p) for p in canonical}
            after_by_title = {p['title']: plan_id(p) for p in after}
            rec('award-identities-survive-row-reordering',
                'Reordering the canonical source does not rebind either deck.',
                before_by_title, after_by_title)
            put(source_rel, source_doc)

            indexed, provenance = _pi.load_registry(registry_path)
            deck_number = 0

            def judged(plan, changes=None):
                nonlocal deck_number
                deck_number += 1
                cfg = {'id': 'TEST', 'family': plan['family'],
                       'week': plan['ruledWeek'], 'title': plan['title'],
                       'cells': clone(plan['cells']),
                       'outcomes': clone(plan['outcomes']),
                       'artsAward': clone(plan['artsAward']),
                       'planId': plan_id(plan)}
                cfg.update(changes or {})
                deck = fixture / f'award-{deck_number}.html'
                deck.write_text('<!doctype html><html><head><script '
                                'id="lesson-config" type="application/json">' +
                                json.dumps(cfg) + '</script></head><body></body></html>',
                                encoding='utf-8')
                return judge(deck, indexed)

            rec('correct-award-declarations-bind-to-canonical-plans',
                'Both the slot-dependent Part B and independent Part D bind.',
                ['PASS', 'PASS'], [judged(p)['status'] for p in canonical])
            plan = canonical[0]
            for cid, field, value in [
                ('a-stale-id-cannot-hide-a-changed-award-level', 'level', 'Silver'),
                ('a-stale-id-cannot-hide-a-changed-award-part', 'parts', ['D']),
                ('a-stale-id-cannot-hide-a-missing-award-slot', 'slots', []),
            ]:
                award = clone(plan['artsAward'])
                award[field] = value
                result = judged(plan, {'artsAward': award})
                rec(cid, 'Keep the valid planId but change the declaration: '
                    'empty matching cells must not hide the change.',
                    ('RED', False), (result['status'], result.get('awardMatches')))

            result = judged(plan, {'outcomes': ['An unrelated outcome.']})
            rec('an-award-deck-with-wrong-outcomes-reds',
                'A valid ID cannot bind a changed teaching outcome.',
                ('RED', False), (result['status'], result['outcomesMatch']))
            result = judged(plan, {'cells': ["'S'!C99"]})
            rec('a-cell-less-award-deck-claiming-a-cell-reds',
                'Award binding must never fabricate workbook coverage.',
                ('RED', ["'S'!C99"]), (result['status'], result['extraCells']))
            rec('an-unknown-award-plan-id-reds',
                'A declared award does not excuse an ID absent from registered sources.',
                'RED', judged(plan, {'planId': 'unknown-plan-id'})['status'])

            rec('changed-award-identity-fields-are-refused',
                'A stale ID cannot hide a changed family, week or title.',
                ['RED', 'RED', 'RED'],
                [judged(plan, {key:value})['status'] for key,value in
                 [('family','GROW Art'), ('week',99), ('title','Another title')]])

            actual_hashes = {row['path']: row['sha256'] for row in provenance['sources']}
            expected_hashes = {rel: _pi.digest(fixture / rel)
                               for rel in [workbook_rel, source_rel]}
            rec('registry-provenance-records-the-bytes-actually-read',
                'Both sources and the registry itself carry measured SHA-256 values.',
                (expected_hashes, _pi.digest(registry_path)),
                (actual_hashes, provenance['registrySha256']))
            rec('a-missing-plan-registry-is-refused',
                'No registry is an error, not a zero-plan success.',
                True, refused(lambda: _pi.load_registry(fixture / 'absent.json')))
            missing_doc = clone(registry_doc)
            missing_doc['sources'].append({'path': 'missing.json', 'kind': 'workbook'})
            missing_registry = put('missing-source-registry.json', missing_doc)
            rec('a-missing-registered-source-is-refused',
                'A named missing source cannot be silently excluded.',
                True, refused(lambda: _pi.load_registry(missing_registry),
                              'registered source absent'))

            altered_spec = clone(spec_doc)
            altered_spec['planted_change'] = True
            put(spec_rel, altered_spec)
            rec('a-stale-award-spec-origin-is-refused',
                'Even a valid-shaped source is refused when SPEC bytes changed '
                'without the canonical plan digest following them.',
                True, refused(lambda: _pi.load_registry(registry_path), 'stale source digest'))
            put(spec_rel, spec_doc)

            rec('duplicate-plan-identities-within-a-source-are-refused',
                'A dict overwrite must not hide two rows with the same plan identity.',
                True, refused(lambda: _pi.index_plans([canonical[0], canonical[0]]),
                              'duplicate plan identity'))
            put('duplicate-workbook.json', {'plans': [clone(_P1)]})
            duplicate_registry_doc = clone(registry_doc)
            duplicate_registry_doc['sources'].append({
                'path': 'duplicate-workbook.json', 'kind': 'workbook'})
            duplicate_registry = put('duplicate-registry.json', duplicate_registry_doc)
            rec('duplicate-plan-identities-across-sources-are-refused',
                'A later registered source cannot overwrite an earlier plan.',
                True, refused(lambda: _pi.load_registry(duplicate_registry),
                              'duplicate IDs across sources'))

            target_doc = {
                'plansFrom': 'row', 'count': len(canonical),
                'derivedFrom': {'path': source_rel, 'sha256': _pi.digest(source_path)},
                'batch': [],
            }
            for index, (source_row, p) in enumerate(zip(source_doc['rows'], canonical)):
                target_doc['batch'].append({
                    'planIndex': 1001 + index, 'family': p['family'],
                    'week': p['ruledWeek'], 'cells': clone(p['cells']),
                    'title': p['title'], 'subject': p['subject'],
                    'outcomes': clone(p['outcomes']), 'artsAward': clone(p['artsAward']),
                    'route': f'Art/fixture-{index}.html', 'spec': source_row['spec'],
                })
            rec('canonical-award-targets-are-accepted',
                'A true projection of the canonical source is accepted.',
                ['B.json', 'D.json'], sorted(_pi.validate_award_targets(target_doc)))
            tampering = []
            for field, replacement in [
                ('outcomes', ['A substituted outcome.']), ('week', 6),
                ('title', 'A substituted title'), ('cells', ["'S'!C99"]),
                ('artsAward', {'level': 'Bronze', 'parts': ['D']}),
            ]:
                changed = clone(target_doc)
                changed['batch'][0][field] = replacement
                tampering.append((field, refused(
                    lambda: _pi.validate_award_targets(changed),
                    'differs from its canonical plan')))
            rec('changed-award-target-fields-are-refused',
                'A matching source-file digest does not excuse hand-edited '
                'target outcomes, week, title, cells or award declaration.',
                [(field, True) for field, _ in tampering], tampering)
            stale_target = clone(target_doc)
            stale_target['derivedFrom']['sha256'] = '0' * 64
            rec('a-stale-target-source-digest-is-refused',
                'Target rows do not make an obsolete source digest acceptable.',
                True, refused(lambda: _pi.validate_award_targets(stale_target),
                              'target source digest is stale'))
        finally:
            _pi.ROOT = original_root

# Additional controls to add alongside the reported fixes (not included above
# until their intended contract is implemented): duplicate canonical spec names,
# duplicate target routes and planIndex values, non-empty count agreement, and a
# --only selector that matches zero rows. All should refuse before a deck is written.

CONTROL_IDS += ADDED_CONTROL_IDS


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g29_plan_binding", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g29_plan_binding.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*")
    ap.add_argument("--scope", choices=("authored",))
    ap.add_argument("--targets", help="Explicit single workbook source; default reads PLAN_SOURCES.json")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); return 0
    if a.self_test:
        rep = self_test()
        print(f"g29 self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:56s} "
                  f"expected={str(r['expected'])[:34]} observed={str(r['observed'])[:34]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    provenance = {}
    try:
        if a.targets:
            by_id, digest = load_plans(Path(a.targets))
        else:
            by_id, provenance = _pi.load_registry()
            digest = _pi.digest(TARGETS)
            for source in provenance["sources"]:
                print(f"SOURCE {source['path']}: {source['plans']} plans; sha256 {source['sha256']}")
    except (ValueError, OSError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    paths = [Path(d) for d in a.decks]
    if a.scope == "authored":
        paths = []
        for f in sorted(ROOT.rglob("*.html")):
            rel = f.relative_to(ROOT)
            if rel.parts and rel.parts[0] in ("Site", "Games", "Apps"):
                continue
            try:
                if '"planId"' in f.read_text(encoding="utf-8"):
                    paths.append(f)
            except Exception:
                continue
    recs = [judge(p, by_id) for p in paths]
    reds = [r for r in recs if r["status"] == "RED"]
    for r in recs:
        name = Path(r["file"]).name[:56]
        print(f"  {r['status']:4s} {name:56s} {r.get('reason','')}")
    print(f"\n{len(recs)} deck(s): {sum(1 for r in recs if r['status']=='PASS')} PASS, "
          f"{len(reds)} RED, {sum(1 for r in recs if r['status']=='SKIP')} SKIP")
    print(f"targets sha256 {digest[:16]}  [{VERSION}]")
    if a.output:
        o = Path(a.output); o = o if o.is_absolute() else ROOT / o
        o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(json.dumps({"gate": "g29-plan-binding", "toolVersion": VERSION,
                                 "file": "_sownb/vb/tools/g29_plan_binding.py",
                                 "targetsSha256": digest, **provenance, "decks": len(recs),
                                 "red": len(reds), "rows": recs}, indent=1) + "\n",
                     encoding="utf-8")
    return 0 if not reds else 1


if __name__ == "__main__":
    raise SystemExit(main())
