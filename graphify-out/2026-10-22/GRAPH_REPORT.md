# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 305 files · ~244,097 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4367 nodes · 9213 edges · 234 communities (70 shown, 164 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 475 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8b82fffb`
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
- NetworkGraph
- ._build_stylesheet
- PageManager
- MapBuffer
- SettingsPage
- ToggleButton
- VisualPalette
- menu_bar.py
- _RightZoneRoom
- .collapsed
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- Kernel
- .__init__
- SessionRecorder
- ViewPort
- PacketTreeview
- pyside6_qtcore
- channels/__init__.py
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- pause_menu.py
- SummaryDrawer
- Camera
- NetFilterQueue
- .__init__
- LocalizationManager
- PopupEntrance
- HostOverlay
- _base_button.py
- Runtime Requirements
- StatusBuffer
- sys
- ConfigEditor
- SectionCard
- .collect
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
- .restyle
- DefenderModbusBuffer
- docking.py
- bare_icon
- StripChartBase
- Builder
- palette_generator.py
- .fill_base
- App
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- MenuBar
- geometry.py
- TabStrip
- .leaf
- HouseBuffer
- WaveGrid
- paint_panel
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- NoteBrowser
- Replay
- _Indicator
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- VariableOverlay
- PacketBuffer
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- Dev/Host_API.py
- config_editor.py
- _MapCanvas
- Kalman
- WorkspaceSelectPage
- Defender Full Suite Exercise Screenshot
- RecordFilter
- .__init__
- Camera
- AnimationManager
- Draw
- _Dim
- Draw
- MainWindow
- .target_at
- core/transforms.py
- ContextManager
- Overlay
- WorkspaceChip
- ProcessManager
- .__init__
- Master
- Style
- AppearEffect
- Wifi
- Slave
- ArpSpoofer
- Panes
- QWidget
- NewWorkspaceDialog
- .renumber
- .slider
- DockArea
- .__init__
- themes.py
- PooledCanvasMixin
- MitmTable
- Proximity
- Builder
- defender_hvac_chart.py
- .css
- important_buttons/__init__.py
- DropZone
- Meter
- .record
- .populate_filter_overlay
- GrowingButton
- fade_in
- .setText
- ShiftWheel
- Paths
- TitleMenu
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- BuildInfo
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- Loader
- .save_current_page
- .leave
- panel
- CLAUDE.md
- _OnHide
- WorkspaceButton
- ._scan_for_networks
- NMapper
- .build_description_tab
- .build_advanced_tab
- surface_shadow
- record_schema.py
- .authored_weights
- .prepare_page_config
- APPoller
- _Chip
- .__init__
- .material_control
- _Grip
- WorkspaceSaveResetButton
- SampleNetwork
- _DrawerLayout
- Telemetry
- DragHandle
- ModeForm
- SampleSubmarine
- Builder
- .__init__
- WifiForm
- RefreshCurrentPage
- align_decimals
- .new_tab
- FilterOverlay
- NetFilterQueue
- ConfigureThisWorkspace
- GoForwardToNextPage
- LinkToPage
- Channel
- _Gaps
- Panel
- InterfaceManager
- Visuals
- edit_modbus_register_display.py
- .new_tab
- ResetCurrentPageToDefaults
- _FollowResize
- TitleFooter
- flusher.py
- frame_callback

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

