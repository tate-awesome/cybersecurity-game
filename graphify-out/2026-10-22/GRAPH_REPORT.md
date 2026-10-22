# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 306 files · ~246,273 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4395 nodes · 9255 edges · 210 communities (77 shown, 133 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 473 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d6858b0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- window_chrome.py
- MetaPacket
- time
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- .__init__
- important_buttons/__init__.py
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- ContextManager
- WindowBarButton
- .__init__
- .columnconfigure
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- .__init__
- SessionRecorder
- ViewPort
- PacketTreeview
- menu_bar.py
- MapBuffer
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- NetFilterQueue
- SummaryDrawer
- Camera
- ModbusBuffer
- .setText
- LocalizationManager
- QWidget
- HostOverlay
- save_layout_as_default.py
- Runtime Requirements
- QWidget
- StatusBuffer
- launch.py
- ConfigEditor
- SectionCard
- NewWorkspaceDialog
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
- .fill_base
- DefenderModbusBuffer
- docking.py
- Prod/Host_API.py
- StripChartBase
- Builder
- palette_generator.py
- Draw
- App
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- VariableOverlay
- WorkspaceSorter
- .__init__
- .leaf
- config_editor.py
- WaveGrid
- Dev/Host_API.py
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- WindowEdges
- Replay
- DropZone
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- Attack
- AnimationManager
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- SettingsOverlayButton
- Map
- Kalman
- .collapsed
- Defender Full Suite Exercise Screenshot
- Camera
- GrowingButton
- _Dim
- Draw
- .workspace_button
- .target_at
- pyside6_qtwidgets
- Overlay
- WorkspaceChip
- ProcessManager
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- Panes
- APPoller
- TabStrip
- ArpSpoofer
- Table
- .slider
- DockArea
- .__init__
- themes.py
- PooledCanvasMixin
- Visual
- Proximity
- select_background.py
- DefenderHVACChart
- NoteBrowser
- .css
- ImportantButton
- .add_section
- Meter
- compile_packet_filter
- examples.py
- _Chip
- fade_in
- .arrow
- ShiftWheel
- SelectColorTheme
- PreferencesData
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- .restyle
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- FilterOverlay
- ConfigureThisWorkspace
- .save_current_page
- MenuBar
- CLAUDE.md
- LinkToPage
- SampleNetwork
- ._scan_for_networks
- NMapper
- .build_description_tab
- paint_panel
- .authored_weights
- .prepare_page_config
- _is_global
- ap_commands.py
- .material_control
- frame_callback
- _Grip
- confirm_dialog
- frame_callback
- DenseMesh
- Telemetry
- DragHandle
- WifiForm
- SelectRegisterPreset
- .integer
- widgets/__init__.py
- _Gaps
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
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `status()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py

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

## Communities (210 total, 133 thin omitted)

### Community 0 - "window_chrome.py"
Cohesion: 0.11
Nodes (7): bar_button_height(), CornerControls, draw_window_bar_line(), _Strip, window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 1 - "MetaPacket"
Cohesion: 0.05
Nodes (7): Channel, _default_gateway_ip(), NetworkGraph, PacketBuffer, Transaction, TransactionManager, MetaPacket

### Community 2 - "time"
Cohesion: 0.05
Nodes (14): flush(), flush_all(), run(), random_spline_path(), build_capability(), _Echo, _BufferShim, _ContextStub (+6 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (7): on_change(), checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "important_buttons/__init__.py"
Cohesion: 0.06
Nodes (11): ClearAllCapturedBufferData, ClearPacketConsole, ClearSavedWorkspaceInputs, LoadSettingsPresetFile, OpenWorkspaceEditor, OpenWorkspaceSelect, RefreshCurrentPage, ResetSavedWorkspaceLayout (+3 more)

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 16 - "ContextManager"
Cohesion: 0.08
Nodes (11): ContextManager, WindowReveal, apply_scale_about(), BoatMotion, Triangle, TitlePage, WorkspaceSelectPage, WorkspacePage (+3 more)

### Community 17 - "WindowBarButton"
Cohesion: 0.10
Nodes (5): SquareButtons, toggle_maximized(), WindowBarButton, WindowControls, WindowDrag

### Community 19 - ".__init__"
Cohesion: 0.09
Nodes (5): bare_icon(), _FollowResize, global_buttons(), icon_button(), _RightZoneRoom

### Community 20 - ".columnconfigure"
Cohesion: 0.08
Nodes (3): Builder, Builder, Builder

### Community 23 - "threading"
Cohesion: 0.07
Nodes (5): Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - ".__init__"
Cohesion: 0.10
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+5 more)

### Community 28 - "ViewPort"
Cohesion: 0.07
Nodes (11): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), scale(), translate() (+3 more)

### Community 30 - "menu_bar.py"
Cohesion: 0.08
Nodes (7): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark, ShowHelpMessage

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 37 - "NetFilterQueue"
Cohesion: 0.06
Nodes (3): NetFilterQueue, NetFilterQueue, Sniffer

### Community 40 - "ModbusBuffer"
Cohesion: 0.09
Nodes (3): HouseBuffer, ModbusBuffer, Loader

### Community 43 - "QWidget"
Cohesion: 0.18
Nodes (4): covered(), settle(), uncovered(), PopupEntrance

### Community 44 - "HostOverlay"
Cohesion: 0.19
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "save_layout_as_default.py"
Cohesion: 0.17
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.12
Nodes (3): _Peek, _SideStrip, TabbedPane

### Community 49 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - "SlidersForm"
Cohesion: 0.14
Nodes (4): push_submarine_settings(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (17): add_tab(), visit(), find(), from_tree(), split(), is_split(), leaf(), move_panel() (+9 more)

### Community 67 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 77 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.15
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

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

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 102 - "SettingsOverlayButton"
Cohesion: 0.14
Nodes (4): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 110 - "Camera"
Cohesion: 0.13
Nodes (3): Camera, padded_fit_uniform(), zoom_and_pan()

### Community 113 - "_Dim"
Cohesion: 0.11
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 118 - "pyside6_qtwidgets"
Cohesion: 0.12
Nodes (14): BaseForm, ModeForm, align_decimals(), format_number(), fraction_width(), APConnectForm, APTunnelForm, ArpForm (+6 more)

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 131 - "TabStrip"
Cohesion: 0.07
Nodes (5): _LentPlaceholder, paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 133 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "Visual"
Cohesion: 0.09
Nodes (6): draw_vessel(), get_arc_points(), get_bearing(), rotate(), draw_glow(), Visual

### Community 145 - "ImportantButton"
Cohesion: 0.04
Nodes (21): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearModbusAndModelData, ClearStatusConsole, EditModbusRegisterDisplay, EditNetworkHosts, ImportThemes (+13 more)

### Community 149 - "compile_packet_filter"
Cohesion: 0.18
Nodes (5): _checkbox_value(), compile_packet_filter(), packet_filter(), activate(), save_filter_summary()

### Community 150 - "examples.py"
Cohesion: 0.04
Nodes (22): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap, ControlsExample, FlagsExample, HouseExample (+14 more)

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

### Community 177 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 180 - "paint_panel"
Cohesion: 0.10
Nodes (4): bar_inset(), minimized_thickness(), paint_panel(), surface_shadow()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.15
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), set_ap_tunnel(), set_encryption() (+8 more)

### Community 188 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog(), message() (+1 more)

### Community 191 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 215 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (10): NetworkDiagramCanvas, StripChart, Scrollable, panel(), Builder, ChartsExample, Builder, Panel (+2 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1755 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **133 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `window_chrome.py`, `InputManager`, `important_buttons/__init__.py`, `PageManager`, `Visual`, `ImportantButton`, `examples.py`, `threading`, `ShiftWheel`, `.__init__`, `menu_bar.py`, `Performance`, `FilterOverlay`, `ConfigureThisWorkspace`, `.setText`, `LocalizationManager`, `LinkToPage`, `save_layout_as_default.py`, `.reset_page`, `Json`, `KeyBinds`, `confirm_dialog`, `Router`, `docking.py`, `PrivilegedHelper`, `Preferences`, `host.py`, `config_editor.py`, `widgets/__init__.py`, `AnimationManager`, `.apply_theme`, `pyside6_qtwidgets`, `ProcessManager`, `.start_session`, `Style`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `window_chrome.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11375661375661375 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.restyle`, `SettingsSection`, `.setText`, `._build_stylesheet`, `.apply_theme`, `.theme_family`, `ContextManager`, `.css`, `.discard_changes`, `ImportantButton`, `Overlay`, `.start_session`, `menu_bar.py`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0451152223304122 - nodes in this community are weakly interconnected._