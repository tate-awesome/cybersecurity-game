# Graph Report - cybersecurity-game  (2026-10-19)

## Corpus Check
- 309 files · ~249,225 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4111 nodes · 8383 edges · 217 communities (65 shown, 152 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 483 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5e17068b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .minimize_button
- MetaPacket
- ContextManager
- Footer
- SettingsSection
- PauseMenu
- VisualBackground
- PacketBuffer
- SettingsPage
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- DefenderV0
- ToggleButton
- Visual
- FilterOverlay
- time
- Attack
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- typing
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- hvac_view.py
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
- ViewPort
- Runtime Requirements
- ThemeEditorPage
- StatusBuffer
- launch.py
- ConfigEditor
- MapBuffer
- SlidersForm
- context_manager.py
- InputManager
- DefenderHVACChart
- VectorField
- Json
- KeyBinds
- ModbusBuffer
- BaseForm
- Modify
- time_core/transforms.py
- Router
- threading
- DefenderStatusBuffer
- Replay
- FileStream
- StripChartBase
- WindowDrag
- palette_generator.py
- AnimationManager
- app.py
- PrivilegedHelper
- Constellation
- Preferences
- DefenderModbusBuffer
- Draw
- VariableOverlay
- ListZone
- .leaf
- confirm_dialog
- WaveGrid
- ModBus MITM Workspace Screenshot
- .__init__
- .add_setting_row
- Rows
- ModBus Submarine Exercise Screenshot
- FadeIn
- NewWorkspaceDialog
- os
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- ap_commands.py
- MitmTable
- WorkspaceSorter
- WindowControls
- ModBus HVAC Exercise Screenshot
- Network Actions Panel
- MenuBar
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- StripChartLayout
- Camera
- .__init__
- WindowEdges
- _Dim
- ModBus Basics Workspace Screenshot
- MainWindow
- RecordFilter
- PopupEntrance
- settings.py
- WorkspaceChip
- Proximity
- Denier
- Master
- Style
- AppearEffect
- Slave
- ArpSpoofer
- NMapper
- Scrollable
- _StyledComboItems
- _Proxy
- .build_menu_bar_section
- style.py
- PooledCanvasMixin
- geometry.py
- .__init__
- Dev/Host_API.py
- Builder
- DropZone
- .__init__
- Telemetry
- performance.py
- Overlay
- .build_tabs
- .__init__
- ToggleLightDarkMode
- GrowingButton
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- _OnHide
- ClickManager
- Canvas
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- menu_bar.py
- NetFilterQueue
- LinkToPage
- CLAUDE.md
- SelectBackground
- _RightZoneRoom
- .build_description_tab
- SelectRegisterPreset
- core/transforms.py
- defender_modbus_panel/_builder.py
- DenseMesh
- ConfigureThisWorkspace
- GoForwardToNextPage
- EditWorkspaceAvailability
- TopLayout
- _base_button.py
- .__init__
- Builder
- APPoller
- ToggleFreezeBackground
- DragHandle
- .__init__
- .load
- WifiForm

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 134 edges
2. `ImportantButton` - 106 edges
3. `Style` - 100 edges
4. `Overlay` - 80 edges
5. `ConfigEditor` - 67 edges
6. `MenuBar` - 63 edges
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

## Communities (217 total, 152 thin omitted)

### Community 0 - ".minimize_button"
Cohesion: 0.21
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "ContextManager"
Cohesion: 0.10
Nodes (10): ContextManager, AttackerV0, BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page (+2 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (4): Visuals, paint_aurora(), pyramid_blur(), VisualBackground

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (19): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay, FilterPacketConsole (+11 more)

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleStripChartAutoFit, ToggleTranslucentSurfaces

### Community 16 - "Visual"
Cohesion: 0.08
Nodes (3): draw_vessel(), draw_glow(), Visual

### Community 17 - "FilterOverlay"
Cohesion: 0.14
Nodes (6): _checkbox_value(), compile_packet_filter(), packet_filter(), FilterOverlay, activate(), save_filter_summary()

### Community 19 - "time"
Cohesion: 0.10
Nodes (12): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 20 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.12
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 30 - "Wifi"
Cohesion: 0.05
Nodes (12): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish() (+4 more)

### Community 31 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 32 - "LayoutEditor"
Cohesion: 0.09
Nodes (4): LayoutEditor, group(), add(), add()

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
Nodes (19): House, WorldMap, ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample, PacketsExample (+11 more)

### Community 44 - "Panel"
Cohesion: 0.06
Nodes (6): panel(), Builder, _DrawerLayout, paint_panel(), Panel, surface_shadow()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): ThemeEditorPage, preview(), message(), PopupWindow

### Community 49 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 50 - "ConfigEditor"
Cohesion: 0.10
Nodes (3): ConfigEditor, remove_nested(), set_nested()

### Community 53 - "context_manager.py"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 60 - "BaseForm"
Cohesion: 0.04
Nodes (10): BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm, NFQForm (+2 more)

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "threading"
Cohesion: 0.08
Nodes (4): Buffer, NetFilterQueueBaseClass, ProcessManager, Process

### Community 65 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.18
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 81 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton (+1 more)

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 91 - "os"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 92 - "Network Actions Panel (Forms, Stop All)"
Cohesion: 0.19
Nodes (13): AP Connection Form (AP URL, Disconnect, waiting indicator), ARP Spoofing Form (Target IP, Host IP, Start Spoofer), Encryption Form, ARP & IP Basics Workspace Screenshot, ARP Spoofing MITM Attack Workflow, Network Actions Panel (Forms, Stop All), Network Graph Panel with Packets per Second Chart, NMapping Form (Map Network) (+5 more)

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "ap_commands.py"
Cohesion: 0.16
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+8 more)

