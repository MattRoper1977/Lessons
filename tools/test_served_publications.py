"""Adversarial provenance and extraction controls; no network or credentials."""
import copy
import io
from pathlib import Path
import tempfile
import time
import unittest
import zipfile
import os
from prepare_served_publications import (Inconclusive, Red, no_result, require,
                                        validate_artifact, publication_run_matches,
                                         extract_archive, prepare_one, digest, select_artifact,
                                         download_limit, DOWNLOAD_MARGIN_BYTES)
import prepare_served_publications


class ProvenanceControls(unittest.TestCase):
    def setUp(self):
        self.run = {'id': 123, 'head_branch': 'main', 'event': 'push', 'head_sha': 'a'*40,
                    'status': 'completed', 'conclusion': 'success', 'run_attempt': 4,
                    'html_url': 'https://github.com/example/run/123'}
        self.artifact = {'id': 456, 'name': 'education-lessons-review', 'expired': False,
                         'created_at': '2026-09-05T18:43:29Z',
                         'workflow_run': {'id': 123, 'head_sha': 'a'*40}, 'digest': 'sha256:'+'b'*64}
        self.jobs = [
            {'id': 100, 'name': 'publish / build', 'run_attempt': 4, 'conclusion': 'success', 'steps': [
                {'name': 'Save the reviewed education output', 'conclusion': 'success',
                 'started_at': '2026-09-05T18:43:28Z', 'completed_at': '2026-09-05T18:43:29Z'}]},
            {'id': 101, 'name': 'publish / deploy', 'run_attempt': 4, 'conclusion': 'success',
             'started_at': '2026-09-05T18:43:38Z'}]

    def test_exact_source_accepts_and_other_source_rejects(self):
        self.assertTrue(publication_run_matches('lessons', self.run, 'a'*40, None))
        self.assertFalse(publication_run_matches('lessons', self.run, 'b'*40, None))
        for field, value in [('event', 'pull_request'), ('head_branch', 'other')]:
            self.assertFalse(publication_run_matches('lessons', {**self.run, field: value}, 'a'*40, None))

    def test_frozen_games_requires_all_publication_inputs_identical(self):
        class GitHub:
            def __init__(self, mutation=None): self.mutation = mutation
            def read(self, route):
                value = 'c'*40
                if self.mutation and self.mutation in route and route.endswith('b'*40): value = 'd'*40
                return {'sha': value}
        self.assertTrue(publication_run_matches('games', self.run, 'b'*40, GitHub()))
        for file in ['games.json', 'play-publication.json', 'play-domain-publication.yml']:
            self.assertFalse(publication_run_matches('games', self.run, 'b'*40, GitHub(file)))

    def test_artifact_must_bind_exact_run_source_and_digest(self):
        validate_artifact(self.artifact, self.run, 'lessons')
        for mutation in [{'expired': True}, {'name': 'unreviewed'}, {'digest': ''},
                         {'workflow_run': {'id': 124, 'head_sha': 'a'*40}},
                         {'workflow_run': {'id': 123, 'head_sha': 'b'*40}}]:
            with self.assertRaises(Red): validate_artifact({**self.artifact, **mutation}, self.run, 'lessons')

    def test_four_reruns_select_only_successful_attempts_upload(self):
        old = [{**self.artifact, 'id': number, 'created_at': created} for number, created in enumerate([
            '2026-09-05T17:27:53Z', '2026-09-05T18:25:18Z', '2026-09-05T18:33:15Z'])]
        artifact, binding = select_artifact(old+[self.artifact], self.run, self.jobs, 'lessons')
        self.assertEqual(artifact['id'], 456)
        self.assertEqual(binding['run_attempt'], 4)
        self.assertEqual(binding['upload_job_id'], 100)
        self.assertEqual(binding['deploy_job_id'], 101)

    def test_duplicate_or_out_of_attempt_artifact_is_rejected(self):
        for artifacts in [[self.artifact, {**self.artifact, 'id': 457}],
                          [{**self.artifact, 'created_at': '2026-09-05T18:33:15Z'}],
                          [{**self.artifact, 'created_at': '2026-09-05T18:43:40Z'}]]:
            with self.assertRaises(Red): select_artifact(artifacts, self.run, self.jobs, 'lessons')
        stale_jobs = copy.deepcopy(self.jobs)
        stale_jobs[1]['run_attempt'] = 3
        with self.assertRaises(Red): select_artifact([self.artifact], self.run, stale_jobs, 'lessons')
        stale_jobs = copy.deepcopy(self.jobs)
        stale_jobs[0]['run_attempt'] = 3
        with self.assertRaises(Red): select_artifact([self.artifact], self.run, stale_jobs, 'lessons')

    def archive(self, name='index.html', data=b'approved'):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive: archive.writestr(name, data)
        return stream.getvalue()

    def test_safe_archive_extracts_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)/'publication'
            extract_archive(self.archive(), dest)
            self.assertEqual((dest/'index.html').read_bytes(), b'approved')
            with self.assertRaises(Red): extract_archive(self.archive(), dest)

    def test_escaping_archive_names_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            for number, name in enumerate(['../outside', '/absolute', 'a/../../outside', 'a\\outside']):
                with self.assertRaises(Red): extract_archive(self.archive(name), Path(temp)/str(number))

    def test_successful_review_without_successful_deploy_fails(self):
        outer = self
        class GitHub:
            deadline = time.monotonic()+30
            def read(self, route, raw=False):
                if '/workflows/' in route: return {'workflow_runs': [outer.run]}
                if '/jobs?' in route: return {'jobs': [{'name': 'publish / deploy', 'conclusion': 'skipped'}]}
                raise AssertionError('Must stop before reading any artifact')
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(Red):
            prepare_one('lessons', 'a'*40, Path(temp), GitHub())

    def test_verified_archive_accepts_and_download_mutation_fails(self):
        outer = self
        archive = self.archive()
        class GitHub:
            deadline = time.monotonic()+30
            mutate = False
            def read(self, route, raw=False):
                if '/workflows/' in route: return {'workflow_runs': [outer.run]}
                if '/jobs?' in route: return {'jobs': outer.jobs}
                if '/artifacts?' in route: return {'artifacts': [{**outer.artifact, 'digest': digest(archive),
                                                                  'size_in_bytes': len(archive)}]}
                raise AssertionError('a publication archive is never read into memory: ' + route)
            def download(self, route, path, limit):
                assert route.endswith('/zip') and limit == len(archive) + DOWNLOAD_MARGIN_BYTES
                data = archive + (b'x' if self.mutate else b'')
                Path(path).write_bytes(data)
                return digest(data)
        with tempfile.TemporaryDirectory() as temp:
            evidence = prepare_one('lessons', 'a'*40, Path(temp), GitHub())
            self.assertEqual(evidence['deployment'], 'success')
            self.assertEqual(Path(evidence['root'], 'index.html').read_bytes(), b'approved')
            self.assertEqual(sorted(p.name for p in Path(temp).iterdir()), ['lessons'],
                             'the downloaded archive is removed once extracted')
        with tempfile.TemporaryDirectory() as temp:
            bad = GitHub(); bad.mutate = True
            with self.assertRaises(Red): prepare_one('lessons', 'a'*40, Path(temp), bad)

    # su-2. The download bound was a constant 1,000,000,000 B and the Lessons review
    # archive grew past it (1,021,684,414 B at 5763eb1a): a correct publication read
    # red. The bound is now the run's own archive size plus a stated margin.
    def test_download_bound_is_the_runs_own_size_plus_the_margin(self):
        grown = {'size_in_bytes': 1_021_684_414}
        self.assertEqual(download_limit(grown, 'lessons'), 1_021_684_414 + DOWNLOAD_MARGIN_BYTES)
        self.assertGreater(download_limit(grown, 'lessons'), 1_000_000_000)
        self.assertEqual(DOWNLOAD_MARGIN_BYTES, 16 * 1024 * 1024)
        for bad in [{}, {'size_in_bytes': 0}, {'size_in_bytes': -1}, {'size_in_bytes': True},
                    {'size_in_bytes': '1021684414'}, {'size_in_bytes': None}]:
            with self.assertRaises(Red): download_limit(bad, 'lessons')

    def test_download_streams_to_disk_and_refuses_past_its_bound(self):
        """The REAL download(), fed a fake response: it writes in chunks, returns the
        digest of what it wrote, and on a stream past its bound raises Red and leaves
        no partial file behind."""
        payload = bytes(range(256)) * (3 * 4096 + 7)          # just over 3 MiB, several chunks
        class Response(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *exc): self.close()
        previous = os.environ.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = 'token-for-this-test'
        try:
            client = prepare_served_publications.GitHub(time.monotonic() + 60)
            client._open = lambda route: Response(payload)
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp)/'review.zip'
                self.assertEqual(client.download('/zip', target, len(payload)), digest(payload))
                self.assertEqual(target.read_bytes(), payload)
                over = Path(temp)/'over.zip'
                with self.assertRaises(Red) as caught:
                    client.download('/zip', over, len(payload) - 1)
                self.assertIn('larger than its bound', str(caught.exception))
                self.assertFalse(over.exists(), 'a refused download leaves no partial file')
                with self.assertRaises(Red):          # never overwrites an earlier archive
                    client.download('/zip', target, len(payload))
                self.assertEqual(target.read_bytes(), payload)
        finally:
            if previous is None:
                del os.environ['GITHUB_TOKEN']
            else:
                os.environ['GITHUB_TOKEN'] = previous


    # GW1-C §1.2. Every assertion above says Red, and the rename is not the
    # point: the point is that these are contradictions the tool OBSERVED --
    # a digest that does not match, an archive member that escapes, a deploy
    # that is missing. They were Inconclusive until now, which meant "the
    # downloaded artifact digest differs" reported in the same words and the
    # same exit code as "I arrived before the publication finished".
    #
    # The distinction is only real if it is tested, so it is tested here rather
    # than left to the class names.
    def test_red_and_inconclusive_are_distinct_states(self):
        self.assertFalse(issubclass(Red, Inconclusive))
        self.assertFalse(issubclass(Inconclusive, Red))

        # a contradiction observed -> Red
        with self.assertRaises(Red):
            require(False, 'lessons: downloaded artifact digest differs')
        # evidence out of reach -> Inconclusive, and it names how long it waited
        with self.assertRaises(Inconclusive) as caught:
            no_result('no result: publication retrieval deadline reached, waited 37 seconds')
        self.assertIn('waited 37 seconds', str(caught.exception))
        self.assertTrue(str(caught.exception).startswith('no result:'))

        # and neither is caught by the other, which is the whole property
        with self.assertRaises(Red):
            try:
                require(False, 'a contradiction')
            except Inconclusive:
                self.fail('a Red was swallowed as Inconclusive')

    def test_a_timeout_never_reports_as_success(self):
        """A wait that times out and returns green is the same defect in
        different clothes. Inconclusive is not a pass."""
        self.assertTrue(issubclass(Inconclusive, Exception))
        with self.assertRaises(Inconclusive):
            no_result('no result: waited 1 seconds')


    # GW1-E §2.2. Every other test in this file uses the STUB GitHub defined
    # below, which takes no arguments and never runs the real __init__. That is
    # why eleven green tests could not see self.token go unassigned: the real
    # constructor is reached only on the live path, and the live path is the one
    # thing a pull request does not run (D51).
    #
    # This test constructs the REAL GitHub exactly as main() does --
    # GitHub(time.monotonic() + args.wait_seconds) -- and asserts the whole of
    # __init__ ran, not just its first two lines.
    def test_real_github_constructor_assigns_every_attribute(self):
        real = prepare_served_publications.GitHub
        previous = os.environ.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = 'token-for-this-test'
        try:
            client = real(time.monotonic() + 1800)      # exactly main()'s call
            self.assertEqual(client.token, 'token-for-this-test')
            self.assertTrue(hasattr(client, 'deadline'))
            self.assertTrue(hasattr(client, 'started'))
            self.assertIsInstance(client.waited(), int)
        finally:
            if previous is None:
                del os.environ['GITHUB_TOKEN']
            else:
                os.environ['GITHUB_TOKEN'] = previous

    def test_no_github_method_has_a_statement_below_its_return(self):
        """The shape of the defect, not just the symptom: two lines of __init__
        ended up below waited()'s return and were never executed."""
        import ast, inspect
        tree = ast.parse(inspect.getsource(prepare_served_publications))
        cls = [n for n in ast.walk(tree)
               if isinstance(n, ast.ClassDef) and n.name == 'GitHub'][0]
        dead = [(fn.name, fn.body[i + 1].lineno)
                for fn in cls.body if isinstance(fn, ast.FunctionDef)
                for i, stmt in enumerate(fn.body[:-1])
                if isinstance(stmt, (ast.Return, ast.Raise))]
        self.assertEqual(dead, [], 'unreachable statements in GitHub: %r' % (dead,))

if __name__ == '__main__': unittest.main(verbosity=2)
