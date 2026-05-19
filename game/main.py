import os, subprocess, sys, platform

from src.app_core.app import App

'''
ENTRY POINT FOR APP

Requirements:
    Must run as root for permissions to access iptables, ip forwarding, and sockets
    Must be on the same network as the target device
    Must be in the venv
    Must run with linux or macos for full functionality. Windows doesn't allow many of the hacking features to work properly, but some GUI features will work.

Known issues:
    As far as I know, the daemon threads close when the program is closed.
    If not, use flusher.py to flush iptables and close all threads.
'''

os_name = platform.system()

# GUI apps usually don't run as root, but this app constantly accesses iptables, ip forwarding, and sockets
if os_name == "Windows":
    print("Running on Windows. Many features will not work properly.")
    ...
elif os_name == "Linux" or os_name == "Darwin":
    if os.geteuid() != 0:
        print("Requesting root privileges for permissions...\a")
        subprocess.check_call(["sudo", sys.executable] + sys.argv)
        sys.exit()
else:
    print(f"Running on an unidentified system: {os_name}")


game = App("title")
