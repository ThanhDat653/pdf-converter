"""pdfplumber integration plugin."""

from __future__ import annotations

from pathlib import Path

from plugins.base_plugin import BasePlugin


class PdfPlumberPlugin(BasePlugin):
    """Text extraction plugin using pdfplumber."""

    @property
    def name(self) -> str:
        return "pdfplumber"

    def available(self) -> bool:
        try:
            import pdfplumber  # noqa: F401
            return True
        except Exception:
            return False

    def extract_text(self, pdf_path: Path, page_from: int, page_to: int | None) -> str:
        try:
            import pdfplumber
        except Exception:
            return ""

        lines: list[str] = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            last = page_to or len(pdf.pages)
            for index in range(max(1, page_from) - 1, min(last, len(pdf.pages))):
                lines.append(pdf.pages[index].extract_text() or "")
        return "\n".join(lines).strip()
