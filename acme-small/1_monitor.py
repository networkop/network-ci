from tools.ping import Ping
import tools.file_io as file_io
from tools.unetlab import UNetLab
from tools.globals import *
import sys
import threading

UNL = UNetLab(**file_io.read_yaml('{}/unetlab.yml'.format(NET_DIR)))
PING_FLOWS = file_io.read_txt('{}/ping_flows.txt'.format(TEST_DIR))
RUN = True


def key_press():
    global RUN
    RUN = raw_input()


def main():
    lab = UNL.get_lab()
    ping = Ping(PING_FLOWS, lab)
    thread = threading.Thread(target=key_press)
    thread.start()
    print('Starting pings. Press "Enter" to stop')
    while RUN:
        ping.run(lab)
    print('\rStopped'),

if __name__ == '__main__':
    sys.exit(main())
