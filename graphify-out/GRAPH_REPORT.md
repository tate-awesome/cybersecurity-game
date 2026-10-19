# Graph Report - cybersecurity-game  (2026-10-19)

## Corpus Check
- 305 files · ~244,733 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4002 nodes · 8135 edges · 199 communities (69 shown, 130 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 465 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4206a50b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- important_buttons/__init__.py
- MetaPacket
- ContextManager
- Footer
- surface_shadow
- SettingsSection
- PauseMenu
- VisualBackground
- flusher.py
- SettingsPage
- ._build_stylesheet
- PageManager
- ImportantButton
- ProcessManager
- ToggleButton
- Visual
- .populate_filter_overlay
- time
- Attack
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- buffer_manager.py
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- pyside6_qtwidgets
- PacketTreeview
- Wifi
- .__init__
- LayoutEditor
- Performance
- HVACView
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- server.py
- LocalizationManager
- examples.py
- Panel
- DefenderV0
- Runtime Requirements
- ThemeEditorPage
- StatusBuffer
- sys
- ConfigEditor
- ModbusBuffer
- SlidersForm
- .load_page_config
- InputManager
- DefenderHVACChart
- VectorField
- Json
- KeyBinds
- NativeFrame
- BaseForm
- Modify
- time_core/transforms.py
- Router
- hardware/__init__.py
- DefenderStatusBuffer
- Replay
- StripChartBase
- CornerControls
- palette_generator.py
- QWidget
- App
- PrivilegedHelper
- Constellation
- Preferences
- PopupWindow
- Draw
- VariableOverlay
- _base_button.py
- .leaf
- confirm_dialog
- WaveGrid
- ModBus MITM Workspace Screenshot
- .add_setting_row
- Rows
- WorkspaceSaveResetButton
- ModBus Submarine Exercise Screenshot
- FadeIn
- NewWorkspaceDialog
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- launch.py
- MitmTable
- _Dim
- .material_control
- ModBus HVAC Exercise Screenshot
- Network Actions Panel
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- StripChartLayout
- Camera
- .columnconfigure
- WindowEdges
- .brush
- ModBus Basics Workspace Screenshot
- MainWindow
- WindowDrag
- .new_tab
- .__init__
- ConfigureThisWorkspace
- WindowControls
- Proximity
- Denier
- Master
- Style
- AppearEffect
- FilterOverlay
- Slave
- NMapper
- menu_bar.py
- .restyle
- .collect
- host.py
- .build_description_tab
- themes.py
- PooledCanvasMixin
- geometry.py
- .__init__
- ap_commands.py
- StreamIncomingPacketsToMcap
- LinkToPage
- .play
- Telemetry
- Overlay
- .build_tabs
- .__init__
- GoBackToPreviousPage
- AnimationManager
- GrowingButton
- paint_panel
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ClickManager
- StripChart
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- CallbackRegistry
- MenuBar
- NetFilterQueue
- RecordFilter
- CLAUDE.md
- DenseMesh
- style.py
- PopupEntrance
- ArpSpoofer
- version.py
- ToggleBookmark
- open_favorite_page.py
- .__init__
- ToggleLightDarkMode
- APPoller
- ToggleFreezeBackground
- SampleSubmarine
- .__init__
- _OnHide
- GoForwardToNextPage
- ModeForm

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 132 edges
2. `ImportantButton` - 104 edges
3. `Style` - 100 edges
4. `Overlay` - 80 edges
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

## Communities (199 total, 130 thin omitted)

### Community 0 - "important_buttons/__init__.py"
Cohesion: 0.06
Nodes (11): AbortAllNetworkActions, EditModbusRegisterDisplay, LoadLocalizationLabelsFile, LoadPcapIntoPacketBuffer, LoadSettingsPresetFile, OpenSettingsPage, OpenTitlePage, OpenWorkspaceEditor (+3 more)

### Community 1 - "MetaPacket"
Cohesion: 0.05
Nodes (6): Channel, NetworkGraph, PacketBuffer, Transaction, TransactionManager, MetaPacket

### Community 2 - "ContextManager"
Cohesion: 0.09
Nodes (14): ContextManager, AttackerV0, BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage (+6 more)

### Community 3 - "Footer"
Cohesion: 0.08
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 4 - "surface_shadow"
Cohesion: 0.12
Nodes (3): surface_shadow(), paint_aurora(), pyramid_blur()

### Community 5 - "SettingsSection"
Cohesion: 0.05
Nodes (15): checked_value(), is_checked(), SettingsSection, save(), save(), on_change(), _drain_evenly(), click_maximize() (+7 more)

### Community 8 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 9 - "SettingsPage"
Cohesion: 0.06
Nodes (3): SettingsPage, save(), SettingsSection

### Community 12 - "ImportantButton"
Cohesion: 0.06
Nodes (8): ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, LoadMcapIntoPacketBuffer, OpenPauseMenu, SaveCurrentPacketBufferToMcap

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleDebugLabels, ToggleFullscreen, ToggleStripChartAutoFit, ToggleTranslucentSurfaces

### Community 16 - "Visual"
Cohesion: 0.08
Nodes (3): draw_vessel(), random_spline_path(), Visual

### Community 17 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 19 - "time"
Cohesion: 0.14
Nodes (10): action(), dumps(), header(), mark(), packet(), packet_from_meta(), poll(), raw_bytes() (+2 more)

### Community 20 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 23 - "buffer_manager.py"
Cohesion: 0.06
Nodes (3): DefenderMapBuffer, DefenderModbusBuffer, _resolve_local_mac()

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "VisualPalette"
Cohesion: 0.09
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 26 - "CheckboxOverlay"
Cohesion: 0.11
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 28 - "pyside6_qtwidgets"
Cohesion: 0.10
Nodes (3): apply_scale_about(), follow_theme(), ShiftWheelSlider

### Community 30 - "Wifi"
Cohesion: 0.05
Nodes (12): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish() (+4 more)

### Community 31 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 32 - "LayoutEditor"
Cohesion: 0.08
Nodes (5): LayoutEditor, group(), add(), add(), on_change()

### Community 34 - "HVACView"
Cohesion: 0.12
Nodes (3): HVACView, enc_button(), slider_callback()

### Community 35 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (6): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update()

### Community 41 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 43 - "examples.py"
Cohesion: 0.05
Nodes (19): Canvas, DefenderWorldMap, House, WorldMap, ControlsExample, FlagsExample, HouseExample, MapExample (+11 more)

### Community 44 - "Panel"
Cohesion: 0.06
Nodes (6): compile_packet_filter(), panel(), Builder, _DrawerLayout, Panel, Builder

### Community 45 - "DefenderV0"
Cohesion: 0.05
Nodes (5): ViewPort, DefenderV0, enc_button(), slider_callback(), draw_defender_map()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "sys"
Cohesion: 0.20
Nodes (4): build_name(), main(), write_build_info(), decode()

### Community 50 - "ConfigEditor"
Cohesion: 0.11
Nodes (3): ConfigEditor, walk(), discard()

### Community 51 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 57 - "Json"
Cohesion: 0.07
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 60 - "BaseForm"
Cohesion: 0.04
Nodes (11): BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm, NFQForm (+3 more)

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "hardware/__init__.py"
Cohesion: 0.05
Nodes (4): Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 65 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.18
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "_base_button.py"
Cohesion: 0.11
Nodes (6): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "confirm_dialog"
Cohesion: 0.09
Nodes (6): DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog()

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 87 - "WorkspaceSaveResetButton"
Cohesion: 0.21
Nodes (3): ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

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

### Community 111 - ".columnconfigure"
Cohesion: 0.07
Nodes (4): Builder, Builder, Builder, Builder

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 118 - ".__init__"
Cohesion: 0.07
Nodes (6): RefreshCurrentPage, ShowHelpMessage, _FollowResize, global_buttons(), icon_button(), _RightZoneRoom

### Community 129 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 131 - "menu_bar.py"
Cohesion: 0.11
Nodes (8): developer_text(), ButtonGroup, offered_sections(), draw_window_bar_line(), toggle_maximized(), window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 137 - "themes.py"
Cohesion: 0.14
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "geometry.py"
Cohesion: 0.07
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+6 more)

