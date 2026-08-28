import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "validate_skill_pack.py"


class SkillPackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("validate_skill_pack", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.module)

    def test_public_skill_pack_is_complete(self):
        self.assertEqual(self.module.main(), 0)

    def test_reviewed_polygon_requirement_path_allows_nominative_reference(self):
        path = "docs/product-requirements/comp-intel/README.md"
        self.assertIsNone(self.module.public_safety_violation(path, "Polygon golden example"))

    def test_polygon_allowlist_does_not_allow_internal_addressing(self):
        path = "docs/product-requirements/comp-intel/README.md"
        self.assertEqual(
            self.module.public_safety_violation(path, "contact user@polygon.example"),
            "@polygon",
        )

    def test_polygon_reference_remains_blocked_outside_allowlist(self):
        path = "skills/example/examples/EX-synthetic.md"
        self.assertEqual(
            self.module.public_safety_violation(path, "Polygon internal example"),
            "Polygon",
        )


if __name__ == "__main__":
    unittest.main()
