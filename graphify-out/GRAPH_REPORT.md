# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 309 files · ~250,333 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4491 nodes · 9421 edges · 203 communities (79 shown, 124 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 479 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4586b391`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .__init__
- MetaPacket
- PacketBuffer
- footer.py
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- router.py
- Scrollable
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- map.py
- App
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- VisualPalette
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
- pause_menu.py
- WorkspaceSelectPage
- Camera
- ModbusBuffer
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- Runtime Requirements
- QWidget
- StatusBuffer
- launch.py
- ConfigEditor
- NMapper
- DropZone
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- Footer
- BaseForm
- SlidersForm
- .strip_chart_layout
- Router
- open_in_browser
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- examples.py
- palette_generator.py
- _SaveLayoutAsDefault
- menu_bar.py
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- WorkspaceSorter
- DragHandle
- .leaf
- config_editor.py
- WaveGrid
- MaterialEditorPopup
- .__init__
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- Draw
- Replay
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- Table
- AnimationManager
- Process
- Denier
- ModBus HVAC Exercise Screenshot
- paint_mark
- paint_panel
- _MapCanvas
- Kalman
- dist.py
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- _PollUnpacker
- Camera
- GrowingButton
- platform
- os
- Draw
- bare_icon
- DockArea
- Overlay
- NoteBrowser
- MenuBar
- SectionCard
- Panes
- .apply_theme
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- .collapsed
- NetFilterQueue
- MaterialEditor
- .__init__
- SettingsSection
- _Dim
- Paths
- style.py
- PooledCanvasMixin
- pyside6_qtcore
- .target_at
- DefenderHVACChart
- .css
- important_buttons/__init__.py
- SampleNetwork
- Meter
- GoForwardToNextPage
- filter_overlay.py
- Panel
- _Chip
- RefreshCurrentPage
- .arrow
- ShiftWheel
- _RightZoneRoom
- TabStrip
- .page_panel_keys
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ConfigureThisWorkspace
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- frame_callback
- .save_current_page
- CLAUDE.md
- .collect
- ._scan_for_networks
- Telemetry
- ProcessManager
- _Drawer
- .authored_weights
- from_tree
- ap_commands.py
- _Grip
- _base_button.py
- .integer
- frame_callback
- _Indicator
- APPoller
- WifiForm
- ContextManager
- open_favorite_page.py
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 139 edges
2. `ImportantButton` - 110 edges
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

## Communities (203 total, 124 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "PacketBuffer"
Cohesion: 0.09
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 3 - "footer.py"
Cohesion: 0.18
Nodes (4): on_off(), on_off(), set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "router.py"
Cohesion: 0.06
Nodes (9): random_spline_path(), BoatMotion, Sprites, Triangle, Visuals, WorkspacePage, NotFound, Page (+1 more)

### Community 9 - "Scrollable"
Cohesion: 0.05
Nodes (8): _Gaps, Scrollable, Builder, ChartsExample, FlagsExample, RegistersExample, Builder, Builder

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 15 - "ToggleButton"
Cohesion: 0.03
Nodes (10): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView (+2 more)

### Community 16 - "map.py"
Cohesion: 0.12
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 23 - "time"
Cohesion: 0.06
Nodes (11): _resolve_local_mac(), build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.08
Nodes (7): ListZone, PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.08
Nodes (8): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), padded_fit_uniform(), zoom_and_pan()

### Community 30 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.11
Nodes (3): key(), CombinedTable, entry()

### Community 37 - "pause_menu.py"
Cohesion: 0.09
Nodes (6): ButtonGroup, offered_sections(), OpenPauseMenu, SetCurrentPageAsFavorite, ToggleBookmark, ShowHelpMessage

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 40 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 44 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.09
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 51 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 60 - "BaseForm"
Cohesion: 0.04
Nodes (8): BaseForm, ModeForm, APConnectForm, ArpForm, DosForm, NFQForm, NmapForm, SniffForm

