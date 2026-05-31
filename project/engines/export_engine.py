"""Export engine for DOCX/XLSX/JSON outputs."""

from __future__ import annotations

from pathlib import Path

from exporters.excel_exporter import ExcelExporter
from exporters.json_exporter import JsonExporter
from exporters.word_exporter import WordExporter
from models.extraction_result import ExtractionResult
from models.task import Task


class ExportEngine:
    """Coordinate export to requested output format."""

    def __init__(self, config) -> None:
        self.config = config
        self.excel_exporter = ExcelExporter()
        self.word_exporter = WordExporter()
        self.json_exporter = JsonExporter()

    def export(self, task: Task, result: ExtractionResult, output_path: Path) -> Path:
        """Export extraction result and companion JSON metadata."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if task.extract_mode == "table":
            self.excel_exporter.export(result.tables, output_path)
        else:
            self.word_exporter.export(result.text, output_path)

        json_path = output_path.with_suffix(".json")
        self.json_exporter.export(result, json_path)
        return output_path
