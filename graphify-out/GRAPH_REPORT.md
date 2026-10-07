# Graph Report - cybersecurity-game  (2026-10-07)

## Corpus Check
- 211 files · ~177,408 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 29 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 2455 nodes · 4897 edges · 132 communities (45 shown, 87 thin omitted)
- Extraction: 92% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 367 edges (avg confidence: 0.86)
- Token cost: 583,915 input · 0 output

## Community Hubs (Navigation)
- Menu Bar & Buttons
- Network Form Base & Context
- WiFi Connection (Linux)
- WiFi Connection (Windows)
- AP Polling & Input State
- Legacy Defender Page
- Page & Process Managers
- Geometry & Transforms
- MetaPacket & Transactions
- AP Commands & Firmware API
- Page Base & Router Wiring
- Buffer Manager & Threads
- Panel Base & Scrollable
- Layout Editor
- Overlays & Register Overlay
- Router, App & Entry Point
- Packet Console
- Processes & File Streams
- Standalone Attack HMI
- Legacy HVAC Defender View
- Animation & Click Managers
- Visual Backgrounds
- Find Bar
- Network Mesh Visual
- Workspace Select Page
- Paths & Preferences
- Visual Palette & Kernel
- Shared Qt Imports
- Theme & Style
- Packet Buffer & Graph Data
- Viewport Drawing Demo
- Design Docs & Requirements
- Nmap & Interface Manager
- Visual Base & Glow
- Defender Sliders Form
- JSON Merge & Config Loading
- ModBus Panel Builders
- ModBus Modify Form
- Localization Labels
- ModBus & House Buffers
- Defender ModBus Buffer
- Packet Replay Save/Load
- Canvas Drawing Primitives
- Strip Chart Camera
- Submarine Map Buffer
- Workspace Config Editor
- Editor Settings Rows
- ModBus MITM Screenshot
- Canvas Base & Frame Loop
- Strip Chart Layout
- NetFilterQueue Interceptor
- ModBus Submarine Screenshot
- New/Delete Workspace Dialogs
- Strip Chart Text Drawing
- Strip Chart Base Widget
- ARP & IP Basics Screenshot
- Full Attacker Suite Screenshot
- DoS Attack Screenshot
- Editor Workspace & Menu Tabs
- Canvas Camera
- ModBus HVAC Screenshot
- Network Recon Screenshot
- Status Buffer
- Defender Console Panel
- Defending the AP Screenshot
- Defender Suite Screenshot
- DoS Denier
- Editor Description Tab
- Network Diagram Canvas
- Confirm & Delete Dialogs
- Packet Filter Overlay
- Status Console Panel
- Attack Script Base Classes
- Defender HVAC Screenshot
- Defender Submarine Screenshot
- ModBus Basics Screenshot
- Keybinds & Fullscreen
- ARP Spoofer
- Live File Stream
- Editor Setting Cell
- Map Canvas Widget
- Kalman Visual
- PCAP Loader
- Virtual ModBus Master
- Defender Flag Panel
- ModBus Model Panel
- MITM Table Form
- Virtual ModBus Slave
- Editor Usage & Sorting
- Defender Strip Chart Panel
- Defender HVAC Chart
- Network Action Panel
- Encryption Form
- Telemetry Visual
- NFQ Linux Backend
- Packet Sniffer
- World Map Canvas
- Pooled Canvas Mixin
- House Canvas
- Pane Container
- Defender World Map
- Triangle Demo Canvas
- Defender Mode Form
- Editor Tab Layout Helper
- Small Canvas Widget
- Generic Panel Factory
- Smart Energy Lab Logo (2)
- Smart Energy Lab Logo
- Editor Key Column Width
- Skull Attacker Art
- Dev Requirements

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 112 edges
2. `MenuBar` - 57 edges
3. `MetaPacket` - 54 edges
4. `ConfigEditor` - 50 edges
5. `BaseForm` - 47 edges
6. `DefenderV0` - 39 edges
7. `Draw` - 36 edges
8. `Panel` - 34 edges
9. `Process` - 31 edges
10. `HVACView` - 31 edges

