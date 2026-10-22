# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 307 files · ~248,153 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4436 nodes · 9333 edges · 221 communities (76 shown, 145 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 473 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4aed7e33`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CornerControls
- MetaPacket
- server.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- .__init__
- settings_overlay_button.py
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- geometry.py
- WindowDrag
- .__init__
- .__init__
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- Kernel
- .__init__
- SessionRecorder
- ViewPort
- PacketTreeview
- menu_bar.py
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- NMapper
- SummaryDrawer
- Camera
- ModbusBuffer
- LocalizationManager
- PopupEntrance
- HostOverlay
- ArpSpoofer
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
- DefenderModbusBuffer
- docking.py
- time
- StripChartBase
- Builder
- palette_generator.py
- App
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- VariableOverlay
- WorkspaceSorter
- ElidingLabel
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
- _Indicator
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- Panes
- AnimationManager
- router.py
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- WindowBarButton
- _MapCanvas
- Kalman
- DockArea
- Defender Full Suite Exercise Screenshot
- typing
- .new_tab
- Camera
- GrowingButton
- context_manager.py
- Draw
- align_decimals
- .target_at
- Overlay
- ContextManager
- .fill_base
- WorkspaceChip
- .__init__
- open_favorite_page.py
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- .collapsed
- APPoller
- .__init__
- PopupWindow
- place
- SettingsSection
- _Dim
- .__init__
- themes.py
- PooledCanvasMixin
- VisualPalette
- WorkspaceSelectPage
- _DrawerLayout
- DefenderHVACChart
- NoteBrowser
- .brush
- important_buttons/__init__.py
- DropZone
- Meter
- Builder
- .populate_filter_overlay
- .__init__
- _Chip
- bare_icon
- core/transforms.py
- ShiftWheel
- Prod/Host_API.py
- TabStrip
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- .restyle
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- packet_console/_builder.py
- .save_current_page
- MenuBar
- CLAUDE.md
- Attack
- .collect
- ._scan_for_networks
- surface_shadow
- .__init__
- .authored_weights
- .prepare_page_config
- PacketBuffer
- ap_commands.py
- .slider
- SampleNetwork
- _Grip
- confirm_dialog
- frame_callback
- .__init__
- Builder
- Telemetry
- BuildInfo
- DragHandle
- .renumber
- .build_description_tab
- fade_in
- SelectRegisterPreset
- _OnHide
- WifiForm
- WorkspaceButton
- SelectBackground
- ModeForm
- frame_callback
- widgets/__init__.py
- SampleHVAC
- PreferencesData
- .new_tab

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

## Communities (221 total, 145 thin omitted)

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
Nodes (6): on_change(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "settings_overlay_button.py"
Cohesion: 0.10
Nodes (7): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, checked_value(), SettingsOverlayButton

### Community 12 - ".__init__"
Cohesion: 0.16
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), ring_spots()

### Community 15 - "ToggleButton"
Cohesion: 0.03
Nodes (10): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView (+2 more)

### Community 16 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 17 - "WindowDrag"
Cohesion: 0.12
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowDrag

### Community 23 - "threading"
Cohesion: 0.08
Nodes (5): Buffer, NetFilterQueueBaseClass, ProcessManager, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - ".__init__"
Cohesion: 0.07
Nodes (8): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns, EditModbusRegisterDisplay, EditNetworkHosts

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+5 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 30 - "menu_bar.py"
Cohesion: 0.07
Nodes (12): ButtonGroup, offered_sections(), ask_to_quit(), QuitApplication, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage, global_buttons() (+4 more)

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 37 - "NMapper"
Cohesion: 0.07
Nodes (5): NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 40 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.09
Nodes (4): _Peek, _SideStrip, TabbedPane, paint_panel()

### Community 49 - "launch.py"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.11
Nodes (5): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems(), delete()

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "SlidersForm"
Cohesion: 0.14
Nodes (4): push_submarine_settings(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 67 - "time"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 77 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.19
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), write_config_values() (+1 more)

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

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

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "router.py"
Cohesion: 0.11
Nodes (8): BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page, Map

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 102 - "WindowBarButton"
Cohesion: 0.19
Nodes (3): bar_button_height(), WindowBarButton, WindowControls

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 113 - "context_manager.py"
Cohesion: 0.13
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 115 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 118 - "ContextManager"
Cohesion: 0.10
Nodes (10): ContextManager, apply_scale_about(), BaseForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm (+2 more)

### Community 119 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 120 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 126 - "Wifi"
Cohesion: 0.10
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 131 - ".__init__"
Cohesion: 0.09
Nodes (6): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideTitle

### Community 133 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 137 - "themes.py"
Cohesion: 0.14
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "VisualPalette"
Cohesion: 0.10
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (33): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+25 more)

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 150 - ".__init__"
Cohesion: 0.08
Nodes (7): ControlsExample, PassWheel, SampleHouse, SampleNetworkDiagram, SamplePackets, SampleSubmarine, SampleWorldMap

### Community 153 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 156 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 167 - "packet_console/_builder.py"
Cohesion: 0.27
Nodes (3): compile_packet_filter(), FilterOverlay, FilterPacketConsole

### Community 173 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 181 - ".__init__"
Cohesion: 0.27
Nodes (5): encryption_enabled(), set_encryption(), EncryptionForm, start_encryption(), stop_encryption()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 184 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 186 - "ap_commands.py"
Cohesion: 0.15
Nodes (13): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), set_ap_tunnel(), set_hvac_kalman() (+5 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.08
Nodes (7): DeleteAllUserData, DeleteAllWorkspaceSavedData, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, confirm_dialog(), message()

### Community 191 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 214 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 215 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (21): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, WorldMap, Scrollable (+13 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1765 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **145 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `settings_overlay_button.py`, `PageManager`, `VisualPalette`, `important_buttons/__init__.py`, `threading`, `ShiftWheel`, `.__init__`, `menu_bar.py`, `Performance`, `packet_console/_builder.py`, `LocalizationManager`, `.start_session`, `.reset_page`, `Json`, `KeyBinds`, `confirm_dialog`, `Router`, `docking.py`, `time`, `PrivilegedHelper`, `Preferences`, `config_editor.py`, `widgets/__init__.py`, `AnimationManager`, `router.py`, `.apply_theme`, `typing`, `context_manager.py`, `open_favorite_page.py`, `Style`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0783673469387755 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.restyle`, `SettingsSection`, `settings_overlay_button.py`, `.apply_theme`, `._build_stylesheet`, `.theme_family`, `.brush`, `context_manager.py`, `.start_session`, `.discard_changes`, `important_buttons/__init__.py`, `Overlay`, `ContextManager`, `open_favorite_page.py`, `menu_bar.py`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._