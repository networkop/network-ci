import os

L3_IMAGE = 'L3-LATEST.bin'
L2_IMAGE = 'L2-LATEST.bin'
NET = 'network'
TEST = 'tests'
CONF = 'config'
TMP = 'tmp'
NET_DIR = os.path.abspath(NET)
CONF_DIR = os.path.abspath(CONF)
TMP_DIR = os.path.abspath(TMP)
TEST_DIR = os.path.abspath(os.path.join(NET, TEST))
IP_REGEX = '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
INTF_DOT1Q_REGEX = '\.[0-9]{1,3}'
IGNORE_CONFIG = ['class-map', 'policy-map', 'service', 'aaa', 'flow', 'ip nbar', 'logging',
                 'snmp', 'banner', 'ntp', 'event', 'ip wccp', 'boot', 'archive', 'privilege', 'tacacs',
                 'ip domain', 'ip ftp', 'ip http', 'ip sla', 'track', 'version', '! ']


def main():
    print NET_DIR
    print CONF_DIR
    print TMP_DIR
    print TEST_DIR

if __name__ == '__main__':
    main()
