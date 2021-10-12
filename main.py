import argparse
from random import randint
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()

parser.add_argument('-i', '--ip', type=str, help='Router\'s ip', default='192.168.1.1', required=False)
parser.add_argument('-a', '--action', type=str, help='Action', choices=['add', 'remove', 'check'], required=True)
parser.add_argument('-p', '--password', type=str, help='Router\'s password', required=True)
parser.add_argument('-d', '--destination-ip', type=str, help='Destination ip', required=True)
parser.add_argument('-n', '--service-name', type=str, help='Service name', required=True)
parser.add_argument('--e-start', type=int, help='External start port', required=True)
parser.add_argument('--e-end', type=int, help='External end port', required=True)
parser.add_argument('--i-start', type=int, help='Internal start port', required=True)
parser.add_argument('--i-end', type=int, help='Internal end port', required=True)
parser.add_argument('--protocol', type=str, help='Protocol', choices=['TCP', 'UDP', 'Both'], required=True)

args = parser.parse_args()

router_ip = args.ip
password = args.password

e_start = args.e_start
e_end = args.e_end
i_start = args.i_start
i_end = args.i_end

destination_ip = args.destination_ip
service_name = args.service_name
protocol = args.protocol
action = args.action

access_url = 'http://' + router_ip + '/te_acceso_router.cgi'
ports_url = 'http://' + router_ip + '/scvrtsrv.cmd'

session_key = ""
cookies = {}
headers = {"Content-Type": "application/x-www-form-urlencoded"}


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def get_session_key():
    global session_key, cookies
    data = {'loginPassword': password}
    session_key = str(random_with_n_digits(10))
    cookies = {'sessionID': session_key}
    requests.post(access_url, data, cookies=cookies, headers=headers)


def add_port_proto():
    if protocol == "TCP":
        return "1,"
    elif protocol == "UDP":
        return "2,"
    else:
        return "0,"


def add_port():
    params = {
        'action': 'add',
        'srvName': service_name,
        'dstWanIf': 'ppp0.1',
        'srvAddr': destination_ip,
        'proto': add_port_proto(),
        'eStart': str(e_start) + ",",
        'eEnd': str(e_end) + ",",
        'iStart': str(i_start) + ",",
        'iEnd': str(i_end) + ",",
        'sessionKey': session_key
    }
    requests.get(ports_url, params=params, cookies=cookies)


def compose_rml_command():
    return destination_ip + "|" + str(e_start) + "|" + str(e_end) + "|" + \
           ("TCP or UDP" if protocol == "Both" else protocol) + "|" + str(i_start) + "|" + str(i_end)


def remove_port():
    params = {
        'action': 'remove',
        'rmLst': compose_rml_command(),
        'sessionKey': session_key
    }
    requests.get(ports_url, params=params, cookies=cookies)


def check_port():
    params = {
        'action': 'view'
    }
    s = requests.get(ports_url, params=params, cookies=cookies)
    soup = BeautifulSoup(s.content, features="html.parser")
    inputs = soup.find_all("input", {"name": "rml"})
    for inp in inputs:
        if inp.get('value') == compose_rml_command():
            print("True")
            return
    print("False")


get_session_key()

if action == "check":
    check_port()
elif action == "add":
    add_port()
elif action == "remove":
    remove_port()