## Surprising Connections (you probably didn't know these)
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `status()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py

## Import Cycles
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/hvac_model/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/modbus_model/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/boat_model/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/status_console/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`

## Hyperedges (group relationships)
- **Modbus Master/Slave Control-Feedback Loop** — game_outline_master, game_outline_slave, game_outline_control_feedback_procedure, game_outline_modbus_protocol [EXTRACTED 1.00]
- **Hack Output Buffer-to-Console Flow** — game_readme_buffer, game_readme_metapacket, game_readme_console_tabview, game_readme_var_buffer_trails [INFERRED 0.75]
- **Recon -> ARP Spoof -> Sniff -> Inspect pipeline** — game_assets_pages_workspaces_arp_ip_screenshot_nmapping_form, game_assets_pages_workspaces_arp_ip_screenshot_arp_spoofing_form, game_assets_pages_workspaces_arp_ip_screenshot_packet_sniffing_form, game_assets_pages_workspaces_arp_ip_screenshot_packets_panel [INFERRED 0.75]
- **ARP & IP workspace panel set** — game_assets_pages_workspaces_arp_ip_screenshot_network_actions_panel, game_assets_pages_workspaces_arp_ip_screenshot_packets_panel, game_assets_pages_workspaces_arp_ip_screenshot_network_graph_panel, game_assets_pages_workspaces_arp_ip_screenshot_status_log_panel [EXTRACTED 1.00]
- **Network attack flow: connect WiFi, map network, ARP spoof, observe packets** — game_assets_pages_workspaces_attacker_suite_screenshot_wifi_connection, game_assets_pages_workspaces_attacker_suite_screenshot_nmapping, game_assets_pages_workspaces_attacker_suite_screenshot_arp_spoofing, game_assets_pages_workspaces_attacker_suite_screenshot_packets_panel [INFERRED 0.75]
- **ModBus process observation via registers, monitors and model** — game_assets_pages_workspaces_attacker_suite_screenshot_modbus_data_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_model_panel, game_assets_pages_workspaces_attacker_suite_screenshot_holding_registers [INFERRED 0.85]
- **Defender AP defense controls (encryption, tunnel, Kalman filter)** — game_assets_pages_workspaces_defender_ap_intro_screenshot_encryption_form, game_assets_pages_workspaces_defender_ap_intro_screenshot_ap_tunnel_form, game_assets_pages_workspaces_defender_ap_intro_screenshot_kalman_filter_toggle [INFERRED 0.75]
- **Defender monitoring flow (packet log, error flags, status log)** — game_assets_pages_workspaces_defender_ap_intro_screenshot_packet_log_panel, game_assets_pages_workspaces_defender_ap_intro_screenshot_submarine_error_detection_flags, game_assets_pages_workspaces_defender_ap_intro_screenshot_status_log_panel [INFERRED 0.75]
- **Defender anomaly detection flow (settings -> Kalman filter -> flags/monitors)** — game_assets_pages_workspaces_defender_hvac_screenshot_defender_data_panel, game_assets_pages_workspaces_defender_hvac_screenshot_kalman_filter, game_assets_pages_workspaces_defender_hvac_screenshot_defender_flags_panel, game_assets_pages_workspaces_defender_hvac_screenshot_defender_monitors_panel [INFERRED 0.75]
- **Defender anomaly detection loop: tune thresholds, observe telemetry, raise flags** — game_assets_pages_workspaces_defender_submarine_screenshot_defender_data_panel, game_assets_pages_workspaces_defender_submarine_screenshot_packet_log, game_assets_pages_workspaces_defender_submarine_screenshot_defender_flags, game_assets_pages_workspaces_defender_submarine_screenshot_defender_monitors, game_assets_pages_workspaces_defender_submarine_screenshot_kalman_filter_detection [INFERRED 0.85]
- **Defender anomaly detection flow: settings -> Kalman filter -> flags -> monitors** — game_assets_pages_workspaces_defender_suite_screenshot_defender_data_panel, game_assets_pages_workspaces_defender_suite_screenshot_kalman_filter, game_assets_pages_workspaces_defender_suite_screenshot_defender_flags_panel, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors [INFERRED 0.75]
- **Submarine telemetry views** — game_assets_pages_workspaces_defender_suite_screenshot_packet_log_panel, game_assets_pages_workspaces_defender_suite_screenshot_modbus_model_map, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors, game_assets_pages_workspaces_defender_suite_screenshot_submarine_modbus_system [INFERRED 0.75]
- **DoS attack flow: connect, map, spoof, observe traffic** — game_assets_pages_workspaces_dos_attack_screenshot_wifi_connection, game_assets_pages_workspaces_dos_attack_screenshot_nmapping, game_assets_pages_workspaces_dos_attack_screenshot_arp_spoofing, game_assets_pages_workspaces_dos_attack_screenshot_packets_panel, game_assets_pages_workspaces_dos_attack_screenshot_network_graph_panel [INFERRED 0.75]
- **ModBus process observation panels** — game_assets_pages_workspaces_dos_attack_screenshot_modbus_data_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_model_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_monitors_panel [INFERRED 0.85]
- **Recon -> ARP spoof -> tamper ModBus values -> observe HVAC effect** — game_assets_pages_workspaces_modbus_hvac_screenshot_network_actions_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_modifiers, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Network traffic observation panels** — game_assets_pages_workspaces_modbus_hvac_screenshot_packets_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_network_graph_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_status_panel [INFERRED 0.75]
- **ModBus Intro MITM observation flow** — game_assets_pages_workspaces_modbus_intro_screenshot_network_actions_panel, game_assets_pages_workspaces_modbus_intro_screenshot_packets_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_data_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Panels sharing common header control pattern** — game_assets_pages_workspaces_modbus_intro_screenshot_panel_header_controls, game_assets_pages_workspaces_modbus_intro_screenshot_packets_panel, game_assets_pages_workspaces_modbus_intro_screenshot_status_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_modbus_intro_screenshot_network_graph_panel [EXTRACTED 1.00]
- **MITM attack workflow: WiFi connect, network mapping, ARP spoofing** — game_assets_pages_workspaces_modbus_mitm_screenshot_wifi_connection, game_assets_pages_workspaces_modbus_mitm_screenshot_nmapping, game_assets_pages_workspaces_modbus_mitm_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_mitm_screenshot_modbus_mitm_attack [INFERRED 0.85]
- **Traffic and register observation panels** — game_assets_pages_workspaces_modbus_mitm_screenshot_packets_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_network_graph_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_status_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Recon, ARP spoof, and ModBus tamper workflow** — game_assets_pages_workspaces_modbus_submarine_screenshot_nmapping, game_assets_pages_workspaces_modbus_submarine_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_data_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_mitm_attack_flow [INFERRED 0.75]
- **Submarine state visualization panels** — game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_submarine_variables [INFERRED 0.75]
- **Recon/MITM action to traffic observation loop** — game_assets_pages_workspaces_network_recon_screenshot_arp_spoofing_form, game_assets_pages_workspaces_network_recon_screenshot_packet_sniffing_form, game_assets_pages_workspaces_network_recon_screenshot_packets_panel, game_assets_pages_workspaces_network_recon_screenshot_network_graph_panel [INFERRED 0.75]
- **Network Recon workspace panel layout** — game_assets_pages_workspaces_network_recon_screenshot_top_toolbar, game_assets_pages_workspaces_network_recon_screenshot_network_actions_panel, game_assets_pages_workspaces_network_recon_screenshot_packets_panel, game_assets_pages_workspaces_network_recon_screenshot_network_graph_panel, game_assets_pages_workspaces_network_recon_screenshot_status_panel [EXTRACTED 1.00]

