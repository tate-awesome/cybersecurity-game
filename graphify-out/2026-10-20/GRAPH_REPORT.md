# Graph Report - cybersecurity-game  (2026-10-20)

## Corpus Check
- 304 files · ~236,204 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4154 nodes · 8782 edges · 193 communities (74 shown, 119 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 458 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a7453db5`
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
- network_diagram/_builder.py
- .begin_drag
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- ToggleButton
- visuals/__init__.py
- ModbusBuffer
- Dev/Host_API.py
- DockArea
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- VisualPalette
- NotFound
- SessionRecorder
- ViewPort
- PacketTreeview
- BaseForm
- NMapper
- LayoutEditor
- Performance
- os
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- platform
- LocalizationManager
- QWidget
- _DrawerLayout
- Runtime Requirements
- StatusBuffer
- launch.py
- ConfigEditor
- .__init__
- .collect
- DefenderStatusBuffer
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
- examples.py
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
- settings.py
- Map
- SettingCell
- Rows
- canvas.py
- ModBus Submarine Exercise Screenshot
- app.py
- WindowEdges
- Replay
- .material
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- FileStream
- MitmTable
- WorkspaceSorter
- Denier
- ModBus HVAC Exercise Screenshot
- ap_commands.py
- overlay.py
- Map
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- QWidget
- Camera
- _RightZoneRoom
- Telemetry
- _Dim
- Overlay
- MainWindow
- .target_at
- .populate_filter_overlay
- .page_panel_keys
- sys
- WorkspaceChip
- DenseMesh
- .play
- Master
- Style
- AppearEffect
- Wifi
- Slave
- ArpSpoofer
- make_workspace
- TabStrip
- NewWorkspaceDialog
- RefreshAndCloseOverlay
- _Chip
- _SaveLayoutAsDefault
- themes.py
- PooledCanvasMixin
- master.py
- .arrow
- DefenderHVACChart
- ListZone
- .__init__
- DropZone
- widgets/__init__.py
- _Drawer
- ContextManager
- Builder
- .new_tab
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ThemeEditorPage
- AnimationManager
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- .save_current_page
- ToggleBookmark
- examples.py
- CLAUDE.md
- confirm_dialog
- ._scan_for_networks
- menu_bar.py
- .build_description_tab
- .apply
- .authored_weights
- _Grip
- .integer
- frame_callback
- frame_callback
- DragHandle
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
6. `MenuBar` - 63 edges
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

## Communities (193 total, 119 thin omitted)

### Community 1 - "MetaPacket"
Cohesion: 0.05
Nodes (6): Channel, NetworkGraph, PacketBuffer, Transaction, TransactionManager, MetaPacket

### Community 2 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (6): on_change(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (3): surface_shadow(), pyramid_blur(), VisualBackground

### Community 9 - ".begin_drag"
Cohesion: 0.18
Nodes (3): _DropPreview, leaf_of(), remove_panel()

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (35): AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms (+27 more)

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleStripChartAutoFit (+1 more)

### Community 16 - "visuals/__init__.py"
Cohesion: 0.11
Nodes (9): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_noise_gradient(), value_noise(), draw_glow(), Visual (+1 more)

### Community 17 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 19 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 23 - "time"
Cohesion: 0.06
Nodes (5): PreferencesData, _resolve_local_mac(), ProcessManager, Process, RetentionPolicy

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 27 - "SessionRecorder"
Cohesion: 0.07
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 30 - "BaseForm"
Cohesion: 0.14
Nodes (8): BaseForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm, NmapForm, SniffForm

### Community 31 - "NMapper"
Cohesion: 0.07
Nodes (6): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 34 - "os"
Cohesion: 0.14
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

### Community 48 - "StatusBuffer"
Cohesion: 0.08
Nodes (4): Buffer, DefenderMapBuffer, StatusBuffer, MetaStatus

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 52 - ".__init__"
Cohesion: 0.28
Nodes (4): encryption_enabled(), EncryptionForm, start_encryption(), stop_encryption()

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "SlidersForm"
Cohesion: 0.14
Nodes (4): submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - "time_core/transforms.py"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "session_recorder.py"
Cohesion: 0.13
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 66 - "walk"
Cohesion: 0.11
Nodes (16): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+8 more)

### Community 67 - "MenuBar"
Cohesion: 0.04
Nodes (3): _FollowResize, MenuBar, WindowBarButton

### Community 69 - "examples.py"
Cohesion: 0.06
Nodes (14): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap, NetworkExample, PassWheel, SampleHouse (+6 more)

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 79 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 83 - "settings.py"
Cohesion: 0.13
Nodes (4): SettingsSection, developer_text(), OpenAccessPointConfigInBrowser, background_choices()

### Community 87 - "canvas.py"
Cohesion: 0.11
Nodes (9): canvas_fit(), padded_fit(), affine(), apply_scale_about(), scale(), translate(), padded_fit_uniform(), padded_fit_uniform_reverse() (+1 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

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
Cohesion: 0.17
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+7 more)

### Community 102 - "overlay.py"
Cohesion: 0.14
Nodes (6): SelectBackground, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "QWidget"
Cohesion: 0.07
Nodes (6): _LentPlaceholder, _Peek, _SideStrip, _SideTitle, TabbedPane, paint_panel()

### Community 113 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 119 - "sys"
Cohesion: 0.14
Nodes (3): build_name(), main(), write_build_info()

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 122 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 126 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 136 - "_SaveLayoutAsDefault"
Cohesion: 0.10
Nodes (6): make(), _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 137 - "themes.py"
Cohesion: 0.10
Nodes (12): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme() (+4 more)

### Community 145 - ".__init__"
Cohesion: 0.09
Nodes (3): FilterOverlay, FilterPacketConsole, OpenFavoritePage

### Community 148 - "widgets/__init__.py"
Cohesion: 0.07
Nodes (10): compile_packet_filter(), panel(), Builder, Builder, Builder, Builder, Builder, Panel (+2 more)

### Community 150 - "ContextManager"
Cohesion: 0.11
Nodes (7): ContextManager, BoatMotion, Sprites, Triangle, Visuals, WorkspacePage, Page

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

### Community 161 - "ThemeEditorPage"
Cohesion: 0.06
Nodes (3): ThemeEditorPage, preview(), PopupWindow

### Community 162 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 171 - "examples.py"
Cohesion: 0.05
Nodes (11): StripChart, Scrollable, ChartsExample, ControlsExample, FlagsExample, HouseExample, MapExample, PacketsExample (+3 more)

### Community 174 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton (+1 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - "menu_bar.py"
Cohesion: 0.05
Nodes (15): ButtonGroup, offered_sections(), GoBackToPreviousPage, EditWorkspaceAvailability, global_buttons(), CornerControls, draw_window_bar_line(), SquareButtons (+7 more)

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1640 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **119 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `.reset_page`, `network_diagram/_builder.py`, `themes.py`, `_SaveLayoutAsDefault`, `PageManager`, `important_buttons/__init__.py`, `visuals/__init__.py`, `.__init__`, `defender_hvac_chart.py`, `widgets/__init__.py`, `time`, `BaseForm`, `Performance`, `AnimationManager`, `LocalizationManager`, `ToggleBookmark`, `.start_session`, `confirm_dialog`, `menu_bar.py`, `Json`, `KeyBinds`, `Router`, `session_recorder.py`, `walk`, `examples.py`, `PrivilegedHelper`, `Preferences`, `host.py`, `settings.py`, `canvas.py`, `overlay.py`, `Style`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.04842105263157895 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `session_recorder.py`, `SettingsSection`, `overlay.py`, `themes.py`, `._build_stylesheet`, `important_buttons/__init__.py`, `.theme_family`, `.start_session`, `.__init__`, `.discard_changes`, `QWidget`, `menu_bar.py`, `Overlay`, `ContextManager`, `.material`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._