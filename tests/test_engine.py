import json
import unittest
from pathlib import Path

from agentic_economics.engine import evaluate_scenario


class EconomicsTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(Path("scenarios/soc-triage.json").read_text())

    def test_cloud_cost_is_attributed_per_unit(self):
        result = evaluate_scenario(self.config, "azure")
        self.assertGreater(result.unit_cost, 0)
        self.assertAlmostEqual(result.monthly_cost, result.unit_cost * 12000)

    def test_on_prem_includes_full_tco(self):
        result = evaluate_scenario(self.config, "on_prem")
        self.assertGreater(result.assumptions["calculated_monthly_tco"], 0)

    def test_release_policy_is_enforced(self):
        self.config["release_policy"]["minimum_roi"] = 10**9
        self.assertEqual(evaluate_scenario(self.config, "azure").release_decision, "BLOCK")

    def test_invalid_deployment_fails_closed(self):
        with self.assertRaises(ValueError):
            evaluate_scenario(self.config, "other")


if __name__ == "__main__":
    unittest.main()
