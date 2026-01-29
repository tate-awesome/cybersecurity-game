import scapy.all as scapy
import socket
from scapy.all import IP, ICMP, sr1

# Dealing with hosts
def get_hosts(network, iface="wlp0s20f3"):
    packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network)
    answered, _ = scapy.srp(packet, timeout=2, verbose=False)

    hosts = []
    for _, recv in answered:
        hosts.append({
            "ip": recv.psrc,
            "mac": recv.hwsrc
        })
    return hosts

def get_host_ips(current_address):
    hosts = get_hosts(current_address)
    out = []
    for h in hosts:
        out.append(h["ip"])
    return out

# {'ip': '192.168.8.1', 'mac': '94:83:c4:52:fa:b2'}
# {'ip': '192.168.8.137', 'mac': '34:85:18:92:02:6c'}
# {'ip': '192.168.8.243', 'mac': '34:cd:b0:33:85:b4'}
def print_hosts(current_address):
    hosts = get_hosts(current_address)
    for h in hosts:
        print(h)

class infer:
    def vendor(mac):
        return scapy.conf.manufdb._get_manuf(mac)

    def dns(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
    def os(ip):
        pkt = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=False)
        if not pkt:
            return None

        ttl = pkt.ttl
        if ttl <= 64:
            return "Linux / Android / IoT"
        elif ttl <= 128:
            return "Windows"
        elif ttl <= 255:
            return "Network device"

def print_host_info(devices):
    for d in devices:
        
        d["vendor"] = infer.vendor(d["mac"])
        d["hostname"] = infer.dns(d["ip"])
        d["os_guess"] = infer.os(d["ip"])
        print("\n",d["hostname"])
        print("\tip:\t",d["ip"])
        print("\tmac:\t",d["mac"])
        print("\tvendor:\t",d["vendor"])
        print("\tos guess:\t",d["os_guess"])
        print("\tIP:",d["ip"])

def get_host_info(devices):
    for d in devices:
        
        d["vendor"] = infer.vendor(d["mac"])
        d["hostname"] = infer.dns(d["ip"])
        d["os_guess"] = infer.os(d["ip"])
    return devices

# Dealing with local
def get_local_ip(prefix=24):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return f"{ip}/{prefix}"