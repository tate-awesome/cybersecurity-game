# Graph Report - cybersecurity-game  (2026-10-20)

## Corpus Check
- 300 files · ~237,585 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4229 nodes · 8638 edges · 231 communities (64 shown, 167 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 464 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7fdc2b69`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Proximity
- MetaPacket
- server.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- DefenderMapBuffer
- record_schema.py
- ._build_stylesheet
- PageManager
- HouseBuffer
- sys
- ToggleButton
- Visual
- MapBuffer
- _DrawerLayout
- DockArea
- NetworkMesh
- time
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- ViewPort
- PacketTreeview
- ContextManager
- NetFilterQueue
- LayoutEditor
- Performance
- os
- wifi_windows.py
- StripChartLayout
- .__init__
- WorkspaceSelectPage
- Camera
- Loader
- TransactionManager
- LocalizationManager
- PopupEntrance
- AnimationManager
- .__init__
- Runtime Requirements
- StatusBuffer
- host.py
- ConfigEditor
- .collapsed
- PacketBuffer
- .collect
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- pyside6_qtwidgets
- Modify
- time_core/transforms.py
- Router
- DefenderModbusBuffer
- docking.py
- MenuBar
- StripChartBase
- Builder
- palette_generator.py
- Canvas
- App
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- VariableOverlay
- TabStrip
- .build_workspace_section
- Attack
- WaveGrid
- surface_shadow
- important_buttons/__init__.py
- .add_setting_row
- Rows
- transformations.py
- ModBus Submarine Exercise Screenshot
- FadeIn
- CallbackRegistry
- Replay
- .css
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- RecordFilter
- MitmTable
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- ap_commands.py
- Overlay
- _MapCanvas
- Kalman
- Builder
- Wifi
- Defender Full Suite Exercise Screenshot
- geometry.py
- .leaf
- Camera
- paint_mark
- Telemetry
- _Dim
- Draw
- MainWindow
- .target_at
- .populate_filter_overlay
- .renumber
- SelectRegisterPreset
- WorkspaceChip
- developer_text
- _PollUnpacker
- Master
- Style
- AppearEffect
- _in_nm_context
- Slave
- ArpSpoofer
- Panes
- QWidget
- NewWorkspaceDialog
- SettingsSection
- DenseMesh
- confirm_dialog
- themes.py
- PooledCanvasMixin
- quit_application.py
- DefenderHVACChart
- SelectBackground
- ImportantButton
- DropZone
- Meter
- .__init__
- Context
- Draw
- .new_tab
- ShiftWheel
- overlay.py
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- ClickManager
- platform
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- NMapper
- .save_current_page
- widgets/__init__.py
- CLAUDE.md
- EditBackgroundChoices
- ToggleBookmark
- ._scan_for_networks
- menu_bar.py
- .build_description_tab
- CreateToolTip
- CreateToolTip
- APConnectForm
- .authored_weights
- .prepare_page_config
- _Chip
- APPoller
- PreferencesData
- _Grip
- FilterOverlay
- _RightZoneRoom
- .__init__
- .__init__
- Map
- NetworkGraph
- DragHandle
- open_favorite_page.py
- EncryptionForm
- .__init__
- LinkToPage
- .__init__
- Sniffer
- WifiForm
- .edit_workspace
- _OnHide
- SettingsPage
- ModeForm
- ConfigureThisWorkspace
- GoForwardToNextPage
- _Gaps
- SampleSubmarine
- Channel
- NetFilterQueueBaseClass
- .integer

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 135 edges
2. `ImportantButton` - 106 edges
3. `Style` - 100 edges
4. `Overlay` - 85 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 59 edges
7. `ConfigEditor` - 58 edges
8. `BaseForm` - 55 edges
9. `DockArea` - 50 edges
10. `Panel` - 48 edges

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

## Communities (231 total, 167 thin omitted)

### Community 2 - "server.py"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "record_schema.py"
Cohesion: 0.17
Nodes (10): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+2 more)

### Community 14 - "sys"
Cohesion: 0.12
Nodes (3): build_name(), main(), write_build_info()

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit (+1 more)

### Community 16 - "Visual"
Cohesion: 0.08
Nodes (3): draw_vessel(), draw_glow(), Visual

### Community 23 - "time"
Cohesion: 0.04
Nodes (7): random_spline_path(), Buffer, ModbusBuffer, _resolve_local_mac(), ProcessManager, Process, RetentionPolicy

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.12
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 30 - "ContextManager"
Cohesion: 0.08
Nodes (11): ContextManager, apply_scale_about(), BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page (+3 more)

### Community 34 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

### Community 35 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (6): fade_in(), NoteBrowser, SummaryCard, WorkspaceButton, WorkspaceSelectPage, update()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "host.py"
Cohesion: 0.13
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - "SlidersForm"
Cohesion: 0.16
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 60 - "pyside6_qtwidgets"
Cohesion: 0.05
Nodes (8): BaseForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm, NmapForm, SniffForm

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 67 - "MenuBar"
Cohesion: 0.04
Nodes (4): bare_icon(), _FollowResize, global_buttons(), MenuBar

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "Canvas"
Cohesion: 0.09
Nodes (5): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 78 - "VariableOverlay"
Cohesion: 0.18
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 80 - ".build_workspace_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 81 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 83 - "surface_shadow"
Cohesion: 0.10
Nodes (4): surface_shadow(), paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 84 - "important_buttons/__init__.py"
Cohesion: 0.05
Nodes (13): AbortAllNetworkActions, ClearPacketConsole, ClearSavedWorkspaceInputs, LoadMcapIntoPacketBuffer, LoadSettingsPresetFile, RefreshCurrentPage, ResetSavedWorkspaceLayout, SaveCurrentPacketBufferToMcap (+5 more)

### Community 87 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

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

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 102 - "Overlay"
Cohesion: 0.08
Nodes (3): EditModelStyle, EditStripChartStyle, Overlay

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 108 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 111 - "paint_mark"
Cohesion: 0.09
Nodes (5): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow, _SideTitle

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 115 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 118 - ".renumber"
Cohesion: 0.19
Nodes (3): delete(), create(), rename()

### Community 121 - "developer_text"
Cohesion: 0.19
Nodes (3): developer_text(), ButtonGroup, offered_sections()

### Community 131 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, _Peek, _SideStrip, TabbedPane, paint_panel()

### Community 132 - "NewWorkspaceDialog"
Cohesion: 0.12
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 136 - "confirm_dialog"
Cohesion: 0.05
Nodes (10): DeleteAllUserData, DeleteAllWorkspaceSavedData, ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, confirm_dialog() (+2 more)

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 145 - "ImportantButton"
Cohesion: 0.04
Nodes (18): ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearStatusConsole, EditModbusRegisterDisplay, ImportThemes, LoadLocalizationLabelsFile (+10 more)

### Community 148 - ".__init__"
Cohesion: 0.05
Nodes (4): Builder, Builder, Builder, Builder

### Community 150 - "Context"
Cohesion: 0.23
Nodes (6): delete_workspace(), drop_unused_labels(), make_workspace(), rename_workspace(), workspace_folder(), workspace_labels()

### Community 157 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.33
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 168 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 171 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (26): NetworkDiagramCanvas, StripChart, Scrollable, panel(), Builder, ChartsExample, ControlsExample, FlagsExample (+18 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "menu_bar.py"
Cohesion: 0.05
Nodes (14): GoBackToPreviousPage, OpenPauseMenu, bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized() (+6 more)

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 194 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

## Knowledge Gaps
- **42 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1723 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **167 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `.reset_page`, `confirm_dialog`, `PageManager`, `quit_application.py`, `Visual`, `ImportantButton`, `time`, `ShiftWheel`, `CheckboxOverlay`, `overlay.py`, `Performance`, `ClickManager`, `LocalizationManager`, `widgets/__init__.py`, `AnimationManager`, `host.py`, `menu_bar.py`, `Json`, `KeyBinds`, `pyside6_qtwidgets`, `FilterOverlay`, `Router`, `.start_session`, `docking.py`, `open_favorite_page.py`, `Canvas`, `Preferences`, `LinkToPage`, `.reload_preferences`, `important_buttons/__init__.py`, `ConfigureThisWorkspace`, `GoForwardToNextPage`, `developer_text`, `Style`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.14039408866995073 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.start_session`, `SettingsSection`, `open_favorite_page.py`, `Overlay`, `._build_stylesheet`, `.theme_family`, `.__init__`, `ImportantButton`, `.discard_changes`, `overlay.py`, `.preset_name`, `menu_bar.py`, `time`, `QWidget`, `.css`, `ContextManager`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09788359788359788 - nodes in this community are weakly interconnected._