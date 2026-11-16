import json
import os
import time
import getpass
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from incident_history import track_incident

BASE = "http://127.0.0.1:58000"
OUTPUT = Path("site/data/health.json")

password = getpass.getpass("Network Controller password: ")

def get_ticket():
    credentials = {
        "username": "netadmin",
        "password": password
    }

    request = Request(
        BASE + "/api/v1/ticket",
        data=json.dumps(credentials).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=10) as response:
        return json.load(response)["response"]["serviceTicket"]

def get_health(ticket):
    request = Request(
        BASE + "/api/v1/assurance/health",
        headers={"X-Auth-Token": ticket}
    )

    with urlopen(request, timeout=10) as response:
        data = json.load(response)["response"][0]

    return {
        "hosts": data["clients"],
        "devices": data["networkDevices"]["networkDevices"],
        "collectedAt": datetime.now(timezone.utc).isoformat()
    }

token = get_ticket()
print("Authenticated. Collecting every 60 seconds.")

try:
    while True:
        try:
            try:
                health = get_health(token)
            except HTTPError as error:
                if error.code != 403:
                    raise
                token = get_ticket()
                health = get_health(token)

            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            temporary = OUTPUT.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(health, indent=2))
            os.replace(temporary, OUTPUT)
            track_incident(health)

            print("Updated:", health["collectedAt"], flush=True)

        except (OSError, ValueError, KeyError, IndexError) as error:
            print("Collection failed:", error, flush=True)

        time.sleep(60)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
