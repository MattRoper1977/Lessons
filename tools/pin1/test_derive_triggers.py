"""PIN1 controls; these are local controls, not GitHub trigger experiments."""
import copy
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

import derive_triggers as d

FIXTURE = '''name: fixture
on:
  pull_request:
    branches: [main]
    paths:
      - index.html
  push:
    branches: [main]
    paths:
      - index.html
  schedule:
    - cron: '53 6 * * *'
  workflow_dispatch:
permissions:
  contents: read
jobs:
  static-contract:
    runs-on: ubuntu-latest
    steps:
      - run: echo unchanged
'''


class TriggerControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.gate = SimpleNamespace(
            detect_kind=lambda _: 'lessons',
            CANONICAL_HASHES={'assets/shared.css': 'digest'},
            MANIFEST_PINS={'resources.json': 'digest', 'apps.json': 'digest'},
            CATALOGUE_PINS={'files': {'index.html': 'digest', 'lessons/one.html': 'digest'}},
            LUNDYLOOP_CI_PINS={'apps/workflow.yml': 'digest'},
            PUBLICATION_CALLER_PATH='.github/workflows/education-pages.yml',
        )
        for path in ('resources.json', 'assets/shared.css', 'index.html',
                     'lessons/one.html', '.github/workflows/education-pages.yml'):
            p = self.root / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('fixture')

    def report(self):
        return d.inventory(self.root, self.gate)

    def test_exact_coverage_and_existing_non_path_bytes_preserved(self):
        r = self.report()
        rendered = d.render(FIXTURE, r['expected_triggers'])
        self.assertEqual(d.check(self.root, rendered, r), [])
        self.assertEqual(rendered, d.render(rendered, r['expected_triggers']))
        normalized = []
        for text in (FIXTURE, rendered):
            for event in d.EVENTS:
                a, b = d.event_paths_span(text, event)
                text = text[:a] + '      - TOKEN\n' + text[b:]
            normalized.append(text)
        self.assertEqual(normalized[0], normalized[1])

    def test_missing_file_trigger_and_unrelated_widening_red(self):
        r = self.report()
        rendered = d.render(FIXTURE, r['expected_triggers'])
        missing = rendered.replace("      - 'lessons/one.html'\n", '')
        self.assertTrue(d.check(self.root, missing, copy.deepcopy(r)))
        widened = rendered.replace(d.END, "      - 'unrelated.txt'\n" + d.END)
        self.assertTrue(d.check(self.root, widened, copy.deepcopy(r)))

    def test_new_pin_requires_regeneration_and_then_gets_coverage(self):
        old = d.render(FIXTURE, self.report()['expected_triggers'])
        self.gate.CATALOGUE_PINS['files']['lessons/two.html'] = 'digest'
        (self.root / 'lessons/two.html').write_text('fixture')
        r = self.report()
        self.assertTrue(d.check(self.root, old, copy.deepcopy(r)))
        new = d.render(old, r['expected_triggers'])
        self.assertEqual(d.check(self.root, new, r), [])
        for event in d.EVENTS:
            self.assertIn('lessons/two.html', d.read_paths(new, event))

    def test_registry_removal_retires_trigger_without_directory_glob(self):
        old = d.render(FIXTURE, self.report()['expected_triggers'])
        del self.gate.CATALOGUE_PINS['files']['lessons/one.html']
        r = self.report()
        self.assertTrue(d.check(self.root, old, copy.deepcopy(r)))
        new = d.render(old, r['expected_triggers'])
        self.assertNotIn('lessons/one.html', d.read_paths(new, 'push'))
        self.assertNotIn('**', new)

    def test_deleted_pinned_file_keeps_coverage_and_fails(self):
        (self.root / 'lessons/one.html').unlink()
        r = self.report()
        self.assertIn('lessons/one.html', r['asserted'])
        self.assertTrue(d.check(self.root, d.render(FIXTURE, r['expected_triggers']), r))

    def test_kind_specific_registries_follow_gate(self):
        r = self.report()
        self.assertNotIn('apps.json', r['asserted'])
        self.assertNotIn('apps/workflow.yml', r['asserted'])
        self.gate.detect_kind = lambda _: 'apps'
        (self.root / 'apps.json').write_text('fixture')
        r = self.report()
        self.assertIn('apps/workflow.yml', r['asserted'])
        self.assertIn('apps.json', r['asserted'])
        self.assertNotIn('lessons/one.html', r['asserted'])

    def test_unrelated_path_remains_outside_each_event(self):
        text = d.render(FIXTURE, self.report()['expected_triggers'])
        for event in d.EVENTS:
            self.assertNotIn('docs/orders/pin1/dormant.txt', d.read_paths(text, event))
            self.assertIn(d.GATE, d.read_paths(text, event))

    def test_unsafe_paths_and_empty_registry_refused(self):
        for path in ('**', 'lessons/*.html', '../a', '/a', 'a//b', 'a?b', 'a\nb', '!a'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                d.exact_path(path)
        self.assertEqual(d.exact_path('A lesson (one)/index.html'), 'A lesson (one)/index.html')
        self.gate.CATALOGUE_PINS['files'].clear()
        with self.assertRaises(ValueError):
            self.report()

    def test_missing_or_ambiguous_events_are_unmeasured(self):
        for bad in (FIXTURE.replace('  push:', '  other:'),
                    FIXTURE.replace('    paths:', '    paths-ignore:', 1),
                    'on:\n  push:\n' + FIXTURE):
            with self.assertRaises(ValueError):
                d.render(bad, self.report()['expected_triggers'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
