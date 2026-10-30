# Install NMap

The **NMap** form runs the `nmap` program that's installed on your computer. The game doesn't include its own copy, and it couldn't find one.

## Fix

1. Install nmap:
   - **Windows:** download the installer from [nmap.org/download.html](https://nmap.org/download.html) and run it. Keep **Npcap** checked when the installer offers it.
   - **macOS:** `brew install nmap`
   - **Linux (Ubuntu/Debian):** `sudo apt install nmap`
2. **Restart the game.** It looks for nmap when it starts, so a game that's already open won't see the new install.

## Still not found?

The installer has to put nmap on your `PATH`. To check, open a new terminal and run `nmap --version`. If that fails too, reinstall nmap, or add its folder (usually `C:\Program Files (x86)\Nmap` on Windows) to `PATH`.
