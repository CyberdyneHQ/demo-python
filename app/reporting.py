"""Report generation utilities for inventory analytics."""

from __future__ import annotations

import csv
import io
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ReportMetadata:
    """Metadata for a generated report."""

    title: str
    generated_at: datetime
    record_count: int
    format: str


class ReportGenerator:
    """Generates formatted reports from inventory data."""

    SUPPORTED_FORMATS = ("csv", "text")

    def __init__(self, title: str = "Inventory Report") -> None:
        self._title = title

    def generate_csv(
        self,
        data: list[dict[str, Any]],
        filters: dict[str, Any] = {},
    ) -> tuple[str, ReportMetadata]:
        """Generate a CSV report from data records.

        Args:
            data: List of record dicts.
            filters: Optional filters that were applied (for metadata).

        Returns:
            Tuple of (csv_content, metadata).
        """
        if not data:
            return "", ReportMetadata(
                title=self._title,
                generated_at=datetime.now(timezone.utc),
                record_count=0,
                format="csv",
            )

        output = io.StringIO()
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for record in data:
            writer.writerow(record)

        metadata = ReportMetadata(
            title=self._title,
            generated_at=datetime.now(timezone.utc),
            record_count=len(data),
            format="csv",
        )
        return output.getvalue(), metadata

    def generate_text_summary(
        self,
        data: list[dict[str, Any]],
        columns: list[str] = [],
    ) -> str:
        """Generate a plain text summary of the data.

        Args:
            data: List of record dicts.
            columns: Which columns to include. Empty means all.
        """
        if not data:
            return f"{self._title}\nNo records found."

        lines = [self._title, "=" * len(self._title), ""]

        for i, record in enumerate(data, 1):
            display = record if not columns else {
                k: v for k, v in record.items() if k in columns
            }
            parts = [f"{k}: {v}" for k, v in display.items()]
            lines.append(f"  {i}. {', '.join(parts)}")

        lines.append("")
        lines.append(f"Total: {len(data)} records")
        return "\n".join(lines)

    def generate_summary_stats(
        self,
        data: list[dict[str, Any]],
        numeric_field: str,
        group_by: Optional[str] = None,
    ) -> dict[str, Any]:
        """Calculate summary statistics for a numeric field.

        Args:
            data: List of record dicts.
            numeric_field: The field to aggregate.
            group_by: Optional field to group results.

        Returns:
            Dict with min, max, mean, total, and count.
        """
        if not data:
            return {"count": 0}

        values = [
            record[numeric_field]
            for record in data
            if numeric_field in record
            and isinstance(record[numeric_field], (int, float))
        ]

        if not values:
            return {"count": 0}

        return {
            "count": len(values),
            "total": sum(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
