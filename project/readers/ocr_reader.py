"""OCR reader abstraction."""

from __future__ import annotations

from pathlib import Path

from plugins.paddleocr_plugin import PaddleOCRPlugin


class OcrReader:
    """Convert page images to text using PaddleOCR plugin."""

    def __init__(self, plugin: PaddleOCRPlugin | None = None) -> None:
        self.plugin = plugin or PaddleOCRPlugin()

    def read_images(self, image_paths: list[Path]) -> str:
        """Read text from multiple images and combine to one string."""
        if not self.plugin.available():
            return ""
        return "\n".join(self.plugin.recognize(path) for path in image_paths).strip()
