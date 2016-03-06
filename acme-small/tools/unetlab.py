from restunl.unetlab import UnlServer
from restunl.device import Router, Switch
from globals import *
import file_io
import decorators
import os


class UNetLab(object):

    def __init__(self, ip='', user='', pwd='', lab_name=''):
        self.ip, self.user, self.pwd, self.lab_name = ip, user, pwd, lab_name
        if os.environ.get('UNL_IP'):
            self.ip = os.environ.get('UNL_IP')
        self.unl = UnlServer(self.ip)
        self.unl.login(self.user, self.pwd)
        self.lab = None
        self.nodes = dict()

    def create_lab(self):
        self.lab = self.unl.create_lab(self.lab_name)
        self.lab.cleanup()

    def get_lab(self):
        return self.unl.get_lab(self.lab_name)

    def build_topo(self, topology):
        real_topo = topology.real
        intf_conv = file_io.read_yaml(INTF_CONV_FILE)
        for ((a_name, a_intf), (b_name, b_intf)) in real_topo:
            a_device = Switch(a_name, L2_IMAGE) if 'sw' in a_name.lower() else Router(a_name, L3_IMAGE)
            b_device = Switch(b_name, L2_IMAGE) if 'sw' in b_name.lower() else Router(b_name, L3_IMAGE)
            if a_name not in self.nodes:
                self.nodes[a_name] = self.lab.create_node(a_device)
                # print("*** NODE {} CREATED".format(a_name))
            if b_name not in self.nodes:
                self.nodes[b_name] = self.lab.create_node(b_device)
                # print("*** NODE {} CREATED".format(b_name))
            node_a = self.nodes[a_name]
            node_b = self.nodes[b_name]
            a_intf_lab = node_a.get_next_intf()
            b_intf_lab = node_b.get_next_intf()
            intf_conv.setdefault(a_name, {})[a_intf] = a_intf_lab
            intf_conv.setdefault(b_name, {})[b_intf] = b_intf_lab
            node_a.connect_node(a_intf_lab, node_b, b_intf_lab)
            # print("*** NODES {} and {} ARE CONNECTED".format(a_name, b_name))
        file_io.write_yaml(INTF_CONV_FILE, intf_conv)
        return None

    def ext_connect(self, topo):
        ext_topo = topo.ext_net
        intf_conv = file_io.read_yaml(INTF_CONV_FILE)
        for (node_name, node_intf), pnet in ext_topo.iteritems():
            ext_net = self.lab.create_net('cloud', net_type=pnet)
            the_node = self.nodes[node_name]
            node_intf_lab = the_node.get_next_intf()
            the_node.connect_interface(node_intf_lab, ext_net)
            intf_conv.setdefault(node_name, {})[node_intf] = node_intf_lab
        file_io.write_yaml(INTF_CONV_FILE, intf_conv)
        return None

    @decorators.timer
    @decorators.progress
    def configure_nodes(self, path):
        import threading
        processes = []
        for node_name in self.nodes:
            conf = 'no\renable\r configure terminal\r no ip domain-lookup\r'
            conf += file_io.read_txt('{0}/{1}.txt'.format(path, node_name))
            conf += '\rend\r write\r'
            process = threading.Thread(target=self.nodes[node_name].configure, args=(conf,))
            # self.nodes[node_name].configure(conf)
            process.start()
            processes.append(process)
            # print("*** NODE {} CONFIGURED".format(node_name))
        [p.join() for p in processes]
        return None

    def start(self):
        return self.lab.start_all_nodes()

    @decorators.timer
    @decorators.progress
    def destroy(self):
        self.lab = self.get_lab()
        self.lab.cleanup()
        self.unl.delete_lab(self.lab_name)






