# Graph Report - cybersecurity-game  (2026-10-14)

## Corpus Check
- 299 files · ~218,246 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3396 nodes · 6979 edges · 167 communities (61 shown, 106 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 419 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Network Action Buttons
- Packet Streams & Transactions
- Overlay Framework
- Footer & Version Info
- Paths & Build Flushing
- Layout & Config Editors
- Modbus Channels & Defender Map
- Background Visuals
- Settings Overlay Buttons
- Settings Page
- Access Point Forms
- Page Manager
- Panes & Packet Console
- Menu Bar & Boat Demo
- Defender Core
- Important Button Base
- Visual Base & Backdrop
- Page Base Class
- Distribution & ARP Scripts
- Simulation Models & Buffers
- Checkbox Overlay
- Network Mesh Visual
- Attack HMI Scripts
- Viewport & Geometry
- Find Bar
- Scrollable Frames
- Title Menu
- Defender Modbus Polling
- Workspace Save & Popups
- Packet Console Treeview
- Linux WiFi Backend
- House & World Map Canvases
- Style Context
- Performance Monitor
- HVAC Defender View
- Windows WiFi Backend
- Time-Core Drawing
- Nmap & Linux NFQ
- Workspace Select Page
- Time-Core Camera
- AP Commands
- Helper Server & Registry
- Localization Manager
- Canvas Core & Diagrams
- Mesh Visual Helpers
- Project Docs & Requirements
- Context & Process Manager
- Buffer Status Channels
- DoS, Sniffing & AP Polling
- Config Editor Core
- Kernel Visual
- Slider Forms
- Click & Callback Registry
- Input Manager
- Packet Filter Console
- Menu Bar Settings
- JSON Context Utils
- Keybinds
- WiFi Abstraction
- Modify Form
- Vector Field Visual
- App Bootstrap & Transitions
- Backdrop Styling
- Defender Status Channel
- Helper Launcher
- Replay
- Strip Chart Canvas
- Map Widget
- Palette Generator
- Windows WiFi Helpers
- Router
- Helper Host Client
- Constellation Visual
- Preferences
- HVAC Chart & Shift Slider
- Core Draw
- Modbus Variable Overlay
- Net Filter Queue
- Config Editor Fields
- Wave Grid Visual
- Theme & Localization Buttons
- Modbus MITM Screenshot
- Geometry & Camera
- Config Editor Lists
- Config Editor Inputs
- Dev Host API
- Modbus Submarine Screenshot
- Route Transitions
- Config Editor Validation
- Time-Core Transforms
- ARP/IP Screenshot
- Attacker Suite Screenshot
- DoS Attack Screenshot
- Fade Transitions
- External Link Buttons
- Table Form
- Prod Host API
- Modbus HVAC Screenshot
- Network Recon Screenshot
- Animation Manager
- Style Fonts
- Config Editor Tree
- Defender Console
- Modbus Model Panel
- Defender Suite Screenshot
- Performance Sampling
- Transition Timing
- Core Camera Draw
- Proximity Visual
- ARP Poisoner
- Modbus Intro Screenshot
- Path & JSON Loading
- Encryption Form
- Config Editor Serialization
- Kalman Visual
- ARP Spoofing
- Saved Data Loader
- Virtual Modbus Master
- Defender Flag Panel
- Transition Overlays
- AP Poller
- Virtual Modbus Slave
- Core Transforms
- Config Editor Misc
- Helper Host Internals
- Config Editor Rows
- Config Editor Actions
- Pooled Canvas
- Favorite Page Button
- Pane Splitting
- App Main Window
- Linux WiFi Scanning
- Draw Transforms
- Configure Workspace Button
- Mode Form
- Telemetry Visual
- Legacy Visualizer v17
- Nmap Scanning
- Workspace Select Cards
- Edit Modbus Register Display
- Windows WiFi Profiles
- Workspace Select Filters
- Dense Mesh Visual
- Smart Energy Image 2
- Smart Energy Image
- Sprites
- Skull Image
- Dev Requirements

## God Nodes (most connected - your core abstractions)
1. `ImportantButton` - 89 edges
2. `ConfigEditor` - 65 edges
3. `Overlay` - 64 edges
4. `MetaPacket` - 59 edges
5. `Style` - 56 edges
6. `VisualPalette` - 48 edges
7. `BaseForm` - 47 edges
8. `MenuBar` - 43 edges
9. `DefenderV0` - 39 edges
10. `VisualBackground` - 37 edges

## Surprising Connections (you probably didn't know these)
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `status()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py

## Import Cycles
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/modbus_model/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/packet_console/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/status_console/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`

## Hyperedges (group relationships)
- **ARP & IP workspace panel set** — game_assets_pages_workspaces_arp_ip_screenshot_network_actions_panel, game_assets_pages_workspaces_arp_ip_screenshot_packets_panel, game_assets_pages_workspaces_arp_ip_screenshot_network_graph_panel, game_assets_pages_workspaces_arp_ip_screenshot_status_log_panel [EXTRACTED 1.00]
- **Panels sharing common header control pattern** — game_assets_pages_workspaces_modbus_intro_screenshot_panel_header_controls, game_assets_pages_workspaces_modbus_intro_screenshot_packets_panel, game_assets_pages_workspaces_modbus_intro_screenshot_status_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_modbus_intro_screenshot_network_graph_panel [EXTRACTED 1.00]
- **Modbus Master/Slave Control-Feedback Loop** — game_outline_master, game_outline_slave, game_outline_control_feedback_procedure, game_outline_modbus_protocol [EXTRACTED 1.00]
- **Network Recon workspace panel layout** — game_assets_pages_workspaces_network_recon_screenshot_top_toolbar, game_assets_pages_workspaces_network_recon_screenshot_network_actions_panel, game_assets_pages_workspaces_network_recon_screenshot_packets_panel, game_assets_pages_workspaces_network_recon_screenshot_network_graph_panel, game_assets_pages_workspaces_network_recon_screenshot_status_panel [EXTRACTED 1.00]
- **Recon -> ARP Spoof -> Sniff -> Inspect pipeline** — game_assets_pages_workspaces_arp_ip_screenshot_nmapping_form, game_assets_pages_workspaces_arp_ip_screenshot_arp_spoofing_form, game_assets_pages_workspaces_arp_ip_screenshot_packet_sniffing_form, game_assets_pages_workspaces_arp_ip_screenshot_packets_panel [INFERRED 0.75]
- **Network attack flow: connect WiFi, map network, ARP spoof, observe packets** — game_assets_pages_workspaces_attacker_suite_screenshot_wifi_connection, game_assets_pages_workspaces_attacker_suite_screenshot_nmapping, game_assets_pages_workspaces_attacker_suite_screenshot_arp_spoofing, game_assets_pages_workspaces_attacker_suite_screenshot_packets_panel [INFERRED 0.75]
- **Defender anomaly detection flow: settings -> Kalman filter -> flags -> monitors** — game_assets_pages_workspaces_defender_suite_screenshot_defender_data_panel, game_assets_pages_workspaces_defender_suite_screenshot_kalman_filter, game_assets_pages_workspaces_defender_suite_screenshot_defender_flags_panel, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors [INFERRED 0.75]
- **Submarine telemetry views** — game_assets_pages_workspaces_defender_suite_screenshot_packet_log_panel, game_assets_pages_workspaces_defender_suite_screenshot_modbus_model_map, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors, game_assets_pages_workspaces_defender_suite_screenshot_submarine_modbus_system [INFERRED 0.75]
- **DoS attack flow: connect, map, spoof, observe traffic** — game_assets_pages_workspaces_dos_attack_screenshot_wifi_connection, game_assets_pages_workspaces_dos_attack_screenshot_nmapping, game_assets_pages_workspaces_dos_attack_screenshot_arp_spoofing, game_assets_pages_workspaces_dos_attack_screenshot_packets_panel, game_assets_pages_workspaces_dos_attack_screenshot_network_graph_panel [INFERRED 0.75]
- **Traffic and register observation panels** — game_assets_pages_workspaces_modbus_mitm_screenshot_packets_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_network_graph_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_status_panel, game_assets_pages_workspaces_modbus_mitm_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Hack Output Buffer-to-Console Flow** — game_readme_buffer, game_readme_metapacket, game_readme_console_tabview, game_readme_var_buffer_trails [INFERRED 0.75]
- **Recon -> ARP spoof -> tamper ModBus values -> observe HVAC effect** — game_assets_pages_workspaces_modbus_hvac_screenshot_network_actions_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_modifiers, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Network traffic observation panels** — game_assets_pages_workspaces_modbus_hvac_screenshot_packets_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_network_graph_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_status_panel [INFERRED 0.75]
- **ModBus Intro MITM observation flow** — game_assets_pages_workspaces_modbus_intro_screenshot_network_actions_panel, game_assets_pages_workspaces_modbus_intro_screenshot_packets_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_data_panel, game_assets_pages_workspaces_modbus_intro_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Recon, ARP spoof, and ModBus tamper workflow** — game_assets_pages_workspaces_modbus_submarine_screenshot_nmapping, game_assets_pages_workspaces_modbus_submarine_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_data_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_mitm_attack_flow [INFERRED 0.75]
- **Submarine state visualization panels** — game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_submarine_variables [INFERRED 0.75]
- **Recon/MITM action to traffic observation loop** — game_assets_pages_workspaces_network_recon_screenshot_arp_spoofing_form, game_assets_pages_workspaces_network_recon_screenshot_packet_sniffing_form, game_assets_pages_workspaces_network_recon_screenshot_packets_panel, game_assets_pages_workspaces_network_recon_screenshot_network_graph_panel [INFERRED 0.75]
- **ModBus process observation via registers, monitors and model** — game_assets_pages_workspaces_attacker_suite_screenshot_modbus_data_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_model_panel, game_assets_pages_workspaces_attacker_suite_screenshot_holding_registers [INFERRED 0.85]
- **ModBus process observation panels** — game_assets_pages_workspaces_dos_attack_screenshot_modbus_data_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_model_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_monitors_panel [INFERRED 0.85]
- **MITM attack workflow: WiFi connect, network mapping, ARP spoofing** — game_assets_pages_workspaces_modbus_mitm_screenshot_wifi_connection, game_assets_pages_workspaces_modbus_mitm_screenshot_nmapping, game_assets_pages_workspaces_modbus_mitm_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_mitm_screenshot_modbus_mitm_attack [INFERRED 0.85]

## Communities (167 total, 106 thin omitted)

### Community 0 - "Network Action Buttons"
Cohesion: 0.04
Nodes (22): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole, GoBackToPreviousPage (+14 more)

### Community 1 - "Packet Streams & Transactions"
Cohesion: 0.04
Nodes (6): Channel, NetworkGraph, PacketBuffer, Transaction, MetaPacket, FileStream

### Community 2 - "Overlay Framework"
Cohesion: 0.05
Nodes (10): ButtonGroup, RefreshCurrentPage, EditBackgroundStyle, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+2 more)

