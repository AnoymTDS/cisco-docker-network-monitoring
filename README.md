# Small Business Network Monitoring Lab

A practical IT Support and infrastructure lab combining a **simulated Cisco small-business network** with a **Docker-hosted monitoring dashboard**. Cisco Packet Tracer supplies network-health information through its Network Controller REST API; a Python collector on macOS processes that information; and an Nginx container serves a browser dashboard.

This project demonstrates network administration, troubleshooting, service monitoring, Python automation and incident documentation.

## Technologies

Cisco Packet Tracer · Cisco Network Controller REST API · Python 3 · Docker Desktop · Nginx · HTML/CSS/JavaScript · Git

## Network design

| Department | VLAN | Subnet | Gateway |
| --- | --- | --- | --- |
| IT | 10 | `192.168.10.0/24` | `192.168.10.1` |
| Finance | 20 | `192.168.20.0/24` | `192.168.20.1` |
| HR | 30 | `192.168.30.0/24` | `192.168.30.1` |

**Simulated equipment:** Cisco 2911 router, Cisco 2960 switch, six employee PCs and a Cisco Network Controller.

Configured features include:
- VLAN segmentation and 802.1Q trunking
- Router-on-a-Stick inter-VLAN routing and DHCP
- An extended ACL restricting HR-to-Finance traffic
- SSH administration and switch management addressing
- Switch syslog buffering and timestamped events

## Monitoring architecture

```text
Cisco Packet Tracer (simulated network)
           |
           v
Packet Tracer Network Controller
           | local REST API on macOS, port 58000
           v
Python collector.py (runs on the Mac)
           | writes JSON snapshots and incident records
           v
site/data/health.json + site/data/incidents.json
           | read-only Docker bind mount
           v
Nginx container (serves HTML, JS and JSON)
           |
           v
Browser dashboard at http://localhost:8088
```

**Docker hosts the dashboard, not the Python collector or the Cisco simulation.** The collector accesses the localhost-only Packet Tracer API from macOS; no controller credentials are embedded in the web assets.

## Features

- Controller health data collected every **60 seconds**
- Dashboard polling every **15 seconds**
- Aggregate host reachability and switch-health metrics
- Host degradation alerts and recovery messages
- Persistent incident records in `incidents.json`
- Stale-data warning when monitoring snapshots stop updating
- Read-only web-server access to generated data

The dashboard reports the controller's metrics rather than independently checking every individual device.

## Demonstrated incident-response test

A controlled test powered off the **HR PC5** in Packet Tracer. Its ping test failed, and reported host reachability fell from **100% to 83%**, producing an incident alert. After powering PC5 back on and verifying ping connectivity, reachability returned to **100%** and the incident was recorded as resolved.

| Field | Recorded result |
| --- | --- |
| Incident ID | `INC-20261116012728` |
| Detected | 16 November 2026, 01:27 UTC |
| Resolved | 16 November 2026, 01:30 UTC |
| Approximate duration | 3 minutes |
| Health during incident | 83% |
| Health after recovery | 100% |

A separate monitoring-reliability test stopped the Python collector. The dashboard showed a **stale-data warning** and cleared it once fresh collection resumed. The saved incident history remained intact.

## Project files

```text
.
├── README.md
├── .gitignore
├── collector.py
├── incident_history.py
├── examples/
│   ├── health.example.json
│   └── incidents.example.json
└── site/
    └── index.html
```

Generated `site/data/health.json` and `site/data/incidents.json` files are intentionally excluded from Git.

## Run locally

**Prerequisites:** Docker Desktop, Python 3, Cisco Packet Tracer, and a configured Packet Tracer Network Controller with **Real World / External REST API access** enabled on local port **58000**.

1. From the cloned repository, create an offline preview using the **fictional** example data:

   ```bash
   mkdir -p site/data
   cp examples/health.example.json site/data/health.json
   cp examples/incidents.example.json site/data/incidents.json
   ```

2. Start Nginx inside Docker:

   ```bash
   docker run -d \
     --name cisco-monitor \
     -p 127.0.0.1:8088:80 \
     --mount "type=bind,source=$PWD/site,target=/usr/share/nginx/html,readonly" \
     nginx:alpine
   ```

3. Visit **http://localhost:8088**. The example snapshot has a fixed timestamp, so a **stale-data warning is expected** in offline-preview mode.

4. To collect real data, open your configured Packet Tracer lab, enable its controller API and run on your Mac:

   ```bash
   python3 collector.py
   ```

   Enter your **Network Controller login password** when prompted. The collector authenticates and refreshes the health snapshot every 60 seconds. Keep the Terminal session running. Press `Ctrl+C` to stop it.

**Note:** These steps reproduce the dashboard and collector when a compatible Packet Tracer simulation is already configured. The project's `.pkt` network file is not included in this repository.

## Known limitations

- The router was reachable using SSH and functioned in the lab, but **was not inventoried** by the Network Controller; the dashboard therefore reports zero inventoried routers.
- Switch-health reporting sometimes fluctuated; an interface-down event does not prove an entire switch has failed.
- Persistent incidents are generated from **aggregate host reachability**, not from per-device identification.
- Collector outages display a stale-data warning but are **not saved as incidents**.
- This is a local learning environment, **not a production-ready monitoring platform**.

## Security notes

The repository contains no authentication tickets or embedded account passwords. The collector asks for a password interactively; the Nginx port is bound to `127.0.0.1`; and runtime data is excluded through `.gitignore`. Review Cisco Packet Tracer `.pkt` files for saved device credentials before sharing them.

## Skills demonstrated

VLANs · Routing · DHCP · ACLs · SSH · Syslog · Network troubleshooting · Python scripting · REST APIs · Docker bind mounts · Monitoring and incident response · Git documentation
