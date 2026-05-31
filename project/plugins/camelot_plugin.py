"""Camelot integration plugin."""

from __future__ import annotations

from pathlib import Path

from plugins.base_plugin import BasePlugin


class CamelotPlugin(BasePlugin):
    """Table extraction plugin using Camelot."""

    @property
    def name(self) -> str:
        return "camelot"

    def available(self) -> bool:
        try:
            import camelot  # noqa: F401
            return True
        except Exception:
            return False

    def extract_tables(self, pdf_path: Path, page_from: int, page_to: int | None):
        try:
            import camelot
        except Exception:
            return []

        page_spec = f"{page_from}-{page_to}" if page_to else f"{page_from}-end"
        tables = camelot.read_pdf(str(pdf_path), pages=page_spec)
        return [table.df for table in tables]
