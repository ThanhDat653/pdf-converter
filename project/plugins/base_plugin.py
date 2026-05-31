"""Base plugin contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """Base class for pluggable extraction providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable plugin name."""

    @abstractmethod
    def available(self) -> bool:
        """Return True when plugin dependencies are available."""
