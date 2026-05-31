"""Controller coordinating UI and processing workers."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from core.task_manager import TaskManager
from engines.export_engine import ExportEngine
from engines.extraction_engine import ExtractionEngine
from models.task import Task
from workers.extraction_worker import ExtractionWorker

LOGGER = logging.getLogger(__name__)


class Controller:
    """Main orchestration layer between UI and business logic."""

    def __init__(self, window, config, base_dir: Path) -> None:
        self.window = window
        self.config = config
        self.base_dir = base_dir
        self.worker: ExtractionWorker | None = None
        self.output_path: Path | None = None

    def start_task(self, task: Task) -> None:
        """Start extraction task in background thread."""
        output_dir = self.base_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        ext = "xlsx" if task.extract_mode == "table" else "docx"
        self.output_path = TaskManager.build_output_path(output_dir, task.pdf_path.name, ext)

        extraction_engine = ExtractionEngine(config=self.config)
        export_engine = ExportEngine(config=self.config)
        self.worker = ExtractionWorker(
            task=task,
            extraction_engine=extraction_engine,
            export_engine=export_engine,
            output_path=self.output_path,
        )
        self.worker.progress_changed.connect(self.window.update_progress)
        self.worker.status_changed.connect(self.window.update_status)
        self.worker.preview_ready.connect(self.window.update_preview)
        self.worker.completed.connect(self._on_completed)
        self.worker.failed.connect(self._on_failed)
        self.worker.start()

    def cancel_task(self) -> None:
        """Request task cancellation."""
        if self.worker is not None:
            self.worker.cancel()

    def open_output_file(self) -> None:
        """Open latest output file using OS shell."""
        if self.output_path and self.output_path.exists():
            self._open_path(self.output_path)

    def open_output_folder(self) -> None:
        """Open output folder in file explorer."""
        self._open_path(self.base_dir / "output")

    def _open_path(self, path: Path) -> None:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)], check=False)

    def _on_completed(self, message: str) -> None:
        LOGGER.info(message)
        self.window.on_completed(message)

    def _on_failed(self, message: str) -> None:
        LOGGER.exception(message)
        self.window.on_failed(message)
