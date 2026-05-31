"""Task utility helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class TaskManager:
    """Create output paths and names for processed files."""

    @staticmethod
    def build_output_path(output_dir: Path, source_name: str, extension: str) -> Path:
        """Build timestamped output path in yyyyMMdd_HHmmss_filename.ext format."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = Path(source_name).stem.replace(" ", "_")
        return output_dir / f"{ts}_{safe_name}.{extension.lstrip('.')}"
