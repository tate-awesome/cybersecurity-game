# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 307 files · ~249,830 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4471 nodes · 9383 edges · 212 communities (77 shown, 135 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dc4aa85b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .__init__
- MetaPacket
- Sniffer
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- ContextManager
- Scrollable
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- geometry.py
- Router
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
- .render_blurred
- SummaryDrawer
- Camera
- ModbusBuffer
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- Runtime Requirements
- QWidget
- StatusBuffer
- host.py
- ConfigEditor
- NMapper
- NewWorkspaceDialog
- Draw
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- .add_header
- Modify
- .strip_chart_layout
- WorkspaceSelectPage
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- Canvas
- palette_generator.py
- .fixed_width_wrapper
- menu_bar.py
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- WorkspaceSorter
- ListZone
- .leaf
- config_editor.py
- WaveGrid
- .renumber
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeOut
- ask_to_quit
- Replay
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- Table
- AnimationManager
- FileStream
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- paint_panel
- Map
- Kalman
- .__init__
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- _PollUnpacker
- Camera
- GrowingButton
- DenseMesh
- flusher.py
- Draw
- DockArea
- Overlay
- NoteBrowser
- DragHandle
- Panes
- .restyle
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- walk
- Process
- .material_control
- align_decimals
- .slider
- _Dim
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
- .populate_filter_overlay
- Panel
- _Chip
- Proximity
- .arrow
- ShiftWheel
- .fill_base
- TabStrip
- on_activated
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- FadeIn
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- fade_in
- _OnHide
- .save_current_page
- MenuBar
- CLAUDE.md
- .collect
- ._scan_for_networks
- WorkspaceButton
- Telemetry
- panel
- .authored_weights
- .prepare_page_config
- .play
- Visuals
- ap_commands.py
- ResetCurrentPageToDefaults
- _Grip
- PopupWindow
- Builder
- .integer
- frame_callback
- DropZone
- .build_description_tab
- APPoller
- .__init__
- WifiForm
- pyside6_qtwidgets
- .__init__
- ModeForm
- PreferencesData
- .new_tab

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

## Communities (212 total, 135 thin omitted)

### Community 0 - ".__init__"
Cohesion: 0.06
Nodes (5): GoBackToPreviousPage, OpenPauseMenu, RefreshCurrentPage, _FollowResize, _RightZoneRoom

### Community 1 - "MetaPacket"
Cohesion: 0.04
Nodes (7): Channel, _default_gateway_ip(), NetworkGraph, PacketBuffer, Transaction, TransactionManager, MetaPacket

### Community 2 - "Sniffer"
Cohesion: 0.07
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.05
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (7): on_change(), checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "ContextManager"
Cohesion: 0.11
Nodes (9): ContextManager, BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page, TriangleCanvas (+1 more)

### Community 9 - "Scrollable"
Cohesion: 0.06
Nodes (6): Scrollable, Builder, Builder, FlagsExample, RegistersExample, Builder

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 15 - "ToggleButton"
Cohesion: 0.03
Nodes (12): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, SetCurrentPageAsFavorite, ToggleBookmark, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen (+4 more)

### Community 16 - "geometry.py"
Cohesion: 0.09
Nodes (11): canvas_fit(), padded_fit(), affine(), apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale() (+3 more)

### Community 19 - "Router"
Cohesion: 0.12
Nodes (3): App, Router, __getattr__()

### Community 23 - "time"
Cohesion: 0.06
Nodes (4): Buffer, _is_global(), _resolve_local_mac(), RetentionPolicy

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "VisualPalette"
Cohesion: 0.12
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 26 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 29 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 30 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 31 - "FlowLayout"
Cohesion: 0.07
Nodes (3): FlowLayout, _Gaps, Builder

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 40 - "ModbusBuffer"
Cohesion: 0.06
Nodes (4): DefenderMapBuffer, HouseBuffer, ModbusBuffer, MapBuffer

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
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 49 - "host.py"
Cohesion: 0.07
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 51 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 59 - "SlidersForm"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (13): add_tab(), find(), from_tree(), split(), leaf(), move_panel(), new_id(), normalize() (+5 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 69 - "Canvas"
Cohesion: 0.12
Nodes (4): Canvas, DefenderWorldMap, House, WorldMap

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 72 - "menu_bar.py"
Cohesion: 0.04
Nodes (18): ButtonGroup, offered_sections(), ShowHelpMessage, bare_icon(), global_buttons(), icon_button(), bar_button_height(), CornerControls (+10 more)

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.18
Nodes (10): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+2 more)

### Community 83 - ".renumber"
Cohesion: 0.19
Nodes (3): delete(), create(), rename()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

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

### Community 98 - "FileStream"
Cohesion: 0.09
Nodes (4): _dialog_parent(), file_dialog(), Paths, FileStream

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
Cohesion: 0.13
Nodes (3): Camera, padded_fit_uniform(), zoom_and_pan()

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 113 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 117 - "Overlay"
Cohesion: 0.05
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 120 - "DragHandle"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), WorkspaceChip, DragHandle

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 128 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 129 - "walk"
Cohesion: 0.12
Nodes (5): visit(), drain_evenly(), is_split(), panel_ids(), walk()

### Community 130 - "Process"
Cohesion: 0.04
Nodes (6): random_spline_path(), NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue, ProcessManager, Process

### Community 133 - "align_decimals"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 137 - "style.py"
Cohesion: 0.14
Nodes (10): button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+2 more)

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (35): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+27 more)

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 150 - "Panel"
Cohesion: 0.04
Nodes (21): NetworkDiagramCanvas, StripChart, ChartsExample, ControlsExample, HouseExample, MapExample, NetworkExample, PassWheel (+13 more)

### Community 158 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 175 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 184 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 186 - "ap_commands.py"
Cohesion: 0.14
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+8 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "PopupWindow"
Cohesion: 0.07
Nodes (6): make(), _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, message(), PopupWindow

### Community 195 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 203 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "pyside6_qtwidgets"
Cohesion: 0.13
Nodes (11): ShiftWheelSlider, BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+3 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1784 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Process`, `InputManager`, `style.py`, `PageManager`, `pyside6_qtcore`, `important_buttons/__init__.py`, `Router`, `GoForwardToNextPage`, `Panel`, `time`, `ShiftWheel`, `CheckboxOverlay`, `Performance`, `LocalizationManager`, `host.py`, `.reset_page`, `Json`, `KeyBinds`, `docking.py`, `Canvas`, `menu_bar.py`, `PrivilegedHelper`, `Preferences`, `config_editor.py`, `pyside6_qtwidgets`, `AnimationManager`, `FileStream`, `.start_session`, `Overlay`, `Style`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.06025641025641026 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `SettingsSection`, `ContextManager`, `style.py`, `.start_session`, `._build_stylesheet`, `menu_bar.py`, `.theme_family`, `.set_theme`, `.css`, `important_buttons/__init__.py`, `.discard_changes`, `Overlay`, `time`, `.restyle`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.04336043360433604 - nodes in this community are weakly interconnected._