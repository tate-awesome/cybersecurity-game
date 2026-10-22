# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 307 files · ~248,781 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4446 nodes · 9360 edges · 215 communities (80 shown, 135 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e4ef837a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MetaPacket
- time
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- Panel
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- geometry.py
- WindowControls
- app.py
- .__init__
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- ViewPort
- PacketTreeview
- DragPayload
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- NetFilterQueue
- SummaryDrawer
- Camera
- Buffer
- LocalizationManager
- QWidget
- HostOverlay
- StripChart
- Runtime Requirements
- QWidget
- StatusBuffer
- launch.py
- ConfigEditor
- SectionCard
- NewWorkspaceDialog
- Draw
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- .__init__
- Modify
- .strip_chart_layout
- Router
- _PollUnpacker
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- Canvas
- palette_generator.py
- sys
- .__init__
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- bare_icon
- WorkspaceSorter
- .leaf
- config_editor.py
- WaveGrid
- Dev/Host_API.py
- BaseForm
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- confirm_dialog
- Replay
- _Indicator
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- transitions.py
- WindowBarButton
- AnimationManager
- context_manager.py
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- paint_panel
- Map
- Kalman
- .__init__
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- .new_tab
- Camera
- GrowingButton
- table.py
- ProcessManager
- Draw
- version.py
- DockArea
- Overlay
- NoteBrowser
- WorkspaceChip
- Panes
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- walk
- NMapper
- paint_mark
- WindowDrag
- fade_in
- .slider
- _Dim
- _SaveLayoutAsDefault
- style.py
- PooledCanvasMixin
- pyside6_qtgui
- WorkspaceSelectPage
- _DropPreview
- defender_hvac_chart.py
- PacketBuffer
- important_buttons/__init__.py
- DropZone
- Meter
- menu_bar.py
- FilterOverlay
- examples.py
- _Chip
- Visual
- core/transforms.py
- ShiftWheel
- TabStrip
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- WorkspaceButton
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- panel
- _DrawerLayout
- .save_current_page
- MenuBar
- CLAUDE.md
- WindowEdges
- .collect
- ._scan_for_networks
- Telemetry
- .authored_weights
- .prepare_page_config
- ap_commands.py
- .material_control
- SampleNetwork
- _Grip
- PopupWindow
- Builder
- CornerControls
- DragHandle
- .build_description_tab
- Loader
- .__init__
- _OnHide
- WifiForm
- ContextManager
- open_favorite_page.py
- frame_callback
- Scrollable
- ModeForm
- PreferencesData
- .new_tab
- os

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 138 edges
2. `ImportantButton` - 108 edges
3. `Style` - 100 edges
4. `Overlay` - 89 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 62 edges
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

## Communities (215 total, 135 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "time"
Cohesion: 0.05
Nodes (12): random_spline_path(), Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run() (+4 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (7): on_change(), checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (3): Visuals, paint_noise_gradient(), VisualBackground

### Community 9 - "Panel"
Cohesion: 0.09
Nodes (3): Builder, Panel, Builder

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 15 - "ToggleButton"
Cohesion: 0.03
Nodes (9): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 16 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 17 - "WindowControls"
Cohesion: 0.11
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowControls

### Community 19 - "app.py"
Cohesion: 0.14
Nodes (5): App, covered(), settle(), uncovered(), __getattr__()

### Community 23 - "threading"
Cohesion: 0.07
Nodes (4): _resolve_local_mac(), NetFilterQueueBaseClass, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.08
Nodes (7): ListZone, PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (12): action(), dumps(), header(), mark(), packet(), packet_from_meta(), poll(), raw_bytes() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.10
Nodes (6): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine()

### Community 29 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.06
Nodes (9): Table, fill_order(), key(), spread_order(), VariableOverlay, autosave(), reset_all(), CombinedTable (+1 more)

### Community 40 - "Buffer"
Cohesion: 0.06
Nodes (4): Buffer, HouseBuffer, ModbusBuffer, MapBuffer

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "StripChart"
Cohesion: 0.16
Nodes (3): StripChart, Builder, ChartsExample

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 66 - "docking.py"
Cohesion: 0.11
Nodes (14): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+6 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 69 - "Canvas"
Cohesion: 0.16
Nodes (3): Canvas, DefenderWorldMap, WorldMap

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "sys"
Cohesion: 0.22
Nodes (3): build_name(), main(), write_build_info()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.12
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.15
Nodes (10): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+2 more)

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 84 - "BaseForm"
Cohesion: 0.09
Nodes (11): APPoller, BaseForm, ElidingLabel, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+3 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "confirm_dialog"
Cohesion: 0.06
Nodes (10): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+2 more)

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "context_manager.py"
Cohesion: 0.13
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 102 - "paint_panel"
Cohesion: 0.11
Nodes (4): _Peek, paint_panel(), surface_shadow(), pyramid_blur()

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 112 - "table.py"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 116 - "DockArea"
Cohesion: 0.09
Nodes (3): DockArea, DropTarget, leaf_of()

