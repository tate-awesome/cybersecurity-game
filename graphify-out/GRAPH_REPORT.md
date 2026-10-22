# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 307 files · ~248,931 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4451 nodes · 9367 edges · 194 communities (84 shown, 110 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b1dafd1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MetaPacket
- server.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- router.py
- widgets/__init__.py
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- map.py
- pyside6_qtgui
- App
- .__init__
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- Kernel
- CheckboxOverlay
- SessionRecorder
- ViewPort
- PacketTreeview
- VariableOverlay
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- .fill_base
- WorkspaceSelectPage
- Camera
- ModbusBuffer
- Prod/Host_API.py
- LocalizationManager
- QWidget
- HostOverlay
- packet_console/_builder.py
- Runtime Requirements
- QWidget
- StatusBuffer
- launch.py
- ConfigEditor
- .section
- .leaf
- Draw
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- Modify
- .strip_chart_layout
- Router
- GrowingButton
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- examples.py
- palette_generator.py
- json
- menu_bar.py
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- WorkspaceSorter
- .build_workspace_section
- config_editor.py
- WaveGrid
- Dev/Host_API.py
- .add_setting_row
- Rows
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- confirm_dialog
- Replay
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- Table
- AnimationManager
- Paths
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- paint_panel
- _MapCanvas
- Kalman
- .__init__
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- SelectRegisterPreset
- Camera
- title.py
- DenseMesh
- buffer_manager.py
- Draw
- BuildInfo
- DockArea
- Overlay
- NoteBrowser
- TopLayout
- SectionCard
- Panes
- .restyle
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- .collapsed
- NMapper
- paint_mark
- settings.py
- _Dim
- save_layout_as_default.py
- themes.py
- PooledCanvasMixin
- VisualPalette
- .target_at
- defender_hvac_chart.py
- PacketBuffer
- .brush
- important_buttons/__init__.py
- from_tree
- Meter
- pause_menu.py
- .populate_filter_overlay
- .__init__
- _Chip
- Visual
- .arrow
- ShiftWheel
- TabStrip
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- .save_current_page
- MenuBar
- CLAUDE.md
- .collect
- ._scan_for_networks
- Telemetry
- .authored_weights
- .prepare_page_config
- ap_commands.py
- _Grip
- ThemeEditorPage
- Builder
- .__init__
- DragHandle
- .build_description_tab
- APPoller
- .__init__
- WifiForm
- ContextManager
- .setText
- frame_callback
- .__init__
- ModeForm
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 138 edges
2. `ImportantButton` - 108 edges
3. `Style` - 100 edges
4. `Overlay` - 89 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
7. `MetaPacket` - 61 edges
8. `ConfigEditor` - 58 edges
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

## Communities (194 total, 110 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.06
Nodes (5): Channel, NetworkGraph, Transaction, TransactionManager, MetaPacket

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "router.py"
Cohesion: 0.08
Nodes (6): Triangle, Visuals, WorkspacePage, NotFound, Page, TriangleCanvas

### Community 9 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (10): StripChart, Scrollable, panel(), Builder, Builder, ChartsExample, Builder, Panel (+2 more)

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 14 - "SettingsPage"
Cohesion: 0.06
Nodes (3): SettingsPage, save(), on_change()

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 16 - "map.py"
Cohesion: 0.19
Nodes (3): apply_scale_about(), scale(), translate()

### Community 23 - "time"
Cohesion: 0.05
Nodes (3): _is_global(), _resolve_local_mac(), NetFilterQueueBaseClass

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (11): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+3 more)

### Community 28 - "ViewPort"
Cohesion: 0.07
Nodes (9): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), BoatMotion, Sprites (+1 more)

