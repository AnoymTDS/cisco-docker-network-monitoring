# Small Business Network Monitoring Lab

## Project Overview

Designed and implemented a simulated small-business
network using Cisco Packet Tracer, integrated with a
Docker-hosted monitoring dashboard.

The project demonstrates network configuration,
secure remote administration, Python automation,
service monitoring and incident response.

## Technologies Used

- Cisco Packet Tracer
- Docker Desktop
- Nginx
- Python 3
- Cisco Network Controller REST API
- HTML, CSS and JavaScript
- Git and GitHub

## Network Architecture

The simulated business consists of three departments:

| Department | VLAN | Subnet |
|------------|------|--------|
| IT | 10 | 192.168.10.0/24 |
| Finance | 20 | 192.168.20.0/24 |
| HR | 30 | 192.168.30.0/24 |

Infrastructure:

- Cisco 2911 router
- Cisco 2960 switch
- Six simulated employee computers
- Cisco Network Controller

## Network Configuration

Implemented:

- Departmental VLAN segmentation
- 802.1Q trunking
- Router-on-a-Stick inter-VLAN routing
- DHCP pools for each department
- Extended ACL restricting HR-to-Finance traffic
- SSH remote administration
- Switch management IP configuration
- Cisco syslog buffering

## Monitoring Architecture

Cisco Packet Tracer Network Controller
        |
        | Authenticated REST API
        v
Python collector on macOS
        |
        | Health data + incident records
        v
JSON files
        |
        | Read-only Docker bind mount
        v
Nginx Docker container
        |
        v
Web Monitoring Dashboard

The Python collector requests controller data locally
and writes JSON snapshots. Docker serves these files
through the monitoring dashboard.

## Monitoring Features

- Automated data collection every 60 seconds
- Dashboard data refresh every 15 seconds
- Host reachability monitoring
- Switch-health reporting
- Network incident warnings
- Recovery notifications
- Persistent incident history
- Stale-data detection

## Incident Response Testing

Simulated an HR workstation outage by powering off
PC5 inside Cisco Packet Tracer.

Observed:

1. PC5 became unreachable.
2. Host reachability dropped from 100% to 83%.
3. The Docker dashboard displayed an incident warning.
4. The Python application created an incident record.
5. PC5 was powered back on.
6. Host reachability recovered to 100%.
7. The incident was marked as resolved.

Recorded incident: INC-20261116012728

Detected: 16 November 2026, 01:27 UTC
Resolved: 16 November 2026, 01:30 UTC
Recorded duration: approximately 3 minutes.

## Monitoring Reliability Test

Stopped the Python collector to simulate monitoring
service failure.

The dashboard detected that its monitoring snapshot
was stale and displayed a warning.

After restarting the collector, the dashboard received
fresh data and cleared the stale-data warning.

## Running the Project Locally

Requirements:

- Docker Desktop
- Python 3
- Cisco Packet Tracer
- A configured Packet Tracer Network Controller

The controller REST API must be enabled locally
on port 58000.

From the project directory, start the web server:

docker run -d \
  --name cisco-monitor \
  -p 127.0.0.1:8088:80 \
  --mount "type=bind,source=$PWD/site,target=/usr/share/nginx/html,readonly" \
  nginx:alpine

Start the monitoring collector:

python3 collector.py

Enter the Network Controller password when prompted.

Open the dashboard:

http://localhost:8088

The controller must be available for live data updates.

## Known Limitations

- The router is operational but has not been added
  to the Network Controller's managed inventory.
- Switch-health values can fluctuate in the
  controller's reporting.
- Incident history currently tracks aggregate host
  reachability rather than individual device identity.
- The Python collector runs locally on the Mac,
  while Nginx runs inside Docker.
- The dashboard is a local lab application,
  not a production monitoring platform.

## Security Considerations

- API authentication tickets are not published.
- The collector requests its password interactively.
- Generated monitoring data is excluded from Git.
- The Docker web server is bound to localhost.
- Packet Tracer configurations should be reviewed
  before any public release.

## Skills Demonstrated

Network troubleshooting, VLAN configuration,
IP addressing, DHCP, ACLs, SSH, Docker deployment,
REST API integration, Python scripting,
monitoring, incident response and documentation.
