"""Access-point report download request handler.

Builds the per-node fibre balance report consumed by the access-point
download endpoint. Circuits are filtered against a registry of address
-> leil identifiers; only circuits whose ending point has a registered
address survive into the report.
"""

from typing import Dict, Iterable, List


def _canonicalize(address: str) -> str:
    return address.strip().lower().replace(" ", "")


def get_fibre_balance_summary(
    circuits: Iterable, addr_to_leil: Dict[str, str]
) -> List:
    """Return the circuits whose ending-point address is in the registry."""
    useable_circs: List = []

    for c in circuits:
        end_point = c.get_ending_point()
        if end_point:
            end_point_addresses = end_point.get_telme_web_data()
            for adr in end_point_addresses["address"]:
                if _canonicalize(adr) in addr_to_leil:
                    useable_circs.append(c)
                    break

    return useable_circs


def build_accesspoint_report(
    circuits: Iterable, addr_to_leil: Dict[str, str]
) -> Dict[str, object]:
    """Assemble the access-point report payload for download."""
    useable = get_fibre_balance_summary(circuits, addr_to_leil)
    return {
        "circuits": [c.identifier() for c in useable],
        "count": len(useable),
    }
