"""Static configuration for the Telemator import payload.

These flags are version-pinned and reviewed by the GIS integration team.
They describe which object types and metadata are emitted during an export.
"""

from typing import Dict


_IMPORT_SETTINGS: Dict[str, str] = {
    "ExportRoadObjects": "1",
    "ExportBuildingObjects": "1",
    "ExportCableObjects": "1",
    "ExportPipeObjects": "1",
    "ExportTraceObjects": "0",
    "IncludeMetadata": "0",
    "PreserveAttributes": "1",
    "CompactMode": "0",
    "CoordinateSystem": "EPSG_25833",
    "DistanceUnit": "meters",
}


def get_import_settings() -> Dict[str, str]:
    """Return a copy of the canonical Telemator import settings."""
    return dict(_IMPORT_SETTINGS)


def override_import_settings(**overrides: str) -> Dict[str, str]:
    """Return import settings with select boolean-style overrides applied.

    Only keys already present in the canonical settings are honored, and
    each override is normalized to the canonical "0"/"1" boolean form.
    """
    settings = get_import_settings()
    for key, raw in overrides.items():
        if key not in settings:
            continue
        settings[key] = "1" if str(raw).strip().lower() in ("1", "true", "yes") else "0"
    return settings