## Communities (132 total, 87 thin omitted)

### Community 0 - "Menu Bar & Buttons"
Cohesion: 0.05
Nodes (14): TitlePage, _drain_evenly(), MenuBar, click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor() (+6 more)

### Community 1 - "Network Form Base & Context"
Cohesion: 0.11
Nodes (12): ContextManager, apply_scale_about(), BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, KalmanForm (+4 more)

### Community 2 - "WiFi Connection (Linux)"
Cohesion: 0.06
Nodes (11): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish(), on_last_scan_changed() (+3 more)

### Community 3 - "WiFi Connection (Windows)"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 4 - "AP Polling & Input State"
Cohesion: 0.05
Nodes (4): InputManager, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 5 - "Legacy Defender Page"
Cohesion: 0.07
Nodes (4): APPoller, DefenderV0, enc_button(), slider_callback()

### Community 7 - "Geometry & Transforms"
Cohesion: 0.06
Nodes (22): draw_vessel(), canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), flatten(), get_arc_points() (+14 more)

### Community 8 - "MetaPacket & Transactions"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 9 - "AP Commands & Firmware API"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 10 - "Page Base & Router Wiring"
Cohesion: 0.08
Nodes (9): AttackerV0, BoatMotion, Sprites, Triangle, Visuals, WorkspacePage, NotFound, Page (+1 more)