### Community 30 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 40 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 41 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 43 - "QWidget"
Cohesion: 0.18
Nodes (4): covered(), settle(), uncovered(), PopupEntrance

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "packet_console/_builder.py"
Cohesion: 0.20
Nodes (4): compile_packet_filter(), FilterOverlay, FilterPacketConsole, Builder

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.09
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 49 - "launch.py"
Cohesion: 0.15
Nodes (8): git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 51 - ".section"
Cohesion: 0.15
Nodes (4): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.11
Nodes (16): add_tab(), drain_evenly(), find(), is_split(), leaf(), leaf_of(), move_panel(), new_id() (+8 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 69 - "examples.py"
Cohesion: 0.07
Nodes (11): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, WorldMap, PassWheel, SampleHouse, SampleHVAC (+3 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "json"
Cohesion: 0.27
Nodes (3): build_name(), main(), write_build_info()

### Community 72 - "menu_bar.py"
Cohesion: 0.04
Nodes (17): bare_icon(), _FollowResize, global_buttons(), icon_button(), _RightZoneRoom, bar_button_height(), CornerControls, draw_window_bar_line() (+9 more)

### Community 78 - "WorkspaceSorter"
Cohesion: 0.06
Nodes (6): WorkspaceSorter, delete(), create(), rename(), DragPayload, DropZone

### Community 80 - ".build_workspace_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.09
Nodes (12): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+4 more)

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "confirm_dialog"
Cohesion: 0.07
Nodes (7): DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, RefreshAndCloseOverlay, confirm_dialog()

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 102 - "paint_panel"
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 110 - "Camera"
Cohesion: 0.11
Nodes (5): Camera, padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 111 - "title.py"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

### Community 113 - "buffer_manager.py"
Cohesion: 0.08
Nodes (8): flush(), flush_all(), run(), Buffer, ProcessManager, Process, FileStream, RetentionPolicy

### Community 117 - "Overlay"
Cohesion: 0.09
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 120 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 126 - "Wifi"
Cohesion: 0.10
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 128 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 130 - "NMapper"
Cohesion: 0.07
Nodes (5): NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 131 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 134 - "settings.py"
Cohesion: 0.07
Nodes (7): SettingsSection, developer_text(), LinkToPage, LoadLocalizationLabelsFile, OpenThemeEditor, OpenWorkspaceEditor, background_choices()

### Community 135 - "_Dim"
Cohesion: 0.11
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 136 - "save_layout_as_default.py"
Cohesion: 0.17
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 137 - "themes.py"
Cohesion: 0.14
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "VisualPalette"
Cohesion: 0.11
Nodes (7): draw_vessel(), get_arc_points(), get_bearing(), rotate(), value_noise(), draw_glow(), VisualPalette

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (28): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+20 more)

### Community 148 - "pause_menu.py"
Cohesion: 0.06
Nodes (7): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, SetCurrentPageAsFavorite, ToggleBookmark, ShowHelpMessage

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 150 - ".__init__"
Cohesion: 0.06
Nodes (12): ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample, RegistersExample, SamplePackets, SampleSubmarine (+4 more)

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.12
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (5): ThemeEditorPage, make(), preview(), message(), PopupWindow

### Community 197 - "DragHandle"
Cohesion: 0.09
Nodes (3): DragHandle, _Indicator, ListZone

### Community 203 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.12
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "ContextManager"
Cohesion: 0.10
Nodes (14): ContextManager, BaseForm, align_decimals(), format_number(), fraction_width(), APConnectForm, APTunnelForm, ArpForm (+6 more)

### Community 211 - ".setText"
Cohesion: 0.06
Nodes (3): OpenFavoritePage, ToggleDebugLabels, ToggleLightDarkMode

### Community 214 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1772 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **110 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `settings.py`, `router.py`, `widgets/__init__.py`, `save_layout_as_default.py`, `PageManager`, `VisualPalette`, `defender_hvac_chart.py`, `map.py`, `pyside6_qtgui`, `important_buttons/__init__.py`, `pause_menu.py`, `time`, `ShiftWheel`, `CheckboxOverlay`, `ViewPort`, `Performance`, `LocalizationManager`, `packet_console/_builder.py`, `.reset_page`, `Json`, `KeyBinds`, `Router`, `docking.py`, `examples.py`, `menu_bar.py`, `PrivilegedHelper`, `Preferences`, `.start_session`, `config_editor.py`, `.setText`, `confirm_dialog`, `AnimationManager`, `Paths`, `.apply_theme`, `title.py`, `buffer_manager.py`, `Style`?**
  _High betweenness centrality (0.239) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.click_open` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `SettingsSection`, `menu_bar.py`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `.start_session`, `.brush`, `pyside6_qtgui`, `ContextManager`, `.discard_changes`, `important_buttons/__init__.py`, `.setText`, `Overlay`, `.restyle`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.06327683615819209 - nodes in this community are weakly interconnected._