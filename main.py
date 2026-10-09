#!/usr/bin/env python3
"""Invariant data validation and append-only ledger generator.

This script validates an incoming payload, checks invariants, and appends a
signed-looking immutable transaction to state_ledger.jsonl.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

LEDGER_PATH = Path("state_ledger.jsonl")
PAYLOAD_PATH = Path("incoming_data.json")


def load_payload() -> Dict[str, Any]:
    if PAYLOAD_PATH.exists():
        with PAYLOAD_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "system_boot",
        "status": "healthy",
        "metadata": {"source": "default_seed"},
    }


def validate_payload(payload: Dict[str, Any]) -> bool:
    if not isinstance(payload, dict):
        return False
    if "event" not in payload:
        return False
    if "status" not in payload:
        return False
    if "metadata" in payload and not isinstance(payload["metadata"], dict):
        return False
    return True


def append_ledger_entry(payload: Dict[str, Any]) -> Dict[str, Any]:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": payload.get("event", "unknown_event"),
        "status": payload.get("status", "unknown"),
        "metadata": payload.get("metadata", {}),
        "source": payload.get("source", "github_actions"),
    }

    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, separators=(',', ':')) + "\n")

    return entry


def main() -> None:
    payload = load_payload()
    valid = validate_payload(payload)
    if not valid:
        raise ValueError("Incoming payload failed invariant validation")

    record = append_ledger_entry(payload)
    print(json.dumps({"status": "ok", "record": record}, indent=2))


if __name__ == "__main__":
    main()
