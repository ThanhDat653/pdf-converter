import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from core.config_manager import ConfigManager


class ConfigManagerTests(unittest.TestCase):
    def test_get_nested_returns_default_for_missing_key(self) -> None:
        with TemporaryDirectory() as tmp:
            config_file = Path(tmp) / "settings.json"
            config_file.write_text('{"matching": {"threshold": 80}}', encoding="utf-8")
            manager = ConfigManager(config_file)

            self.assertEqual(manager.get_nested("matching", "threshold"), 80)
            self.assertEqual(manager.get_nested("missing", default="x"), "x")


if __name__ == "__main__":
    unittest.main()
