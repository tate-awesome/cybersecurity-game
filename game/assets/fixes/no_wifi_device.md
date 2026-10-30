# No Wi-Fi Adapter

The game couldn't find a Wi-Fi adapter on this computer.

## Fix

- **Desktop computers** often have no Wi-Fi at all. Plug in a USB Wi-Fi adapter, or connect to the lab network with an Ethernet cable and skip the WiFi Switch form.
- **Laptops:** check that the adapter isn't disabled in **Device Manager** (Windows) or with `nmcli radio` (Linux).
- **Virtual machines** usually can't see the host's Wi-Fi. Pass a USB Wi-Fi adapter through to the VM.
