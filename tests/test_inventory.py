import json
import tempfile
import unittest
from pathlib import Path

from inventory_automation.client import ApiRequestError, HttpsApiClient
from inventory_automation.parsers import InventoryFormatError, parse_file
from inventory_automation.service import validate_inventory, write_results


ROOT = Path(__file__).resolve().parents[1]


class InventoryAutomationTests(unittest.TestCase):
    def test_parses_all_supported_sample_formats(self):
        for filename in ("inventory.json", "inventory.csv", "inventory.xml", "inventory.yaml"):
            with self.subTest(filename=filename):
                self.assertGreaterEqual(len(parse_file(ROOT / "data" / filename)), 2)

    def test_validates_invalid_ip_and_keeps_valid_records(self):
        result = validate_inventory(parse_file(ROOT / "data" / "inventory.json"))
        self.assertEqual(3, len(result.devices))
        self.assertEqual(1, len(result.errors))
        self.assertEqual(2, result.summary()["active_devices"])

    def test_rejects_non_https_api(self):
        with self.assertRaises(ApiRequestError):
            HttpsApiClient().get_json("http://inventory.example/api")

    def test_writes_structured_results(self):
        result = validate_inventory(parse_file(ROOT / "data" / "inventory.csv"))
        with tempfile.TemporaryDirectory() as directory:
            write_results(result, Path(directory))
            report = json.loads((Path(directory) / "inventory_report.json").read_text(encoding="utf-8"))
            self.assertEqual(2, report["summary"]["total_devices"])
            self.assertTrue((Path(directory) / "inventory_report.csv").exists())

    def test_rejects_unsupported_format(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "inventory.txt"
            source.write_text("not an inventory", encoding="utf-8")
            with self.assertRaises(InventoryFormatError):
                parse_file(source)


if __name__ == "__main__":
    unittest.main()
