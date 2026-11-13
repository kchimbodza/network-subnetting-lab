# network-subnetting-lab

Planned and documented a multi-site lab network using CIDR subnetting.
Defines subnet masks, usable host ranges, broadcast addresses, and IP
allocation tables for each segment to support accurate network topology
setup in lab environments.

## Architecture

<p align="center"><img src="docs/architecture.svg" width="100%" alt="A core router connects three switches. Site A, primary lab: 192.168.10.0/24, 254 hosts, .1 to .254, broadcast .255. Site B, secondary lab: 192.168.20.0/26, 62 hosts, .1 to .62, broadcast .63. Site C, management: 10.0.1.0/28, 14 hosts, .1 to .14, broadcast .15."></p>

The plain-text version is in [`topology.md`](topology.md); every address is in [`ip-allocation-table.md`](ip-allocation-table.md).

**Why this architecture**

| Choice | Why |
|---|---|
| One core router, one switch per site | Each site is its own broadcast domain; traffic between sites goes through one place. |
| Subnet size matched to each site's role | Primary lab needs the most hosts (/24, 254), secondary fewer (/26, 62), management only a few (/28, 14). |
| Management on its own range (10.0.1.0/28) | Keeps management addresses separate from the two lab ranges, and small. |
| Private (RFC 1918) addresses only | It is a lab; nothing needs to be reachable from the internet. |

## Results

There is no live network in this repo; it is a plan. The plan is checked by a script instead:
[`scripts/check_subnets.py`](scripts/check_subnets.py) reads the allocation table, recalculates mask, usable range,
broadcast and host count for every row with Python's `ipaddress` module, and checks that no two subnets overlap.

```text
$ python3 scripts/check_subnets.py
OK   Site A: 192.168.10.0/24  mask 255.255.255.0, hosts 192.168.10.1 - 192.168.10.254, broadcast 192.168.10.255, 254 hosts
OK   Site B: 192.168.20.0/26  mask 255.255.255.192, hosts 192.168.20.1 - 192.168.20.62, broadcast 192.168.20.63, 62 hosts
OK   Site C: 10.0.1.0/28  mask 255.255.255.240, hosts 10.0.1.1 - 10.0.1.14, broadcast 10.0.1.15, 14 hosts

3 subnets checked, 0 problem(s)
```

All 3 rows match the calculation and none overlap (run 2026-11-13, Python 3.14, Linux). The script exits with an
error and names the wrong column if the table is edited by mistake.

## What worked and what didn't

| | |
|---|---|
| ✅ | Every mask, host range, broadcast and host count in the table is correct (checked above). |
| ✅ | The three subnets don't overlap, so they can all sit behind one router. |
| ⚠️ | Router interface addresses and default gateways for each site are not assigned yet. |
| ⚠️ | The plan has not been built and tested on real or virtual equipment in this repo. |

## Files
- `topology.md` — ASCII network diagram with site layout
- `ip-allocation-table.md` — Full IP allocation per subnet
- `docs/architecture.svg` — the diagram above
- `scripts/check_subnets.py` — checks the allocation table (Python 3, no extra packages)

## Skills Demonstrated
- CIDR notation and subnet planning
- IP address allocation and range calculation
- Network topology documentation for lab infrastructure
