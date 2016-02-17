import yaml


def read_txt(filename):
    try:
        with open(filename) as stream:
            return ''.join(stream.readlines())
    except IOError:
        return ''


def read_yaml(filename):
    try:
        with open(filename, 'r') as stream:
            yml = yaml.load(stream)
        return yml
    except IOError:
        return {}


def write_txt(filename, text):
    with open(filename, 'w+') as f:
        f.write(text)
    return None


def write_yaml(filename, data):
    write_txt(filename, yaml.dump(data, default_flow_style=False))
    return None

