# WinDivert Couldn't Open

On Windows, the NFQ hook intercepts packets with the **WinDivert** driver, and the driver didn't load.

## Fix

1. **Run as Administrator.** WinDivert loads a kernel driver, so close the game, then start it from a terminal or editor opened as Administrator.
2. **Install pydivert:** `pip install pydivert`
3. **Antivirus.** Some antivirus tools block WinDivert's driver. Allow it, or pause the antivirus while you're in the lab.
4. **IP forwarding.** To pass the intercepted traffic on, Windows also needs IP forwarding turned on. See the *IP Forwarding* fix.
