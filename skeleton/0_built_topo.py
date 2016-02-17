#!/usr/bin/python
import sys
from tools.globals import *
import tools.file_io as file_io
from tools.unetlab import UNetLab
from tools.conf_analyzer import ConfAnalyzer
from network import topology

UNL = UNetLab(**file_io.read_yaml('{}/unetlab.yml'.format(NET_DIR)))
INTF_CONV = file_io.read_yaml('{}/intf_conv.yml'.format(NET_DIR))


def main():
    try:
        conf_files = ConfAnalyzer()
        conf_files.normalize(INTF_CONV)
        print("*** CONFIG FILES NORMALIZED")
        conf_files.extract_ip()
        print("*** IPs EXTRACTED")
        UNL.create_lab()
        print("*** CONNECTED TO UNL")
        UNL.build_topo(topology)
        print("*** TOPOLOGY IS BUILT")
        UNL.start()
        print("*** NODES STARTED")
        UNL.configure_nodes(TMP_DIR)
        print("*** ALL NODES CONFIGURED")
    except Exception:
        UNL.destroy()
        raise
    return 0

if __name__ == '__main__':
    sys.exit(main())

