"""Extraction result model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExtractionResult:
    """Standard extraction payload across engines and plugins."""

    text: str = ""
    tables: list[list[dict[str, Any]]] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
