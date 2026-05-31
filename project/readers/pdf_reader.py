"""PDF reading helpers."""

from __future__ import annotations

from pathlib import Path


class PdfReader:
    """Utilities for PDF type detection and page rendering."""

    @staticmethod
    def is_text_pdf(pdf_path: Path) -> bool:
        """Return True if at least one page contains text."""
        try:
            import fitz
        except Exception:
            return False

        doc = fitz.open(str(pdf_path))
        try:
            return any(page.get_text("text").strip() for page in doc)
        finally:
            doc.close()

    @staticmethod
    def render_pages(pdf_path: Path, output_dir: Path, page_from: int, page_to: int | None) -> list[Path]:
        """Render selected pages to PNG files and return generated image paths."""
        try:
            import fitz
        except Exception:
            return []

        output_dir.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(str(pdf_path))
        paths: list[Path] = []
        try:
            end = page_to or len(doc)
            for index in range(max(1, page_from) - 1, min(end, len(doc))):
                pix = doc[index].get_pixmap(dpi=200)
                path = output_dir / f"page_{index + 1}.png"
                pix.save(str(path))
                paths.append(path)
        finally:
            doc.close()
        return paths
