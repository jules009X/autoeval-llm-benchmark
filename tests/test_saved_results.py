import copy
import tempfile
import unittest
from pathlib import Path

from autoeval.core import read_json
from scripts.preview_results import render, verify

ROOT = Path(__file__).resolve().parents[1]


class SavedResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = read_json(ROOT / "results/pilot-v0.1.json")

    def test_saved_results_recompute_exactly(self):
        self.assertEqual(verify(self.datasets), {"runs": 2, "observations": 42})

    def test_changed_score_is_rejected(self):
        changed = copy.deepcopy(self.datasets)
        changed[0]["aggregates"][0]["field_accuracy"] = 0.12345
        with self.assertRaisesRegex(ValueError, "aggregates"):
            verify(changed)

    def test_duplicated_observation_is_rejected(self):
        changed = copy.deepcopy(self.datasets)
        changed[0]["results"].append(changed[0]["results"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            verify(changed)

    def test_preview_without_documents_and_html_injection(self):
        changed = copy.deepcopy(self.datasets)
        changed[0]["results"][0]["raw_response"] = "</script><script>alert('x')</script>"
        with tempfile.TemporaryDirectory() as tmp:
            render(changed, tmp)
            text = (Path(tmp) / "index.html").read_text()
            self.assertNotIn("</script><script>alert", text)
            self.assertIn("\\u003c/script>", text)
            self.assertTrue((Path(tmp) / "results.json").exists())
            self.assertFalse((Path(tmp) / "sources").exists())


if __name__ == "__main__":
    unittest.main()
