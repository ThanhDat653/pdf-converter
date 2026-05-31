"""Table extraction services."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from extractors.schema_matcher import SchemaMatcher
from plugins.camelot_plugin import CamelotPlugin


class TableExtractor:
    """Extract and normalize tabular data from PDF."""

    def __init__(self, plugin: CamelotPlugin | None = None, matcher: SchemaMatcher | None = None) -> None:
        self.plugin = plugin or CamelotPlugin()
        self.matcher = matcher or SchemaMatcher()

    def extract(
        self,
        pdf_path: Path,
        page_from: int,
        page_to: int | None,
        headers: list[str],
        auto_detect_header: bool,
    ) -> list[list[dict[str, Any]]]:
        """Extract tables and return row dictionaries."""
        if not self.plugin.available():
            return []

        table_frames = self.plugin.extract_tables(pdf_path, page_from, page_to)
        normalized: list[list[dict[str, Any]]] = []

        for frame in table_frames:
            if frame.empty:
                continue
            if auto_detect_header:
                local_headers = [str(cell).strip() for cell in frame.iloc[0].tolist()]
            else:
                local_headers = headers

            if headers and not self.matcher.is_match(local_headers[: len(headers)], headers):
                continue

            if auto_detect_header:
                data = frame.iloc[1:]
            else:
                data = frame

            columns = local_headers[: len(data.columns)]
            data.columns = columns
            normalized.append(data.fillna("").to_dict(orient="records"))

        return normalized
