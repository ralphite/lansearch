__author__ = 'yawen'

import sys

import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def to_human_readable(size):
    size = int(size)
    if size < 1024:
        return ('%d' % size) + ' Bytes'
    size /= 1024.0
    if size < 1024:
        return ('%.2f' % size) + ' KB'
    size /= 1024.0
    if size < 1024:
        return ('%.2f' % size) + ' MB'
    size /= 1024.0
    return ('%.2f' % size) + ' GB'


def gen_pagination_list(page_count, current_page):
    pages = []
    if page_count > 10:
        if current_page < 7:
            pages = [i + 1 for i in range(7)]
            pages += ['..', page_count - 1, page_count]
        elif current_page > page_count - 7:
            pages = [1, 2, '..']
            pages += [page_count - 6 + i for i in range(7)]
        else:
            pages += [1, 2, 3, '..']
            pages += [current_page - 1, current_page, current_page + 1, '..']
            pages += [page_count - 1, page_count]
    else:
        pages = [i + 1 for i in range(page_count)]
    return pages


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


class Result:
    def __init__(self, link, machine, path, name, size, mtime):
        self.link = link
        self.name = name
        self.machine = machine
        self.path = path
        self.size = size
        self.mtime = mtime