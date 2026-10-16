# Graph Report - cybersecurity-game  (2026-10-16)

## Corpus Check
- 303 files · ~243,264 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 3952 nodes · 8334 edges · 206 communities (65 shown, 141 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 466 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7ec92f59`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- important_buttons/__init__.py
- MetaPacket
- BaseForm
- Footer
- channels/__init__.py
- SettingsSection
- PauseMenu
- VisualBackground
- MapBuffer
- SettingsPage
- ._build_stylesheet
- PageManager
- .setText
- DefenderV0
- ToggleButton
- VisualPalette
- FilterOverlay
- .fill_base
- CheckboxOverlay
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- DefenderModbusBuffer
- FindBar
- Canvas
- SessionRecorder
- hvac_view.py
- PacketTreeview
- Wifi
- .__init__
- LayoutEditor
- Performance
- HVACView
- Wifi
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- APPoller
- os
- LocalizationManager
- QWidget
- .__init__
- NetFilterQueue
- Runtime Requirements
- examples.py
- StatusBuffer
- PopupEntrance
- ConfigEditor
- Kernel
- SlidersForm
- AnimationManager
- InputManager
- .minimize_button
- VectorField
- Json
- KeyBinds
- WifiBaseClass
- Modify
- ask_to_quit
- Router
- time
- DefenderStatusBuffer
- Replay
- StripChartBase
- Dev/Host_API.py
- palette_generator.py
- wifi_windows.py
- app.py
- PrivilegedHelper
- Constellation
- Preferences
- ThemeEditorPage
- Draw
- VariableOverlay
- .leaf
- WorkspaceSaveResetButton
- WaveGrid
- ModBus MITM Workspace Screenshot
- ProcessManager
- SettingCell
- .add_setting_row
- .__init__
- ModBus Submarine Exercise Screenshot
- FadeOut
- NewWorkspaceDialog
- .strip_chart_layout
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- sys
- MitmTable
- _Dim
- ModBus HVAC Exercise Screenshot
- Network Actions Panel
- .__init__
- Map
- Visuals
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- GrowingButton
- Camera
- .__init__
- WindowEdges
- .key_column_width
- ModBus Basics Workspace Screenshot
- MainWindow
- CornerControls
- .new_tab
- version.py
- .slider
- WindowDrag
- Denier
- Master
- Style
- AppearEffect
- transformations.py
- Slave
- PacketBuffer
- NMapper
- .__init__
- padded_fit_uniform
- .restyle
- .collect
- host.py
- .build_description_tab
- themes.py
- PooledCanvasMixin
- geometry.py
- .__init__
- ap_commands.py
- ._scan_for_networks
- window_chrome.py
- confirm_dialog
- _OnHide
- panel
- pathlib
- Kalman
- StreamIncomingPacketsToMcap
- Overlay
- .build_tabs
- Visual
- Proximity
- record_schema.py
- Telemetry
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ContextManager
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- PreferencesData
- MenuBar
- RecordFilter
- WindowControls
- CLAUDE.md
- dumps
- SelectRegisterPreset
- .arrow
- ArpSpoofer
- OpenFavoritePage
- ToggleDebugLabels
- SampleSubmarine
- _DrawerLayout
- FreeScrollStatusConsole
- PausePacketConsole
- RefreshAndCloseOverlay
- ToggleBookmark
- frame_callback
- ToggleLightDarkMode
- ToggleStripChartAutoFit
- SampleNetwork
- DenseMesh

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 132 edges
2. `ImportantButton` - 108 edges
3. `Style` - 99 edges
4. `Overlay` - 76 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 61 edges
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

## Communities (206 total, 141 thin omitted)

### Community 0 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (39): AbortAllNetworkActions, ImportantButton, open_in_browser(), ButtonGroup, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole (+31 more)

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "BaseForm"
Cohesion: 0.15
Nodes (13): BaseForm, ModeForm, RegistersExample, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm (+5 more)

### Community 3 - "Footer"
Cohesion: 0.08
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 4 - "channels/__init__.py"
Cohesion: 0.09
Nodes (3): HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 5 - "SettingsSection"
Cohesion: 0.12
Nodes (5): checked_value(), SettingsSection, save(), save(), on_change()

### Community 10 - "._build_stylesheet"
Cohesion: 0.09
Nodes (3): at_opacity(), shaded(), gradient_points()

### Community 16 - "VisualPalette"
Cohesion: 0.17
Nodes (3): draw_vessel(), draw_glow(), VisualPalette

### Community 17 - "FilterOverlay"
Cohesion: 0.14
Nodes (6): _checkbox_value(), packet_filter(), FilterOverlay, activate(), save_filter_summary(), FilterPacketConsole

### Community 20 - "CheckboxOverlay"
Cohesion: 0.14
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "Canvas"
Cohesion: 0.16
Nodes (3): Canvas, DefenderWorldMap, WorldMap

### Community 30 - "Wifi"
Cohesion: 0.11
Nodes (6): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 31 - ".__init__"
Cohesion: 0.09
Nodes (5): frame_callback(), sprite(), sprite_enabled(), draw_host(), frame_callback()

### Community 32 - "LayoutEditor"
Cohesion: 0.11
Nodes (3): LayoutEditor, add(), add()

### Community 35 - "Wifi"
Cohesion: 0.11
Nodes (6): _list_item(), Wifi, finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.05
Nodes (8): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update(), paint_panel(), surface_shadow()

### Community 41 - "os"
Cohesion: 0.05
Nodes (14): flush(), flush_all(), run(), Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub (+6 more)

### Community 43 - "QWidget"
Cohesion: 0.15
Nodes (3): ControlsExample, StatusExample, TabsExample

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "examples.py"
Cohesion: 0.11
Nodes (11): House, NetworkDiagramCanvas, HouseExample, MapExample, NetworkExample, PassWheel, SampleHouse, SampleHVAC (+3 more)

### Community 52 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 53 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 55 - ".minimize_button"
Cohesion: 0.17
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 64 - "time"
Cohesion: 0.06
Nodes (6): random_spline_path(), Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 69 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 72 - "app.py"
Cohesion: 0.15
Nodes (5): App, FadeIn, covered(), uncovered(), __getattr__()

### Community 78 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "WorkspaceSaveResetButton"
Cohesion: 0.23
Nodes (3): ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

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

### Community 96 - "sys"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 98 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Actions Panel"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - ".__init__"
Cohesion: 0.04
Nodes (5): Builder, FlagsExample, Builder, Builder, Builder

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 120 - "WindowDrag"
Cohesion: 0.15
Nodes (3): SquareButtons, toggle_maximized(), WindowDrag

### Community 122 - "Denier"
Cohesion: 0.10
Nodes (4): Denier, Attack, PreAttack, toggle_IP_Forward

### Community 126 - "transformations.py"
Cohesion: 0.15
Nodes (7): canvas_fit(), padded_fit(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 129 - "NMapper"
Cohesion: 0.14
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 131 - ".__init__"
Cohesion: 0.11
Nodes (4): _FollowResize, global_buttons(), _pane_is_minimized(), _RightZoneRoom

### Community 132 - "padded_fit_uniform"
Cohesion: 0.14
Nodes (3): padded_fit_uniform(), zoom_and_pan(), draw_defender_map()

### Community 134 - ".collect"
Cohesion: 0.17
Nodes (3): remove_nested(), set_nested(), group()

### Community 137 - "themes.py"
Cohesion: 0.14
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 141 - "ap_commands.py"
Cohesion: 0.10
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+9 more)

### Community 143 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 144 - "window_chrome.py"
Cohesion: 0.18
Nodes (5): draw_window_bar_line(), _Strip, window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 145 - "confirm_dialog"
Cohesion: 0.08
Nodes (4): make(), confirm_dialog(), message(), PopupWindow

### Community 152 - "Overlay"
Cohesion: 0.09
Nodes (8): SelectColorTheme, EditBackgroundStyle, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, is_checked(), SettingsOverlayButton, Overlay

### Community 156 - "record_schema.py"
Cohesion: 0.19
Nodes (8): action(), decode(), mark(), packet(), packet_from_meta(), poll(), raw_bytes(), status()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "ContextManager"
Cohesion: 0.10
Nodes (11): ContextManager, StripChart, developer_text(), compile_packet_filter(), Scrollable, Builder, ChartsExample, Builder (+3 more)

### Community 168 - "MenuBar"
Cohesion: 0.04
Nodes (14): ViewPort, AttackerV0, BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound (+6 more)

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **43 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `ARP Spoofing Form` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1542 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **141 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `BaseForm`, `channels/__init__.py`, `host.py`, `PageManager`, `window_chrome.py`, `VisualPalette`, `CheckboxOverlay`, `Overlay`, `Canvas`, `hvac_view.py`, `Performance`, `MenuBar`, `LocalizationManager`, `examples.py`, `AnimationManager`, `InputManager`, `Json`, `KeyBinds`, `Router`, `time`, `PrivilegedHelper`, `Preferences`, `WorkspaceSaveResetButton`, `ProcessManager`, `Style`?**
  _High betweenness centrality (0.260) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.025755717480701247 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `important_buttons/__init__.py`, `ContextManager`, `QWidget`, `.restyle`, `SettingsSection`, `._build_stylesheet`, `.theme_family`, `.link_color`, `.discard_changes`, `Overlay`, `.setting`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0783673469387755 - nodes in this community are weakly interconnected._