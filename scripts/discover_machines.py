__author__ = 'Ralph'
'''
scan ip range and get available machines.
list shared folders.
'''

import nmap
import socket
from smb.SMBConnection import SMBConnection

from config import config


def get_share_list(user, password, localhost_name, remote_target_name):
    conn = SMBConnection(user, password, localhost_name, remote_target_name, use_ntlm_v2=True)
    ip = socket.gethostbyname(remote_target_name)
    print ip, type(ip)
    conn.connect(ip)
    rs = conn.listShares()
    return [r'\\' + remote_target_name + '\\' + r.name.lower() for r in rs if r.name.lower()[-1] != '$']


if __name__ == '__main__':
    print get_share_list(config['user'], config['password'],
                         config['localhost'], 'chn-yawen')