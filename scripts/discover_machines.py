__author__ = 'Ralph'
'''
scan ip range and get available machines.
list shared folders.
'''

import os
import sys
import nmap
import socket
import ping
import win32net
import win32com.client
from smb.SMBConnection import SMBConnection

from config import config


class DummyStream:
    """ DummyStream behaves like a stream but does nothing. """

    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self, data):
        pass

    def flush(self):
        pass

    def close(self):
        pass


def get_share_list(user, password, localhost_name, remote_target_name):
    conn = SMBConnection(user, password, localhost_name,
                         remote_target_name, use_ntlm_v2=True)
    ip = socket.gethostbyname(remote_target_name)
    conn.connect(ip)
    rs = conn.listShares()
    return [r'\\' + remote_target_name + '\\' + r.name.lower()
            for r in rs if r.name.lower()[-1] != '$']


def get_machines_in_domain(domain):
    adsi = win32com.client.Dispatch("ADsNameSpaces")
    nt = adsi.GetObject("", "WinNT:")
    result = nt.OpenDSObject("WinNT://%s" % domain, "", "", 0)
    result.Filter = ["computer"]
    for computer in result:
        yield computer.Name


def get_belonging_domain():
    domain_controller = win32net.NetGetDCName(None, None)
    return win32net.NetUserModalsGet(domain_controller, 2)['domain_name']


def check_machine_availability(machine_name):
    try:
        # Copy old print deals
        old_printerators = [sys.stdout, sys.stderr, sys.stdin,
                            sys.__stdout__, sys.__stderr__, sys.__stdin__][:]
        # redirect all print deals
        sys.stdout = DummyStream()
        sys.stderr = DummyStream()
        sys.stdin = DummyStream()
        sys.__stdout__ = DummyStream()
        sys.__stderr__ = DummyStream()
        sys.__stdin__ = DummyStream()

        res = ping.quiet_ping(machine_name, 5, 5)

        # Turn printing back on!
        sys.stdout, sys.stderr, sys.stdin, sys.__stdout__, \
        sys.__stderr__, sys.__stdin__ = old_printerators

        if res[1]:
            return True
        else:
            return False
    except socket.error, e:
        pass


if __name__ == '__main__':
    print get_share_list(config['user'], config['password'],
                         config['localhost'], 'chn-yawen')

    for machine in get_machines_in_domain('corp'):
        if machine[:4] == 'CHN-' and check_machine_availability(machine):
            print machine
