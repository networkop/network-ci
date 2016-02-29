# ACME-SMALL

A simple 4-node topology. 

![Alt text](./network/acme-small.jpg?raw=true "4-node topology")

## Prerequisites

* UNetLab server reachable from local machine
* L2 and L3 IOU images with renamed to 'L2-LATEST.bin' and 'L3-LATEST.bin'

## Install dependencies

```bash
pip install -r requirements.txt
```

## Environment setup

* Change `./network/tests/traffic_flows.txt` file to match the expected traffic paths
* Change `./network/unetlab.yml` to match your UNetLab server environment

## Workflow

1. Build and configure topology
    ```bash
    ./0_build_topo.py
    ```  
  
  After this step you should be able to find the lab up and running on UNetLab server.

2. Verify real-time connectivity while making configuration changes  
 
    ```bash
    ./1_monitor.py
    ```  

  You can change `./network/tests/ping_flows.txt` to change how the pings are run.

3. Verify test scenarios

    ```bash
    ./3_test.py
    ```  

  If any of the scenarios have failed, examine the output, adjust configuration as needed and re-run the tests.

4. Shutdown and delete the lab

    ```bash
    ./3_destroy_topo.py
    ```  

## Caveats

* Designed only for IPv4 on Cisco IOS devices
*  You can override default image and directory names in  `./tools/globals.py` 
