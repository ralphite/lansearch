__author__ = 'Ralph'

import re

from config import config
from utils.crawler import get_belonging_domain, get_machines_in_domain, \
    check_machine_availability, get_shared_folders_list
from utils.es_wrapper import scan_and_push_to_es


def get_folders():
    domain = config['domain']
    if domain == '':
        domain = get_belonging_domain()

    res = []
    for machine in get_machines_in_domain(domain):
        if re.search(config['machine_filter'], machine):
            # if check_machine_availability(machine):
            try:
                folders = get_shared_folders_list(
                    config['user'], config['password'],
                    config['localhost'], machine.encode('ascii', 'ignore')
                )
                print '+' * 5 + machine, folders
                res += folders
            except Exception, e:
                print '-' * 5 + machine, e
    return res


if __name__ == '__main__':
    #for folder in get_folders():
    #    print folder
    for folder in open('folders.csv', 'r'):
        if not folder[0] == '#':
            folder = folder.strip()
            print 'scanning ', folder
            try:
                folder = unicode(folder)
                #print folder, type(folder)
                scan_and_push_to_es(folder)
            except Exception, e:
                print '-' * 10 + 'Error ', folder, e