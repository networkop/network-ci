#!/usr/bin/python
import sys
import tools.file_io as file_io
from tools.unetlab import UNetLab
from tools.globals import *

UNL = UNetLab(**file_io.read_yaml('{}/unetlab.yml'.format(NET_DIR)))


def main():
    try:
        UNL.destroy()
        print("*** LAB DESTROYED")
        for f in os.listdir(TMP_DIR):
            if not f.startswith('.'):
                file_path = os.path.join(TMP_DIR, f)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        print("*** TMP DIRECTORY CLEANED UP")
    except:
        print ('*** Emulation Failed')
        raise
    return 0

if __name__ == '__main__':
    sys.exit(main())

