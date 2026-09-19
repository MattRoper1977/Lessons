#!/usr/bin/env python3
"""Red-prove tools/sx3/admit_landing_decks.py. A tool that writes to 36 decks
must refuse rather than damage, and must be idempotent.

Every case runs against synthetic text in memory. No repository file is touched.

  python3 tools/sx3/test_admit_landing_decks.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
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
    """The skip in main() for a deck whose bytes already equal the base.

    A held deck reverted to the base in the working tree still appears in the
    diff against that base, so main() is handed a deck it has no work to do on.
    The base's own lesson-config is pretty-printed and does not round-trip, so
    without the skip the tool REFUSES that deck instead of passing over it.

    The first version of this test asserted only the premise - that
    restore_binding_keys refuses a pretty-printed config - and so passed with
    the skip deleted. It therefore controlled nothing. These two cases drive
    main() itself, and the second is the control: it deletes the skip from a
    copy of the source and requires the refusal to come back.
    """

    PRETTY = deck(BASE_CONFIG).replace(json.dumps(BASE_CONFIG, ensure_ascii=False),
                                       json.dumps(BASE_CONFIG, indent=2))

    def _run(self, module):
        """Run module.main() over one deck whose bytes equal its base."""
        rel = "Science_Teesside/Grow/W1_2026-27/SCI_G_W1_Held.html"
        root = Path(tempfile.mkdtemp())
        (root / rel).parent.mkdir(parents=True)
        (root / rel).write_text(self.PRETTY)
        (root / admit.BINDINGS).parent.mkdir(parents=True, exist_ok=True)
        (root / admit.BINDINGS).write_text(json.dumps({"entries": []}))
        old_root, old_changed, old_git, old_argv = (
            module.ROOT, module.changed_science, module.git_text, sys.argv)
        module.ROOT = root
        module.changed_science = lambda base: [rel]
        module.git_text = lambda base, path: self.PRETTY
        sys.argv = ["admit", "--base", "origin/main", "--check"]
        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = module.main()
            return code, buffer.getvalue()
        finally:
            (module.ROOT, module.changed_science, module.git_text, sys.argv) = (
                old_root, old_changed, old_git, old_argv)

    def test_a_deck_equal_to_its_base_is_skipped_not_refused(self):
        code, out = self._run(admit)
        self.assertEqual(code, 0, out)
        self.assertIn("REFUSED               : 0 deck(s)", out)
        self.assertIn("already correct       : 1 deck(s)", out)

    def test_control_removing_the_skip_brings_the_refusal_back(self):
        source = (ROOT / "tools/sx3/admit_landing_decks.py").read_text()
        skip = ("        if base_text is not None and text == base_text:\n"
                "            untouched.append(rel)\n"
                "            continue\n")
        self.assertTrue(skip in source,
                        "the skip this test controls is no longer in main()")
        patched = Path(tempfile.mkdtemp()) / "admit_no_skip.py"
        patched.write_text(source.replace(skip, ""))
        spec_no_skip = importlib.util.spec_from_file_location("admit_no_skip", patched)
        module = importlib.util.module_from_spec(spec_no_skip)
        spec_no_skip.loader.exec_module(module)
        code, out = self._run(module)
        self.assertEqual(code, 1, out)
        self.assertIn("REFUSED               : 1 deck(s)", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
