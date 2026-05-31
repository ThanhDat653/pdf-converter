"""Image reader utilities."""

from __future__ import annotations

from pathlib import Path


class ImageReader:
    """Simple image metadata loader."""

    @staticmethod
    def size(image_path: Path) -> tuple[int, int] | None:
        """Return image width and height."""
        try:
            from PIL import Image
        except Exception:
            return None
        with Image.open(image_path) as img:
            return img.size