### Community 3 - "Footer & Version Info"
Cohesion: 0.06
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 4 - "Paths & Build Flushing"
Cohesion: 0.07
Nodes (7): flush(), flush_all(), run(), _dialog_parent(), file_dialog(), PreferencesData, Process

### Community 5 - "Layout & Config Editors"
Cohesion: 0.08
Nodes (6): remove_nested(), set_nested(), LayoutEditor, group(), add(), add()

### Community 6 - "Modbus Channels & Defender Map"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, ModbusBuffer, TransactionManager, _resolve_local_mac()

### Community 8 - "Settings Overlay Buttons"
Cohesion: 0.07
Nodes (11): ThemeWindow, checkbox(), dropdown(), row(), slider(), checked_value(), is_checked(), SettingsSection (+3 more)

### Community 9 - "Settings Page"
Cohesion: 0.07
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 10 - "Access Point Forms"
Cohesion: 0.12
Nodes (11): BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm, NFQForm (+3 more)

### Community 12 - "Panes & Packet Console"
Cohesion: 0.11
Nodes (9): StripChart, Panes, panel(), Builder, Builder, Builder, Panel, Builder (+1 more)

### Community 15 - "Important Button Base"
Cohesion: 0.06
Nodes (6): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleStripChartAutoFit

### Community 16 - "Visual Base & Backdrop"
Cohesion: 0.14
Nodes (3): blur_levels(), draw_glow(), Visual

