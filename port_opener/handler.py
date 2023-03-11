from random import randint
from bs4 import BeautifulSoup

import requests

from ..port_opener.port_message import PortMessage


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
        ports = self.get_ports()
        for port in ports:
            if port.compare(port_message):
                return True
        return False

    def get_ports(self):
        if self.session_key is None:
            self.get_session_key()

        params = {
            'action': 'view'
        }

        s = requests.get(self.ports_url, params=params, cookies=self.cookies)
        soup = BeautifulSoup(s.content, features="html.parser")
        inputs = soup.find_all("tr")
        ports = []
        for inp in inputs[1:]:
            tds = inp.find_all("td")
            ports.append(PortMessage(
                title=str(tds[0].string),
                protocol=PortMessage.resolve_protocol(tds[3].string),
                destination=str(tds[6].string),
                external_port_range=(int(tds[1].string), int(tds[2].string)),
                internal_port_range=(int(tds[4].string), int(tds[5].string))
            ))
        return ports

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
        if self.session_key is None:
            self.get_session_key()

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
