from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from generate_data import generate_dataset, write_dataset
from validate_data import validate


class DataGenerationSmokeTest(unittest.TestCase):
    def test_generation_is_deterministic(self) -> None:
        first_tables, first_manifest = generate_dataset(28, 20260801)
        second_tables, second_manifest = generate_dataset(28, 20260801)
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(first_tables, second_tables)

    def test_every_scenario_and_business_rule_passes(self) -> None:
        tables, manifest = generate_dataset(28, 20260801)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_dataset(tables, manifest, root)
            report = validate(root)
        self.assertEqual("PASS", report["status"], report["errors"])
        self.assertEqual(14, len(manifest["scenario_counts"]))


if __name__ == "__main__":
    unittest.main()
