#!/usr/bin/python
import sys
from tools.globals import *
import tools.file_io as file_io
from tools.unetlab import UNetLab
from tools.conf_analyzer import ConfAnalyzer
from network import topology

UNL = UNetLab(**file_io.read_yaml('{}/unetlab.yml'.format(NET_DIR)))


def main():
    try:
        print("*** CONNECTING TO UNL")
        UNL.create_lab()
        print("*** BUILDING TOPOLOGY")
        UNL.build_topo(topology)
        UNL.ext_connect(topology)
        print("*** NORMALIZING CONFIGURATION FILES")
        conf_files = ConfAnalyzer()
        conf_files.normalize(file_io.read_yaml(INTF_CONV_FILE))
        print("*** EXTRACTING IP")
        conf_files.extract_ip()
        print("*** STARTING ALL NODES")
        UNL.start()
        print("*** CONFIGURING NODES")
        UNL.configure_nodes(TMP_DIR)
        print("*** ALL NODES CONFIGURED")
    except Exception:
        UNL.destroy()
        raise
    return 0

if __name__ == '__main__':
    sys.exit(main())

