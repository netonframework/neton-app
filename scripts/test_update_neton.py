import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("updater", Path(__file__).with_name("update-neton.py"))
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class VersionSelectionTest(unittest.TestCase):
    def test_numeric_order(self):
        versions = ["1.0.0-beta9", "1.0.0-beta25"]
        self.assertEqual(updater.latest_shared(versions, versions), versions[1])

    def test_shared_final_preferred_over_preview(self):
        self.assertEqual(updater.latest_shared(
            ["1.0.0-beta25", "1.0.0-beta26", "1.0.0", "2.0.0-beta1"],
            ["1.0.0-beta25", "1.0.0", "2.0.0-beta1"]), "1.0.0")

    def test_partial_final_publication_not_selected(self):
        self.assertEqual(updater.latest_shared(
            ["1.0.0-rc1", "1.0.0"], ["1.0.0-rc1"]), "1.0.0-rc1")

    def test_final_never_downgrades_to_preview(self):
        self.assertGreater(updater.version_key("1.0.0"), updater.version_key("1.0.0-rc999"))

    def test_unapproved_release_line_rejected(self):
        with self.assertRaises(ValueError):
            updater.version_key("2.0.0")

    def test_rc_after_beta(self):
        versions = ["1.0.0-beta99", "1.0.0-rc1"]
        self.assertEqual(updater.latest_shared(versions, versions), versions[1])

    def test_no_common_version_fails(self):
        with self.assertRaises(ValueError):
            updater.latest_shared(["1.0.0-beta25"], ["1.0.0-beta24"])


if __name__ == "__main__":
    unittest.main()
