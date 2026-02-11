import os
import time

scripts = {
    "python": [
        "sudo pkill -f netfilterqueue",
        "sudo pkill -f scapy"
    ],
    "iptables": [
        "sudo iptables -F",
        "sudo iptables -X",
        "sudo iptables -t nat -F",
        "sudo iptables -t nat -X",
        "sudo iptables -t mangle -F",
        "sudo iptables -t mangle -X"
    ],
    "policies": [
        "sudo iptables -P INPUT ACCEPT",
        "sudo iptables -P FORWARD ACCEPT",
        "sudo iptables -P OUTPUT ACCEPT"
    ],
    "arp": [
        "sudo ip neigh flush all"
    ],
    "network_manager": [
        "sudo systemctl restart NetworkManager"
    ],
}

def run(cmd):
    print(f"\n▶ {cmd}")
    os.system(cmd)

def flush_all():
    for key in scripts:
        flush(key)

def flush(key: str):
    for script in scripts[key]:
        run(script)


if __name__ == "__main__":
    flush_all()