### Community 12 - "Panel Base & Scrollable"
Cohesion: 0.11
Nodes (11): House, StripChart, WorldMap, CheckboxOverlay, Panes, Scrollable, Builder, Builder (+3 more)

### Community 13 - "Layout Editor"
Cohesion: 0.09
Nodes (6): remove_nested(), set_nested(), LayoutEditor, group(), add(), add()

### Community 14 - "Overlays & Register Overlay"
Cohesion: 0.08
Nodes (4): Overlay, VariableOverlay, autosave(), reset_all()

### Community 15 - "Router, App & Entry Point"
Cohesion: 0.07
Nodes (5): build_name(), main(), App, MainWindow, Router

### Community 16 - "Packet Console"
Cohesion: 0.08
Nodes (4): Builder, reset_capture(), autosave(), PacketTreeview

### Community 17 - "Processes & File Streams"
Cohesion: 0.09
Nodes (5): flush(), flush_all(), run(), Buffer, Process

### Community 19 - "Legacy HVAC Defender View"
Cohesion: 0.12
Nodes (3): HVACView, enc_button(), slider_callback()

### Community 20 - "Animation & Click Managers"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 22 - "Find Bar"
Cohesion: 0.10
Nodes (3): FindBar, walk(), FindField

### Community 24 - "Workspace Select Page"
Cohesion: 0.11
Nodes (3): WorkspaceButton, WorkspaceSelectPage, delete()

### Community 30 - "Packet Buffer & Graph Data"
Cohesion: 0.10
Nodes (3): DefenderMapBuffer, NetworkGraph, PacketBuffer

### Community 32 - "Design Docs & Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 33 - "Nmap & Interface Manager"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 36 - "Defender Sliders Form"
Cohesion: 0.16
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 50 - "ModBus MITM Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 54 - "ModBus Submarine Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 58 - "ARP & IP Basics Screenshot"
Cohesion: 0.19
Nodes (13): AP Connection Form (AP URL, Disconnect, waiting indicator), ARP Spoofing Form (Target IP, Host IP, Start Spoofer), Encryption Form, ARP & IP Basics Workspace Screenshot, ARP Spoofing MITM Attack Workflow, Network Actions Panel (Forms, Stop All), Network Graph Panel with Packets per Second Chart, NMapping Form (Map Network) (+5 more)

