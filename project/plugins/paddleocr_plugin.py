"""PaddleOCR integration plugin."""

from __future__ import annotations

from pathlib import Path

from plugins.base_plugin import BasePlugin


class PaddleOCRPlugin(BasePlugin):
    """OCR plugin using PaddleOCR."""

    @property
    def name(self) -> str:
        return "paddleocr"

    def available(self) -> bool:
        try:
            import paddleocr  # noqa: F401
            return True
        except Exception:
            return False

    def recognize(self, image_path: Path) -> str:
        try:
            from paddleocr import PaddleOCR
        except Exception:
            return ""

        ocr = PaddleOCR(use_angle_cls=True, lang="vi")
        result = ocr.ocr(str(image_path), cls=True)
        lines: list[str] = []
        for row in result or []:
            for item in row:
                lines.append(item[1][0])
        return "\n".join(lines)
