#!/usr/bin/env python3
"""Red-prove tools/sx3/admit_landing_decks.py. A tool that writes to 36 decks
must refuse rather than damage, and must be idempotent.

Every case runs against synthetic text in memory. No repository file is touched.

  python3 tools/sx3/test_admit_landing_decks.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("admit", ROOT / "tools/sx3/admit_landing_decks.py")
admit = importlib.util.module_from_spec(spec)
sys.modules["admit"] = admit
spec.loader.exec_module(admit)

BASE_CONFIG = {"title": "T", "sow": "Outcome.", "objective": "Obj.", "week": 4,
               "id": "x1", "previousFile": "a.html", "nextFile": "b.html",
               "timings": [1, 2], "source": {"sheet": "S", "cell": "C1"}}
PACK_CONFIG = {"title": "T", "key": "k", "pathway": "GROW", "stages": []}


def deck(config, meta="GROW · SCIENCE · 2 MINUTES", blocks=1):
    body = "".join(
        f'<script type="application/json" id="lesson-config">{json.dumps(config, ensure_ascii=False)}</script>'
        for _ in range(blocks))
    return f'<html><body><div class="slide"><p class="science-meta">{meta}</p></div>{body}</body></html>'


class RestoreBindingKeys(unittest.TestCase):
    def test_carries_every_binding_key_the_pack_dropped(self):
        out, carried = admit.restore_binding_keys(deck(PACK_CONFIG), deck(BASE_CONFIG))
        self.assertEqual(sorted(carried), sorted(admit.BINDING_KEYS))
        self.assertEqual(json.loads(admit.CONFIG_RE.search(out).group(2))["sow"], "Outcome.")

    def test_never_overwrites_a_key_the_pack_supplied(self):
        pack = dict(PACK_CONFIG, sow="The pack's own outcome.")
        out, carried = admit.restore_binding_keys(deck(pack), deck(BASE_CONFIG))
        self.assertNotIn("sow", carried)
        self.assertEqual(json.loads(admit.CONFIG_RE.search(out).group(2))["sow"],
                         "The pack's own outcome.")

    def test_carries_nothing_but_the_binding_keys(self):
        base = dict(BASE_CONFIG, packOnlyProse="should not travel")
        out, _ = admit.restore_binding_keys(deck(PACK_CONFIG), deck(base))
        self.assertNotIn("packOnlyProse", json.loads(admit.CONFIG_RE.search(out).group(2)))

    def test_idempotent(self):
        once, _ = admit.restore_binding_keys(deck(PACK_CONFIG), deck(BASE_CONFIG))
        twice, carried = admit.restore_binding_keys(once, deck(BASE_CONFIG))
        self.assertEqual(carried, [])
        self.assertEqual(once, twice)

    def test_refuses_a_config_that_does_not_round_trip(self):
        # Pretty-printed JSON does not round-trip to the compact form, so
        # splicing would rewrite bytes this tool did not intend to touch.
        ugly = deck(PACK_CONFIG).replace(json.dumps(PACK_CONFIG, ensure_ascii=False),
                                         json.dumps(PACK_CONFIG, indent=2))
        with self.assertRaises(admit.Refuse):
            admit.restore_binding_keys(ugly, deck(BASE_CONFIG))

    def test_refuses_more_than_one_config_block(self):
        with self.assertRaises(admit.Refuse):
            admit.restore_binding_keys(deck(PACK_CONFIG, blocks=2), deck(BASE_CONFIG))

    def test_refuses_invalid_json(self):
        broken = deck(PACK_CONFIG).replace(json.dumps(PACK_CONFIG, ensure_ascii=False), "{not json")
        with self.assertRaises(admit.Refuse):
            admit.restore_binding_keys(broken, deck(BASE_CONFIG))


class RestoreToken(unittest.TestCase):
    bindings = {"p.html": {"weeks": [{"key": "Aut2·W4"}]}}

    def test_appends_the_derived_token_to_the_meta_line(self):
        out, written = admit.restore_token(deck(PACK_CONFIG), "p.html", self.bindings)
        self.assertEqual(written, ["Aut2·W4"])
        self.assertIn("2 MINUTES · Aut2·W4", out)

    def test_idempotent(self):
        once, _ = admit.restore_token(deck(PACK_CONFIG), "p.html", self.bindings)
        twice, written = admit.restore_token(once, "p.html", self.bindings)
        self.assertEqual(written, [])
        self.assertEqual(once, twice)

    def test_writes_nothing_when_the_record_has_no_week(self):
        out, written = admit.restore_token(deck(PACK_CONFIG), "p.html", {"p.html": {"weeks": []}})
        self.assertEqual(written, [])
        self.assertEqual(out, deck(PACK_CONFIG))

    def test_refuses_when_there_is_no_meta_line_to_carry_it(self):
        bare = '<html><body><div class="slide"><h1>T</h1></div></body></html>'
        with self.assertRaises(admit.Refuse):
            admit.restore_token(bare, "p.html", self.bindings)

    def test_token_is_verbatim_from_the_record_not_derived_from_the_path(self):
        # The path says W99; the record says Aut2·W4. The record wins.
        out, written = admit.restore_token(deck(PACK_CONFIG), "p.html",
                                           {"p.html": {"weeks": [{"key": "Aut2·W4"}]}})
        self.assertEqual(written, ["Aut2·W4"])
        self.assertNotIn("W99", out)


class IdenticalToBase(unittest.TestCase):
    def test_a_deck_equal_to_its_base_is_skipped_not_refused(self):
        # The base's lesson-config is pretty-printed and would not round-trip.
        # A held deck reverted to the base still appears in the diff, so without
        # the skip the tool refuses a deck it has no work to do on.
        pretty = deck(BASE_CONFIG).replace(json.dumps(BASE_CONFIG, ensure_ascii=False),
                                           json.dumps(BASE_CONFIG, indent=2))
        with self.assertRaises(admit.Refuse):
            admit.restore_binding_keys(pretty, pretty)


if __name__ == "__main__":
    unittest.main(verbosity=2)
