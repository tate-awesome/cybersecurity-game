# Graph Report - cybersecurity-game  (2026-10-20)

## Corpus Check
- 304 files · ~234,836 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4123 nodes · 8714 edges · 207 communities (72 shown, 135 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 457 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0e43432`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Visual
- MetaPacket
- server.py
- Footer
- .apply_theme
- SettingsSection
- PauseMenu
- VisualBackground
- WindowBarButton
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- PacketBuffer
- CheckboxOverlay
- visuals/__init__.py
- MapBuffer
- Dev/Host_API.py
- DockArea
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- SessionRecorder
- ViewPort
- PacketTreeview
- NetFilterQueue
- LayoutEditor
- Performance
- flusher.py
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- LocalizationManager
- QWidget
- _DrawerLayout
- Runtime Requirements
- StatusBuffer
- PrivilegedHelper
- ConfigEditor
- ModbusBuffer
- Prod/Host_API.py
- .collect
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- Modify
- time_core/transforms.py
- Router
- session_recorder.py
- buffer_manager.py
- walk
- MenuBar
- StripChartBase
- Canvas
- palette_generator.py
- bare_icon
- App
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- Draw
- VariableOverlay
- wifi_windows.py
- .leaf
- Attack
- WaveGrid
- add
- ThemeEditorPage
- SettingCell
- Rows
- config_editor.py
- ModBus Submarine Exercise Screenshot
- app.py
- WindowControls
- Replay
- .css
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- MitmTable
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- ap_commands.py
- .section
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- QWidget
- Camera
- .__init__
- _Dim
- Overlay
- MainWindow
- .target_at
- .populate_filter_overlay
- time
- WorkspaceChip
- APPoller
- NetFilterQueue
- Master
- Style
- AppearEffect
- Wifi
- Slave
- ArpSpoofer
- NMapper
- TabStrip
- NewWorkspaceDialog
- ProcessManager
- _Chip
- _SaveLayoutAsDefault
- themes.py
- PooledCanvasMixin
- overlay.py
- .arrow
- StreamIncomingPacketsToMcap
- DefenderHVACChart
- ListZone
- filter_overlay.py
- DropZone
- PopupWindow
- widgets/__init__.py
- InterfaceManager
- ContextManager
- SampleNetwork
- Builder
- time_core/transforms.py
- SampleSubmarine
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- .slider
- AnimationManager
- .fill_base
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- paint_panel
- .save_current_page
- GoForwardToNextPage
- examples.py
- CLAUDE.md
- SelectBackground
- ask_to_quit
- ._scan_for_networks
- menu_bar.py
- .build_description_tab
- ToggleFullscreen
- .authored_weights
- .prepare_page_config
- ToggleWorkspaceBackground
- _OnHide
- _Grip
- .integer
- frame_callback
- frame_callback
- DragHandle
- PreferencesData
- .key_column_width
- .__init__
- WifiForm
- SettingsPage
- ModeForm
- Panes

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 134 edges
2. `ImportantButton` - 108 edges
3. `Style` - 100 edges
4. `Overlay` - 84 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 62 edges
7. `MetaPacket` - 59 edges
8. `BaseForm` - 55 edges
9. `Panel` - 48 edges
10. `VisualPalette` - 48 edges

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

## Communities (207 total, 135 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.07
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

### Community 8 - "WindowBarButton"
Cohesion: 0.14
Nodes (3): CornerControls, WindowBarButton, WindowControls

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (39): AbortAllNetworkActions, ImportantButton, open_in_browser(), ToggleButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs (+31 more)

### Community 15 - "CheckboxOverlay"
Cohesion: 0.04
Nodes (9): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns, OpenFavoritePage, ToggleDebugLabels (+1 more)

### Community 16 - "visuals/__init__.py"
Cohesion: 0.08
Nodes (8): draw_vessel(), get_arc_points(), get_bearing(), rotate(), surface_shadow(), draw_glow(), DenseMesh, Telemetry

### Community 19 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 20 - "DockArea"
Cohesion: 0.12
Nodes (3): DockArea, visit(), drain_evenly()

### Community 23 - "threading"
Cohesion: 0.06
Nodes (5): Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 34 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 35 - "wifi_windows.py"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.07
Nodes (5): fade_in(), SummaryCard, WorkspaceButton, WorkspaceSelectPage, update()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "PrivilegedHelper"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 52 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.05
Nodes (4): InputManager, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - "time_core/transforms.py"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 64 - "session_recorder.py"
Cohesion: 0.12
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 65 - "buffer_manager.py"
Cohesion: 0.05
Nodes (4): DefenderMapBuffer, DefenderModbusBuffer, ModbusBuffer, _resolve_local_mac()

### Community 66 - "walk"
Cohesion: 0.12
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), new_id() (+8 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.29
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 85 - "SettingCell"
Cohesion: 0.14
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 87 - "config_editor.py"
Cohesion: 0.05
Nodes (19): canvas_fit(), padded_fit(), affine(), apply_scale_about(), scale(), translate(), BoatMotion, make_workspace() (+11 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 90 - "WindowControls"
Cohesion: 0.10
Nodes (3): SquareButtons, WindowDrag, WindowEdges

### Community 91 - "Replay"
Cohesion: 0.08
Nodes (3): decode(), RecordFilter, Replay

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 98 - "WorkspaceSorter"
Cohesion: 0.17
Nodes (3): WorkspaceSorter, create(), DragPayload

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "ap_commands.py"
Cohesion: 0.14
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 102 - ".section"
Cohesion: 0.13
Nodes (4): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, RefreshAndCloseOverlay

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "QWidget"
Cohesion: 0.12
Nodes (3): _SideStrip, _SideTitle, TabbedPane

### Community 110 - "Camera"
Cohesion: 0.13
Nodes (3): Camera, zoom_and_pan(), zoom_and_pan_reverse()

### Community 111 - ".__init__"
Cohesion: 0.09
Nodes (3): ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 119 - "time"
Cohesion: 0.08
Nodes (9): random_spline_path(), action(), header(), mark(), packet(), packet_from_meta(), poll(), raw_bytes() (+1 more)

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 126 - "Wifi"
Cohesion: 0.10
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 136 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "overlay.py"
Cohesion: 0.24
Nodes (4): EditWorkspaceAvailability, SelectRegisterPreset, SettingsOverlayButton, background_choices()

### Community 145 - "filter_overlay.py"
Cohesion: 0.27
Nodes (3): compile_packet_filter(), FilterOverlay, FilterPacketConsole

### Community 147 - "PopupWindow"
Cohesion: 0.11
Nodes (3): make(), message(), PopupWindow

### Community 148 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (13): NetworkDiagramCanvas, StripChart, panel(), Builder, Builder, ChartsExample, Builder, Builder (+5 more)

### Community 150 - "ContextManager"
Cohesion: 0.10
Nodes (12): ContextManager, DefenderWorldMap, BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm (+4 more)

### Community 157 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 162 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 163 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 171 - "examples.py"
Cohesion: 0.04
Nodes (18): House, WorldMap, Scrollable, ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample (+10 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "menu_bar.py"
Cohesion: 0.08
Nodes (13): ButtonGroup, offered_sections(), GoBackToPreviousPage, OpenPauseMenu, RefreshCurrentPage, ShowHelpMessage, global_buttons(), draw_window_bar_line() (+5 more)

### Community 178 - ".build_description_tab"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 194 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1629 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `ProcessManager`, `PageManager`, `important_buttons/__init__.py`, `overlay.py`, `CheckboxOverlay`, `filter_overlay.py`, `widgets/__init__.py`, `threading`, `Performance`, `AnimationManager`, `.fill_base`, `.save_current_page`, `LocalizationManager`, `examples.py`, `.start_session`, `menu_bar.py`, `DefenderStatusBuffer`, `Json`, `KeyBinds`, `Router`, `session_recorder.py`, `buffer_manager.py`, `walk`, `PrivilegedHelper`, `Preferences`, `config_editor.py`, `Style`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Visual` be split into smaller, more focused modules?**
  _Cohesion score 0.09195402298850575 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.apply_theme`, `SettingsSection`, `.preset_name`, `._build_stylesheet`, `overlay.py`, `important_buttons/__init__.py`, `.theme_family`, `.start_session`, `menu_bar.py`, `.discard_changes`, `Overlay`, `threading`, `ContextManager`, `config_editor.py`, `.link_color`, `.set_theme`, `.css`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.06715063520871144 - nodes in this community are weakly interconnected._