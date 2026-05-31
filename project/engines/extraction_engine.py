"""Main extraction workflow engine."""

from __future__ import annotations

from models.extraction_result import ExtractionResult
from models.task import Task
from readers.pdf_reader import PdfReader
from extractors.layout_analyzer import LayoutAnalyzer
from extractors.table_extractor import TableExtractor
from extractors.text_extractor import TextExtractor


class ExtractionEngine:
    """Run extraction flow based on task mode and PDF type."""

    def __init__(self, config) -> None:
        self.config = config
        threshold = int(config.get_nested("matching", "threshold", default=80))
        self.table_extractor = TableExtractor()
        self.table_extractor.matcher.threshold = threshold
        self.text_extractor = TextExtractor()

    def execute(self, task: Task, progress_callback=None) -> ExtractionResult:
        """Execute extraction task and return normalized result."""
        result = ExtractionResult()
        is_text_pdf = PdfReader.is_text_pdf(task.pdf_path)
        result.metadata.update(LayoutAnalyzer.analyze(task.pdf_path))
        result.metadata["is_text_pdf"] = is_text_pdf

        if progress_callback:
            progress_callback(10, "Đang phân tích loại PDF")

        if task.extract_mode == "table":
            if progress_callback:
                progress_callback(50, "Đang trích xuất bảng")
            result.tables = self.table_extractor.extract(
                task.pdf_path,
                task.page_from,
                task.page_to,
                task.headers,
                task.auto_detect_header,
            )
        else:
            if progress_callback:
                progress_callback(50, "Đang trích xuất nội dung văn bản")
            use_ocr = task.use_ocr_for_scan and not is_text_pdf
            result.text = self.text_extractor.extract(task.pdf_path, task.page_from, task.page_to, use_ocr)

        if progress_callback:
            progress_callback(90, "Đang hoàn tất trích xuất")
        return result
