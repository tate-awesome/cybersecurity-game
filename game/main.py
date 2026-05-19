from src.app_core.app import App
import os, subprocess, sys
import platform

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

os_name = platform.system()

if platform.system() == "Windows":
    # Elevation is not possible
    print("Running on Windows. Many features will not work properly.")
    ...
elif os_name == "Linux" or os_name == "Darwin":
    # Elevation is possible
    if os.geteuid() != 0:
        print("Requesting root privileges for permissions...\a")
        subprocess.check_call(["sudo", sys.executable] + sys.argv)
        # GUI apps usually don't run as root, but this app constantly accesses iptables, ip forwarding, and sockets
        sys.exit()
else:
    print(f"Running on an unidentified system: {os_name}")



game = App("title")
