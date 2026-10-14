# Graph Report - cybersecurity-game  (2026-10-14)

## Corpus Check
- 311 files · ~232,567 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 3693 nodes · 7770 edges · 187 communities (65 shown, 122 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 454 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fd06c675`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- important_buttons/__init__.py
- MetaPacket
- Builder
- Footer
- .__init__
- LayoutEditor
- PauseMenu
- VisualBackground
- channels/__init__.py
- .new_tab
- pyside6_qtcore
- PageManager
- DefenderV0
- ToggleButton
- Visual
- Overlay
- ThemeEditorPage
- CheckboxOverlay
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- ViewPort
- FindBar
- WorkspaceSaveResetButton
- SettingsPage
- main.py
- PacketTreeview
- Wifi
- .__init__
- Style
- Performance
- HVACView
- Wifi
- Draw
- MapBuffer
- WorkspaceSelectPage
- Camera
- ArpSpoofer
- server.py
- LocalizationManager
- examples.py
- TitleMenu
- Runtime Requirements
- os
- StatusBuffer
- .__init__
- ConfigEditor
- VisualPalette
- SlidersForm
- AnimationManager
- InputManager
- .minimize_button
- PopupEntrance
- Json
- KeyBinds
- WifiBaseClass
- Modify
- VectorField
- app.py
- threading
- DefenderStatusBuffer
- padded_fit_uniform
- Replay
- StripChartBase
- _MapCanvas
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
- WaveGrid
- .populate_filter_overlay
- ModBus MITM Workspace Screenshot
- Proximity
- SettingCell
- .add_setting_row
- Dev/Host_API.py
- ModBus Submarine Exercise Screenshot
- FadeOut
- NewWorkspaceDialog
- .strip_chart_layout
- Network Actions Panel (Forms, Stop All)
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
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
- .build_workspace_section
- Camera
- GrowingButton
- WindowEdges
- TitleFooter
- ModBus Basics Workspace Screenshot
- MainWindow
- .__init__
- panel
- Attack
- CornerControls
- dist.py
- Denier
- Master
- ProcessManager
- AppearEffect
- .__init__
- Slave
- .material_control
- NetFilterQueue
- DefenderModbusBuffer
- geometry.py
- .apply_theme
- SettingsSection
- host.py
- NoteBrowser
- themes.py
- PooledCanvasMixin
- .__init__
- ap_commands.py
- menu_bar.py
- ._scan_for_networks
- file_dialog
- confirm_dialog
- _PollUnpacker
- Telemetry
- Kalman
- hvac_view.py
- .setText
- .__init__
- core/transforms.py
- transformations.py
- LinkToPage
- widgets/__init__.py
- ContextManager
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- on_notification
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- APPoller
- MenuBar
- CLAUDE.md
- configure_this_workspace.py
- window_bar_height
- edit_modbus_register_display.py
- DenseMesh
- _base_button.py
- Canvas
- Map
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 131 edges
2. `ImportantButton` - 108 edges
3. `Style` - 79 edges
4. `Overlay` - 68 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 60 edges
7. `MetaPacket` - 59 edges
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

## Communities (187 total, 122 thin omitted)

### Community 0 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (23): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, LoadLocalizationLabelsFile, LoadMcapIntoPacketBuffer (+15 more)

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "Builder"
Cohesion: 0.10
Nodes (3): Builder, Builder, Builder

### Community 3 - "Footer"
Cohesion: 0.12
Nodes (5): Footer, on_off(), on_off(), set_text(), tooltip()

### Community 5 - "LayoutEditor"
Cohesion: 0.05
Nodes (9): LayoutEditor, add(), add(), checked_value(), is_checked(), SettingsSection, save(), save() (+1 more)

### Community 6 - "PauseMenu"
Cohesion: 0.11
Nodes (3): _Dim, _FollowResize, PauseMenu

### Community 8 - "channels/__init__.py"
Cohesion: 0.08
Nodes (3): HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 10 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (11): AttackerV0, BoatMotion, menu_bar_buttons(), Sprites, Triangle, Visuals, TitlePage, WorkspacePage (+3 more)

### Community 15 - "ToggleButton"
Cohesion: 0.06
Nodes (6): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleStripChartAutoFit

### Community 16 - "Visual"
Cohesion: 0.11
Nodes (5): draw_vessel(), nice_number(), nice_ticks(), draw_glow(), Visual

### Community 17 - "Overlay"
Cohesion: 0.05
Nodes (10): RefreshCurrentPage, SelectColorTheme, EditBackgroundStyle, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+2 more)

### Community 20 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "WorkspaceSaveResetButton"
Cohesion: 0.21
Nodes (3): ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 30 - "Wifi"
Cohesion: 0.11
Nodes (6): Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 31 - ".__init__"
Cohesion: 0.08
Nodes (8): frame_callback(), sprite(), sprite_enabled(), draw_host(), frame_callback(), frame_callback(), sprite(), sprite_enabled()

### Community 35 - "Wifi"
Cohesion: 0.14
Nodes (3): _list_item(), Wifi, on_notification()

### Community 41 - "server.py"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 43 - "examples.py"
Cohesion: 0.05
Nodes (19): House, WorldMap, ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample, PacketsExample (+11 more)

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 50 - "ConfigEditor"
Cohesion: 0.13
Nodes (3): ConfigEditor, walk(), discard()

### Community 52 - "SlidersForm"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 53 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 55 - ".minimize_button"
Cohesion: 0.19
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 63 - "app.py"
Cohesion: 0.13
Nodes (6): App, FadeIn, covered(), uncovered(), WindowReveal, __getattr__()

### Community 64 - "threading"
Cohesion: 0.08
Nodes (5): random_spline_path(), Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "NMapper"
Cohesion: 0.20
Nodes (3): NMapper, InterfaceManager, job()

### Community 82 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 83 - "ModBus MITM Workspace Screenshot"
Cohesion: 0.17
Nodes (16): ARP Spoofing Form (Target IP, Host IP), ModBus Holding Registers (HReg), ModBus Data Panel (Variables, Forms), ModBus Man-in-the-Middle Attack, ModBus Monitors Panel (HReg 1-4 time plots), ModBus Readings Table (HReg Received/Sent/Command), Network Actions Panel, Network Graph Panel with Packets per Second Plot (+8 more)

### Community 87 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

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

### Community 96 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Network Actions Panel"
Cohesion: 0.21
Nodes (13): Network Recon Exercise Screenshot, AP Connection Form, ARP Spoofing Form, Encryption Form, Modbus Protocol, Network Actions Panel, Network Graph Panel with Packets per Second Chart, NMapping (Map Network) Form (+5 more)

### Community 102 - ".collect"
Cohesion: 0.17
Nodes (3): remove_nested(), set_nested(), group()

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - ".build_workspace_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 114 - "ModBus Basics Workspace Screenshot"
Cohesion: 0.25
Nodes (11): ModBus Basics Workspace Screenshot, ARP Spoofing Form (Target IP, Host IP), Modbus Holding Registers (HReg), ModBus Data Panel (ModBus Readings table: HReg Received/Sent/Command), ModBus Monitors Panel (HReg 1-4 time-series plots), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second chart), Packets Panel (Time, No., Observer, Direction, Protocol, ModBus Info) (+3 more)

### Community 117 - ".__init__"
Cohesion: 0.26
Nodes (6): encryption_enabled(), set_encryption(), enc_button(), enc_button(), start_encryption(), stop_encryption()

### Community 119 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 120 - "CornerControls"
Cohesion: 0.11
Nodes (6): CornerControls, draw_window_bar_line(), _Strip, toggle_maximized(), window_bar_has_line(), WindowControls

### Community 121 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 132 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 136 - "NoteBrowser"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 137 - "themes.py"
Cohesion: 0.23
Nodes (5): is_hex(), _old_palette(), read_theme(), resolve_materials(), theme_file()

### Community 141 - "ap_commands.py"
Cohesion: 0.14
Nodes (13): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+5 more)

### Community 142 - "menu_bar.py"
Cohesion: 0.05
Nodes (8): ButtonGroup, GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark, _FollowResize, group_button_names(), _pane_is_minimized()

### Community 143 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 145 - "confirm_dialog"
Cohesion: 0.08
Nodes (8): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ResetCurrentPageToDefaults, ShowHelpMessage, confirm_dialog(), message(), quit_dialog()

### Community 154 - "core/transforms.py"
Cohesion: 0.28
Nodes (4): padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 155 - "transformations.py"
Cohesion: 0.32
Nodes (3): canvas_fit(), padded_fit(), affine()

### Community 157 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (11): StripChart, compile_packet_filter(), Panes, Scrollable, Builder, ChartsExample, Builder, Builder (+3 more)

### Community 158 - "ContextManager"
Cohesion: 0.12
Nodes (14): ContextManager, apply_scale_about(), BaseForm, ModeForm, APConnectForm, APTunnelForm, ArpForm, DosForm (+6 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 178 - "_base_button.py"
Cohesion: 0.11
Nodes (7): open_in_browser(), FilterOverlay, FilterPacketConsole, ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 179 - "Canvas"
Cohesion: 0.13
Nodes (4): Canvas, DefenderWorldMap, NetworkDiagramCanvas, TriangleCanvas

## Knowledge Gaps
- **43 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `ARP Spoofing Form` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1431 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **122 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `Footer`, `.apply_theme`, `host.py`, `channels/__init__.py`, `pyside6_qtcore`, `PageManager`, `menu_bar.py`, `Visual`, `Overlay`, `CheckboxOverlay`, `hvac_view.py`, `.setText`, `WorkspaceSaveResetButton`, `LinkToPage`, `widgets/__init__.py`, `Style`, `Performance`, `LocalizationManager`, `examples.py`, `configure_this_workspace.py`, `edit_modbus_register_display.py`, `_base_button.py`, `Canvas`, `AnimationManager`, `InputManager`, `Json`, `KeyBinds`, `threading`, `Router`, `PrivilegedHelper`, `Preferences`, `.start_session`, `ProcessManager`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.03342046303211352 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `LayoutEditor`, `.collect`, `WorkspaceSelectPage`, `NoteBrowser`, `.new_tab`, `pyside6_qtcore`, `.create_workspace`, `.build_workspace_section`, `configure_this_workspace.py`, `.leaf`, `.sort_settings`, `.add_setting_row`, `SettingCell`, `FindBar`, `NewWorkspaceDialog`, `.__init__`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07058001397624039 - nodes in this community are weakly interconnected._