import re
from endpoint import Endpoint


class Ping(object):

    def print_results(self, result=''):
        intro = '\rFailed connectivity : '
        result = ', '.join(from_node + ' -> ' + ', '.join(to_nodes)
                           for from_node, to_nodes in self.failed.iteritems() if to_nodes)
        print intro + result,

    def __init__(self, scenarios, lab):
        self.failed = dict()
        self.scenarios = self._parse_scenarios(scenarios, lab)

    def run(self, lab):
        enable = 'enable\r\n'
        for from_point in self.scenarios:
            for to_point in self.scenarios[from_point]:
                command = enable + 'ping {} {}'.format(to_point.ip, 'source ' + from_point.intf)
                from_node = from_point.node(lab)
                result = from_node.configure(command)
                percentage = self._parse_result(result)
                if not int(percentage) > 0:
                    self.failed.setdefault(str(from_point), set([])).add(str(to_point))
                else:
                    self.failed.setdefault(str(from_point), set([])).discard(str(to_point))
                self.print_results()

    @staticmethod
    def _parse_result(output):
        for line in output.splitlines():
            match_percent = re.match(r'Success rate is (\d+) percent', line)
            if match_percent:
                return match_percent.group(1)
        return '100'

    @staticmethod
    def _parse_scenarios(scenarios, lab):
        result = {}
        for line in scenarios.splitlines():
            try:
                _, flow = line.split('From ')
                from_, to_ = flow.split(' to ')
                from_point = Endpoint(from_)
                to_point = Endpoint(to_)
                result.setdefault(from_point, []).append(to_point)
            except:
                print('*** Failed to parse scenario {}'.format(line))
                raise
        return result


def main():
    pass

if __name__ == '__main__':
    main()
