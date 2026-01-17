import os
import time

def run(cmd):
    print(f"\n▶ {cmd}")
    os.system(cmd)

print("\n=== Network Reset Script Starting ===\n")

# 1. Kill leftover python / scapy / nfq processes
run("sudo pkill -f netfilterqueue")
run("sudo pkill -f scapy")

# 2. Flush iptables (all tables)
run("sudo iptables -F")
run("sudo iptables -X")
run("sudo iptables -t nat -F")
run("sudo iptables -t nat -X")
run("sudo iptables -t mangle -F")
run("sudo iptables -t mangle -X")

# 3. Reset default policies
run("sudo iptables -P INPUT ACCEPT")
run("sudo iptables -P FORWARD ACCEPT")
run("sudo iptables -P OUTPUT ACCEPT")

# 4. Clear ARP cache
run("sudo ip neigh flush all")

# 5. Restart NetworkManager
run("sudo systemctl restart NetworkManager")

print("\n=== Network Reset Complete ===\n")

# 6. Kill python
run("sudo pkill -f python3")
