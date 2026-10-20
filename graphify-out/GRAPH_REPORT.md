# Graph Report - cybersecurity-game  (2026-10-19)

## Corpus Check
- 301 files · ~232,147 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4069 nodes · 8363 edges · 201 communities (66 shown, 135 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 466 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `45e817e8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .minimize_button
- MetaPacket
- Footer
- .restyle
- SettingsSection
- PauseMenu
- VisualBackground
- .__init__
- SettingsPage
- ._build_stylesheet
- PageManager
- ImportantButton
- DefenderV0
- ToggleButton
- hvac_view.py
- Prod/Host_API.py
- Scrollable
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- important_buttons/__init__.py
- SessionRecorder
- ViewPort
- PacketTreeview
- Wifi
- NetFilterQueue
- LayoutEditor
- Performance
- HVACView
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- Dev/Host_API.py
- LocalizationManager
- QWidget
- _DrawerLayout
- DefenderStatusBuffer
- Runtime Requirements
- StatusBuffer
- sys
- ConfigEditor
- channels/__init__.py
- .all_ids
- InputManager
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- _PollUnpacker
- BaseForm
- Modify
- time_core/transforms.py
- Router
- context_manager.py
- DefenderModbusBuffer
- StripChartBase
- confirm_dialog
- palette_generator.py
- .play
- App
- PrivilegedHelper
- Constellation
- Preferences
- paint_panel
- Draw
- VariableOverlay
- .leaf
- ToggleBookmark
- WaveGrid
- add
- MapBuffer
- .add_setting_row
- Rows
- MenuBar
- ModBus Submarine Exercise Screenshot
- app.py
- menu_bar.py
- RecordFilter
- .css
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- MitmTable
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- APPoller
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- StripChartLayout
- Camera
- .__init__
- WindowEdges
- _Dim
- MainWindow
- APConnectForm
- .populate_filter_overlay
- EncryptionForm
- time
- WorkspaceChip
- Proximity
- arp_poisoner.py
- Master
- Style
- AppearEffect
- _in_nm_context
- Slave
- ArpSpoofer
- NMapper
- NewWorkspaceDialog
- .new_tab
- host.py
- themes.py
- PooledCanvasMixin
- geometry.py
- .__init__
- ap_commands.py
- DefenderHVACChart
- FilterOverlay
- DropZone
- ThemeEditorPage
- widgets/__init__.py
- Telemetry
- ContextManager
- Overlay
- Builder
- .build_tabs
- ConfigureThisWorkspace
- paint_noise_gradient
- DenseMesh
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- AnimationManager
- Canvas
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- Builder
- DeleteWorkspaceDialog
- Visualizer.py
- examples.py
- CLAUDE.md
- _Drawer
- ._scan_for_networks
- .build_menu_bar_section
- .build_description_tab
- submarine_settings_synced
- TriangleCanvas
- open_favorite_page.py
- WorldMap
- LinkToPage
- DragHandle
- flusher.py
- .__init__
- .collect
- .__init__
- .__init__
- WifiForm
- ModeForm
- NetworkDiagramCanvas
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 134 edges
2. `ImportantButton` - 106 edges
3. `Style` - 99 edges
4. `Overlay` - 80 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 64 edges
7. `MetaPacket` - 59 edges
8. `BaseForm` - 55 edges
9. `VisualPalette` - 48 edges
10. `Panel` - 47 edges

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

## Communities (201 total, 135 thin omitted)

### Community 0 - ".minimize_button"
Cohesion: 0.21
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 1 - "MetaPacket"
Cohesion: 0.04
Nodes (7): Channel, NetworkGraph, PacketBuffer, Transaction, TransactionManager, MetaPacket, _BufferShim

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 12 - "ImportantButton"
Cohesion: 0.03
Nodes (15): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, GoBackToPreviousPage, GoForwardToNextPage, LoadMcapIntoPacketBuffer, LoadSettingsPresetFile, OpenSettingsPage (+7 more)

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit (+1 more)

### Community 19 - "Prod/Host_API.py"
Cohesion: 0.19
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status(), encryption_enabled() (+1 more)

### Community 20 - "Scrollable"
Cohesion: 0.08
Nodes (3): Scrollable, ChartsExample, FlagsExample

### Community 23 - "threading"
Cohesion: 0.03
Nodes (15): Buffer, NetFilterQueueBaseClass, Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run() (+7 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 25 - "VisualPalette"
Cohesion: 0.08
Nodes (4): draw_glow(), Visual, VisualPalette, Kernel

### Community 26 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (19): open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns, ClearModbusAndModelData (+11 more)

### Community 29 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 34 - "HVACView"
Cohesion: 0.07
Nodes (6): HVACView, enc_button(), slider_callback(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 35 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (6): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update()

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "sys"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 51 - "channels/__init__.py"
Cohesion: 0.06
Nodes (4): DefenderMapBuffer, HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 60 - "BaseForm"
Cohesion: 0.05
Nodes (8): BaseForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm, NmapForm, SniffForm

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "context_manager.py"
Cohesion: 0.08
Nodes (4): _dialog_parent(), file_dialog(), Paths, ProcessManager

### Community 69 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton (+1 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - ".play"
Cohesion: 0.24
Nodes (3): covered(), settle(), uncovered()

### Community 78 - "VariableOverlay"
Cohesion: 0.18
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 83 - "add"
Cohesion: 0.14
Nodes (3): add(), on_change(), SettingsSection

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.17
Nodes (4): DesktopFade, FadeIn, FadeOut, WindowReveal

### Community 90 - "menu_bar.py"
Cohesion: 0.07
Nodes (11): CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_button_height(), window_bar_height(), window_bar_room() (+3 more)

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

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - ".__init__"
Cohesion: 0.07
Nodes (6): OpenPauseMenu, ShowHelpMessage, _FollowResize, global_buttons(), _pane_is_minimized(), _RightZoneRoom

### Community 113 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 119 - "time"
Cohesion: 0.11
Nodes (11): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+3 more)

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 122 - "arp_poisoner.py"
Cohesion: 0.15
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 129 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 132 - "NewWorkspaceDialog"
Cohesion: 0.16
Nodes (3): make_workspace(), NewWorkspaceDialog, workspace_folder()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "geometry.py"
Cohesion: 0.07
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+6 more)

### Community 141 - "ap_commands.py"
Cohesion: 0.18
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+7 more)

### Community 147 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): ThemeEditorPage, preview(), message(), PopupWindow

### Community 148 - "widgets/__init__.py"
Cohesion: 0.11
Nodes (8): StripChart, Panes, panel(), Builder, Builder, Panel, Builder, Builder

### Community 150 - "ContextManager"
Cohesion: 0.09
Nodes (12): ContextManager, apply_scale_about(), AttackerV0, BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage (+4 more)

### Community 151 - "Overlay"
Cohesion: 0.04
Nodes (15): developer_text(), ButtonGroup, offered_sections(), RefreshCurrentPage, SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle (+7 more)

### Community 157 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.33
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 162 - "AnimationManager"
Cohesion: 0.06
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 168 - "Builder"
Cohesion: 0.16
Nodes (3): Builder, Builder, Builder

### Community 171 - "examples.py"
Cohesion: 0.06
Nodes (16): House, ControlsExample, HouseExample, MapExample, NetworkExample, PassWheel, RegistersExample, SampleHouse (+8 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 176 - ".build_menu_bar_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 192 - "WorldMap"
Cohesion: 0.25
Nodes (4): WorldMap, frame_callback(), sprite(), sprite_enabled()

### Community 198 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 203 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 219 - "NetworkDiagramCanvas"
Cohesion: 0.18
Nodes (3): NetworkDiagramCanvas, draw_host(), frame_callback()

## Knowledge Gaps
- **42 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1629 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `.restyle`, `host.py`, `PageManager`, `ImportantButton`, `hvac_view.py`, `FilterOverlay`, `widgets/__init__.py`, `threading`, `Overlay`, `VisualPalette`, `important_buttons/__init__.py`, `ConfigureThisWorkspace`, `Performance`, `AnimationManager`, `LocalizationManager`, `examples.py`, `channels/__init__.py`, `.start_session`, `InputManager`, `Json`, `KeyBinds`, `BaseForm`, `Router`, `context_manager.py`, `LinkToPage`, `open_favorite_page.py`, `confirm_dialog`, `PrivilegedHelper`, `Preferences`, `menu_bar.py`, `Style`?**
  _High betweenness centrality (0.268) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.042901234567901236 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `context_manager.py`, `.restyle`, `SettingsSection`, `.preset_name`, `menu_bar.py`, `._build_stylesheet`, `.theme_family`, `.discard_changes`, `QWidget`, `.start_session`, `ContextManager`, `Overlay`, `important_buttons/__init__.py`, `.css`, `open_favorite_page.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Footer` be split into smaller, more focused modules?**
  _Cohesion score 0.06144393241167435 - nodes in this community are weakly interconnected._