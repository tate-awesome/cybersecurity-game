# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 305 files · ~244,154 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4369 nodes · 9215 edges · 216 communities (81 shown, 135 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 475 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5147a8a6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- MetaPacket
- server.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- confirm_dialog
- settings_overlay_button.py
- ._build_stylesheet
- PageManager
- MapBuffer
- SettingsPage
- ToggleButton
- Visual
- menu_bar.py
- MenuBar
- Panel
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- ViewPort
- PacketTreeview
- ContextManager
- typing
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- ToggleBookmark
- SummaryDrawer
- Camera
- NetFilterQueue
- LocalizationManager
- PopupEntrance
- HostOverlay
- StripChart
- Runtime Requirements
- StatusBuffer
- launch.py
- ConfigEditor
- SectionCard
- _base_button.py
- .collect
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- Modify
- .strip_chart_layout
- Router
- .restyle
- DefenderModbusBuffer
- docking.py
- WindowBarButton
- StripChartBase
- Builder
- palette_generator.py
- .__init__
- App
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- geometry.py
- TabStrip
- .leaf
- CallbackRegistry
- WaveGrid
- Prod/Host_API.py
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- NoteBrowser
- Replay
- DropZone
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- Attack
- PacketBuffer
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- Dev/Host_API.py
- pyside6_qtcore
- Map
- Kalman
- Defender Full Suite Exercise Screenshot
- time
- .build_advanced_tab
- Camera
- AnimationManager
- Draw
- _Dim
- Draw
- MainWindow
- QRect
- core/transforms.py
- pyside6_qtwidgets
- Overlay
- WorkspaceChip
- ProcessManager
- dist.py
- Master
- Style
- AppearEffect
- Wifi
- Slave
- ArpSpoofer
- Panes
- QWidget
- NewWorkspaceDialog
- SettingsSection
- DockArea
- .__init__
- themes.py
- PooledCanvasMixin
- quit_application.py
- .__init__
- Builder
- DefenderHVACChart
- .page_panel_keys
- .css
- important_buttons/__init__.py
- .add_section
- Meter
- open_favorite_page.py
- .populate_filter_overlay
- StreamIncomingPacketsToMcap
- fade_in
- ShiftWheel
- ConfigureThisWorkspace
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- reset_current_page_to_defaults.py
- BuildInfo
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- APPoller
- .save_current_page
- .leave
- router.py
- CLAUDE.md
- _OnHide
- .workspace_button
- ._scan_for_networks
- NMapper
- .build_description_tab
- _GlobalClickFilter
- surface_shadow
- .authored_weights
- .integer
- ap_commands.py
- .slider
- _Grip
- RefreshCurrentPage
- DenseMesh
- _DrawerLayout
- Telemetry
- from_tree
- DragHandle
- ModeForm
- Builder
- .__init__
- WifiForm
- LinkToPage
- GoForwardToNextPage
- Scrollable
- examples.py
- .new_tab

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 138 edges
2. `ImportantButton` - 108 edges
3. `Style` - 100 edges
4. `Overlay` - 89 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 61 edges
7. `ConfigEditor` - 58 edges
8. `BaseForm` - 58 edges
9. `DockArea` - 53 edges
10. `Panel` - 51 edges

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
- **Modbus Master/Slave Control-Feedback Loop** — game_outline_master, game_outline_slave, game_outline_control_feedback_procedure, game_outline_modbus_protocol [EXTRACTED 1.00]
- **Network attack flow: connect WiFi, map network, ARP spoof, observe packets** — game_assets_pages_workspaces_attacker_suite_screenshot_wifi_connection, game_assets_pages_workspaces_attacker_suite_screenshot_nmapping, game_assets_pages_workspaces_attacker_suite_screenshot_arp_spoofing, game_assets_pages_workspaces_attacker_suite_screenshot_packets_panel [INFERRED 0.75]
- **Defender anomaly detection flow: settings -> Kalman filter -> flags -> monitors** — game_assets_pages_workspaces_defender_suite_screenshot_defender_data_panel, game_assets_pages_workspaces_defender_suite_screenshot_kalman_filter, game_assets_pages_workspaces_defender_suite_screenshot_defender_flags_panel, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors [INFERRED 0.75]
- **Submarine telemetry views** — game_assets_pages_workspaces_defender_suite_screenshot_packet_log_panel, game_assets_pages_workspaces_defender_suite_screenshot_modbus_model_map, game_assets_pages_workspaces_defender_suite_screenshot_defender_monitors, game_assets_pages_workspaces_defender_suite_screenshot_submarine_modbus_system [INFERRED 0.75]
- **DoS attack flow: connect, map, spoof, observe traffic** — game_assets_pages_workspaces_dos_attack_screenshot_wifi_connection, game_assets_pages_workspaces_dos_attack_screenshot_nmapping, game_assets_pages_workspaces_dos_attack_screenshot_arp_spoofing, game_assets_pages_workspaces_dos_attack_screenshot_packets_panel, game_assets_pages_workspaces_dos_attack_screenshot_network_graph_panel [INFERRED 0.75]
- **Hack Output Buffer-to-Console Flow** — game_readme_buffer, game_readme_metapacket, game_readme_console_tabview, game_readme_var_buffer_trails [INFERRED 0.75]
- **Recon -> ARP spoof -> tamper ModBus values -> observe HVAC effect** — game_assets_pages_workspaces_modbus_hvac_screenshot_network_actions_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_modifiers, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_modbus_monitors_panel [INFERRED 0.75]
- **Network traffic observation panels** — game_assets_pages_workspaces_modbus_hvac_screenshot_packets_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_network_graph_panel, game_assets_pages_workspaces_modbus_hvac_screenshot_status_panel [INFERRED 0.75]
- **Recon, ARP spoof, and ModBus tamper workflow** — game_assets_pages_workspaces_modbus_submarine_screenshot_nmapping, game_assets_pages_workspaces_modbus_submarine_screenshot_arp_spoofing, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_data_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_mitm_attack_flow [INFERRED 0.75]
- **Submarine state visualization panels** — game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_model_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_modbus_submarine_screenshot_submarine_variables [INFERRED 0.75]
- **ModBus process observation via registers, monitors and model** — game_assets_pages_workspaces_attacker_suite_screenshot_modbus_data_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_monitors_panel, game_assets_pages_workspaces_attacker_suite_screenshot_modbus_model_panel, game_assets_pages_workspaces_attacker_suite_screenshot_holding_registers [INFERRED 0.85]
- **ModBus process observation panels** — game_assets_pages_workspaces_dos_attack_screenshot_modbus_data_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_model_panel, game_assets_pages_workspaces_dos_attack_screenshot_modbus_monitors_panel [INFERRED 0.85]

