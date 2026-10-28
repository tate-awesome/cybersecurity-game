# Cyber-ICS Training Module

An educational cybersecurity game about **industrial control systems (ICS)**. The
scenario is a small maritime control loop: a "master" steers a vessel by reading its
position and writing rudder and speed commands to a "slave" over
[ModBus](https://en.wikipedia.org/wiki/Modbus), the same request/response protocol used
on real industrial networks.

Players work through **attacker** and **defender** lessons, using a desktop app to
observe and interact with that traffic the way a real analyst would — scanning the
network, sniffing packets, mapping hosts, and watching the vessel move on a live world
map as commands flow across the wire. It is built for teaching and authorized, hands-on
practice in a controlled lab, not for use against networks you don't own or operate.

## The game lives in [`game/`](game/)

The playable application is a PySide6 (Qt) desktop app. **Start there:**

```bash
cd game
python -m venv ../venv            # see game/pyproject.toml for the expected venv path
# activate the venv, then:
pip install -r requirements.txt
python main.py
```

A few things to know before running (full notes are in [`game/main.py`](game/main.py)
and [`game/requirements.txt`](game/requirements.txt)):

- **Run with administrator / root privileges.** The app elevates itself where it can,
  but packet capture and interception need elevated rights. On Windows, launching your
  editor or shell as Administrator is the most reliable route.
- **Be on the same network as the target device** (the ESP32-based router/vessel setup;
  firmware is under [`firmware/`](firmware/)).
- Some dependencies are **platform-specific** — `netfilterqueue` and `PyGObject` on
  Linux, `pydivert`/WinDivert on Windows. The comments in
  [`game/requirements.txt`](game/requirements.txt) list the extra system packages and
  registry settings each platform needs.
- `nmap` must be installed separately on the system (for `python-nmap`).

The app's own design notes and screen outline are in
[`game/README.md`](game/README.md) and [`game/outline.txt`](game/outline.txt).

## Repository layout

| Path | What's there |
| --- | --- |
| [`game/`](game/) | **The main application** — the PySide6 training game, its source (`src/`), assets, and build scripts. |
| [`firmware/`](firmware/) | ESP32 Arduino sketches for the lab hardware — access point, client/server, HMI, and a REST API. |
| [`ICS_Attacks/`](ICS_Attacks/) | Standalone scripts and captures used while developing and demonstrating the ICS attack techniques. |
| [`archive/`](archive/) | Older versions and experiments kept for reference, including an HVAC model. |
| [`build/`](build/) | Firmware build artifacts and configuration. |
| [`graphify-out/`](graphify-out/) | Generated knowledge graph of the codebase (see [`CLAUDE.md`](CLAUDE.md)). |

## Intended use

This project is for **education and authorized security practice** — classroom use,
training labs, and testing on equipment you own or have explicit permission to test.
Only run the network tools against the project's own lab devices or other targets you
are authorized to assess.
