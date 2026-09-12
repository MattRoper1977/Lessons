"""Controls for the PIN1 reporter, not claims of GitHub trigger execution."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from drift_census import PROOFS, census


class CensusTests(unittest.TestCase):
    def setUp(self):
        self.needs = {job: {"result": "success", "outputs": dict.fromkeys(proofs, "success")}
                      for job, proofs in PROOFS.items()}
        self.context = {"repository": "fixture/repo", "sha": "a" * 40, "event": "schedule",
                        "run_id": "1", "run_attempt": "1"}

    def test_all_nine_proofs_required(self):
        report, code = census(self.needs, self.context)
        self.assertEqual((report["verdict"], code, len(report["proofs"])), ("PASS", 0, 9))
        for job, proofs in PROOFS.items():
            for proof in proofs:
                for outcome, expected in [("failure", 1), ("skipped", 2), ("cancelled", 2),
                                          ("", 2), ("unknown", 2), (None, 2)]:
                    with self.subTest(job=job, proof=proof, outcome=outcome):
                        value = copy.deepcopy(self.needs)
                        value[job]["outputs"][proof] = outcome
                        self.assertEqual(census(value, self.context)[1], expected)
                value = copy.deepcopy(self.needs)
                del value[job]["outputs"][proof]
                self.assertEqual(census(value, self.context)[1], 2)

    def test_job_failure_and_incomplete_population(self):
        for job in PROOFS:
            for result, expected in [("failure", 1), ("skipped", 2), ("cancelled", 2), (None, 2)]:
                value = copy.deepcopy(self.needs)
                value[job]["result"] = result
                self.assertEqual(census(value, self.context)[1], expected)
            value = copy.deepcopy(self.needs)
            del value[job]
            self.assertEqual(census(value, self.context)[1], 2)
        value = copy.deepcopy(self.needs)
        value["new-job"] = {"result": "success"}
        self.assertEqual(census(value, self.context)[1], 2)

    def test_missing_context_and_malformed_evidence(self):
        for key in self.context:
            context = dict(self.context)
            del context[key]
            self.assertEqual(census(self.needs, context)[1], 2)
        for value in [None, [], "success", {}, {"derived-data": []}]:
            self.assertEqual(census(value, self.context)[1], 2)

    def test_incomplete_census_retains_known_failure(self):
        self.needs["derived-data"]["outputs"] = {"spine": "failure", "sizes": "skipped"}
        report, code = census(self.needs, self.context)
        self.assertEqual((report["verdict"], code), ("UNMEASURED", 2))
        self.assertTrue(report["failures"])
        self.assertTrue(report["unmeasured"])

    def test_cli_preserves_report_on_unmeasured(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {**os.environ, "UX2_NEEDS": "{malformed", "GITHUB_STEP_SUMMARY": folder + "/summary.md"}
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("drift_census.py")),
                                     "--out", folder], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            report = json.loads(Path(folder, "census.json").read_text())
            self.assertEqual(report["verdict"], "UNMEASURED")
            self.assertIn("UNMEASURED", Path(folder, "summary.md").read_text())
            self.assertEqual(Path(folder, "summary.md").read_text(), Path(folder, "census.md").read_text())


if __name__ == "__main__":
    unittest.main()
