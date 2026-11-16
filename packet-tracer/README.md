# Cisco Packet Tracer Network Lab

This directory is intended for the saved Cisco Packet Tracer **Small Business Network Lab** simulation (`.pkt`).

## What the simulation demonstrates

| Component | Configuration described in the lab |
| --- | --- |
| Router | Cisco 2911, router-on-a-stick for IT/Finance/HR VLANs |
| Switch | Cisco 2960, VLAN access ports and trunk to the router |
| IT | VLAN 10, `192.168.10.0/24` |
| Finance | VLAN 20, `192.168.20.0/24` |
| HR | VLAN 30, `192.168.30.0/24` |
| Hosts | Six simulated employee workstations |
| Controller | Packet Tracer Network Controller, intended for localhost REST API monitoring |

### Expected configuration checks

1. Open the simulation with Cisco Packet Tracer and wait for interfaces to settle.
2. On the switch, inspect `show vlan brief` and `show interfaces trunk`.
3. On the router, inspect `show ip interface brief` and `show ip route`.
4. Test DHCP assignment where applicable and check hosts have the intended subnet and default gateway.
5. Test **HR-to-Finance restriction** (blocked), **HR-to-IT** and **IT-to-Finance** connectivity (allowed by the configured ACL policy).
6. Check the controller health display; note that the operational router was **not added to controller inventory** during the original lab.
7. For the separate Docker dashboard, enable the Packet Tracer controller external/local REST API access and run the host-side Python collector described in the [project README](../README.md).

## Security before sharing a `.pkt`

Packet Tracer saves device and controller configurations in the project file. Before adding a public copy, **open it inside Packet Tracer** and ensure the simulation contains no real or reused passwords, personal information, authentication tokens or sensitive details.

Replace lab-only credentials on the copied simulation rather than reusing credentials from other services. Review local router/switch login secrets, console and VTY lines, SSH administrator accounts, and the Network Controller account. Retain the original private lab file separately.

The absence of readable password strings in a raw binary-file scan **does not** prove that no secrets are stored.

## Evidence

The [screenshots directory](../screenshots) and [incident report](../docs/INCIDENT-REPORT.md) demonstrate the configuration and an intentionally induced workstation outage.
