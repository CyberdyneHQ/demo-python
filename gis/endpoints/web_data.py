"""Endpoint adapter for the TelMe web data feed.

Wraps the upstream `TelMeWebData` payload into the shape consumed by the
report builders. The feed is variable across vendors, so this adapter
normalizes it to a fixed schema: every returned mapping always exposes
`address`, `area_code`, and `node_id`.
"""

from typing import Dict, List, Optional


class EndpointAddress:
    """Endpoint metadata for a fibre access point."""

    def __init__(
        self,
        raw_address: Optional[str],
        area_code: str,
        node_id: str,
    ) -> None:
        self._raw_address = raw_address or ""
        self._area_code = area_code
        self._node_id = node_id

    def _normalize_address_list(self) -> List[str]:
        if not self._raw_address:
            return []
        parts = [p.strip() for p in self._raw_address.replace(",", ";").split(";")]
        return [p for p in parts if p]

    def get_telme_web_data(self) -> Dict[str, object]:
        """Return the normalized TelMe web-data payload.

        The returned mapping always includes the `address`, `area_code`,
        and `node_id` keys. `address` is always a list (possibly empty)
        of stripped, non-empty address strings.
        """
        return {
            "address": self._normalize_address_list(),
            "area_code": self._area_code,
            "node_id": self._node_id,
        }


def build_endpoint(raw: Dict[str, str]) -> EndpointAddress:
    """Construct an EndpointAddress from a raw vendor record."""
    return EndpointAddress(
        raw_address=raw.get("address"),
        area_code=raw.get("area_code", ""),
        node_id=raw.get("node_id", ""),
    )
