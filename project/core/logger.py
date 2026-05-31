"""Logging configuration utilities."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_file: Path) -> None:
    """Configure application-wide logging output."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
    )
