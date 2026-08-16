#!/usr/bin/env python3
"""Upsert connector definitions into the connector API (idempotent by name).

Reads /seed/connectors.json (rendered from Helm values), substitutes
``${ENV_VAR}`` placeholders from the environment (credentials come from a
Kubernetes Secret referenced by the chart), and POSTs/PATCHes each connector
against ``$CONNECTOR_API_BASE_URL``.

A connector whose placeholders cannot all be resolved is SKIPPED with a
warning instead of failing the whole seed — this lets the chart install
cleanly before the operator has created the credentials Secret.

For websub connectors, subscription sync is triggered after the upsert when
SYNC_WEBSUB_SUBSCRIPTIONS=true (default). Sync failures are logged but not
fatal: the hub may be unreachable from a fresh environment.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("CONNECTOR_API_BASE_URL", "http://127.0.0.1:8050").rstrip("/")
SYNC = os.environ.get("SYNC_WEBSUB_SUBSCRIPTIONS", "true").lower() in ("1", "true", "yes")
WAIT_ATTEMPTS = int(os.environ.get("API_WAIT_ATTEMPTS", "60"))

_PLACEHOLDER = re.compile(r"\$\{([A-Z0-9_]+)\}")


def req(method: str, url: str, body: dict | None = None):
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=120) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {}


def wait_for_api() -> None:
    for attempt in range(WAIT_ATTEMPTS):
        try:
            req("GET", f"{BASE}/health")
            print(f"[connector-seed] API is up at {BASE}")
            return
        except Exception as exc:  # noqa: BLE001
            print(f"[connector-seed] waiting for API ({attempt + 1}/{WAIT_ATTEMPTS}): {exc}")
            time.sleep(5)
    print("[connector-seed] ERROR: connector API never became ready", file=sys.stderr)
    sys.exit(1)


def substitute(value, missing: set[str]):
    if isinstance(value, str):
        def _repl(match: re.Match) -> str:
            name = match.group(1)
            env = os.environ.get(name)
            if env is None or env == "":
                missing.add(name)
                return match.group(0)
            return env

        return _PLACEHOLDER.sub(_repl, value)
    if isinstance(value, dict):
        return {k: substitute(v, missing) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, missing) for v in value]
    return value


def main() -> int:
    with open("/seed/connectors.json", encoding="utf-8") as fh:
        specs = json.load(fh)

    if not specs:
        print("[connector-seed] No connector definitions configured; nothing to do.")
        return 0

    wait_for_api()

    existing = req("GET", f"{BASE}/connectors")
    by_name = {c["name"]: c for c in existing}

    failures = 0
    for spec in specs:
        name = spec.get("name", "<unnamed>")
        missing: set[str] = set()
        body = substitute(spec, missing)
        if missing:
            print(
                f"[connector-seed] SKIP {name!r}: unresolved placeholders "
                f"{sorted(missing)} (create/populate the seed Secret and re-run "
                "the upgrade to load this connector)"
            )
            continue

        try:
            if name in by_name:
                cid = by_name[name]["connector_id"]
                out = req(
                    "PATCH",
                    f"{BASE}/connectors/{cid}",
                    {k: v for k, v in body.items() if k != "name"},
                )
                connector_id = out.get("connector_id", cid)
                print(f"[connector-seed] UPDATED {name} ({connector_id})")
            else:
                out = req("POST", f"{BASE}/connectors", body)
                connector_id = out.get("connector_id")
                print(f"[connector-seed] CREATED {name} ({connector_id})")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            print(f"[connector-seed] ERROR upserting {name}: HTTP {exc.code} {detail}", file=sys.stderr)
            failures += 1
            continue

        if SYNC and body.get("transport_type") == "websub" and connector_id:
            try:
                sync = req("POST", f"{BASE}/connectors/{connector_id}/websub/sync-subscriptions")
                print(f"[connector-seed] SYNC {name}: {json.dumps(sync)}")
            except Exception as exc:  # noqa: BLE001
                print(f"[connector-seed] WARN: subscription sync failed for {name}: {exc}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
