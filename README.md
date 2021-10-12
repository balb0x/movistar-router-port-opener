# Movistar Router Port Opener

This simple script can open, close and check the status of the ports of the Movistar's router.
Currently, its only been tested on Askey HGU RFT3505VW. 

## Usage

```
main.py [-h] [-i IP] -a {add,remove,check} -p PASSWORD -d
               DESTINATION_IP -n SERVICE_NAME --e-start E_START --e-end E_END
               --i-start I_START --i-end I_END --protocol {TCP,UDP,Both}
```

## Installation

You just need to install the packages from the requirements.txt

```
pip3 install -r requirements.txt
```

## Parameters

| Parameter                 | Usage                                       |
|---------------------------|---------------------------------------------|
| `-i, --ip`                | The router ip address                       |
| `-p, --password`          | The router admin password                   |
| `-a, --action`            | Whether to add/remove/check the ports       |
| `-d, --destination-ip`    | The destination ip                          |
| `-n, --service-name`      | The service name. Just for display purposes |
| `--e-start`               | External start port                         |
| `--e-end`                 | External end port                           |
| `--i-start`               | Internal start port                         |
| `--i-end`                 | Internal end port                           |
| `--protocol`              | Protocol to use (UDP/TCP/Both)              |

## Example

Add port forwarding from 1111 to 1111 in both UDP and TCP to a given ip (`192.168.1.100`)

```
python3 main.py -a add -p {router_password} --e-start 1111 --e-end 1111 --i-start 1111 --i-end 1111 --protocol Both -d 192.168.1.100 -n service_name
```

Remove previous port forwarding

```
python3 main.py -a remove -p {router_password} --e-start 1111 --e-end 1111 --i-start 1111 --i-end 1111 --protocol Both -d 192.168.1.100 -n service_name
```

Check a port forwarding

```
python3 main.py -a check -p {router_password} --e-start 1111 --e-end 1111 --i-start 1111 --i-end 1111 --protocol Both -d 192.168.1.100 -n service_name
```

The previous example should return `True` or `False` in the stdout


## Notes

If you are using the script to open multiple ports, the service name should be different, otherwise, the router won't add the port forwarding.  