# Graph Report - cybersecurity-game  (2026-10-20)

## Corpus Check
- 304 files · ~239,498 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4228 nodes · 8637 edges · 230 communities (73 shown, 157 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 462 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec454410`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Proximity
- MetaPacket
- server.py
- footer.py
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- buffer_manager.py
- settings.py
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- ToggleButton
- VisualPalette
- MapBuffer
- Panel
- DockArea
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- Kernel
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
- WorkspaceSelectPage
- Camera
- Loader
- platform
- LocalizationManager
- PopupEntrance
- window_chrome.py
- .apply_theme
- Runtime Requirements
- StatusBuffer
- launch.py
- ConfigEditor
- walk
- PacketBuffer
- .collect
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- SlidersForm
- BaseForm
- Modify
- time_core/transforms.py
- Router
- DefenderModbusBuffer
- docking.py
- .__init__
- StripChartBase
- Builder
- palette_generator.py
- Footer
- app.py
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- VariableOverlay
- _base_button.py
- .leaf
- Attack
- WaveGrid
- .fill_base
- RefreshCurrentPage
- .add_setting_row
- Rows
- geometry.py
- ModBus Submarine Exercise Screenshot
- FadeOut
- WindowEdges
- Replay
- .brush
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- FileStream
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
- .__init__
- paint_panel
- Camera
- paint_arrow
- Telemetry
- _Dim
- Draw
- MainWindow
- .target_at
- compile_packet_filter
- TabbedPane
- dist.py
- WorkspaceChip
- bare_icon
- .__init__
- Master
- Style
- AppearEffect
- _in_nm_context
- Slave
- ArpSpoofer
- Panes
- TabStrip
- config_editor.py
- DenseMesh
- popup.py
- themes.py
- PooledCanvasMixin
- CornerControls
- .__init__
- DefenderHVACChart
- ImportantButton
- DropZone
- Meter
- .add_deadspace
- SettingsSection
- router.py
- Draw
- .new_tab
- ShiftWheel
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- context_manager.py
- Paths
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- NMapper
- .save_current_page
- file_dialog
- examples.py
- CLAUDE.md
- menu_bar.py
- ._scan_for_networks
- WindowBarButton
- NoteBrowser
- MenuBar
- APConnectForm
- .authored_weights
- zoom_and_pan
- _Chip
- APPoller
- .build_menu_bar_section
- _Grip
- FilterOverlay
- .__init__
- EncryptionForm
- .__init__
- .page_panel_keys
- nfq_linux.py
- DragHandle
- open_favorite_page.py
- _OnHide
- TriangleCanvas
- ConfigureThisWorkspace
- .__init__
- LinkToPage
- .__init__
- KalmanForm
- WifiForm
- Builder
- Visualizer.py
- SettingsPage
- .integer
- ModeForm
- Scrollable
- shorten_line

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 135 edges
2. `ImportantButton` - 106 edges
3. `Style` - 100 edges
4. `Overlay` - 84 edges
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

## Communities (230 total, 157 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "footer.py"
Cohesion: 0.18
Nodes (4): on_off(), on_off(), set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "buffer_manager.py"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 9 - "settings.py"
Cohesion: 0.06
Nodes (7): developer_text(), DeleteAllUserData, DeleteAllWorkspaceSavedData, LoadLocalizationLabelsFile, OpenThemeEditor, OpenWorkspaceEditor, ToggleLightDarkMode

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.06
Nodes (10): AbortAllNetworkActions, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay, LoadMcapIntoPacketBuffer, LoadPcapIntoPacketBuffer, OpenTitlePage (+2 more)

### Community 15 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 16 - "VisualPalette"
Cohesion: 0.10
Nodes (6): get_arc_points(), get_bearing(), rotate(), draw_glow(), Visual, VisualPalette

### Community 19 - "Panel"
Cohesion: 0.07
Nodes (4): panel(), _DrawerLayout, Panel, surface_shadow()

### Community 23 - "time"
Cohesion: 0.06
Nodes (14): random_spline_path(), Buffer, ProcessManager, Process, action(), dumps(), header(), mark() (+6 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.12
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 28 - "ViewPort"
Cohesion: 0.09
Nodes (4): ViewPort, BoatMotion, Sprites, Map

### Community 34 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 35 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.07
Nodes (5): fade_in(), SummaryCard, WorkspaceButton, WorkspaceSelectPage, update()

### Community 44 - "window_chrome.py"
Cohesion: 0.18
Nodes (5): bar_button_height(), draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 51 - "walk"
Cohesion: 0.14
Nodes (4): visit(), is_split(), panel_ids(), walk()

### Community 59 - "SlidersForm"
Cohesion: 0.16
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 60 - "BaseForm"
Cohesion: 0.05
Nodes (8): BaseForm, ControlsExample, RegistersExample, ArpForm, DosForm, NFQForm, NmapForm, SniffForm

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.11
Nodes (14): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+6 more)

### Community 67 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 72 - "app.py"
Cohesion: 0.16
Nodes (3): App, WindowReveal, __getattr__()

### Community 78 - "VariableOverlay"
Cohesion: 0.18
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "_base_button.py"
Cohesion: 0.15
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 81 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 83 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 84 - "RefreshCurrentPage"
Cohesion: 0.15
Nodes (4): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 87 - "geometry.py"
Cohesion: 0.10
Nodes (10): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), scale(), translate() (+2 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 98 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (3): WorkspaceSorter, delete(), rename()

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 102 - "Overlay"
Cohesion: 0.06
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "paint_panel"
Cohesion: 0.13
Nodes (3): _Peek, _SideStrip, paint_panel()

### Community 111 - "paint_arrow"
Cohesion: 0.15
Nodes (3): bar_inset(), minimized_thickness(), paint_arrow()

### Community 113 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 117 - "compile_packet_filter"
Cohesion: 0.18
Nodes (5): _checkbox_value(), compile_packet_filter(), packet_filter(), activate(), save_filter_summary()

### Community 119 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 120 - "WorkspaceChip"
Cohesion: 0.15
Nodes (4): checkbox(), WorkspaceChip, edit(), DragPayload

### Community 122 - ".__init__"
Cohesion: 0.21
Nodes (4): FadeIn, covered(), settle(), uncovered()

### Community 131 - "TabStrip"
Cohesion: 0.09
Nodes (4): _LentPlaceholder, PeekArrow, _SideTitle, TabStrip

### Community 132 - "config_editor.py"
Cohesion: 0.09
Nodes (11): decode(), delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, rename_workspace(), RenameWorkspaceDialog (+3 more)

### Community 136 - "popup.py"
Cohesion: 0.05
Nodes (10): ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, confirm_dialog() (+2 more)

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 145 - "ImportantButton"
Cohesion: 0.07
Nodes (8): ImportantButton, ClearAllCapturedBufferData, LoadSettingsPresetFile, OpenSettingsPage, SaveCurrentPacketBufferToMcap, StreamMcapIntoPacketBuffer, StreamPcapIntoPacketBuffer, icon_button()

### Community 148 - ".add_deadspace"
Cohesion: 0.08
Nodes (4): Builder, Builder, Builder, Builder

### Community 150 - "router.py"
Cohesion: 0.11
Nodes (5): Triangle, Visuals, WorkspacePage, NotFound, Page

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

### Community 162 - "context_manager.py"
Cohesion: 0.06
Nodes (5): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter, PreferencesData

### Community 167 - "SectionCard"
Cohesion: 0.19
Nodes (3): SectionCard, create(), ListZone

### Community 168 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 171 - "examples.py"
Cohesion: 0.05
Nodes (19): Canvas, DefenderWorldMap, House, WorldMap, FlagsExample, HouseExample, MapExample, NetworkExample (+11 more)

### Community 174 - "menu_bar.py"
Cohesion: 0.09
Nodes (6): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "WindowBarButton"
Cohesion: 0.10
Nodes (5): SquareButtons, toggle_maximized(), WindowBarButton, WindowControls, WindowDrag

### Community 178 - "NoteBrowser"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

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

### Community 219 - "Scrollable"
Cohesion: 0.07
Nodes (8): NetworkDiagramCanvas, StripChart, _Gaps, Scrollable, Builder, ChartsExample, Builder, Builder

## Knowledge Gaps
- **42 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1723 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **157 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `footer.py`, `InputManager`, `.reset_page`, `config_editor.py`, `buffer_manager.py`, `settings.py`, `popup.py`, `PageManager`, `important_buttons/__init__.py`, `VisualPalette`, `router.py`, `time`, `ShiftWheel`, `CheckboxOverlay`, `ViewPort`, `Performance`, `context_manager.py`, `Paths`, `LocalizationManager`, `examples.py`, `window_chrome.py`, `.apply_theme`, `menu_bar.py`, `Json`, `KeyBinds`, `FilterOverlay`, `Router`, `.start_session`, `docking.py`, `open_favorite_page.py`, `ConfigureThisWorkspace`, `Preferences`, `host.py`, `LinkToPage`, `_base_button.py`, `.reload_preferences`, `defender_hvac_chart.py`, `Scrollable`, `Overlay`, `Style`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07591836734693877 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.start_session`, `context_manager.py`, `SettingsSection`, `Overlay`, `.set_theme`, `open_favorite_page.py`, `._build_stylesheet`, `.theme_family`, `.apply_theme`, `_base_button.py`, `menu_bar.py`, `.discard_changes`, `.brush`, `ContextManager`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._