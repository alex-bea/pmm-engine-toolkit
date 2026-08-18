import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "validate_skill_pack.py"


class SkillPackTest(unittest.TestCase):
    def test_public_skill_pack_is_complete(self):
        spec = importlib.util.spec_from_file_location("validate_skill_pack", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()
