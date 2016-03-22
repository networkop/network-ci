from restunl.device import IOL
from globals import *
from dns import DNS
import file_io
import re


DEFAULT_INTF = 'Loopback0'
DNS_RESOLVER = DNS(file_io.read_yaml('{}/ip.yml'.format(TMP_DIR)))


class IncorrectEndpointFormat(Exception):
    pass


class Endpoint(object):

    def __init__(self, text):
        self.dev, self.intf, self.ip = '', '', ''
        self.node = None
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
            return seq[0], Endpoint.expand(seq[1])
        else:
            return seq[0], DEFAULT_INTF

    @staticmethod
    def expand(intf):
        intf_re = re.match('([a-zA-Z]+)(\d+(/\d+)*)', intf)
        try:
            intf_name = intf_re.group(1)
            intf_number = intf_re.group(2)
        except IndexError:
            raise IncorrectEndpointFormat('Could not split interface into name and number: {}'.format(intf))
        if intf_name.startswith('G'):
            intf_name = 'GigabitEthernet'
        elif intf_name.startswith('T'):
            intf_name = 'TenGigabitEthernet'
        elif intf_name.startswith('E'):
            intf_name = 'Ethernet'
        elif intf_name.startswith('L'):
            intf_name = 'Loopback'
        elif intf_name.startswith('V'):
            intf_name = 'Vlan'
        else:
            raise IncorrectEndpointFormat('Could not expand interface name: {}'.format(intf))
        return intf_name + intf_number

    def __str__(self):
        return self.dev + '(' + self.intf + ')'

    def get_node(self):
        return self.node


class ActiveEndpoint(Endpoint):

    def __init__(self, text, lab):
        super(ActiveEndpoint, self).__init__(text)
        if not self.dev == 'None':
            self.node = self._set_node(lab)
        else:
            self.node = None

    def _set_node(self, lab):
        return lab.get_node(IOL(self.dev))