### Community 99 - "WindowControls"
Cohesion: 0.11
Nodes (4): CornerControls, draw_window_bar_line(), _Strip, WindowControls

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Actions Panel"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 118 - "settings.py"
Cohesion: 0.08
Nodes (6): on_change(), SettingsSection, developer_text(), LoadLocalizationLabelsFile, OpenWorkspaceEditor, OpenWorkspaceSorter

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 129 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 131 - "Scrollable"
Cohesion: 0.06
Nodes (7): StripChart, Scrollable, Builder, ChartsExample, Builder, Builder, Builder

### Community 137 - "style.py"
Cohesion: 0.14
Nodes (10): button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+2 more)

### Community 139 - "geometry.py"
Cohesion: 0.08
Nodes (13): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), get_arc_points(), get_bearing() (+5 more)

### Community 141 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (17): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+9 more)

### Community 151 - "Overlay"
Cohesion: 0.12
Nodes (6): SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, Overlay

### Community 157 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "Canvas"
Cohesion: 0.10
Nodes (4): Canvas, DefenderWorldMap, NetworkDiagramCanvas, Builder

### Community 168 - "menu_bar.py"
Cohesion: 0.06
Nodes (13): ButtonGroup, offered_sections(), GoBackToPreviousPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage, global_buttons() (+5 more)

### Community 191 - "_base_button.py"
Cohesion: 0.10
Nodes (6): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenFavoritePage, OpenProjectRepository, ReportAnIssue

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.18
Nodes (3): set_read_only(), set_text(), WifiForm

## Knowledge Gaps
- **58 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1646 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **152 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Scrollable`, `.restyle`, `style.py`, `PageManager`, `important_buttons/__init__.py`, `.apply`, `Visual`, `.start_session`, `performance.py`, `typing`, `Overlay`, `CheckboxOverlay`, `hvac_view.py`, `Performance`, `ClickManager`, `Canvas`, `menu_bar.py`, `LocalizationManager`, `LinkToPage`, `examples.py`, `.reload_preferences`, `context_manager.py`, `InputManager`, `defender_modbus_panel/_builder.py`, `Json`, `KeyBinds`, `ConfigureThisWorkspace`, `GoForwardToNextPage`, `BaseForm`, `Router`, `threading`, `_base_button.py`, `AnimationManager`, `Preferences`, `confirm_dialog`, `os`, `settings.py`, `Style`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07390648567119155 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.restyle`, `SettingsSection`, `menu_bar.py`, `style.py`, `._build_stylesheet`, `.theme_family`, `.discard_changes`, `.start_session`, `context_manager.py`, `.preset_name`, `Overlay`, `.link_color`, `.apply_theme`, `_base_button.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.10492139439507861 - nodes in this community are weakly interconnected._