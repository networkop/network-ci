# ACME-LARGE

A large 14-node topology. 

![Alt text](./network/acme-large.jpg?raw=true "4-node topology")

## Prerequisites

* UNetLab server reachable from local machine
* L2 and L3 IOU images under `/opt/unetlab/addons/iol/bin` renamed to 'L2-LATEST.bin' and 'L3-LATEST.bin'

## Install dependencies

```bash
pip install -r requirements.txt
```

## Environment setup

* Change `./network/tests/traffic_flows.txt` file to match the expected traffic paths
* Change `./network/tests/ping_flows.txt` file to match the destinations that need to be monitored
* Change `./network/unetlab.yml` to match your UNetLab server environment

## Workflow

1. Build and configure topology
    ```bash
    ./0_build_topo.py
    ```  
  
  After this step you should be able to find the lab up and running on UNetLab server.

2. Verify real-time connectivity while making configuration changes. Example of changes required 
   to convert from OSPF to BGP can be found in `./network/ospf-bgp.txt` file
 
    ```bash
    ./1_monitor.py
    ```  

  Only failed pings will be displayed.

3. Verify test scenarios

    ```bash
    ./2_test.py
    ```  

  If any of the scenarios have failed, examine the output, adjust configuration as needed and re-run the tests.

4. Shutdown and delete the lab

    ```bash
    ./3_destroy_topo.py
    ```  

## Caveats

* Designed only for IPv4 on Cisco IOS devices
* Assuming only 15 seconds for protocol reconvergence when creating failure conditions
