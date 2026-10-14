# Graph Report - cybersecurity-game  (2026-10-14)

## Corpus Check
- 311 files · ~231,160 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 3668 nodes · 7710 edges · 191 communities (69 shown, 122 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 450 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a5f74ae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- important_buttons/__init__.py
- MetaPacket
- SettingsOverlayButton
- Footer
- SettingsSection
- LayoutEditor
- PauseMenu
- VisualBackground
- ModbusBuffer
- MapBuffer
- pyside6_qtwidgets
- PageManager
- MenuBar
- DefenderV0
- ToggleButton
- Visual
- Overlay
- SettingsPage
- CheckboxOverlay
- NetworkMesh
- ViewPort
- FindBar
- TransactionManager
- WorkspaceSaveResetButton
- PacketTreeview
- Wifi
- .__init__
- Style
- Performance
- HVACView
- Wifi
- Draw
- ContextManager
- WorkspaceSelectPage
- Camera
- APPoller
- server.py
- LocalizationManager
- .__init__
- GrowingButton
- Runtime Requirements
- os
- StatusBuffer
- Loader
- ConfigEditor
- VisualPalette
- SlidersForm
- AnimationManager
- InputManager
- .populate_filter_overlay
- NetFilterQueue
- Json
- KeyBinds
- WifiBaseClass
- Modify
- VectorField
- app.py
- threading
- DefenderStatusBuffer
- sys
- Replay
- StripChartBase
- Map
- palette_generator.py
- wifi_windows.py
- Router
- PrivilegedHelper
- Constellation
- Preferences
- DefenderHVACChart
- Draw
- VariableOverlay
- NMapper
- .leaf
- WaveGrid
- ModBus MITM Workspace Screenshot
- Proximity
- .add_setting_row
- Rows
- Dev/Host_API.py
- ModBus Submarine Exercise Screenshot
- FadeIn
- NewWorkspaceDialog
- .strip_chart_layout
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- launch.py
- MitmTable
- PacketBuffer
- ModBus HVAC Exercise Screenshot
- Network Actions Panel
- .collect
- ._build_stylesheet
- .new_tab
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- QWidget
- Camera
- WindowEdges
- arp_poisoner.py
- ModBus Basics Workspace Screenshot
- MainWindow
- .__init__
- .build_tabs
- CornerControls
- ArpSpoofer
- Denier
- Master
- ap_tunnel_enabled
- AppearEffect
- buffer_manager.py
- Slave
- developer_text
- NetFilterQueue
- DefenderModbusBuffer
- geometry.py
- .apply_theme
- edit_workspace_availability.py
- host.py
- .build_description_tab
- context_manager.py
- PooledCanvasMixin
- panel
- .__init__
- submarine_mode
- .__init__
- ._scan_for_networks
- .__init__
- confirm_dialog
- .__init__
- .__init__
- Telemetry
- Kalman
- CreateToolTip
- SampleSubmarine
- CreateToolTip
- core/transforms.py
- Paths
- Builder
- .add_deadspace
- ToggleBookmark
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Scrollable
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- frame_callback
- frame_callback
- SampleNetwork
- .add_header
- file_dialog
- CLAUDE.md
- BuildInfo
- Sniffer
- .arrow
- DenseMesh
- OpenFavoritePage
- router.py
- SelectColorTheme
- SelectRegisterPreset
- configure_this_workspace.py
- Channel
- pyside6_qtcore
- WorkspaceButton

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 131 edges
2. `ImportantButton` - 105 edges
3. `Style` - 74 edges
4. `Overlay` - 67 edges
5. `ConfigEditor` - 65 edges
6. `MetaPacket` - 59 edges
7. `MenuBar` - 59 edges
8. `BaseForm` - 55 edges
9. `VisualPalette` - 48 edges
10. `Panel` - 41 edges

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

## Communities (191 total, 122 thin omitted)

### Community 0 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (28): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, ImportThemes (+20 more)

### Community 1 - "MetaPacket"
Cohesion: 0.09
Nodes (3): Transaction, MetaPacket, FileStream

### Community 2 - "SettingsOverlayButton"
Cohesion: 0.13
Nodes (4): EditBackgroundStyle, EditModelStyle, EditStripChartStyle, SettingsOverlayButton

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 4 - "SettingsSection"
Cohesion: 0.06
Nodes (15): checked_value(), is_checked(), SettingsSection, save(), save(), on_change(), _drain_evenly(), click_maximize() (+7 more)

### Community 5 - "LayoutEditor"
Cohesion: 0.09
Nodes (4): LayoutEditor, group(), add(), add()

### Community 6 - "PauseMenu"
Cohesion: 0.10
Nodes (3): _Dim, _FollowResize, PauseMenu

### Community 10 - "pyside6_qtwidgets"
Cohesion: 0.12
Nodes (11): ShiftWheelSlider, BaseForm, ModeForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm (+3 more)

### Community 14 - "DefenderV0"
Cohesion: 0.11
Nodes (3): submarine_kalman_enabled(), DefenderV0, slider_callback()

### Community 15 - "ToggleButton"
Cohesion: 0.06
Nodes (6): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleStripChartAutoFit

### Community 19 - "SettingsPage"
Cohesion: 0.05
Nodes (3): SettingsPage, save(), ThemeEditorPage

### Community 20 - "CheckboxOverlay"
Cohesion: 0.14
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 23 - "ViewPort"
Cohesion: 0.10
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), draw_defender_map()

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 30 - "Wifi"
Cohesion: 0.11
Nodes (6): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 34 - "HVACView"
Cohesion: 0.18
Nodes (3): hvac_kalman_enabled(), HVACView, slider_callback()

