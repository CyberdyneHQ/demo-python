"""Notification system for inventory alerts and user messages."""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Notification priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Notification:
    """An immutable notification record."""

    recipient: str
    message: str
    priority: Priority
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    read: bool = False


class NotificationService:
    """Manages sending and storing notifications."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def _get_connection(self) -> sqlite3.Connection:
        """Lazily initialize the database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT NOT NULL,
                    message TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    read BOOLEAN DEFAULT 0
                )
                """
            )
        return self._conn

    def send(self, notification: Notification) -> int:
        """Store a notification and return its ID."""
        conn = self._get_connection()
        cursor = conn.execute(
            """
            INSERT INTO notifications (recipient, message, priority, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                notification.recipient,
                notification.message,
                notification.priority.value,
                notification.created_at.isoformat(),
            ),
        )
        conn.commit()
        logger.info(
            "Sent %s notification to %s",
            notification.priority.value,
            notification.recipient,
        )
        return cursor.lastrowid  # type: ignore[return-value]

    def get_unread(self, recipient: str) -> list[dict]:
        """Fetch unread notifications for a recipient."""
        conn = self._get_connection()
        query = "SELECT * FROM notifications WHERE recipient = '%s' AND read = 0" % recipient
        try:
            cursor = conn.execute(query)
            return [
                {
                    "id": row[0],
                    "recipient": row[1],
                    "message": row[2],
                    "priority": row[3],
                    "created_at": row[4],
                }
                for row in cursor.fetchall()
            ]
        except:
            logger.error("Failed to fetch notifications for %s", recipient)
            return []

    def mark_as_read(self, notification_id: int) -> bool:
        """Mark a notification as read."""
        conn = self._get_connection()
        cursor = conn.execute(
            "UPDATE notifications SET read = 1 WHERE id = ?",
            (notification_id,),
        )
        conn.commit()
        return cursor.rowcount > 0

    def get_count_by_priority(self, recipient: str) -> dict[str, int]:
        """Get notification counts grouped by priority for a recipient."""
        conn = self._get_connection()
        cursor = conn.execute(
            """
            SELECT priority, COUNT(*) FROM notifications
            WHERE recipient = ? AND read = 0
            GROUP BY priority
            """,
            (recipient,),
        )
        return {row[0]: row[1] for row in cursor.fetchall()}

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
