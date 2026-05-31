"""Application entrypoint for PDF Document Converter Pro."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.config_manager import ConfigManager
from core.controller import Controller
from core.logger import configure_logging
from ui.main_window import MainWindow


def main() -> int:
    """Initialize dependencies and launch the desktop application."""
    base_dir = Path(__file__).resolve().parent
    configure_logging(base_dir / "logs" / "application.log")
    config = ConfigManager(base_dir / "config" / "settings.json")

    app = QApplication(sys.argv)
    app.setApplicationName("PDF Document Converter Pro")

    window = MainWindow(config=config)
    controller = Controller(window=window, config=config, base_dir=base_dir)
    window.bind_controller(controller)

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
