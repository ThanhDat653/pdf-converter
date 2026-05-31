"""Schema model for table header matching."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HeaderSchema:
    """Expected header schema and fuzzy matching threshold."""

    headers: list[str]
    threshold: int = 80
