# Sniffer Didn't Start

The traffic sniffer couldn't open the network interface to capture packets.

## Fix

- **Privileges.** Capturing needs administrator or root rights. Restart the game **as Administrator** (Windows) or with `sudo` (Linux/macOS).
- **Capture driver (Windows).** Install **Npcap** from [npcap.com](https://npcap.com), in *WinPcap API-compatible mode*.
- **Privileged helper.** If the **network helper** setting is on, the sniffer runs in a separate elevated process. Accept its permission prompt when it appears. If you dismissed the prompt, reopen the workspace to get it back.