## Communities (216 total, 135 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.11
Nodes (5): apply_scale_about(), Canvas, DefenderWorldMap, House, WorldMap

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (5): on_change(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (3): paint_noise_gradient(), pyramid_blur(), VisualBackground

### Community 8 - "confirm_dialog"
Cohesion: 0.07
Nodes (7): make(), DeleteAllWorkspaceSavedData, _SaveLayoutAsDefault, ShowHelpMessage, confirm_dialog(), message(), PopupWindow

### Community 9 - "settings_overlay_button.py"
Cohesion: 0.10
Nodes (8): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, checked_value(), is_checked(), SettingsOverlayButton

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 16 - "Visual"
Cohesion: 0.10
Nodes (4): draw_vessel(), value_noise(), draw_glow(), Visual

### Community 17 - "menu_bar.py"
Cohesion: 0.05
Nodes (16): ButtonGroup, offered_sections(), SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, global_buttons(), icon_button(), CornerControls, draw_window_bar_line() (+8 more)

### Community 19 - "MenuBar"
Cohesion: 0.06
Nodes (3): _FollowResize, MenuBar, _RightZoneRoom

### Community 20 - "Panel"
Cohesion: 0.11
Nodes (3): StatusExample, TabsExample, Panel

### Community 23 - "threading"
Cohesion: 0.05
Nodes (6): flush(), flush_all(), run(), NetFilterQueueBaseClass, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.14
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.09
Nodes (3): Buffer, dumps(), SessionRecorder

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 29 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 30 - "ContextManager"
Cohesion: 0.10
Nodes (7): ContextManager, NetworkDiagramCanvas, TriangleCanvas, EditModbusRegisterDisplay, EditNetworkHosts, compile_packet_filter(), Builder

### Community 31 - "typing"
Cohesion: 0.08
Nodes (4): HouseBuffer, ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.05
Nodes (6): VariableOverlay, autosave(), reset_all(), CombinedTable, entry(), MitmTable

### Community 44 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "StripChart"
Cohesion: 0.10
Nodes (4): StripChart, Builder, ChartsExample, Builder

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "launch.py"
Cohesion: 0.15
Nodes (8): git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 52 - "_base_button.py"
Cohesion: 0.14
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.09
Nodes (16): add_tab(), DropTarget, find(), is_split(), leaf(), leaf_of(), move_panel(), new_id() (+8 more)

### Community 67 - "WindowBarButton"
Cohesion: 0.05
Nodes (9): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, bare_icon(), bar_button_height(), WindowBarButton (+1 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 79 - "TabStrip"
Cohesion: 0.10
Nodes (3): _LentPlaceholder, _SideTitle, TabStrip

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 83 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 92 - "DropZone"
Cohesion: 0.11
Nodes (3): DropZone, _Indicator, ListZone

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 97 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 98 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 102 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (12): PreferencesData, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+4 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 108 - "time"
Cohesion: 0.07
Nodes (12): random_spline_path(), action(), decode(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 115 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 117 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 118 - "pyside6_qtwidgets"
Cohesion: 0.13
Nodes (13): BaseForm, align_decimals(), format_number(), fraction_width(), APConnectForm, APTunnelForm, ArpForm, DosForm (+5 more)

### Community 119 - "Overlay"
Cohesion: 0.09
Nodes (5): SelectBackground, SelectColorTheme, SelectRegisterPreset, Overlay, background_choices()

### Community 122 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 126 - "Wifi"
Cohesion: 0.10
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 132 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 135 - "DockArea"
Cohesion: 0.10
Nodes (3): DockArea, visit(), drain_evenly()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.05
Nodes (17): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, LoadLocalizationLabelsFile, LoadMcapIntoPacketBuffer (+9 more)

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 157 - "GrowingButton"
Cohesion: 0.08
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 171 - "router.py"
Cohesion: 0.06
Nodes (9): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page (+1 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.12
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "RefreshCurrentPage"
Cohesion: 0.15
Nodes (4): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 203 - ".__init__"
Cohesion: 0.06
Nodes (12): frame_callback(), sprite(), sprite_enabled(), _edge_distance(), draw_arrow(), draw_host(), frame_callback(), node_half_size() (+4 more)

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 216 - "GoForwardToNextPage"
Cohesion: 0.11
Nodes (3): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu

### Community 219 - "Scrollable"
Cohesion: 0.10
Nodes (4): _Gaps, Scrollable, FlagsExample, RegistersExample

### Community 220 - "examples.py"
Cohesion: 0.07
Nodes (12): ControlsExample, HouseExample, MapExample, NetworkExample, PassWheel, SampleHouse, SampleHVAC, SampleNetwork (+4 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1741 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `InputManager`, `.start_session`, `settings_overlay_button.py`, `PageManager`, `quit_application.py`, `Visual`, `menu_bar.py`, `open_favorite_page.py`, `threading`, `ShiftWheel`, `CheckboxOverlay`, `ConfigureThisWorkspace`, `typing`, `Performance`, `LocalizationManager`, `router.py`, `_base_button.py`, `.reset_page`, `Json`, `KeyBinds`, `RefreshCurrentPage`, `Router`, `docking.py`, `.__init__`, `PrivilegedHelper`, `Preferences`, `host.py`, `CallbackRegistry`, `GoForwardToNextPage`, `examples.py`, `pyside6_qtcore`, `.apply_theme`, `AnimationManager`, `pyside6_qtwidgets`, `ProcessManager`, `Style`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.10582010582010581 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.restyle`, `.start_session`, `pyside6_qtcore`, `SettingsSection`, `settings_overlay_button.py`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `.css`, `menu_bar.py`, `.discard_changes`, `_base_button.py`, `open_favorite_page.py`, `Overlay`, `ContextManager`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0783673469387755 - nodes in this community are weakly interconnected._