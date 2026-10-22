# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 305 files · ~245,434 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4384 nodes · 9234 edges · 215 communities (77 shown, 138 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 473 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `007df75b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- MetaPacket
- server.py
- Footer
- InputManager
- .add_row
- PauseMenu
- VisualBackground
- PopupWindow
- master.py
- ._build_stylesheet
- PageManager
- PacketBuffer
- SettingsPage
- ToggleButton
- Visual
- menu_bar.py
- MenuBar
- widgets/__init__.py
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- .__init__
- SessionRecorder
- ViewPort
- PacketTreeview
- .__init__
- ModbusBuffer
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- NetFilterQueue
- SummaryDrawer
- Camera
- time
- .__init__
- LocalizationManager
- PopupEntrance
- HostOverlay
- Runtime Requirements
- StatusBuffer
- sys
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
- .__init__
- Modify
- .strip_chart_layout
- Router
- DefenderModbusBuffer
- docking.py
- _SaveLayoutAsDefault
- StripChartBase
- Builder
- palette_generator.py
- open_favorite_page.py
- app.py
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- VariableOverlay
- WorkspaceSorter
- TabStrip
- .leaf
- CallbackRegistry
- WaveGrid
- Dev/Host_API.py
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
- transitions.py
- Attack
- AnimationManager
- WorkspaceSelectPage
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- pyside6_qtcore
- _MapCanvas
- Kalman
- walk
- Defender Full Suite Exercise Screenshot
- .fill_base
- Camera
- GrowingButton
- Draw
- _Dim
- Draw
- MainWindow
- .target_at
- ContextManager
- Overlay
- WorkspaceChip
- ProcessManager
- Prod/Host_API.py
- Master
- Style
- AppearEffect
- Wifi
- Slave
- WindowEdges
- Panes
- QWidget
- Loader
- SettingsSection
- DockArea
- .__init__
- style.py
- PooledCanvasMixin
- .add_header
- .__init__
- Builder
- DefenderHVACChart
- important_buttons/__init__.py
- .add_section
- Meter
- .populate_filter_overlay
- .__init__
- _Chip
- .page_panel_keys
- ShiftWheel
- fade_in
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- NetFilterQueue
- context_manager.py
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- ArpSpoofer
- WorkspaceButton
- .save_current_page
- router.py
- CLAUDE.md
- .arrow
- SampleNetwork
- ._scan_for_networks
- NMapper
- .build_description_tab
- frame_callback
- paint_panel
- Table
- .authored_weights
- align_decimals
- save_layout_as_default.py
- ap_commands.py
- .material_control
- _Grip
- confirm_dialog
- DenseMesh
- APPoller
- _DrawerLayout
- Telemetry
- InterfaceManager
- DragHandle
- _GlobalClickFilter
- .__init__
- .play
- WifiForm
- _Drawer
- SampleHVAC
- .integer
- Scrollable
- .__init__
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

## Communities (215 total, 138 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.05
Nodes (15): canvas_fit(), padded_fit(), affine(), apply_scale_about(), scale(), translate(), Canvas, padded_fit_uniform() (+7 more)

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 5 - ".add_row"
Cohesion: 0.10
Nodes (6): on_change(), checked_value(), is_checked(), save(), save(), on_change()

### Community 8 - "PopupWindow"
Cohesion: 0.11
Nodes (3): make(), message(), PopupWindow

### Community 12 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 15 - "ToggleButton"
Cohesion: 0.03
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit (+1 more)

### Community 16 - "Visual"
Cohesion: 0.09
Nodes (7): draw_vessel(), get_arc_points(), get_bearing(), rotate(), nice_number(), nice_ticks(), Visual

### Community 17 - "menu_bar.py"
Cohesion: 0.04
Nodes (19): developer_text(), ButtonGroup, offered_sections(), ShowHelpMessage, bare_icon(), global_buttons(), icon_button(), bar_button_height() (+11 more)

