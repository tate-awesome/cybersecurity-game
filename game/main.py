from src.app_core.app import App
import os, subprocess, sys

# Run as sudo for socket permissions?
# sudo python3 
# Password = veronica
# Be on GL-SFT1200-ab1 wifi
# Reset device before clicking start buttons
# ctrl+c in terminal to stop os commands - note: you shouldn't need to do this anymore
# trash terminal - note: you shouldn't need to do this anymore
# Wireshark filter:     ip.addr == 192.168.8.137 || arp

# Deactivate venv: deactivate
# Create venv: python -m venv myenv
# Activate: source myenv/bin/activate   

def privilege_elevation():
    if os.geteuid() != 0:
        print("Requesting root privileges for permissions...\a")
        subprocess.check_call(["sudo", sys.executable] + sys.argv)
        # GUI apps usually don't run as root, but this app constantly accesses iptables, ip forwarding, and sockets
        sys.exit()

privilege_elevation()

game = App("title")
