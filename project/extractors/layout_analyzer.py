"""Document layout analyzer placeholders."""

from __future__ import annotations

from pathlib import Path


class LayoutAnalyzer:
    """Analyze basic PDF metadata and layout hints."""

    @staticmethod
    def analyze(pdf_path: Path) -> dict[str, str]:
        """Return lightweight layout metadata."""
        return {"filename": pdf_path.name}
