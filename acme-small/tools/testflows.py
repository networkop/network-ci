from endpoint import Endpoint

class TestFlows(object):

    def __init__(self, flows):
        self.flows = flows
        self.parsed_flows = dict()

    @staticmethod
    def split_strip(text, separator):
        return [word.strip() for word in text.split(separator)]

    def parse(self):
        flows = [line for line in self.flows.split('\n') if line and not line.startswith('#')]
        for line in flows:
            if 'Failed' in line and line[0].isdigit():
                scenario = dict()
                seq, actions = self.split_strip(line, 'Failed')
                parsed_action = [Endpoint(word) for word in self.split_strip(actions, ',')]
                flow_key = (seq, tuple(parsed_action))
                self.parsed_flows[flow_key] = scenario
            elif all([token in line for token in ['From', 'to', 'via']]):
                _, rule = self.split_strip(line, 'From')
                from_device, to_via = self.split_strip(rule, 'to')
                from_point = Endpoint(from_device)
                to_device, flow = self.split_strip(to_via, 'via')
                to_point = Endpoint(to_device)
                flow_and = self.split_strip(flow, ',')
                flow_and_or = [['OR', self.split_strip(word, 'or')] if 'or' in word else word for word in flow_and]
                flow_and_or_not = [word.split() if 'not' in word else word for word in flow_and_or]
                flow_final = [['AND', word] if type(word) is str else word for word in flow_and_or_not]
                scenario_key = (from_point, to_point)
                scenario[scenario_key] = {'text': flow, 'parsed': flow_final}
            else:
                raise Exception('Incorrect traffic flow syntax in {}'.format(line))
        return self.parsed_flows

    def print_flow(self, number, from_device, to_device):
        print('From: {}, to: {}, via: {}'.format(from_device, to_device,
                                                 self.parsed_flows[number][from_device][to_device]))


def main():
    pass

if __name__ == '__main__':
    main()