### Community 117 - "Overlay"
Cohesion: 0.07
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 129 - "walk"
Cohesion: 0.13
Nodes (4): visit(), is_split(), panel_ids(), walk()

### Community 130 - "NMapper"
Cohesion: 0.09
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 131 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 137 - "style.py"
Cohesion: 0.11
Nodes (12): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme() (+4 more)

### Community 139 - "pyside6_qtgui"
Cohesion: 0.11
Nodes (6): draw_vessel(), nice_number(), nice_ticks(), value_noise(), draw_glow(), DenseMesh

### Community 143 - "PacketBuffer"
Cohesion: 0.07
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (30): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, ConfigureThisWorkspace (+22 more)

### Community 148 - "menu_bar.py"
Cohesion: 0.07
Nodes (12): ButtonGroup, offered_sections(), GoForwardToNextPage, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ToggleBookmark, ShowHelpMessage, global_buttons() (+4 more)

### Community 149 - "FilterOverlay"
Cohesion: 0.12
Nodes (7): _checkbox_value(), compile_packet_filter(), packet_filter(), FilterOverlay, activate(), save_filter_summary(), FilterPacketConsole

### Community 150 - "examples.py"
Cohesion: 0.06
Nodes (15): NetworkDiagramCanvas, ControlsExample, HouseExample, MapExample, NetworkExample, PassWheel, RegistersExample, SampleHouse (+7 more)

### Community 153 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

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
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+9 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "PopupWindow"
Cohesion: 0.12
Nodes (3): make(), message(), PopupWindow

### Community 203 - ".__init__"
Cohesion: 0.10
Nodes (4): House, frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.13
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "ContextManager"
Cohesion: 0.08
Nodes (11): ContextManager, BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page (+3 more)

### Community 214 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 215 - "Scrollable"
Cohesion: 0.08
Nodes (4): Scrollable, Builder, FlagsExample, Builder

### Community 225 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1769 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Footer`, `InputManager`, `style.py`, `PageManager`, `pyside6_qtgui`, `defender_hvac_chart.py`, `geometry.py`, `important_buttons/__init__.py`, `menu_bar.py`, `FilterOverlay`, `examples.py`, `threading`, `ShiftWheel`, `CheckboxOverlay`, `host.py`, `Performance`, `LocalizationManager`, `.reset_page`, `Json`, `KeyBinds`, `Router`, `docking.py`, `Canvas`, `PrivilegedHelper`, `Preferences`, `.start_session`, `WifiForm`, `config_editor.py`, `open_favorite_page.py`, `BaseForm`, `confirm_dialog`, `AnimationManager`, `context_manager.py`, `.apply_theme`, `table.py`, `ProcessManager`, `Overlay`, `Style`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.click_open` be split into smaller, more focused modules?**
  _Cohesion score 0.08666666666666667 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `context_manager.py`, `SettingsSection`, `style.py`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `.start_session`, `.css`, `important_buttons/__init__.py`, `ContextManager`, `.discard_changes`, `open_favorite_page.py`, `Overlay`, `menu_bar.py`, `.set_theme`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0783673469387755 - nodes in this community are weakly interconnected._