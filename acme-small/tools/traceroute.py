import re
from globals import *
from endpoint import Endpoint


class Traceroute(object):
    def __init__(self, output):
        self.trace = output
        self.parsed_result = dict()
        self.result_list = []
        self.trace_re = re.compile(r'(\d+)?\s+({ip}|\*)+'.format(ip=IP_REGEX))

    def parse(self):
        self.trace = [line for line in self.trace.split('\n') if line]
        seq, ip = None, None
        for line in self.trace:
            try:
                trace_match = self.trace_re.search(line)
                if trace_match:
                    ip = trace_match.group(3)
                    if trace_match.group(1):
                        seq = trace_match.group(1)
                    if seq and ip:
                        self.parsed_result.setdefault(int(seq), []).append(Endpoint(ip))
            except AttributeError:
                print('Cannot parse traceroute output {}'.format(line))
                raise
        return self.parsed_result

    def resolve(self):
        for key in sorted(self.parsed_result.keys()):
            self.result_list.append([hop.dev for hop in self.parsed_result[key]])
        return self.result_list

    def as_string(self, from_node=[]):
        return '->'.join('|'.join([dev for dev in set(el)]) for el in [from_node] + self.result_list)

    def verify(self, flow):
        index = 0
        for step in self.result_list:
            if index < len(flow):
                index += self.bool_compare(step, flow[index])
        rc = 1 if len(flow[index:]) > 0 else 0
        return rc

    @staticmethod
    def bool_compare(hops, rule):
        op, device = rule
        # print("COMPARING TRACE {} with RULE {}".format(hops, rule))
        if op.upper() == 'NOT':
            return 1 if device not in hops else 0
        elif op.upper() == 'OR':
            return 1 if all([hop in device for hop in hops]) else 0
        else:
            return 1 if all([hop in device for hop in set(hops)]) else 0
        return 0


def main():
    line1 = '''
    Type escape sequence to abort.
Tracing the route to 10.0.0.3
VRF info: (vrf in name/id, vrf out name/id)
  1 * *
    12.12.12.2 1 msec
  2 23.23.23.3 0 msec
    34.34.34.3 1 msec *
    '''
    line2 = '''
    Type escape sequence to abort.
Tracing the route to 10.0.0.3
VRF info: (vrf in name/id, vrf out name/id)
  1 14.14.14.4 0 msec
    12.12.12.2 1 msec
    14.14.14.4 0 msec
  2 23.23.23.3 0 msec
    34.34.34.3 1 msec *
    '''
    line3 = '''
    Type escape sequence to abort.
Tracing the route to 10.0.0.3
VRF info: (vrf in name/id, vrf out name/id)
  1 * * *
  2 23.23.23.3 0 msec
    34.34.34.3 1 msec *
    '''
    print Traceroute(line1).parse()
    print Traceroute(line2).parse()
    print Traceroute(line3).parse()


if __name__ == '__main__':
    main()