### Community 61 - "SlidersForm"
Cohesion: 0.06
Nodes (5): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback(), Modify

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "open_in_browser"
Cohesion: 0.14
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 66 - "docking.py"
Cohesion: 0.11
Nodes (16): add_tab(), drain_evenly(), find(), is_split(), leaf(), leaf_of(), move_panel(), new_id() (+8 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 69 - "examples.py"
Cohesion: 0.07
Nodes (14): Canvas, padded_fit_uniform_reverse(), zoom_and_pan_reverse(), DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, WorldMap (+6 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 72 - "menu_bar.py"
Cohesion: 0.06
Nodes (13): global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_button_height() (+5 more)

### Community 78 - "WorkspaceSorter"
Cohesion: 0.11
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.08
Nodes (14): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+6 more)

### Community 85 - "QWidget"
Cohesion: 0.14
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "Table"
Cohesion: 0.33
Nodes (3): Table, fill_order(), spread_order()

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "Process"
Cohesion: 0.06
Nodes (5): _dialog_parent(), file_dialog(), Buffer, Process, FileStream

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 102 - "paint_panel"
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 105 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (3): TitlePage, TitleFooter, GrowingButton

### Community 113 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 117 - "Overlay"
Cohesion: 0.05
Nodes (5): SelectBackground, SelectColorTheme, EditBackgroundChoices, SelectRegisterPreset, Overlay

### Community 118 - "NoteBrowser"
Cohesion: 0.14
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 120 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 128 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 130 - "NetFilterQueue"
Cohesion: 0.08
Nodes (3): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue

### Community 135 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 137 - "style.py"
Cohesion: 0.14
Nodes (10): button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+2 more)

### Community 139 - "pyside6_qtcore"
Cohesion: 0.10
Nodes (5): draw_vessel(), paint_noise_gradient(), value_noise(), draw_glow(), Visual

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (27): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay, EditNetworkHosts (+19 more)

### Community 149 - "filter_overlay.py"
Cohesion: 0.13
Nodes (7): _checkbox_value(), compile_packet_filter(), packet_filter(), FilterOverlay, activate(), save_filter_summary(), FilterPacketConsole

### Community 150 - "Panel"
Cohesion: 0.03
Nodes (16): panel(), ControlsExample, HouseExample, MapExample, NetworkExample, PacketsExample, SampleHVAC, SamplePackets (+8 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 168 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.08
Nodes (20): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+12 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "_base_button.py"
Cohesion: 0.05
Nodes (12): make(), ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+4 more)

### Community 195 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 200 - "APPoller"
Cohesion: 0.08
Nodes (3): APPoller, Sniffer, Loader

### Community 207 - "WifiForm"
Cohesion: 0.06
Nodes (6): ElidingLabel, MitmTable, set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "ContextManager"
Cohesion: 0.08
Nodes (8): ContextManager, TriangleCanvas, ShiftWheelSlider, TitleMenu, align_decimals(), format_number(), fraction_width(), APTunnelForm

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1791 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **124 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `PacketBuffer`, `footer.py`, `InputManager`, `Paths`, `style.py`, `router.py`, `PageManager`, `pyside6_qtcore`, `map.py`, `important_buttons/__init__.py`, `GoForwardToNextPage`, `filter_overlay.py`, `time`, `ShiftWheel`, `CheckboxOverlay`, `Performance`, `ConfigureThisWorkspace`, `pause_menu.py`, `.save_current_page`, `LocalizationManager`, `ProcessManager`, `Json`, `KeyBinds`, `_base_button.py`, `Router`, `docking.py`, `examples.py`, `menu_bar.py`, `PrivilegedHelper`, `Preferences`, `host.py`, `config_editor.py`, `open_favorite_page.py`, `AnimationManager`, `Process`, `.start_session`, `.apply_theme`, `Style`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.14705882352941177 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.preset_name`, `SettingsSection`, `menu_bar.py`, `style.py`, `.start_session`, `._build_stylesheet`, `.theme_family`, `.css`, `important_buttons/__init__.py`, `ContextManager`, `.discard_changes`, `open_favorite_page.py`, `Overlay`, `.apply_theme`, `_base_button.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.06688311688311688 - nodes in this community are weakly interconnected._