# Wi-Fi Control Unavailable

The **WiFi Switch** form talks to your computer's Wi-Fi service, and the game couldn't reach that service.

## Windows

The **WLAN AutoConfig** service has to be running. Open **Services** (`services.msc`), find *WLAN AutoConfig*, and click **Start**. Also set its startup type to *Automatic*.

## Linux

The form uses **NetworkManager** through its Python bindings:

```
sudo apt-get install -y network-manager gir1.2-nm-1.0 libcairo2-dev libgirepository-2.0-dev gobject-introspection
pip install PyGObject
```

Then check that NetworkManager is running: `systemctl status NetworkManager`.

Restart the game after installing.
