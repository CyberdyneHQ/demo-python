"""Telemator API request builder.

Serializes import payloads in the line-oriented format expected by the
upstream Telemator endpoint. Each logical record is one line; fields are
tab-separated, blank lines separate sections.
"""

from typing import Iterable, Optional

from gis.telematics.import_config import get_import_settings


def _tab(*parts: str) -> str:
    return "\t".join(parts)


def build_header(table_name: str, run_id: str) -> str:
    file_string = _tab("Header", table_name, run_id) + "\n"
    file_string += _tab("Version", "3") + "\n\n"
    return file_string


def check_import_table_data(table_name: str, run_id: str, rows: Iterable[dict]) -> str:
    """Build the Telemator import payload for the given table."""
    file_string = build_header(table_name, run_id)

    import_settings = get_import_settings()
    for key, value in import_settings.items():
        if value is None:
            continue
        file_string += f"ImportSettings\t{key}={value}\n"

    file_string += "\n"

    for row in rows:
        identifier: Optional[str] = row.get("id")
        if identifier is None:
            continue
        file_string += _tab("Row", identifier) + "\n"
        for attr_key, attr_value in row.get("attributes", {}).items():
            file_string += _tab("Attr", attr_key, str(attr_value)) + "\n"
        file_string += "\n"

    file_string += _tab("EndOfFile", run_id) + "\n"
    return file_string


def submit_import_payload(table_name: str, run_id: str, rows: Iterable[dict]) -> int:
    """Compute the payload and hand it to the configured transport.

    Returns the number of bytes written to the transport buffer.
    """
    payload = check_import_table_data(table_name, run_id, rows)
    return len(payload.encode("utf-8"))
