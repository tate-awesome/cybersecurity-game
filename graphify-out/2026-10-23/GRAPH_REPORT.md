# Graph Report - cybersecurity-game  (2026-10-23)

## Corpus Check
- 315 files · ~265,925 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4798 nodes · 10134 edges · 237 communities (81 shown, 156 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 507 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e59732e9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- time
- MetaPacket
- PacketBuffer
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- MaterialEditor
- FilterOverlay
- ._build_stylesheet
- PageManager
- .__init__
- packet_filter.py
- PacketColumnsOverlay
- App
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- server.py
- FindBar
- Kernel
- MenuBar
- SessionRecorder
- ViewPort
- PacketTreeview
- ContextManager
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- describe.py
- WorkspaceSelectPage
- Camera
- .__init__
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- channels/__init__.py
- Runtime Requirements
- TabStrip
- ModbusBuffer
- PrivilegedHelper
- ConfigEditor
- DropZone
- RecordFilter
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- .__init__
- Modify
- .strip_chart_layout
- Router
- .fill_base
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- SettingsPage
- palette_generator.py
- pyside6_qtcore
- NetFilterQueue
- Constellation
- Preferences
- record_schema.py
- ._draw_text
- WorkspaceSorter
- DragHandle
- .leaf
- WindowControls
- WaveGrid
- paint_mark
- Overlay
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- SlidersForm
- Replay
- _Dim
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- StatusBuffer
- AnimationManager
- Canvas
- Prod/Host_API.py
- ModBus HVAC Exercise Screenshot
- Camera
- .collapsed
- Draw
- Kalman
- SampleNetwork
- WorkspaceChip
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- GrowingButton
- NewWorkspaceDialog
- _SaveLayoutAsDefault
- Draw
- SectionCard
- QWidget
- CycleBox
- NoteBrowser
- MaterialEditorPopup
- geometry.py
- Panes
- .apply_theme
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- APPoller
- NMapper
- ToggleButton
- bare_icon
- WindowBarButton
- on_activated
- themes.py
- PooledCanvasMixin
- link.py
- DefenderHVACChart
- .__init__
- .css
- important_buttons/__init__.py
- ProcessManager
- Meter
- _Chip
- MitmTable
- .visible_arrow
- ShiftWheel
- SummaryDrawer
- ComboColumn
- compile_filter
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Telemetry
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- paint_panel
- Map
- .save_current_page
- WindowEdges
- DockArea
- CLAUDE.md
- columns_overlay.py
- .collect
- ._scan_for_networks
- .__init__
- Loader
- SettingsSection
- Builder
- .page_panel_keys
- .authored_weights
- WindowDrag
- ap_commands.py
- .integer
- .__init__
- PopupWindow
- .build_description_tab
- fade_in
- _DropPreview
- CheckboxOverlay
- _Indicator
- WorkspaceButton
- DragPayload
- StreamIncomingPacketsToMcap
- ToggleDebugLabels
- .__init__
- FreeScrollStatusConsole
- WifiForm
- _OnHide
- OpenFavoritePage
- ModeForm
- Builder
- PausePacketConsole
- ToggleFullscreen
- _DrawerLayout
- ToggleLightDarkMode
- router.py
- VisualPalette
- ToggleNetworkGraphRingView
- ToggleBookmark
- .fixed_width_wrapper
- ToggleStripChartAutoFit
- .new_tab
- ToggleWorkspaceBackground
- SampleSubmarine
- modbus_function
- to_state
- flusher.py
- PreferencesData
- .make_built_in

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 141 edges
2. `ImportantButton` - 114 edges
3. `Style` - 100 edges
4. `Overlay` - 93 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
7. `MetaPacket` - 63 edges
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
- 3-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 4-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 4-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/transaction_manager.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/hvac_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/modbus.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/network_graph.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/packet.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/submarine_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/saved/__init__.py -> game/src/network/saved/file_stream.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`

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

## Communities (237 total, 156 thin omitted)

### Community 0 - "time"
Cohesion: 0.04
Nodes (6): random_spline_path(), Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 2 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 16 - "packet_filter.py"
Cohesion: 0.16
Nodes (9): Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes(), tokenize() (+1 more)

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsOverlay, autosave()

### Community 23 - "server.py"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 30 - "ContextManager"
Cohesion: 0.05
Nodes (36): ContextManager, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, WorldMap, form_order() (+28 more)

### Community 31 - "FlowLayout"
Cohesion: 0.06
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.06
Nodes (9): Table, fill_order(), key(), spread_order(), VariableOverlay, autosave(), reset_all(), CombinedTable (+1 more)

### Community 37 - "describe.py"
Cohesion: 0.10
Nodes (24): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+16 more)

### Community 40 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 44 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "channels/__init__.py"
Cohesion: 0.10
Nodes (3): DefenderMapBuffer, _is_global(), _resolve_local_mac()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 48 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 49 - "PrivilegedHelper"
Cohesion: 0.05
Nodes (14): build_name(), main(), write_build_info(), BuildInfo, git(), PrivilegedHelper, _Proxy, HelperHandle (+6 more)

### Community 53 - "RecordFilter"
Cohesion: 0.13
Nodes (4): decode(), dumps(), header(), RecordFilter

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - ".__init__"
Cohesion: 0.04
Nodes (9): Builder, ControlsExample, PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SamplePackets, SampleWorldMap (+1 more)

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 66 - "docking.py"
Cohesion: 0.16
Nodes (15): add_tab(), find(), is_split(), leaf(), leaf_of(), move_panel(), new_id(), normalize() (+7 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (12): conjugate(), quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+4 more)

### Community 76 - "record_schema.py"
Cohesion: 0.14
Nodes (7): link_of(), action(), mark(), packet(), packet_from_meta(), raw_bytes(), status()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.11
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 83 - "paint_mark"
Cohesion: 0.10
Nodes (5): bar_inset(), _LentPlaceholder, paint_mark(), PeekArrow, _SideTitle

### Community 84 - "Overlay"
Cohesion: 0.04
Nodes (21): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, SelectBackground, SelectColorTheme, EditBackgroundChoices (+13 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 92 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 99 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "Camera"
Cohesion: 0.09
Nodes (8): canvas_fit(), padded_fit(), affine(), Camera, padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 106 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 112 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 120 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 129 - "APPoller"
Cohesion: 0.07
Nodes (3): APPoller, Denier, Sniffer

### Community 130 - "NMapper"
Cohesion: 0.13
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 135 - "WindowBarButton"
Cohesion: 0.18
Nodes (3): minimized_thickness(), bar_button_height(), WindowBarButton

### Community 136 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 143 - ".__init__"
Cohesion: 0.15
Nodes (3): encryption_enabled(), EncryptionForm, stop_encryption()

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (43): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs (+35 more)

### Community 158 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 167 - "paint_panel"
Cohesion: 0.14
Nodes (3): _SideStrip, paint_panel(), surface_shadow()

### Community 173 - "columns_overlay.py"
Cohesion: 0.12
Nodes (6): BinZone, column_position(), is_column_available(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault

### Community 175 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 184 - "WindowDrag"
Cohesion: 0.12
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowDrag

### Community 186 - "ap_commands.py"
Cohesion: 0.16
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+7 more)

### Community 189 - ".__init__"
Cohesion: 0.12
Nodes (5): from_tree(), split(), _Grip, _SashGrip, _ShadowWatch

### Community 190 - "PopupWindow"
Cohesion: 0.13
Nodes (3): start_encryption(), message(), PopupWindow

### Community 195 - "CheckboxOverlay"
Cohesion: 0.11
Nodes (6): ListZone, PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 203 - ".__init__"
Cohesion: 0.09
Nodes (6): frame_callback(), sprite(), sprite_enabled(), frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 218 - "router.py"
Cohesion: 0.10
Nodes (8): apply_scale_about(), BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page

### Community 219 - "VisualPalette"
Cohesion: 0.10
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 230 - "modbus_function"
Cohesion: 0.50
Nodes (4): modbus_function(), modbus_info(), modbus_summary(), register_values()

### Community 232 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1898 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **156 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `time`, `InputManager`, `PageManager`, `important_buttons/__init__.py`, `.start_session`, `ProcessManager`, `ShiftWheel`, `Performance`, `LocalizationManager`, `channels/__init__.py`, `columns_overlay.py`, `PrivilegedHelper`, `Json`, `KeyBinds`, `Router`, `docking.py`, `CheckboxOverlay`, `pyside6_qtcore`, `.reload_preferences`, `Preferences`, `Overlay`, `router.py`, `VisualPalette`, `AnimationManager`, `.reset_page`, `Style`?**
  _High betweenness centrality (0.240) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `time` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `SettingsSection`, `pyside6_qtcore`, `._build_stylesheet`, `.theme_family`, `.preset_name`, `.css`, `important_buttons/__init__.py`, `.start_session`, `.discard_changes`, `QWidget`, `Overlay`, `.apply_theme`, `ContextManager`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._