"""Fuzzy schema matching for table headers."""

from __future__ import annotations

from difflib import SequenceMatcher


class SchemaMatcher:
    """Match detected headers to expected schema using fuzzy comparison."""

    def __init__(self, threshold: int = 80) -> None:
        self.threshold = threshold

    @staticmethod
    def _score(left: str, right: str) -> int:
        try:
            from rapidfuzz import fuzz

            return int(fuzz.ratio(left, right))
        except Exception:
            return int(SequenceMatcher(None, left.lower(), right.lower()).ratio() * 100)

    def is_match(self, detected: list[str], expected: list[str]) -> bool:
        """Return True if expected headers align with detected headers by threshold."""
        if not detected or not expected or len(detected) < len(expected):
            return False

        return all(
            self._score(detected[i].strip(), expected[i].strip()) >= self.threshold
            for i in range(len(expected))
        )