### Community 17 - "Page Base Class"
Cohesion: 0.11
Nodes (10): AttackerV0, BoatMotion, menu_bar_buttons(), Sprites, Triangle, Visuals, WorkspacePage, NotFound (+2 more)

### Community 18 - "Distribution & ARP Scripts"
Cohesion: 0.07
Nodes (3): build_name(), main(), write_build_info()

### Community 20 - "Checkbox Overlay"
Cohesion: 0.09
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 23 - "Viewport & Geometry"
Cohesion: 0.11
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), draw_defender_map()

### Community 24 - "Find Bar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "Scrollable Frames"
Cohesion: 0.09
Nodes (4): Scrollable, Builder, Builder, Builder

### Community 26 - "Title Menu"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 28 - "Workspace Save & Popups"
Cohesion: 0.09
Nodes (8): DeleteAllUserData, DeleteAllWorkspaceSavedData, ResetSavedWorkspaceLayout, ShowHelpMessage, WorkspaceSaveResetButton, confirm_dialog(), message(), quit_dialog()

### Community 30 - "Linux WiFi Backend"
Cohesion: 0.11
Nodes (6): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 31 - "House & World Map Canvases"
Cohesion: 0.08
Nodes (8): frame_callback(), sprite(), sprite_enabled(), draw_host(), frame_callback(), frame_callback(), sprite(), sprite_enabled()

### Community 35 - "Windows WiFi Backend"
Cohesion: 0.14
Nodes (3): _list_item(), Wifi, on_notification()

### Community 37 - "Nmap & Linux NFQ"
Cohesion: 0.10
Nodes (4): NetFilterQueueBaseClass, NetFilterQueue, NMapper, job()

