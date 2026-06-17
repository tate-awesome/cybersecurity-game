import os, subprocess, sys, platform, ctypes

from src.app_core.app import App

'''
ENTRY POINT FOR APP

Requirements:
    The Game tries to do privelege elevation on all platforms, but it's better to run VSCode as Admin on Windows.
    Must be on the same network as the target device - our ESP32-config router
    Must be in the venv
        Install requirements.txt. IDK how to do platform-dependent package installs
    We are working on cross-platform features

Known issues:
    As far as I know, the daemon threads close when the program is closed.
    The DEFENDER page fails to close threads
    If not, use flusher.py to flush iptables and close all threads.
'''

os_name = platform.system()


def is_admin_windows():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


if os_name == "Windows":
    if not is_admin_windows():
        print("Requesting administrator privileges...")

        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",                  # UAC elevation
            sys.executable,
            " ".join(f'"{arg}"' for arg in sys.argv),
            None,
            1
        )
        sys.exit()
elif os_name == "Linux" or os_name == "Darwin":
    if os.geteuid() != 0:
        print("Requesting root privileges for permissions...\a")
        subprocess.check_call(["sudo", sys.executable] + sys.argv)
        sys.exit()
else:
    print(f"Running on an unidentified system: {os_name}")

# Create the App object, which owns the CTk root
game = App("title", title="Game", start_fullscreen=False)
