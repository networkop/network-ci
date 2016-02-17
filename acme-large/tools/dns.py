import re
# from globals import *
IP_REGEX = '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'

class DNS(object):

    @staticmethod
    def reverse_dict(original):
        result = {}
        for device, intf_ips in original.iteritems():
            for intf, ips in intf_ips.iteritems():
                for ip in ips:
                    result[ip] = (device, intf)
        return result

    def __init__(self, host_to_ips):
        self.ip_re = re.compile(IP_REGEX)
        self.host_to_ips = host_to_ips
        self.ips_to_host = self.reverse_dict(self.host_to_ips)

    def is_ip(self, text):
        return self.ip_re.search(text)

    def get(self, text, intf='Loopback0'):
        if self.is_ip(text):
            return self.ips_to_host.get(text, (text, ''))
        else:
            return self.host_to_ips.get(text, {}).get(intf, ['127.0.0.1'])[0]
