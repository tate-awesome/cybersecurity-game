# Graph Report - cybersecurity-game  (2026-10-14)

## Corpus Check
- 301 files · ~238,850 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 3833 nodes · 8067 edges · 178 communities (68 shown, 110 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 458 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fb78253d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- important_buttons/__init__.py
- MetaPacket
- Builder
- Footer
- LayoutEditor
- SettingsSection
- PauseMenu
- VisualBackground
- buffer_manager.py
- .new_tab
- ._build_stylesheet
- PageManager
- SettingsPage
- DefenderV0
- ToggleButton
- pyside6_qtcore
- Overlay
- ThemeEditorPage
- CheckboxOverlay
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- DefenderModbusBuffer
- FindBar
- Canvas
- Page
- VectorField
- PacketTreeview
- Wifi
- .__init__
- NetFilterQueue
- Performance
- HVACView
- Wifi
- Draw
- widgets/__init__.py
- WorkspaceSelectPage
- Camera
- APPoller
- os
- LocalizationManager
- ContextManager
- WaveGrid
- GrowingButton
- Runtime Requirements
- examples.py
- StatusBuffer
- Dev/Host_API.py
- ConfigEditor
- VisualPalette
- SlidersForm
- time
- InputManager
- .minimize_button
- MapBuffer
- Json
- KeyBinds
- WifiBaseClass
- Modify
- WorkspaceSaveResetButton
- Router
- threading
- DefenderStatusBuffer
- Replay
- StripChartBase
- Prod/Host_API.py
- palette_generator.py
- wifi_windows.py
- App
- PrivilegedHelper
- Constellation
- Preferences
- _PollUnpacker
- Draw
- VariableOverlay
- .__init__
- .leaf
- .build_preview
- Proximity
- ModBus MITM Workspace Screenshot
- ProcessManager
- .add_setting_row
- Rows
- .__init__
- ModBus Submarine Exercise Screenshot
- app.py
- NewWorkspaceDialog
- .strip_chart_layout
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- sys
- MitmTable
- _Dim
- Style
- ModBus HVAC Exercise Screenshot
- Network Actions Panel
- .__init__
- _MapCanvas
- .new_tab
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- defender.py
- Camera
- packet_console/_builder.py
- WindowEdges
- Attack
- ModBus Basics Workspace Screenshot
- MainWindow
- ArpSpoofer
- .entry
- Map
- SettingsSection
- window_chrome.py
- .slider
- Denier
- Master
- AppearEffect
- Slave
- Buffer
- NMapper
- menu_bar.py
- router.py
- .restyle
- .collect
- _Proxy
- .build_description_tab
- style.py
- PooledCanvasMixin
- affine
- .__init__
- ap_commands.py
- LinkToPage
- ._scan_for_networks
- paths.py
- popup.py
- .all_ids
- NotFound
- .arrow
- Kalman
- _DrawerLayout
- Telemetry
- .build_tabs
- DenseMesh
- on_notification
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- PreferencesData
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- map.py
- MenuBar
- CLAUDE.md
- frame_callback
- scrollable.py
- .__init__
- SampleSubmarine
- Visualizer.py
- frame_callback

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 131 edges
2. `ImportantButton` - 109 edges
3. `Style` - 99 edges
4. `Overlay` - 68 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 60 edges
7. `MetaPacket` - 59 edges
8. `BaseForm` - 55 edges
9. `VisualPalette` - 48 edges
10. `Panel` - 47 edges

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

## Communities (178 total, 110 thin omitted)

### Community 0 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (29): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, ImportThemes (+21 more)

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "Builder"
Cohesion: 0.14
Nodes (3): Builder, Builder, Builder

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (8): BuildInfo, _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.07
Nodes (3): paint_aurora(), pyramid_blur(), VisualBackground

### Community 8 - "buffer_manager.py"
Cohesion: 0.09
Nodes (3): HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, SetCurrentPageAsFavorite, ToggleBookmark, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleStripChartAutoFit

### Community 16 - "pyside6_qtcore"
Cohesion: 0.12
Nodes (4): nice_number(), nice_ticks(), developer_text(), Visual

### Community 17 - "Overlay"
Cohesion: 0.05
Nodes (10): RefreshCurrentPage, SelectColorTheme, EditBackgroundStyle, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+2 more)

### Community 20 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "Canvas"
Cohesion: 0.13
Nodes (5): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, TriangleCanvas

### Community 26 - "Page"
Cohesion: 0.15
Nodes (3): Visuals, WorkspacePage, Page

### Community 30 - "Wifi"
Cohesion: 0.11
Nodes (6): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 35 - "Wifi"
Cohesion: 0.14
Nodes (3): _list_item(), Wifi, on_notification()

### Community 37 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (9): StripChart, Panes, panel(), Builder, Builder, Builder, Panel, Builder (+1 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.05
Nodes (8): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update(), paint_panel(), surface_shadow()

### Community 40 - "APPoller"
Cohesion: 0.08
Nodes (3): APPoller, Sniffer, Loader

### Community 41 - "os"
Cohesion: 0.07
Nodes (13): flush(), flush_all(), run(), build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch() (+5 more)