### Community 40 - "AP Commands"
Cohesion: 0.14
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+7 more)

### Community 41 - "Helper Server & Registry"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 43 - "Canvas Core & Diagrams"
Cohesion: 0.13
Nodes (6): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, TriangleCanvas, WorldMap

### Community 46 - "Project Docs & Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 48 - "Buffer Status Channels"
Cohesion: 0.12
Nodes (3): Buffer, StatusBuffer, MetaStatus

### Community 52 - "Slider Forms"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 53 - "Click & Callback Registry"
Cohesion: 0.13
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 55 - "Packet Filter Console"
Cohesion: 0.13
Nodes (7): _checkbox_value(), compile_packet_filter(), packet_filter(), FilterOverlay, activate(), save_filter_summary(), FilterPacketConsole

### Community 56 - "Menu Bar Settings"
Cohesion: 0.16
Nodes (9): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize() (+1 more)

### Community 63 - "App Bootstrap & Transitions"
Cohesion: 0.15
Nodes (5): App, FadeIn, covered(), uncovered(), __getattr__()

### Community 66 - "Helper Launcher"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 70 - "Palette Generator"
Cohesion: 0.22
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "Windows WiFi Helpers"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 78 - "Modbus Variable Overlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 82 - "Theme & Localization Buttons"
Cohesion: 0.12
Nodes (4): developer_text(), LoadLocalizationLabelsFile, OpenWorkspaceEditor, SelectColorTheme

### Community 83 - "Modbus MITM Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 84 - "Geometry & Camera"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 87 - "Dev Host API"
Cohesion: 0.20
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 88 - "Modbus Submarine Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 91 - "Time-Core Transforms"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 92 - "ARP/IP Screenshot"
Cohesion: 0.19
Nodes (13): AP Connection Form (AP URL, Disconnect, waiting indicator), ARP Spoofing Form (Target IP, Host IP, Start Spoofer), Encryption Form, ARP & IP Basics Workspace Screenshot, ARP Spoofing MITM Attack Workflow, Network Actions Panel (Forms, Stop All), Network Graph Panel with Packets per Second Chart, NMapping Form (Map Network) (+5 more)

### Community 93 - "Attacker Suite Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "External Link Buttons"
Cohesion: 0.18
Nodes (4): open_in_browser(), OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 99 - "Prod Host API"
Cohesion: 0.23
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 100 - "Modbus HVAC Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Recon Screenshot"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 103 - "Style Fonts"
Cohesion: 0.22
Nodes (5): s(), replace_declaration(), replace_hex(), replace_tagged(), rewrite()

### Community 107 - "Defender Suite Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 113 - "ARP Poisoner"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 114 - "Modbus Intro Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 117 - "Encryption Form"
Cohesion: 0.24
Nodes (5): encryption_enabled(), enc_button(), enc_button(), start_encryption(), stop_encryption()

### Community 128 - "Core Transforms"
Cohesion: 0.28
Nodes (4): padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 143 - "Linux WiFi Scanning"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 159 - "Smart Energy Image 2"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Smart Energy Image"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

## Knowledge Gaps
- **43 isolated node(s):** `Power Grid / Transmission Tower`, `Power Grid / Transmission Infrastructure`, `Malicious Hacking / Attacker Theme`, `Skull Hacker Image (skull.png)`, `Dev Requirements (pyright)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1294 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **106 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style Context` to `Backdrop Styling`, `Style Widgets`, `Overlay Framework`, `Paths & Build Flushing`, `Style Context Binding`, `Style Metrics`, `Style Fonts`, `Palette Generator`, `Settings Overlay Buttons`, `Style Themes`, `Context & Process Manager`, `Visual Base & Backdrop`, `Theme & Localization Buttons`, `Style Colors`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ConfigEditor` (e.g. with `LayoutEditor` and `NoteBrowser`) actually correct?**
  _`ConfigEditor` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Power Grid / Transmission Tower`, `Power Grid / Transmission Infrastructure`, `Malicious Hacking / Attacker Theme` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Network Action Buttons` be split into smaller, more focused modules?**
  _Cohesion score 0.037606837606837605 - nodes in this community are weakly interconnected._
- **Why does `Overlay` connect `Overlay Framework` to `Panes & Packet Console`, `Menu Bar & Boat Demo`, `Modbus Variable Overlay`, `Transition Timing`, `Page Base Class`, `Checkbox Overlay`, `Packet Filter Console`, `Button Group`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Overlay` (e.g. with `ButtonGroup` and `CheckboxOverlay`) actually correct?**
  _`Overlay` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `Packet Streams & Transactions` be split into smaller, more focused modules?**
  _Cohesion score 0.04202174551866 - nodes in this community are weakly interconnected._