"""Text extraction services."""

from __future__ import annotations

from pathlib import Path

from plugins.pdfplumber_plugin import PdfPlumberPlugin
from readers.ocr_reader import OcrReader
from readers.pdf_reader import PdfReader


class TextExtractor:
    """Extract text from text PDFs or scanned PDFs (OCR)."""

    def __init__(self, pdf_plugin: PdfPlumberPlugin | None = None, ocr_reader: OcrReader | None = None) -> None:
        self.pdf_plugin = pdf_plugin or PdfPlumberPlugin()
        self.ocr_reader = ocr_reader or OcrReader()

    def extract(self, pdf_path: Path, page_from: int, page_to: int | None, use_ocr: bool) -> str:
        """Extract text based on PDF type and OCR preference."""
        if self.pdf_plugin.available():
            text = self.pdf_plugin.extract_text(pdf_path, page_from, page_to)
            if text:
                return text

        if not use_ocr:
            return ""

        image_paths = PdfReader.render_pages(pdf_path, pdf_path.parent / ".tmp_images", page_from, page_to)
        return self.ocr_reader.read_images(image_paths)
