import os

NET = 'network'
TEST = 'testing'
CONF = 'config'
TMP = 'tmp'
NET_DIR = os.path.abspath(NET)
CONF_DIR = os.path.abspath(CONF)
TMP_DIR = os.path.abspath(TMP)
TEST_DIR = os.path.abspath(os.path.join(NET, TEST))
IP_REGEX = '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
INTF_DOT1Q_REGEX = '\.[0-9]{1,3}'


def main():
    print NET_DIR
    print CONF_DIR
    print TMP_DIR
    print TEST_DIR

if __name__ == '__main__':
    main()