# Incident Report — Simulated HR Workstation Outage

**Environment:** Cisco Packet Tracer small-business network, macOS Python collector, and Docker-hosted Nginx monitoring dashboard  
**Test date:** 16 November 2026 (UTC)  
**Incident ID:** `INC-20261116012728`  
**Classification:** Simulated host-reachability degradation  
**Status:** Resolved

## Objective

Validate whether the monitoring workflow detects a workstation outage, warns the operator, and records a recovery. This was a controlled lab exercise, not a real business outage.

## Environment

The simulated network includes six workstations across three VLANs: IT (10), Finance (20) and HR (30). The Packet Tracer Network Controller exposes an authenticated localhost REST API. A Python script on macOS polls network-health data at approximately 60-second intervals and writes JSON snapshots. An Nginx container serves those snapshots through a dashboard that polls at approximately 15-second intervals.

The incident-history script opens or resolves records based on the **aggregate host-reachability percentage** reported by the controller. It does not independently identify the failed device.

## Test procedure and observations

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | Confirm normal network operation | Six hosts reported as reachable |
| 2 | Power off HR workstation PC5 | Connectivity to `192.168.30.11` failed in a four-packet ping test (100% packet loss) |
| 3 | Wait for the next controller health collection | Aggregate host health fell from 100% to **83%** |
| 4 | Review monitoring dashboard | Incident warning appeared for reduced host reachability |
| 5 | Review saved incident history | An `Open` incident recorded the degraded-health percentage |
| 6 | Power on PC5 and repeat connectivity test | Ping succeeded and host health returned to **100%** |
| 7 | Allow health collection to run | The incident record was marked `Resolved` |

## Recorded timeline

| Field | Value |
| --- | --- |
| Incident ID | `INC-20261116012728` |
| Detected | 2026-11-16 01:27:28 UTC |
| Resolved | 2026-11-16 01:30:28 UTC |
| Approximate incident duration | 3 minutes |
| Host health at detection | 83% |
| Host health after recovery | 100% |
| Outcome | Alert and incident status recovered |

Times are taken from the lab's incident history. The collection interval means the observed detection and resolution timestamps are not necessarily the exact moments at which the workstation was powered off and on.

## Additional reliability test

The Python collector was stopped with `Ctrl+C` while the Docker dashboard remained accessible. Once the last saved snapshot aged beyond the dashboard's configured threshold (150 seconds), a **stale monitoring-data warning** appeared. Restarting the collector resumed updates and cleared the stale-data warning.

This collector stoppage was **not recorded** as an incident in `incidents.json`; the current history logic tracks only aggregate host-reachability degradation.

## Evidence available

Relevant captured screenshots include the Packet Tracer topology, switch VLAN configuration, Controller health display, Python collection output, failed ping, 83% host-health warning, recovery notification and resolved incident table.

These images should be reviewed and uploaded separately before inclusion as live image links in this document or the README.

## Limitations and next improvements

- The Network Controller inventories one switch but **does not discover the operational router**. A zero-router dashboard value must not be interpreted as an offline router.
- Switch-health figures fluctuated during the lab. A controller report of `0:1 healthy` is not sufficient by itself to conclude switch hardware failure.
- Incident tracking currently relies on aggregate reachability rather than the identity of a particular workstation.
- Collector outages cause dashboard warnings, but they are not yet persisted as separate monitoring incidents.
- The lab demonstrates monitoring behaviour in a simulator and does not establish production reliability or security readiness.

## Skills demonstrated

Connectivity troubleshooting, controlled fault injection, monitoring validation, REST API integration, Python automation, Docker-hosted dashboards, incident logging, recovery checks and technical documentation.
