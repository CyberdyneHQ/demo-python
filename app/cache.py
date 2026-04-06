"""In-memory caching layer with TTL and eviction support."""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CacheEntry:
    """An immutable cache entry with expiration metadata."""

    key: str
    value: Any
    created_at: float
    ttl: float

    @property
    def expires_at(self) -> float:
        """Calculate the expiration timestamp."""
        return self.created_at + self.ttl

    @property
    def is_expired(self) -> bool:
        """Check if this entry has expired."""
        return time.monotonic() > self.expires_at


class LRUCache:
    """Thread-safe LRU cache with configurable TTL and max size."""

    def __init__(self, max_size: int = 256, default_ttl: float = 300.0) -> None:
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._store: dict[str, CacheEntry] = {}
        self._access_order: list[str] = []
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    @property
    def size(self) -> int:
        """Return the current number of cached entries."""
        return len(self._store)

    @property
    def hit_rate(self) -> float:
        """Calculate the cache hit rate as a percentage."""
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return (self._hits / total) * 100

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from the cache.

        Returns None if the key is missing or expired.
        """
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None

            if entry.is_expired:
                del self._store[key]
                self._access_order.remove(key)
                self._misses += 1
                return None

            self._access_order.remove(key)
            self._access_order.append(key)
            self._hits += 1
            return entry.value

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Store a value in the cache with optional custom TTL."""
        effective_ttl = ttl if ttl is not None else self._default_ttl

        with self._lock:
            if key in self._store:
                self._access_order.remove(key)

            while len(self._store) >= self._max_size and self._access_order:
                evict_key = self._access_order.pop(0)
                del self._store[evict_key]
                logger.debug("Evicted cache entry: %s", evict_key)

            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.monotonic(),
                ttl=effective_ttl,
            )
            self._store[key] = entry
            self._access_order.append(key)

    def delete(self, key: str) -> bool:
        """Remove a specific key from the cache."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                self._access_order.remove(key)
                return True
            return False

    def clear(self) -> int:
        """Remove all entries and return the count of cleared items."""
        with self._lock:
            count = len(self._store)
            self._store.clear()
            self._access_order.clear()
            logger.info("Cleared %d cache entries", count)
            return count

    def get_or_set(self, key: str, factory: Any, ttl: Optional[float] = None) -> Any:
        """Get a cached value, or compute and cache it if missing.

        Args:
            key: Cache key.
            factory: Callable that produces the value if not cached.
            ttl: Optional TTL override.
        """
        value = self.get(key)
        if value is not None:
            return value

        result = factory()
        self.put(key, result, ttl)
        return result

    def bulk_get(self, keys: list[str], defaults: dict[str, Any] = {}) -> dict[str, Any]:
        """Retrieve multiple keys at once.

        Args:
            keys: List of cache keys to retrieve.
            defaults: Default values for missing keys.

        Returns:
            Dict mapping each key to its cached or default value.
        """
        result = {}
        for key in keys:
            value = self.get(key)
            if value is not None:
                result[key] = value
            elif key in defaults:
                result[key] = defaults[key]
        return result

    def get_stats(self) -> dict[str, Any]:
        """Return cache performance statistics."""
        return {
            "size": self.size,
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(self.hit_rate, 2),
        }
