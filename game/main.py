import os, subprocess, sys, platform

'''
ENTRY POINT FOR APP

Requirements:
    Full build (attacker mode enabled) must run as root for permissions to
    access iptables, ip forwarding, and raw sockets.
    Defender-only build needs no elevated privileges — it only talks HTTP
    to the ESP32 board.
    Must be on the same network as the target device.
    Must be in the venv.
    Must run with linux or macos for full functionality. Windows doesn't allow
    many of the hacking features to work properly, but some GUI features will work.

Known issues:
    As far as I know, the daemon threads close when the program is closed.
    The DEFENDER page fails to close threads
    If not, use flusher.py to flush iptables and close all threads.
'''

# Set to True for the defender-only public build. Set to False (or remove
# this flag entirely) for the full dev build with attacker mode enabled.
DEFENDER_ONLY_BUILD = os.environ.get("GAME_DEFENDER_ONLY", "0") == "1"

from src.app_core.app import App

os_name = platform.system()

if not DEFENDER_ONLY_BUILD:
    # GUI apps usually don't run as root, but the full app constantly
    # accesses iptables, ip forwarding, and raw sockets via attacker mode.
    if os_name == "Windows":
        print("Running on Windows. Many features will not work properly.")
    elif os_name == "Linux" or os_name == "Darwin":
        if os.geteuid() != 0:
            print("Requesting root privileges for permissions...\a")
            subprocess.check_call(["sudo", sys.executable] + sys.argv)
            sys.exit()
    else:
        print(f"Running on an unidentified system: {os_name}")

# Create the App object, which owns the CTk root
game = App("title", title="Game", start_fullscreen=False)