from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = "https://prices.azure.com/api/retail/prices"


def fetch_retail_prices(filter_expression: str, output: Path) -> dict:
    """Fetch a timestamped Azure retail price snapshot; no Azure login required."""
    query = urllib.parse.urlencode({"api-version": "2023-01-01-preview", "$filter": filter_expression})
    request = urllib.request.Request(f"{ENDPOINT}?{query}", headers={"User-Agent": "a2z-agentic-economics/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    snapshot = {
        "source": ENDPOINT,
        "filter": filter_expression,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "currency": "USD",
        "items": payload.get("Items", []),
        "next_page_link": payload.get("NextPageLink"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return snapshot

