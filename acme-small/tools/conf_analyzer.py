import re
import file_io
from globals import *


class ConfAnalyzer(object):

    @staticmethod
    def convert_intf(text, intf_conv):
        new_text = []
        for line in text.splitlines():
            for old_intf, new_intf in intf_conv.iteritems():
                if re.match(r'^.*{}({})?$'.format(old_intf, INTF_DOT1Q_REGEX), line):
                    line = line.replace(old_intf, new_intf)
            if line.startswith('interface '):
                    line += '\r no shut'
            new_text.append(line)
        return '\r'.join(new_text)

    @staticmethod
    def cleanup(text):
        new_text = []
        ignore_lines = False
        for line in text.splitlines():
            if any([line.startswith(ignore) for ignore in IGNORE_CONFIG]):
                ignore_lines = True
            elif '!' in line:
                new_text.append(line)
                ignore_lines = False
            elif not ignore_lines:
                new_text.append(line)
        return '\r'.join(new_text)

    def normalize(self, intf_conv):
        for f in os.listdir(CONF_DIR):
            if f.endswith('.txt'):
                file_name = os.path.splitext(f)[0]
                file_text = file_io.read_txt(CONF_DIR + '/' + f)
                converted_intf = self.convert_intf(file_text, intf_conv.get(file_name, {}))
                updated_text = self.cleanup(converted_intf)
                new_filename = os.path.join(TMP_DIR, file_name + '.txt')
                file_io.write_txt(new_filename, updated_text)
        return

    @staticmethod
    def get_ips(text):
        result = {}
        ip, intf_name = None, None
        for line in text.splitlines():
            if re.search(r'^interface (.*)$', line):
                intf_name = re.search(r'^interface (.*)$', line).group(1)
            elif intf_name and re.search(r'{}'.format(IP_REGEX), line):
                ip = re.search(r'{}'.format(IP_REGEX), line).group(1)
            elif intf_name and re.search(r'shut', line):
                ip = None
            elif intf_name and re.search(r'!', line):
                if ip:
                    result.setdefault(intf_name, []).append(ip)
                ip, intf_name = None, None
        return result

    def extract_ip(self):
        result = {}
        cwd = os.path.join(TMP_DIR, CONF_DIR)
        for f in os.listdir(cwd):
            if f.endswith('.txt'):
                dev_name = os.path.splitext(f)[0]
                file_text = file_io.read_txt(cwd + '/' + f)
                ips = self.get_ips(file_text)
                result[dev_name] = ips
        file_io.write_yaml(TMP_DIR + '/' + 'ip.yml', result)
        return result


def main():
    pass

if __name__ == '__main__':
    main()