## Communities (234 total, 164 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.13
Nodes (3): Canvas, DefenderWorldMap, TriangleCanvas

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "confirm_dialog"
Cohesion: 0.05
Nodes (11): make(), DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage (+3 more)

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 16 - "VisualPalette"
Cohesion: 0.12
Nodes (7): draw_vessel(), paint_noise_gradient(), value_noise(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 17 - "menu_bar.py"
Cohesion: 0.06
Nodes (13): global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_button_height() (+5 more)

### Community 23 - "time"
Cohesion: 0.06
Nodes (5): Buffer, TransactionManager, NetFilterQueueBaseClass, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - ".__init__"
Cohesion: 0.11
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 28 - "ViewPort"
Cohesion: 0.10
Nodes (6): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine()

### Community 29 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 30 - "pyside6_qtcore"
Cohesion: 0.09
Nodes (4): CallbackRegistry, ClickManager, PreferencesData, apply_scale_about()

### Community 31 - "channels/__init__.py"
Cohesion: 0.10
Nodes (3): ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 37 - "pause_menu.py"
Cohesion: 0.15
Nodes (3): ButtonGroup, offered_sections(), ToggleBookmark

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "_base_button.py"
Cohesion: 0.15
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "sys"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.15
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 79 - "TabStrip"
Cohesion: 0.09
Nodes (4): paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

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

### Community 96 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Dev/Host_API.py"
Cohesion: 0.07
Nodes (19): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+11 more)

### Community 102 - "config_editor.py"
Cohesion: 0.08
Nodes (16): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+8 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 108 - "RecordFilter"
Cohesion: 0.14
Nodes (3): header(), RecordFilter, RetentionPolicy

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 115 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 117 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 118 - "ContextManager"
Cohesion: 0.12
Nodes (12): ContextManager, compile_packet_filter(), BaseForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+4 more)

### Community 119 - "Overlay"
Cohesion: 0.08
Nodes (10): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, SelectRegisterPreset, SettingsOverlayButton (+2 more)

### Community 120 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 122 - ".__init__"
Cohesion: 0.19
Nodes (8): _edge_distance(), draw_arrow(), draw_host(), frame_callback(), is_hidden(), setting(), node_half_size(), _snap_direction()

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 131 - "QWidget"
Cohesion: 0.09
Nodes (5): bar_inset(), _LentPlaceholder, minimized_thickness(), _SideStrip, TabbedPane

### Community 132 - "NewWorkspaceDialog"
Cohesion: 0.11
Nodes (5): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems(), delete()

### Community 136 - ".__init__"
Cohesion: 0.27
Nodes (4): hvac_kalman_enabled(), kalman_enabled(), submarine_kalman_enabled(), Builder

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 141 - "Builder"
Cohesion: 0.16
Nodes (3): Builder, Builder, Builder

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (22): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, EditNetworkHosts, GoBackToPreviousPage (+14 more)

### Community 148 - ".record"
Cohesion: 0.15
Nodes (4): action(), mark(), poll(), status()

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 156 - "Paths"
Cohesion: 0.12
Nodes (3): _dialog_parent(), file_dialog(), Paths

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

### Community 181 - "record_schema.py"
Cohesion: 0.31
Nodes (4): decode(), packet(), packet_from_meta(), raw_bytes()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - ".__init__"
Cohesion: 0.11
Nodes (14): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), _hvac_send(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel(), set_encryption() (+6 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 203 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 209 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 220 - "Panel"
Cohesion: 0.03
Nodes (23): House, NetworkDiagramCanvas, StripChart, WorldMap, Scrollable, Builder, ChartsExample, ControlsExample (+15 more)

### Community 228 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 230 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1738 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **164 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `confirm_dialog`, `PageManager`, `defender_hvac_chart.py`, `VisualPalette`, `important_buttons/__init__.py`, `menu_bar.py`, `time`, `.setText`, `ShiftWheel`, `.__init__`, `Paths`, `pyside6_qtcore`, `channels/__init__.py`, `Performance`, `pause_menu.py`, `LocalizationManager`, `_base_button.py`, `Json`, `KeyBinds`, `Router`, `docking.py`, `PrivilegedHelper`, `Preferences`, `host.py`, `FilterOverlay`, `ConfigureThisWorkspace`, `GoForwardToNextPage`, `LinkToPage`, `Panel`, `edit_modbus_register_display.py`, `config_editor.py`, `.apply_theme`, `AnimationManager`, `Overlay`, `ProcessManager`, `Style`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.restyle`, `.setText`, `SettingsSection`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `_base_button.py`, `.css`, `menu_bar.py`, `.discard_changes`, `.preset_name`, `.set_theme`, `ContextManager`, `Overlay`, `ProcessManager`, `pyside6_qtcore`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._