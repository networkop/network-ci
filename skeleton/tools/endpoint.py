from restunl.device import Router
import file_io as file_io
from dns import DNS
import re
from globals import *


DEFAULT_INTF = 'Loopback0'
DNS_RESOLVER = DNS(file_io.read_yaml('{}/ip.yml'.format(TMP_DIR)))


class Endpoint(object):

    def __init__(self, text):
        self.dev, self.intf, self.ip = '', '', ''
        if DNS_RESOLVER.is_ip(text):
            self.dev, self.intf = DNS_RESOLVER.get(text)
            self.ip = text
        else:
            self.dev, self.intf = self._parse(text)
            self.ip = DNS_RESOLVER.get(self.dev, self.intf)

    @staticmethod
    def _parse(text):
        separators = ',|\s'
        seq = [word.strip() for word in re.split(separators, text)]
        if len(seq) > 1:
            return seq[0], seq[1]
        else:
            return seq[0], DEFAULT_INTF

    def __str__(self):
        return self.dev + '(' + self.intf + ')'

    def node(self, lab):
        return lab.get_node(Router(self.dev))