### Community 35 - "Wifi"
Cohesion: 0.11
Nodes (6): _list_item(), Wifi, finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 37 - "ContextManager"
Cohesion: 0.06
Nodes (22): ContextManager, Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, WorldMap (+14 more)

### Community 40 - "APPoller"
Cohesion: 0.18
Nodes (5): _hvac_send(), push_hvac_settings(), read_hvac_state(), set_hvac_kalman(), APPoller

### Community 41 - "server.py"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 43 - ".__init__"
Cohesion: 0.11
Nodes (7): PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SamplePackets, SampleWorldMap, is_on()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "os"
Cohesion: 0.10
Nodes (3): flush(), flush_all(), run()

### Community 50 - "ConfigEditor"
Cohesion: 0.11
Nodes (3): ConfigEditor, walk(), discard()

### Community 51 - "VisualPalette"
Cohesion: 0.11
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 52 - "SlidersForm"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 53 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 55 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 63 - "app.py"
Cohesion: 0.19
Nodes (3): App, WindowReveal, __getattr__()

### Community 64 - "threading"
Cohesion: 0.07
Nodes (4): random_spline_path(), Buffer, ProcessManager, Process

### Community 66 - "sys"
Cohesion: 0.22
Nodes (3): build_name(), main(), write_build_info()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "NMapper"
Cohesion: 0.20
Nodes (3): NMapper, InterfaceManager, job()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 87 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (5): DesktopFade, FadeIn, covered(), uncovered(), FadeOut

### Community 91 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 92 - "Network Actions Panel (Forms, Stop All)"
Cohesion: 0.19
Nodes (13): AP Connection Form (AP URL, Disconnect, waiting indicator), ARP Spoofing Form (Target IP, Host IP, Start Spoofer), Encryption Form, ARP & IP Basics Workspace Screenshot, ARP Spoofing MITM Attack Workflow, Network Actions Panel (Forms, Stop All), Network Graph Panel with Packets per Second Chart, NMapping Form (Map Network) (+5 more)

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Actions Panel"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 113 - "arp_poisoner.py"
Cohesion: 0.15
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 117 - ".__init__"
Cohesion: 0.22
Nodes (7): encryption_enabled(), set_encryption(), enc_button(), enc_button(), EncryptionForm, start_encryption(), stop_encryption()

### Community 124 - "ap_tunnel_enabled"
Cohesion: 0.47
Nodes (3): ap_tunnel_enabled(), ap_tunnel_key(), set_ap_tunnel()

### Community 128 - "developer_text"
Cohesion: 0.11
Nodes (4): on_change(), SettingsSection, preview(), developer_text()

### Community 132 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 134 - "edit_workspace_availability.py"
Cohesion: 0.25
Nodes (3): RefreshCurrentPage, EditWorkspaceAvailability, RefreshAndCloseOverlay

### Community 136 - ".build_description_tab"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 137 - "context_manager.py"
Cohesion: 0.12
Nodes (6): PreferencesData, is_hex(), _old_palette(), read_theme(), resolve_materials(), theme_file()

### Community 141 - "submarine_mode"
Cohesion: 0.21
Nodes (5): kalman_enabled(), set_kalman(), set_submarine_kalman(), submarine_mode(), Builder

### Community 142 - ".__init__"
Cohesion: 0.07
Nodes (4): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, _FollowResize

### Community 143 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 144 - ".__init__"
Cohesion: 0.07
Nodes (5): ButtonGroup, EditModbusRegisterDisplay, FilterOverlay, FilterPacketConsole, LinkToPage

### Community 145 - "confirm_dialog"
Cohesion: 0.08
Nodes (8): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ResetCurrentPageToDefaults, ShowHelpMessage, confirm_dialog(), message(), quit_dialog()

### Community 154 - "core/transforms.py"
Cohesion: 0.28
Nodes (4): padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 167 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 168 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 179 - "router.py"
Cohesion: 0.09
Nodes (10): AttackerV0, BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound (+2 more)

### Community 186 - "pyside6_qtcore"
Cohesion: 0.12
Nodes (5): apply_scale_about(), menu_bar_buttons(), compile_packet_filter(), group_button_names(), WindowDrag

## Knowledge Gaps
- **43 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `ARP Spoofing Form` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1418 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **122 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `.apply_theme`, `host.py`, `context_manager.py`, `pyside6_qtwidgets`, `PageManager`, `.__init__`, `.__init__`, `Visual`, `CheckboxOverlay`, `Paths`, `WorkspaceSaveResetButton`, `Style`, `Performance`, `LocalizationManager`, `OpenFavoritePage`, `router.py`, `AnimationManager`, `InputManager`, `configure_this_workspace.py`, `Json`, `KeyBinds`, `pyside6_qtcore`, `threading`, `Router`, `PrivilegedHelper`, `Preferences`, `.start_session`, `buffer_manager.py`?**
  _High betweenness centrality (0.253) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.036036036036036036 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `NewWorkspaceDialog`, `.collect`, `LayoutEditor`, `.build_description_tab`, `.new_tab`, `WorkspaceSelectPage`, `.leaf`, `router.py`, `.add_setting_row`, `Rows`, `.build_tabs`, `FindBar`, `configure_this_workspace.py`, `pyside6_qtcore`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.08773784355179703 - nodes in this community are weakly interconnected._