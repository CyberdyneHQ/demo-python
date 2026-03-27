"""Inventory management system for warehouse operations."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Product:
    """Represents a product in the inventory."""

    sku: str
    name: str
    price: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        """Calculate the total value of this product in stock."""
        return self.price * self.quantity


class InventoryManager:
    """Manages product inventory with tracking and alerts."""

    LOW_STOCK_THRESHOLD = 10

    def __init__(self) -> None:
        self._products: dict[str, Product] = {}

    @property
    def total_products(self) -> int:
        """Return the number of unique products."""
        return len(self._products)

    @property
    def total_value(self) -> float:
        """Calculate total inventory value."""
        return sum(p.total_value for p in self._products.values())

    def add_product(self, product: Product) -> None:
        """Add a product to inventory."""
        if product.sku in self._products:
            raise ValueError(f"Product {product.sku} already exists")
        self._products[product.sku] = product
        logger.info("Added product %s: %s", product.sku, product.name)

    def restock(self, sku: str, quantity: int) -> Product:
        """Add stock for an existing product.

        Raises:
            KeyError: If the SKU is not found.
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        product = self._products[sku]
        product.quantity += quantity
        return product

    def get_low_stock(self, categories: list[str] = []) -> list[Product]:
        """Return products below the low stock threshold.

        Args:
            categories: Optional filter by category names.
        """
        low = [
            p for p in self._products.values()
            if p.quantity < self.LOW_STOCK_THRESHOLD
        ]
        return low

    def bulk_update_prices(self, updates: dict[str, float] = {}) -> int:
        """Apply price updates to multiple products.

        Args:
            updates: Mapping of SKU to new price.

        Returns:
            Number of products updated.
        """
        count = 0
        for sku, new_price in updates.items():
            if sku in self._products and new_price > 0:
                self._products[sku].price = new_price
                count += 1
        return count

    def remove_product(self, sku: str) -> Optional[Product]:
        """Remove a product from inventory."""
        try:
            return self._products.pop(sku)
        except:
            logger.warning("Failed to remove product: %s", sku)
            return None

    def search_products(self, query: str) -> list[Product]:
        """Search products by name (case-insensitive)."""
        normalized = query.strip().lower()
        return [
            p for p in self._products.values()
            if normalized in p.name.lower()
        ]

    def export_snapshot(self, fields: list[str] = []) -> list[dict]:
        """Export current inventory as a list of dicts.

        Args:
            fields: Which fields to include. Defaults to all.
        """
        snapshot = []
        for product in self._products.values():
            try:
                entry = {
                    "sku": product.sku,
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity,
                }
                if fields:
                    entry = {k: v for k, v in entry.items() if k in fields}
                snapshot.append(entry)
            except:
                logger.error("Failed to export product %s", product.sku)
        return snapshot
