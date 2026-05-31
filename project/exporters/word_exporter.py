"""Word exporter implementation."""

from __future__ import annotations

from pathlib import Path


class WordExporter:
    """Export text to .docx file."""

    def export(self, text: str, output_path: Path) -> None:
        """Write text into a Word document."""
        try:
            from docx import Document
        except Exception as exc:
            raise RuntimeError("python-docx is required for Word export") from exc

        document = Document()
        for line in text.splitlines() or [""]:
            document.add_paragraph(line)
        document.save(str(output_path))
