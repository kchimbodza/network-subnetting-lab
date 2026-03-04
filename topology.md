# Lab Network Topology

## Overview
Three-site lab network designed to simulate a subnetted lab environment.
```
[Site A] 192.168.10.0/24          [Site B] 192.168.20.0/26
    |                                    |
[Switch A]                          [Switch B]
    |                                    |
    +----------[Core Router]-------------+
                      |
                 [Switch C]
                      |
              [Site C] 10.0.1.0/28
```

## Sites
- **Site A** — Primary lab segment, up to 254 hosts
- **Site B** — Secondary lab segment, up to 62 hosts  
- **Site C** — Management segment, up to 14 hosts
