# NMap Scan Failed

nmap started, but the scan stopped partway with the error shown.

## Common causes

- **Not enough privileges.** A ping scan (`-sn -PE`) sends raw ICMP packets, which needs administrator or root rights. Close the game, then start it from a terminal or editor opened **as Administrator** (Windows) or with `sudo` (Linux/macOS).
- **No packet capture driver (Windows).** nmap needs **Npcap**. Reinstall nmap and keep the Npcap option checked, or install Npcap on its own from [npcap.com](https://npcap.com).
- **A firewall or antivirus blocked it.** Allow nmap through, or pause the firewall while you're on the lab network.

## Then

Click **NMap** again. A successful scan ends with a **View report** link that lists every host it found.
