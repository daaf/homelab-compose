import os


def bytes_to_ascii(b):
    return b.decode('ascii').strip()


def bytes_to_ascii_list(*args):
    return [bytes_to_ascii(b) for b in args]


def create_dir_if_not_extant(path):
    if not os.path.exists(path):
        os.mkdir(path)