### Community 43 - "ContextManager"
Cohesion: 0.11
Nodes (12): ContextManager, BaseForm, ModeForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+4 more)

### Community 45 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "examples.py"
Cohesion: 0.04
Nodes (19): WorldMap, Scrollable, ChartsExample, ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample (+11 more)

### Community 49 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 50 - "ConfigEditor"
Cohesion: 0.11
Nodes (3): ConfigEditor, walk(), discard()

### Community 51 - "VisualPalette"
Cohesion: 0.09
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 52 - "SlidersForm"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 53 - "time"
Cohesion: 0.05
Nodes (5): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter, random_spline_path()

### Community 55 - ".minimize_button"
Cohesion: 0.17
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 62 - "WorkspaceSaveResetButton"
Cohesion: 0.21
Nodes (3): ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 64 - "threading"
Cohesion: 0.08
Nodes (3): NetFilterQueueBaseClass, Process, FileStream

### Community 69 - "Prod/Host_API.py"
Cohesion: 0.15
Nodes (12): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status(), encryption_enabled() (+4 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.16
Nodes (4): EditModbusRegisterDisplay, VariableOverlay, autosave(), reset_all()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.11
Nodes (6): DesktopFade, FadeIn, covered(), uncovered(), FadeOut, WindowReveal

### Community 91 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 92 - "Network Actions Panel (Forms, Stop All)"
Cohesion: 0.19
Nodes (13): AP Connection Form (AP URL, Disconnect, waiting indicator), ARP Spoofing Form (Target IP, Host IP, Start Spoofer), Encryption Form, ARP & IP Basics Workspace Screenshot, ARP Spoofing MITM Attack Workflow, Network Actions Panel (Forms, Stop All), Network Graph Panel with Packets per Second Chart, NMapping Form (Map Network) (+5 more)

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 95 - "QWidget"
Cohesion: 0.13
Nodes (3): PageTransition, PopupEntrance, SnapshotOverlay

### Community 96 - "sys"
Cohesion: 0.07
Nodes (11): build_name(), main(), write_build_info(), git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux() (+3 more)

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Actions Panel"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "defender.py"
Cohesion: 0.12
Nodes (3): DefenderHVACChart, follow_theme(), ShiftWheelSlider

### Community 111 - "packet_console/_builder.py"
Cohesion: 0.13
Nodes (7): _checkbox_value(), compile_packet_filter(), packet_filter(), FilterOverlay, activate(), save_filter_summary(), FilterPacketConsole

### Community 113 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 120 - "window_chrome.py"
Cohesion: 0.07
Nodes (11): CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_button_height(), window_bar_has_line(), window_bar_height() (+3 more)

### Community 128 - "Buffer"
Cohesion: 0.06
Nodes (4): Buffer, DefenderMapBuffer, NetworkGraph, PacketBuffer

### Community 129 - "NMapper"
Cohesion: 0.14
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 131 - "menu_bar.py"
Cohesion: 0.05
Nodes (9): ButtonGroup, ConfigureThisWorkspace, GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, _FollowResize, global_buttons(), _pane_is_minimized() (+1 more)

### Community 132 - "router.py"
Cohesion: 0.11
Nodes (6): padded_fit_uniform(), zoom_and_pan(), ViewPort, draw_defender_map(), BoatMotion, Sprites

### Community 137 - "style.py"
Cohesion: 0.14
Nodes (10): button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+2 more)

### Community 139 - "affine"
Cohesion: 0.33
Nodes (3): canvas_fit(), padded_fit(), affine()

### Community 141 - "ap_commands.py"
Cohesion: 0.14
Nodes (13): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+5 more)

### Community 143 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 145 - "popup.py"
Cohesion: 0.06
Nodes (9): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ResetCurrentPageToDefaults, ShowHelpMessage, confirm_dialog(), message(), PopupWindow (+1 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 169 - "map.py"
Cohesion: 0.09
Nodes (10): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate(), padded_fit_uniform(), padded_fit_uniform_reverse() (+2 more)

### Community 173 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **43 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `ARP Spoofing Form` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1500 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **110 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `menu_bar.py`, `router.py`, `buffer_manager.py`, `style.py`, `PageManager`, `pyside6_qtcore`, `Overlay`, `popup.py`, `CheckboxOverlay`, `Canvas`, `Performance`, `widgets/__init__.py`, `os`, `LocalizationManager`, `map.py`, `scrollable.py`, `examples.py`, `time`, `InputManager`, `Json`, `KeyBinds`, `WorkspaceSaveResetButton`, `Router`, `threading`, `PrivilegedHelper`, `Preferences`, `ProcessManager`, `Style`, `defender.py`, `packet_console/_builder.py`, `window_chrome.py`, `.start_session`?**
  _High betweenness centrality (0.258) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.027821855495609858 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `important_buttons/__init__.py`, `menu_bar.py`, `.restyle`, `SettingsSection`, `style.py`, `._build_stylesheet`, `ContextManager`, `.set_theme`, `.theme_family`, `Overlay`, `.discard_changes`, `.link_color`, `.start_session`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.06883116883116883 - nodes in this community are weakly interconnected._