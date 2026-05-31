"""JSON exporter for extraction metadata and content."""

from __future__ import annotations

import json
from pathlib import Path

from models.extraction_result import ExtractionResult


class JsonExporter:
    """Serialize extraction results to JSON."""

    def export(self, result: ExtractionResult, output_path: Path) -> None:
        """Dump extraction result as UTF-8 JSON."""
        payload = {
            "text": result.text,
            "tables": result.tables,
            "images": result.images,
            "metadata": result.metadata,
            "errors": result.errors,
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
