# ACME-LARGE

A large 14-node topology

![Alt text](./network/acme-large.jpg?raw=true "14-node topology")

Input information:

* topology in `topology.py`
* unetlab in `unetlab.yml`
* per-device ip address information in `ip.yml`
* test scenarios in `traffic_flows.txt`

To Run:

1. Create topology

```
./0_build_topo.py
```

2. Verify test scenarios

```
./2_test.py
```

3. Cleanup the lab

```
./3_destroy_topo.py
```

TODO Tasks:

1. Extract IP address information directly from configuration files
2. Extract topology from device interface description from configuration files.


