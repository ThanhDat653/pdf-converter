"""Configuration management from JSON settings file."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """Load and expose settings from config/settings.json."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._config = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, key: str, default: Any = None) -> Any:
        """Get a top-level config value."""
        return self._config.get(key, default)

    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """Get a nested config value safely."""
        current: Any = self._config
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current
