from random import randint
from bs4 import BeautifulSoup

import requests

from movistar_router_port_opener.port_opener.port_message import PortMessage


class PortHandler:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, admin_password, device_address="192.168.1.1"):
        self.admin_password = admin_password
        self.session_key = None
        self.access_url = 'http://' + device_address + '/te_acceso_router.cgi'
        self.ports_url = 'http://' + device_address + '/scvrtsrv.cmd'
        self.cookies = {}

    def get_session_key(self):
        data = {'loginPassword': self.admin_password}
        self.session_key = str(PortHandler.new_key())
        self.cookies = {'sessionID': self.session_key}
        requests.post(self.access_url, data, cookies=self.cookies, headers=self.headers)

    def check_port(self, port_message: PortMessage):
        if self.session_key is None:
            self.get_session_key()

        params = {
            'action': 'view'
        }
        s = requests.get(self.ports_url, params=params, cookies=self.cookies)
        soup = BeautifulSoup(s.content, features="html.parser")
        inputs = soup.find_all("input", {"name": "rml"})
        for inp in inputs:
            values = inp.get('value').split("|")
            if len(values) == 6:
                if port_message.destination == values[0] \
                        and port_message.e_start == int(values[1]) \
                        and port_message.e_end == int(values[2]) \
                        and port_message.protocol == PortMessage.resolve_protocol(values[3]) \
                        and port_message.i_start == int(values[4]) \
                        and port_message.i_end == int(values[5]):
                    return True
        return False

    def add_port(self, port_message: PortMessage):
        if self.session_key is None:
            self.get_session_key()

        params = {
            'action': 'add',
            'srvName': port_message.title,
            'dstWanIf': 'ppp0.1',
            'srvAddr': port_message.destination,
            'proto': port_message.protocol + ",",
            'eStart': str(port_message.e_start) + ",",
            'eEnd': str(port_message.e_end) + ",",
            'iStart': str(port_message.i_start) + ",",
            'iEnd': str(port_message.i_end) + ",",
            'sessionKey': self.session_key
        }
        requests.get(self.ports_url, params=params, cookies=self.cookies)

    def remove_port(self, port_message: PortMessage):
        params = {
            'action': 'remove',
            'rmLst': port_message.compose(),
            'sessionKey': self.session_key
        }
        requests.get(self.ports_url, params=params, cookies=self.cookies)

    @staticmethod
    def new_key():
        length = 10
        range_start = 10 ** (length - 1)
        range_end = (10 ** length) - 1
        return randint(range_start, range_end)

    @staticmethod
    def compose_rml_command(destination_ip, e_start, e_end, protocol):
        return destination_ip + "|" + str(e_start) + "|" + str(e_end) + "|" + \
               ("TCP or UDP" if protocol == "Both" else protocol) + "|" + str(i_start) + "|" + str(i_end)
