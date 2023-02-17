import argparse
from random import randint
import requests
from bs4 import BeautifulSoup

from movistar_router_port_opener.port_opener.handler import PortHandler
from movistar_router_port_opener.port_opener.port_message import PortMessage

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

port_handler = PortHandler(password)

port_message = PortMessage(title=service_name,
                           protocol=PortMessage.resolve_protocol(protocol),
                           destination=destination_ip,
                           external_port_range=(e_start, e_end),
                           internal_port_range=(i_start, i_end)
                           )

if action == "check":
    port_handler.check_port(port_message)
elif action == "add":
    port_handler.add_port(port_message)
elif action == "remove":
    port_handler.remove_port(port_message)
