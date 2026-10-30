# ARP Spoof Error

Sending or receiving ARP packets failed partway through the spoof.

## Common causes

- **Not enough privileges.** Raw packets need administrator or root rights. Restart the game **as Administrator** (Windows) or with `sudo` (Linux/macOS).
- **No capture driver (Windows).** Scapy needs **Npcap** ([npcap.com](https://npcap.com)). Install it in *WinPcap API-compatible mode*.
- **The network changed.** If you switched Wi-Fi networks mid-spoof, stop it and start it again.

Stop the ARP spoof, fix whatever caused the error, then start it again.
