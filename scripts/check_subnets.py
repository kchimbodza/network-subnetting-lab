#!/usr/bin/env python3
"""Recompute every column of ip-allocation-table.md and check the subnets don't overlap.

Usage: python3 scripts/check_subnets.py   (Python 3 standard library only)
"""
import ipaddress
import itertools
import pathlib
import sys

TABLE = pathlib.Path(__file__).resolve().parent.parent / "ip-allocation-table.md"

rows = []
for line in TABLE.read_text().splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 7 and cells[0].startswith("Site ") and cells[2].startswith("/"):
        rows.append(cells)

failures = 0
nets = []
for site, subnet, cidr, mask, usable, broadcast, max_hosts in rows:
    net = ipaddress.ip_network(subnet + cidr)
    hosts = list(net.hosts())
    expected = {
        "mask": str(net.netmask),
        "usable": f"{hosts[0]} - {hosts[-1]}",
        "broadcast": str(net.broadcast_address),
        "max hosts": str(len(hosts)),
    }
    given = {"mask": mask, "usable": usable, "broadcast": broadcast, "max hosts": max_hosts}
    bad = [k for k in expected if expected[k] != given[k]]
    failures += bool(bad)
    status = "OK  " if not bad else "FAIL"
    print(f"{status} {site}: {net}  mask {mask}, hosts {usable}, broadcast {broadcast}, {max_hosts} hosts")
    for k in bad:
        print(f"     {k}: table says {given[k]!r}, calculated {expected[k]!r}")
    nets.append((site, net))

for (a, na), (b, nb) in itertools.combinations(nets, 2):
    if na.overlaps(nb):
        failures += 1
        print(f"FAIL {a} ({na}) overlaps {b} ({nb})")

print(f"\n{len(rows)} subnets checked, {failures} problem(s)")
sys.exit(1 if failures or not rows else 0)
