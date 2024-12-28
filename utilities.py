import os

def parse_size(size):
    size = size.upper()
    if size.endswith("KB"):
        return int(size[:-2]) * 1024
    elif size.endswith("MB"):
        return int(size[:-2]) * 1024 * 1024
    elif size.endswith("GB"):
        return int(size[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size)
