__author__ = 'Ralph'
'''
scan ip range and get available machines.
list shared folders.
'''

import os
import sys
import nmap
import socket
import win32net
import win32com.client
from smb.SMBConnection import SMBConnection

from config import config


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
    for machine in result:
        yield machine.Name


if __name__ == '__main__':
    print get_share_list(config['user'], config['password'],
                         config['localhost'], 'chn-yawen')

    domain_controller = win32net.NetGetDCName(None, None)
    domain_name = win32net.NetUserModalsGet(domain_controller, 2)['domain_name']
    print "Listing machines in", domain_name
    for machine in get_machines_in_domain(domain_name):
        print machine