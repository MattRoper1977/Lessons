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

    def test_all_ten_proofs_required(self):
        report, code = census(self.needs, self.context)
        self.assertEqual((report["verdict"], code, len(report["proofs"])), ("PASS", 0, 10))
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


def declared_outputs(workflow):
    """Each job's declared outputs and the census job's needs, read from the workflow text.
    Stdlib only: the census job's runner has no YAML parser installed."""
    jobs, needs, job, in_jobs, in_outputs = {}, None, None, False, False
    for line in workflow.splitlines():
        if line == "jobs:":
            in_jobs = True
            continue
        if not in_jobs or not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 2 and line.rstrip().endswith(":"):
            job, in_outputs = line.strip()[:-1], False
        elif indent == 4:
            in_outputs = line.strip() == "outputs:"
            if job == "drift-census" and line.strip().startswith("needs:"):
                needs = [n.strip() for n in line.split("[", 1)[1].split("]", 1)[0].split(",")]
        elif indent == 6 and in_outputs:
            jobs.setdefault(job, []).append(line.strip().split(":", 1)[0])
    return jobs, needs


class WorkflowTieTests(unittest.TestCase):
    """The census must expect exactly the proofs the workflow declares: a proof added to a
    job without adding it here leaves the census UNMEASURED on every run."""

    def test_census_population_equals_the_workflow(self):
        workflow = (Path(__file__).resolve().parents[2] / ".github/workflows/ux2-gates.yml").read_text("utf-8")
        jobs, needs = declared_outputs(workflow)
        self.assertEqual(sorted(needs or []), sorted(PROOFS))
        for job, proofs in PROOFS.items():
            with self.subTest(job=job):
                self.assertEqual(sorted(jobs.get(job, [])), sorted(proofs))

    def test_the_tie_can_fail(self):
        workflow = "jobs:\n  catalogue-contract:\n    outputs:\n      schema: x\n      extra: y\n" \
                   "  drift-census:\n    needs: [catalogue-contract]\n"
        jobs, needs = declared_outputs(workflow)
        self.assertEqual((jobs, needs), ({"catalogue-contract": ["schema", "extra"]}, ["catalogue-contract"]))
        self.assertNotEqual(sorted(jobs["catalogue-contract"]), sorted(PROOFS["catalogue-contract"]))


if __name__ == "__main__":
    unittest.main()
