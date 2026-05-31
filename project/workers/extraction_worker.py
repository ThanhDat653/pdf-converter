"""Background worker for extraction and export tasks."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from models.task import Task


class ExtractionWorker(QThread):
    """QThread worker to keep long-running tasks off the UI thread."""

    progress_changed = Signal(int)
    status_changed = Signal(str)
    preview_ready = Signal(list)
    completed = Signal(str)
    failed = Signal(str)

    def __init__(self, task: Task, extraction_engine, export_engine, output_path: Path) -> None:
        super().__init__()
        self.task = task
        self.extraction_engine = extraction_engine
        self.export_engine = export_engine
        self.output_path = output_path
        self._cancelled = False

    def cancel(self) -> None:
        """Cancel worker execution."""
        self._cancelled = True

    def run(self) -> None:
        """Execute extraction and export workflow."""
        try:
            def on_progress(value: int, status: str) -> None:
                if self._cancelled:
                    raise RuntimeError("Tác vụ đã bị hủy")
                self.progress_changed.emit(value)
                self.status_changed.emit(status)

            result = self.extraction_engine.execute(self.task, progress_callback=on_progress)
            if result.tables:
                self.preview_ready.emit(result.tables[0])
            elif result.text:
                self.preview_ready.emit([{"text": result.text[:1000]}])

            self.status_changed.emit("Đang xuất file")
            self.export_engine.export(self.task, result, self.output_path)
            self.progress_changed.emit(100)
            self.completed.emit(f"Hoàn thành: {self.output_path}")
        except Exception as exc:
            self.failed.emit(str(exc))
