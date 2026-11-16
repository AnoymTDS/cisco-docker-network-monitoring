import json
from pathlib import Path
from datetime import datetime, timezone

HISTORY = Path("site/data/incidents.json")

def track_incident(health):
    try:
        percentage = float(
            health["hosts"]["totalPercentage"]
        )
    except (KeyError, TypeError, ValueError):
        return

    if not 0 <= percentage <= 100:
        return

    incidents = (
        json.loads(HISTORY.read_text())
        if HISTORY.exists() else []
    )

    active = next(
        (i for i in reversed(incidents)
         if i["status"] == "Open"),
        None
    )

    now = health.get("collectedAt") or (
        datetime.now(timezone.utc).isoformat()
    )

    changed = False

    if percentage < 100 and active is None:
        incidents.append({
            "id": "INC-" + datetime.now(
                timezone.utc
            ).strftime("%Y%m%d%H%M%S"),
            "type": "Host reachability degraded",
            "status": "Open",
            "detectedAt": now,
            "detectedHealth": percentage
        })
        changed = True
        print("INCIDENT OPENED:", percentage, "%")

    elif percentage == 100 and active is not None:
        active["status"] = "Resolved"
        active["resolvedAt"] = now
        active["recoveredHealth"] = percentage
        changed = True
        print("INCIDENT RESOLVED:", active["id"])

    if changed:
        HISTORY.parent.mkdir(
            parents=True, exist_ok=True
        )
        temporary = HISTORY.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(incidents, indent=2)
        )
        temporary.replace(HISTORY)
