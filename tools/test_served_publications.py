"""Adversarial provenance and extraction controls; no network or credentials."""
import copy
import io
from pathlib import Path
import tempfile
import time
import unittest
import zipfile
from prepare_served_publications import (Inconclusive, validate_artifact, publication_run_matches,
                                         extract_archive, prepare_one, digest, select_artifact)


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
            with self.assertRaises(Inconclusive): validate_artifact({**self.artifact, **mutation}, self.run, 'lessons')

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
            with self.assertRaises(Inconclusive): select_artifact(artifacts, self.run, self.jobs, 'lessons')
        stale_jobs = copy.deepcopy(self.jobs)
        stale_jobs[1]['run_attempt'] = 3
        with self.assertRaises(Inconclusive): select_artifact([self.artifact], self.run, stale_jobs, 'lessons')
        stale_jobs = copy.deepcopy(self.jobs)
        stale_jobs[0]['run_attempt'] = 3
        with self.assertRaises(Inconclusive): select_artifact([self.artifact], self.run, stale_jobs, 'lessons')

    def archive(self, name='index.html', data=b'approved'):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive: archive.writestr(name, data)
        return stream.getvalue()

    def test_safe_archive_extracts_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)/'publication'
            extract_archive(self.archive(), dest)
            self.assertEqual((dest/'index.html').read_bytes(), b'approved')
            with self.assertRaises(Inconclusive): extract_archive(self.archive(), dest)

    def test_escaping_archive_names_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            for number, name in enumerate(['../outside', '/absolute', 'a/../../outside', 'a\\outside']):
                with self.assertRaises(Inconclusive): extract_archive(self.archive(name), Path(temp)/str(number))

    def test_successful_review_without_successful_deploy_fails(self):
        outer = self
        class GitHub:
            deadline = time.monotonic()+30
            def read(self, route, raw=False):
                if '/workflows/' in route: return {'workflow_runs': [outer.run]}
                if '/jobs?' in route: return {'jobs': [{'name': 'publish / deploy', 'conclusion': 'skipped'}]}
                raise AssertionError('Must stop before reading any artifact')
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(Inconclusive):
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
                if '/artifacts?' in route: return {'artifacts': [{**outer.artifact, 'digest': digest(archive)}]}
                if route.endswith('/zip'): return archive + (b'x' if self.mutate else b'')
                raise AssertionError(route)
        with tempfile.TemporaryDirectory() as temp:
            evidence = prepare_one('lessons', 'a'*40, Path(temp), GitHub())
            self.assertEqual(evidence['deployment'], 'success')
            self.assertEqual(Path(evidence['root'], 'index.html').read_bytes(), b'approved')
        with tempfile.TemporaryDirectory() as temp:
            bad = GitHub(); bad.mutate = True
            with self.assertRaises(Inconclusive): prepare_one('lessons', 'a'*40, Path(temp), bad)


if __name__ == '__main__': unittest.main(verbosity=2)