### Community 20 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (16): NetworkDiagramCanvas, StripChart, compile_packet_filter(), panel(), Builder, HouseExample, MapExample, NetworkExample (+8 more)

### Community 23 - "threading"
Cohesion: 0.05
Nodes (8): flush(), flush_all(), run(), Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "VisualPalette"
Cohesion: 0.10
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 26 - ".__init__"
Cohesion: 0.06
Nodes (8): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns, FilterOverlay, FilterPacketConsole

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (11): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+3 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 30 - ".__init__"
Cohesion: 0.05
Nodes (5): GoBackToPreviousPage, GoForwardToNextPage, ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 31 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 41 - ".__init__"
Cohesion: 0.15
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place()

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "sys"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (14): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+6 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 72 - "app.py"
Cohesion: 0.11
Nodes (3): App, WindowReveal, __getattr__()

### Community 77 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 79 - "TabStrip"
Cohesion: 0.09
Nodes (4): paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

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

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 102 - "pyside6_qtcore"
Cohesion: 0.09
Nodes (10): PreferencesData, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+2 more)

### Community 105 - "walk"
Cohesion: 0.12
Nodes (4): visit(), is_split(), panel_ids(), walk()

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 108 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 113 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 118 - "ContextManager"
Cohesion: 0.15
Nodes (11): ContextManager, BaseForm, ModeForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+3 more)

### Community 119 - "Overlay"
Cohesion: 0.04
Nodes (12): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+4 more)

### Community 122 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 131 - "QWidget"
Cohesion: 0.09
Nodes (5): bar_inset(), _LentPlaceholder, minimized_thickness(), _SideStrip, TabbedPane

### Community 137 - "style.py"
Cohesion: 0.11
Nodes (12): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme() (+4 more)

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (31): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, ConfigureThisWorkspace (+23 more)

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "context_manager.py"
Cohesion: 0.13
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 171 - "router.py"
Cohesion: 0.09
Nodes (8): BoatMotion, Sprites, Triangle, Visuals, WorkspacePage, NotFound, Page, Map

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 179 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 180 - "paint_panel"
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 181 - "Table"
Cohesion: 0.33
Nodes (3): Table, fill_order(), key()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 184 - "align_decimals"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 186 - "ap_commands.py"
Cohesion: 0.12
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.06
Nodes (8): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, WorkspaceSaveResetButton, confirm_dialog()

### Community 203 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 204 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 219 - "Scrollable"
Cohesion: 0.12
Nodes (3): _Gaps, Scrollable, ChartsExample

### Community 220 - ".__init__"
Cohesion: 0.10
Nodes (7): FlagsExample, PassWheel, SampleHouse, SampleNetworkDiagram, SamplePackets, SampleSubmarine, SampleWorldMap

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1749 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **138 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `Footer`, `InputManager`, `.start_session`, `style.py`, `PageManager`, `Visual`, `important_buttons/__init__.py`, `menu_bar.py`, `widgets/__init__.py`, `threading`, `ShiftWheel`, `.__init__`, `.__init__`, `Performance`, `context_manager.py`, `time`, `LocalizationManager`, `router.py`, `Json`, `KeyBinds`, `save_layout_as_default.py`, `confirm_dialog`, `Router`, `.reset_page`, `docking.py`, `open_favorite_page.py`, `PrivilegedHelper`, `Preferences`, `host.py`, `CallbackRegistry`, `AnimationManager`, `pyside6_qtcore`, `.apply_theme`, `Overlay`, `ProcessManager`, `Style`?**
  _High betweenness centrality (0.254) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.053544494720965306 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.set_theme`, `context_manager.py`, `.start_session`, `open_favorite_page.py`, `style.py`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `.css`, `important_buttons/__init__.py`, `.discard_changes`, `menu_bar.py`, `ContextManager`, `Overlay`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07616892911010557 - nodes in this community are weakly interconnected._