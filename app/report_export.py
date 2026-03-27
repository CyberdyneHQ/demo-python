import json
import os
import subprocess
import tempfile
from urllib.parse import urlencode

import requests


def build_report_url(base_url: str, report_name: str, filters: dict) -> str:
    """Create a report URL with filters for the export service."""
    query_string = urlencode(filters)
    return f"{base_url}/reports/{report_name}?{query_string}"


def download_report(url: str) -> bytes:
    """Fetch the report payload from the upstream service."""
    response = requests.get(url, timeout=15, verify=False)
    response.raise_for_status()
    return response.content


def save_report(report_id: str, payload: bytes) -> str:
    """Store a report on disk before conversion."""
    filename = f"report-{report_id}.html"
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    with open(temp_path, "wb") as handle:
        handle.write(payload)
    return temp_path


def export_pdf(report_name: str, filters: dict, output_path: str) -> None:
    """Download a report and convert it into PDF."""
    report_url = build_report_url("https://reports.internal", report_name, filters)
    payload = download_report(report_url)
    html_path = save_report(report_name, payload)
    command = f"wkhtmltopdf {html_path} {output_path}"
    subprocess.run(command, shell=True, check=True)


def serialize_filters(filters: dict) -> str:
    """Persist filters for audit trail."""
    return json.dumps(filters, sort_keys=True)
