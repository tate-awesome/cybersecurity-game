# Graph Report - cybersecurity-game  (2026-10-20)

## Corpus Check
- 304 files · ~234,352 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4105 nodes · 8677 edges · 209 communities (69 shown, 140 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 466 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `85d4355c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .minimize_button
- MetaPacket
- server.py
- Footer
- _StyledComboItems
- SettingsSection
- PauseMenu
- VisualBackground
- CornerControls
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- PacketBuffer
- ToggleButton
- Visual
- MapBuffer
- Dev/Host_API.py
- .__init__
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
- os
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- TransactionManager
- LocalizationManager
- QWidget
- .__init__
- DefenderStatusBuffer
- Runtime Requirements
- StatusBuffer
- PrivilegedHelper
- ConfigEditor
- ModbusBuffer
- Prod/Host_API.py
- InputManager
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- .__init__
- Modify
- time_core/transforms.py
- Router
- session_recorder.py
- DefenderModbusBuffer
- walk
- MenuBar
- StripChartBase
- WorkspaceSaveResetButton
- palette_generator.py
- .play
- App
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- Draw
- VariableOverlay
- wifi_windows.py
- .leaf
- DefenderMapBuffer
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
- _PollUnpacker
- MitmTable
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- ap_commands.py
- SettingsOverlayButton
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- DockArea
- Camera
- .__init__
- WindowEdges
- _Dim
- Overlay
- MainWindow
- .target_at
- .populate_filter_overlay
- .add_deadspace
- arpy2a.py
- WorkspaceChip
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
- edit_workspace_availability.py
- .__init__
- .__init__
- DefenderHVACChart
- ListZone
- packet_console/_builder.py
- DropZone
- PopupWindow
- widgets/__init__.py
- Telemetry
- ContextManager
- SampleNetwork
- Builder
- SampleSubmarine
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- .material_control
- AnimationManager
- .fill_base
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- Builder
- .save_current_page
- QWidget
- CLAUDE.md
- select_background.py
- Builder
- ._scan_for_networks
- menu_bar.py
- .build_description_tab
- Builder
- DenseMesh
- .authored_weights
- .prepare_page_config
- _OnHide
- Channel
- _DropPreview
- _Grip
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
6. `MenuBar` - 65 edges
7. `MetaPacket` - 59 edges
8. `BaseForm` - 55 edges
9. `Panel` - 49 edges
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

## Communities (209 total, 140 thin omitted)

### Community 0 - ".minimize_button"
Cohesion: 0.16
Nodes (11): _drain_evenly(), attach(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), redocked(), restore_floor() (+3 more)

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.11
Nodes (6): save(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "CornerControls"
Cohesion: 0.13
Nodes (5): CornerControls, draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (40): AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms (+32 more)

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit (+1 more)

### Community 16 - "Visual"
Cohesion: 0.12
Nodes (4): draw_vessel(), draw_glow(), Visual, VisualPalette

### Community 19 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 23 - "threading"
Cohesion: 0.11
Nodes (4): Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (11): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+3 more)

### Community 28 - "ViewPort"
Cohesion: 0.05
Nodes (16): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), get_arc_points(), get_bearing() (+8 more)

### Community 29 - "PacketTreeview"
Cohesion: 0.09
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 34 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

### Community 35 - "wifi_windows.py"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.05
Nodes (8): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update(), paint_panel(), surface_shadow()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "PrivilegedHelper"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 50 - "ConfigEditor"
Cohesion: 0.09
Nodes (4): ConfigEditor, discard(), remove_nested(), set_nested()

### Community 52 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 59 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - "time_core/transforms.py"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "session_recorder.py"
Cohesion: 0.11
Nodes (3): _dialog_parent(), file_dialog(), RetentionPolicy

### Community 66 - "walk"
Cohesion: 0.14
Nodes (14): add_tab(), find(), is_split(), leaf(), leaf_of(), new_id(), normalize(), tidy() (+6 more)

### Community 69 - "WorkspaceSaveResetButton"
Cohesion: 0.20
Nodes (3): ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - ".play"
Cohesion: 0.28
Nodes (3): covered(), settle(), uncovered()

### Community 78 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 85 - "SettingCell"
Cohesion: 0.16
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 87 - "config_editor.py"
Cohesion: 0.08
Nodes (11): BoatMotion, make_workspace(), workspace_folder(), Sprites, Triangle, WorkspacePage, NotFound, Page (+3 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "WindowControls"
Cohesion: 0.10
Nodes (5): SquareButtons, toggle_maximized(), WindowBarButton, WindowControls, WindowDrag

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
Cohesion: 0.13
Nodes (19): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+11 more)

### Community 102 - "SettingsOverlayButton"
Cohesion: 0.10
Nodes (6): SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "DockArea"
Cohesion: 0.20
Nodes (3): from_tree(), split(), TabbedPane

### Community 111 - ".__init__"
Cohesion: 0.10
Nodes (4): _FollowResize, global_buttons(), _pane_is_minimized(), _RightZoneRoom

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.18
Nodes (5): _checkbox_value(), compile_packet_filter(), packet_filter(), activate(), save_filter_summary()

### Community 119 - "arpy2a.py"
Cohesion: 0.09
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 129 - "NMapper"
Cohesion: 0.20
Nodes (3): NMapper, InterfaceManager, job()

### Community 137 - "themes.py"
Cohesion: 0.14
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 145 - "packet_console/_builder.py"
Cohesion: 0.09
Nodes (3): FilterOverlay, FilterPacketConsole, OpenFavoritePage

### Community 147 - "PopupWindow"
Cohesion: 0.11
Nodes (3): make(), message(), PopupWindow

### Community 148 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (18): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, EditModbusRegisterDisplay, Scrollable (+10 more)

### Community 150 - "ContextManager"
Cohesion: 0.08
Nodes (12): CallbackRegistry, ContextManager, apply_scale_about(), _resolve_local_mac(), BaseForm, APTunnelForm, ArpForm, DosForm (+4 more)

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
Nodes (3): AnimationManager, ClickManager, _GlobalClickFilter

### Community 163 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 171 - "QWidget"
Cohesion: 0.11
Nodes (7): WorldMap, ControlsExample, PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SampleWorldMap

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "menu_bar.py"
Cohesion: 0.06
Nodes (10): ButtonGroup, offered_sections(), GoBackToPreviousPage, ask_to_quit(), QuitApplication, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ToggleBookmark (+2 more)

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1621 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **140 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `ProcessManager`, `PageManager`, `important_buttons/__init__.py`, `Visual`, `packet_console/_builder.py`, `widgets/__init__.py`, `threading`, `Performance`, `AnimationManager`, `.save_current_page`, `LocalizationManager`, `menu_bar.py`, `InputManager`, `Json`, `KeyBinds`, `Router`, `walk`, `PrivilegedHelper`, `Preferences`, `host.py`, `config_editor.py`, `SettingsOverlayButton`, `Style`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.get_font_size`, `SettingsSection`, `.preset_name`, `SettingsOverlayButton`, `._build_stylesheet`, `important_buttons/__init__.py`, `.theme_family`, `menu_bar.py`, `.discard_changes`, `Overlay`, `ContextManager`, `.link_color`, `QWidget`, `.css`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Footer` be split into smaller, more focused modules?**
  _Cohesion score 0.06829573934837092 - nodes in this community are weakly interconnected._