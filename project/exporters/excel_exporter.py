"""Excel exporter implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ExcelExporter:
    """Export tables to .xlsx using pandas/openpyxl."""

    def export(self, tables: list[list[dict[str, Any]]], output_path: Path) -> None:
        """Write each table to a dedicated sheet."""
        try:
            import pandas as pd
        except Exception as exc:
            raise RuntimeError("pandas is required for Excel export") from exc

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            if not tables:
                pd.DataFrame().to_excel(writer, sheet_name="Table_1", index=False)
                return
            for index, rows in enumerate(tables, start=1):
                pd.DataFrame(rows).to_excel(writer, sheet_name=f"Table_{index}", index=False)
