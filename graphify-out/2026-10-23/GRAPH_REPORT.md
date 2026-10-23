# Graph Report - cybersecurity-game  (2026-10-23)

## Corpus Check
- 326 files · ~276,431 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4839 nodes · 10221 edges · 231 communities (90 shown, 141 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 509 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d0cc46de`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- threading
- MetaPacket
- PacketBuffer
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- Draw
- FilterOverlay
- ._build_stylesheet
- PageManager
- .__init__
- window_chrome.py
- packet_filter.py
- PacketColumnsOverlay
- app.py
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- VisualPalette
- MenuBar
- SessionRecorder
- ViewPort
- PacketTreeview
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- describe.py
- to_state
- Camera
- .__init__
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- pyside6_qtwidgets
- Runtime Requirements
- TabStrip
- MapBuffer
- launch.py
- ConfigEditor
- Overlay
- Denier
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
- ContextManager
- NetFilterQueue
- PrivilegedHelper
- Constellation
- Preferences
- geometry.py
- ._draw_text
- WorkspaceSorter
- DragHandle
- .leaf
- WaveGrid
- paint_mark
- RefreshCurrentPage
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- SlidersForm
- Replay
- pause_menu.py
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- StatusBuffer
- AnimationManager
- Canvas
- file_dialog
- ModBus HVAC Exercise Screenshot
- DropZone
- DockArea
- Kalman
- SampleNetwork
- WorkspaceChip
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- ToggleBookmark
- .__init__
- GrowingButton
- open_in_browser
- VariableOverlay
- Draw
- bare_icon
- QWidget
- CycleBox
- NoteBrowser
- NewWorkspaceDialog
- Camera
- Panes
- .restyle
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- WorkspaceSelectPage
- NMapper
- _Peek
- router.py
- config_editor.py
- Builder
- _Indicator
- is_column_available
- themes.py
- PooledCanvasMixin
- WindowEdges
- dist.py
- BuildInfo
- DefenderHVACChart
- on_activated
- important_buttons/__init__.py
- ask_to_quit
- DenseMesh
- .__init__
- Meter
- widgets/__init__.py
- _Chip
- ShiftWheel
- SummaryDrawer
- ComboColumn
- compile_filter
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Telemetry
- Prod/Host_API.py
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- paint_panel
- Map
- .save_current_page
- .target_at
- CLAUDE.md
- DragPayload
- .collect
- ._scan_for_networks
- .__init__
- menu_bar.py
- SettingsSection
- Scanlines
- .page_panel_keys
- .authored_weights
- WindowControls
- APPoller
- ap_commands.py
- .integer
- .brush
- _Grip
- _base_button.py
- .build_description_tab
- SampleSubmarine
- .__init__
- modbus_panel/_builder.py
- _PollUnpacker
- _SaveLayoutAsDefault
- core/transforms.py
- ToggleButton
- Builder
- combined.py
- Table
- WifiForm
- _RightZoneRoom
- host.py
- fade_in
- _DrawerLayout
- WorkspaceButton
- Visual
- frame_callback
- MitmTable
- .new_tab
- frame_callback
- ProcessManager
- os
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 142 edges
2. `ImportantButton` - 114 edges
3. `Style` - 108 edges
4. `Overlay` - 93 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
7. `MetaPacket` - 63 edges
8. `ConfigEditor` - 58 edges
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

## Communities (231 total, 141 thin omitted)

### Community 0 - "threading"
Cohesion: 0.09
Nodes (4): Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 1 - "MetaPacket"
Cohesion: 0.06
Nodes (7): Channel, ModbusBuffer, Transaction, TransactionManager, MetaPacket, _resolve_local_mac(), Builder

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

### Community 15 - "window_chrome.py"
Cohesion: 0.11
Nodes (7): bar_button_height(), draw_window_bar_line(), SquareButtons, _Strip, window_bar_height(), window_bar_room(), WindowBarButton

### Community 16 - "packet_filter.py"
Cohesion: 0.16
Nodes (9): Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes(), tokenize() (+1 more)

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.11
Nodes (4): RowZone, column_category(), PacketColumnsOverlay, autosave()

### Community 20 - "ThemeEditorPage"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, MaterialEditor, preview(), ThemeEditorPage

### Community 23 - "time"
Cohesion: 0.07
Nodes (12): random_spline_path(), Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run() (+4 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "VisualPalette"
Cohesion: 0.08
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 31 - "FlowLayout"
Cohesion: 0.06
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 37 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "pyside6_qtwidgets"
Cohesion: 0.16
Nodes (11): BaseForm, ModeForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+3 more)

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 48 - "MapBuffer"
Cohesion: 0.06
Nodes (3): DefenderMapBuffer, HouseBuffer, MapBuffer

### Community 49 - "launch.py"
Cohesion: 0.15
Nodes (8): git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 51 - "Overlay"
Cohesion: 0.05
Nodes (9): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SelectRegisterPreset, SettingsOverlayButton, Overlay (+1 more)

### Community 59 - ".__init__"
Cohesion: 0.07
Nodes (7): ControlsExample, PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SamplePackets, SampleWorldMap

### Community 62 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 64 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "ContextManager"
Cohesion: 0.11
Nodes (4): ContextManager, apply_scale_about(), _is_global(), ChooseShownPacketConsoleColumns

### Community 76 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (5): SectionCard, WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 83 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 84 - "RefreshCurrentPage"
Cohesion: 0.24
Nodes (3): RefreshCurrentPage, EditWorkspaceAvailability, RefreshAndCloseOverlay

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.16
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 91 - "Replay"
Cohesion: 0.07
Nodes (4): dissect(), link_of(), RecordFilter, Replay

### Community 92 - "pause_menu.py"
Cohesion: 0.08
Nodes (7): GoBackToPreviousPage, ShowHelpMessage, _Dim, _Drawer, _FollowResize, _OnHide, toggle_maximized()

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "Canvas"
Cohesion: 0.12
Nodes (4): Canvas, DefenderWorldMap, House, WorldMap

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 106 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 110 - ".__init__"
Cohesion: 0.05
Nodes (3): LinkToPage, OpenFavoritePage, ToggleDebugLabels

### Community 112 - "open_in_browser"
Cohesion: 0.14
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 113 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 116 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 119 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 122 - ".restyle"
Cohesion: 0.12
Nodes (3): _DressedWidgets, _StyledComboItems, StyleSignals

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 130 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 132 - "router.py"
Cohesion: 0.06
Nodes (11): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page (+3 more)

### Community 133 - "config_editor.py"
Cohesion: 0.14
Nodes (11): conjugate(), quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+3 more)

### Community 136 - "is_column_available"
Cohesion: 0.16
Nodes (5): column_position(), is_column_available(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault

### Community 137 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 140 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 143 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (24): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay (+16 more)

### Community 148 - ".__init__"
Cohesion: 0.32
Nodes (4): encryption_enabled(), set_encryption(), start_encryption(), stop_encryption()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (18): NetworkDiagramCanvas, StripChart, Scrollable, panel(), Builder, ChartsExample, FlagsExample, HouseExample (+10 more)

### Community 158 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 167 - "paint_panel"
Cohesion: 0.13
Nodes (3): _one_shadow(), paint_panel(), surface_shadow()

### Community 175 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 178 - "menu_bar.py"
Cohesion: 0.08
Nodes (7): developer_text(), ButtonGroup, offered_sections(), ConfigureThisWorkspace, DeleteAllUserData, GoForwardToNextPage, SaveLayoutShapeAsDefault

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.18
Nodes (14): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), set_ap_tunnel() (+6 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "_base_button.py"
Cohesion: 0.06
Nodes (9): make(), ClearSavedWorkspaceInputs, DeleteAllWorkspaceSavedData, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton, confirm_dialog(), message() (+1 more)

### Community 194 - ".__init__"
Cohesion: 0.28
Nodes (3): covered(), settle(), uncovered()

### Community 195 - "modbus_panel/_builder.py"
Cohesion: 0.11
Nodes (7): ListZone, PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 201 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 202 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 205 - "combined.py"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 206 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 219 - "Visual"
Cohesion: 0.11
Nodes (4): draw_vessel(), nice_number(), nice_ticks(), Visual

### Community 221 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 225 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 232 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1915 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **141 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `threading`, `MetaPacket`, `InputManager`, `router.py`, `config_editor.py`, `PageManager`, `window_chrome.py`, `important_buttons/__init__.py`, `widgets/__init__.py`, `ShiftWheel`, `Performance`, `.save_current_page`, `LocalizationManager`, `pyside6_qtwidgets`, `menu_bar.py`, `Overlay`, `Json`, `KeyBinds`, `_base_button.py`, `Router`, `docking.py`, `modbus_panel/_builder.py`, `PrivilegedHelper`, `Preferences`, `combined.py`, `host.py`, `Visual`, `pause_menu.py`, `AnimationManager`, `Canvas`, `ProcessManager`, `.__init__`, `Style`?**
  _High betweenness centrality (0.233) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `threading` be split into smaller, more focused modules?**
  _Cohesion score 0.0851063829787234 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `SettingsSection`, `.setting`, `ContextManager`, `._build_stylesheet`, `.preset_name`, `.theme_family`, `.__init__`, `QWidget`, `.discard_changes`, `Overlay`, `.apply_theme`, `menu_bar.py`, `.restyle`, `.brush`, `_base_button.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.05555555555555555 - nodes in this community are weakly interconnected._