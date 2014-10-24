__author__ = 'Ralph'

'''
features:

- get current domain name
- get machine list in the domain
- check if machine is up
- get list of shared folders of a Windows server

> note: this script depends on win32net and win32com
> and need to run on Windows
'''

import socket
import ping
import win32net
import win32com.client
from warnings import warn
from smb.SMBConnection import SMBConnection

from scripts.config import config
from console import ConsoleUtil


def get_belonging_domain():
    """
    get domain of localhost
    """
    domain_controller = win32net.NetGetDCName(None, None)
    return win32net.NetUserModalsGet(domain_controller, 2)['domain_name']


def get_machines_in_domain(domain):
    """
    get list of machines registered in the domain.
    note: the machine might not be available anymore.
    :param domain: name of the domain
    :return: list of machines in the domain
    """
    adsi = win32com.client.Dispatch("ADsNameSpaces")
    nt = adsi.GetObject("", "WinNT:")
    result = nt.OpenDSObject("WinNT://%s" % domain, "", "", 0)
    result.Filter = ["computer"]
    for computer in result:
        yield computer.Name


def check_machine_availability(machine_name):
    """
    seems to be very unstable. need to rewrite!!!
    :param machine_name: machine name
    :return: boolean indicating whether machine is up or down
    """
    warn("this method doesn't guarantee to return True when"
         " machine is actually available and thus is deprecated.")
    try:
        console = ConsoleUtil()
        console.disable_console_output()

        res = ping.quiet_ping(machine_name, 5, 5)

        console.enable_console_output()

        if res[1]:
            return True
        else:
            return False
    except socket.error, e:
        pass


def get_shared_folders_list(user, password, localhost_name, remote_target_name):
    """
    get list of shared folders of type 0 (those people normally
    use to share files) on a Windows server.
    :param user: user name without domain and slash
    :param password: password
    :param localhost_name: name of the local machine
    :param remote_target_name: name of the remote target machine
    :return: list of folder names in this format "\\machine-name\folder-name"
    """
    conn = SMBConnection(user, password, localhost_name,
                         remote_target_name, use_ntlm_v2=True)
    ip = socket.gethostbyname(remote_target_name)
    conn.connect(ip)
    rs = conn.listShares()
    return [r'\\' + remote_target_name + '\\' + r.name.lower()
            for r in rs if r.name.lower()[-1] != '$']


if __name__ == '__main__':
    print '#' * 30
    print 'testing check_machine_availability'
    for m in ['chn-aaa', 'chn-xihou1', 'baidu.com']:
        print m, check_machine_availability(m)

    print
    print '#' * 30
    print 'testing get_shared_folders_list'
    print get_shared_folders_list(config['user'], config['password'],
                                  config['localhost'], 'chn-yawen')