### Community 59 - "Full Attacker Suite Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 60 - "DoS Attack Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 63 - "ModBus HVAC Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 64 - "Network Recon Screenshot"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 67 - "Defending the AP Screenshot"
Cohesion: 0.21
Nodes (12): Defending the AP Workspace Screenshot, AP Connection Form (AP URL, Disconnect), AP Tunnel Form (Enable AP Tunnel), Defender Flags Panel, Encryption Form (Key, Enable Encryption), Kalman Filter Toggle, Minimizable Panel Layout Pattern, Network Access Panel (+4 more)

### Community 68 - "Defender Suite Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 70 - "Editor Description Tab"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 72 - "Network Diagram Canvas"
Cohesion: 0.18
Nodes (3): NetworkDiagramCanvas, draw_host(), frame_callback()

### Community 73 - "Confirm & Delete Dialogs"
Cohesion: 0.41
Nodes (6): confirm_dialog(), delete_all_workspace_data_dialog(), delete_user_data_dialog(), delete_workspace_data_dialog(), message(), quit_dialog()

### Community 74 - "Packet Filter Overlay"
Cohesion: 0.23
Nodes (3): FilterOverlay, packet_filter(), activate()

### Community 76 - "Attack Script Base Classes"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 77 - "Defender HVAC Screenshot"
Cohesion: 0.27
Nodes (11): Defender HVAC Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors Panel (X/Y Position plots), Kalman Filter Anomaly Detection, Minimizable Three-Column Panel Layout, ModBus Model Panel (Temperature Trajectory Over Time), Network Access Panel (AP Connection, Encryption, AP Tunnel) (+3 more)

### Community 78 - "Defender Submarine Screenshot"
Cohesion: 0.24
Nodes (11): Defender Submarine Workspace Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position time plots), Kalman Filter Anomaly Detection, Minimizable Multi-Panel Dashboard Layout, ModBus Model (Defender Map plot), Network Access Panel (AP Connection, Encryption, AP Tunnel) (+3 more)

### Community 79 - "ModBus Basics Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 101 - "World Map Canvas"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 103 - "House Canvas"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 117 - "Smart Energy Lab Logo (2)"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 118 - "Smart Energy Lab Logo"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

## Ambiguous Edges - Review These
- `Defender Data Panel (Operation Mode, Submarine Settings sliders)` → `ModBus Model Panel (Temperature Trajectory Over Time)`  [AMBIGUOUS]
  game/assets/pages/workspaces/defender_hvac/screenshot.png · relation: conceptually_related_to

## Knowledge Gaps
- **67 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+62 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 939 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Defender Data Panel (Operation Mode, Submarine Settings sliders)` and `ModBus Model Panel (Temperature Trajectory Over Time)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `ContextManager` connect `Network Form Base & Context` to `AP Polling & Input State`, `JSON Merge & Config Loading`, `Page & Process Managers`, `Localization Labels`, `Matplotlib HVAC Chart`, `Page Base & Router Wiring`, `Buffer Manager & Threads`, `Panel Base & Scrollable`, `Confirm & Delete Dialogs`, `Keybinds & Fullscreen`, `Processes & File Streams`, `Animation & Click Managers`, `Paths & Preferences`, `Shared Qt Imports`, `Theme & Style`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _67 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Menu Bar & Buttons` be split into smaller, more focused modules?**
  _Cohesion score 0.05381400208986416 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `Workspace Config Editor` to `Menu Bar & Buttons`, `Editor Description Tab`, `Page Base & Router Wiring`, `Layout Editor`, `Workspace Creation`, `Editor Settings Rows`, `Editor Setting Cell`, `Editor Key Column Width`, `Find Bar`, `New/Delete Workspace Dialogs`, `Workspace Select Page`, `Shared Qt Imports`, `Editor Usage & Sorting`, `Editor Workspace & Menu Tabs`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MetaPacket` (e.g. with `Buffer` and `HouseBuffer`) actually correct?**
  _`MetaPacket` has 12 INFERRED edges - model-reasoned connections that need verification._