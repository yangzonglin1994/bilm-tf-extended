import os
import sys


def get_fnames_under_path(path):
    """
    get filename seq under path.
    :param path: string
    :return: filename seq
    """
    if not os.path.isdir(path):
        raise ValueError('In ' + sys._getframe().f_code.co_name +
                         '() function, path value error.')
    fnames = set()
    for fname in os.listdir(path):
        fname = os.path.join(path, fname)
        if os.path.isdir(fname):
            continue
        fnames.add(fname)
    return fnames


def my_getattr(obj, attr, default):
    """
    if not obj.attr:
        return default
    else:
        return obj.attr
    """
    return default if not obj.__getattribute__(attr) else obj.__getattribute__(attr)
