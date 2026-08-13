import socket
import nmap

def get_local_subnet():
    # Connect to an external IP briefly to discover the active local interface IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    
    # Convert local IP (e.g., 192.168.1.15) to a /24 subnet string (192.168.1.0/24)
    ip_parts = local_ip.split('.')
    ip_parts[-1] = '0/24'
    return '.'.join(ip_parts)

# Initialize scanner
nm = nmap.PortScanner()
subnet = get_local_subnet()

print(f"Target Subnet Detected: {subnet}")
print("Scanning for active hosts (this may take a few seconds)...")

# -sn: Ping scan (no port scan, host discovery only)
# -PE: ICMP Echo Request
nm.scan(hosts=subnet, arguments='-sn -PE')

print("\n--- Active Hosts Found ---")
# Iterate through all discovered up hosts
for host in nm.all_hosts():
    if nm[host].state() == 'up':
        hostname = nm[host].hostname()
        hostname_str = f"({hostname})" if hostname else "(No Hostname)"
        print(f"IP Address: {host:<15} State: {nm[host].state():<5} Hostname: {hostname_str}")















