"""Task model for conversion requests."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Task:
    """Task options collected from UI."""

    pdf_path: Path
    extract_mode: str
    page_from: int = 1
    page_to: int | None = None
    use_ocr_for_scan: bool = True
    auto_detect_header: bool = True
    headers: list[str] = field(default_factory=list)