### Community 141 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 151 - "Overlay"
Cohesion: 0.04
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 157 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "StripChart"
Cohesion: 0.10
Nodes (5): NetworkDiagramCanvas, StripChart, Builder, ChartsExample, Builder

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **58 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1611 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **130 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `menu_bar.py`, `host.py`, `PageManager`, `ProcessManager`, `Visual`, `LinkToPage`, `buffer_manager.py`, `Overlay`, `CheckboxOverlay`, `pyside6_qtwidgets`, `AnimationManager`, `Performance`, `ClickManager`, `LocalizationManager`, `.reload_preferences`, `examples.py`, `Panel`, `style.py`, `InputManager`, `Json`, `KeyBinds`, `BaseForm`, `Router`, `hardware/__init__.py`, `open_favorite_page.py`, `Preferences`, `GoForwardToNextPage`, `_base_button.py`, `confirm_dialog`, `.save_current_page`, `WorkspaceSaveResetButton`, `ConfigureThisWorkspace`, `Style`, `FilterOverlay`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05555555555555555 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `menu_bar.py`, `.restyle`, `SettingsSection`, `._build_stylesheet`, `.theme_family`, `.link_color`, `_base_button.py`, `style.py`, `.brush`, `.discard_changes`, `Overlay`, `QWidget`, `open_favorite_page.py`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.04736842105263158 - nodes in this community are weakly interconnected._