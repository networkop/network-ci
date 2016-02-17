from tools.ping import Ping
import tools.file_io as file_io
from tools.unetlab import UNetLab
from tools.globals import *
import sys


UNL = UNetLab(**file_io.read_yaml('{}/unetlab.yml'.format(NET_DIR)))
PING_FLOWS = file_io.read_txt('{}/ping_flows.txt'.format(TEST_DIR))


def main():
    lab = UNL.get_lab()
    ping = Ping(PING_FLOWS, lab)
    while True:
        ping.run(lab)

if __name__ == '__main__':
    sys.exit(main())
