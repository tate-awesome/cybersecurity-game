'''
Module
'''
import scapy.all as scapy
from scapy.all import IP, ICMP, sr1
import ipaddress, netifaces
import threading


def get_network() -> tuple[str, str]:
    '''
    Returns your ip and the netmask
    '''
    iface = "wlp0s20f3"
    info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]

    ip = info["addr"]
    netmask = info["netmask"]
    return ip, netmask


def compute_network(ip: str, netmask: str) -> str:
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return network


def get_hosts(network: str, iface="wlp0s20f3"):
    '''
    Returns: list[tuple[ip: str, mac: str]]
    May block for up to 2 seconds.
    '''
    network = str(network)
    packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network)
    answered, _ = scapy.srp(packet, timeout=2, verbose=False)

    hosts = []
    for _, recv in answered:
        hosts.append({
            "ip": recv.psrc,
            "mac": recv.hwsrc
        })
    return hosts


def get_host_ips(hosts):
    out = []
    for h in hosts:
        out.append(h["ip"])
    return out


if __name__ == "__main__":
    
    ip, netmask = get_network()
    print("IP: ",ip)
    print("Netmask: ",netmask)
    network = compute_network(ip, netmask)
    print("Network: ",network)
    hosts = get_hosts(network)
    print(hosts)
    print(get_host_ips(hosts))