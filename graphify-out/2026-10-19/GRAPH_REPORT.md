# Graph Report - cybersecurity-game  (2026-10-19)

## Corpus Check
- 302 files · ~232,272 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4077 nodes · 8372 edges · 199 communities (68 shown, 131 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 465 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `579c9705`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .minimize_button
- MetaPacket
- router.py
- Footer
- .apply_theme
- SettingsSection
- PauseMenu
- VisualBackground
- PacketBuffer
- SettingsPage
- ._build_stylesheet
- PageManager
- important_buttons/__init__.py
- DefenderV0
- ToggleButton
- Visual
- hvac_view.py
- os
- arp_poisoner.py
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- threading
- FindBar
- VisualPalette
- CheckboxOverlay
- SessionRecorder
- ViewPort
- PacketTreeview
- Wifi
- .__init__
- LayoutEditor
- Performance
- HVACView
- wifi_windows.py
- Draw
- _Gaps
- WorkspaceSelectPage
- Camera
- Loader
- server.py
- LocalizationManager
- .columnconfigure
- _DrawerLayout
- DefenderStatusBuffer
- Runtime Requirements
- StatusBuffer
- launch.py
- ConfigEditor
- ModbusBuffer
- SlidersForm
- .collect
- InputManager
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- _PollUnpacker
- pyside6_qtwidgets
- Modify
- time_core/transforms.py
- Process
- DefenderModbusBuffer
- Replay
- FileStream
- StripChartBase
- confirm_dialog
- palette_generator.py
- AnimationManager
- App
- PrivilegedHelper
- Constellation
- Preferences
- .populate_filter_overlay
- Draw
- VariableOverlay
- CornerControls
- .leaf
- ThemeEditorPage
- WaveGrid
- ap_commands.py
- MapBuffer
- SettingCell
- .add_setting_row
- ModBus Submarine Exercise Screenshot
- FadeIn
- window_chrome.py
- .__init__
- CallbackRegistry
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- sys
- MitmTable
- WorkspaceSorter
- version.py
- ModBus HVAC Exercise Screenshot
- MenuBar
- _MapCanvas
- Kalman
- Builder
- Builder
- Defender Full Suite Exercise Screenshot
- Meter
- StripChartLayout
- Camera
- menu_bar.py
- WindowEdges
- _Dim
- MainWindow
- PopupEntrance
- record_schema.py
- WorkspaceChip
- Proximity
- WindowDrag
- Master
- Style
- AppearEffect
- _in_nm_context
- Slave
- ArpSpoofer
- NMapper
- SelectRegisterPreset
- NewWorkspaceDialog
- .new_tab
- host.py
- NativeFrame
- themes.py
- PooledCanvasMixin
- geometry.py
- .__init__
- Dev/Host_API.py
- DefenderHVACChart
- ListZone
- FilterOverlay
- DropZone
- Builder
- Telemetry
- ContextManager
- Overlay
- RecordFilter
- .build_tabs
- .__init__
- ToggleLightDarkMode
- GrowingButton
- .connect_to_saved_wifi
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- ClickManager
- Canvas
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- SectionCard
- WindowControls
- NetFilterQueue
- DenseMesh
- widgets/__init__.py
- CLAUDE.md
- ._scan_for_networks
- saved/__init__.py
- NoteBrowser
- .play
- SampleSubmarine
- ModeForm
- make_workspace
- master.py
- overlay.py
- PreferencesData
- open_favorite_page.py
- .__init__
- APPoller
- DragHandle
- .__init__
- WifiForm

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 134 edges
2. `ImportantButton` - 106 edges
3. `Style` - 100 edges
4. `Overlay` - 80 edges
5. `ConfigEditor` - 65 edges
6. `MenuBar` - 63 edges
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

## Communities (199 total, 131 thin omitted)

### Community 0 - ".minimize_button"
Cohesion: 0.21
Nodes (8): _drain_evenly(), click_maximize(), click_minimize(), grow_pane(), on_sash_moved(), restore_floor(), shrink_pane(), unminimize()

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "router.py"
Cohesion: 0.06
Nodes (12): Router, PageTransition, AttackerV0, BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage (+4 more)

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (4): Visuals, paint_aurora(), pyramid_blur(), VisualBackground

### Community 10 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), gradient_points()

### Community 12 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (29): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+21 more)

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFreezeBackground, ToggleFullscreen, ToggleStripChartAutoFit (+1 more)

### Community 16 - "Visual"
Cohesion: 0.08
Nodes (3): draw_vessel(), draw_glow(), Visual

### Community 19 - "os"
Cohesion: 0.07
Nodes (4): flush(), flush_all(), run(), NetFilterQueueBaseClass

### Community 20 - "arp_poisoner.py"
Cohesion: 0.15
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "CheckboxOverlay"
Cohesion: 0.14
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 31 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 32 - "LayoutEditor"
Cohesion: 0.07
Nodes (5): LayoutEditor, add(), add(), on_change(), SettingsSection

### Community 34 - "HVACView"
Cohesion: 0.12
Nodes (3): HVACView, enc_button(), slider_callback()

### Community 35 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 38 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (7): fade_in(), SummaryCard, WorkspaceButton, WorkspaceSelectPage, update(), paint_panel(), surface_shadow()

### Community 41 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 43 - ".columnconfigure"
Cohesion: 0.05
Nodes (4): Builder, Builder, Builder, Builder

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 50 - "ConfigEditor"
Cohesion: 0.14
Nodes (3): ConfigEditor, walk(), discard()

### Community 53 - ".collect"
Cohesion: 0.11
Nodes (3): remove_nested(), set_nested(), group()

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 60 - "pyside6_qtwidgets"
Cohesion: 0.05
Nodes (10): BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm, NFQForm (+2 more)

### Community 62 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "Process"
Cohesion: 0.07
Nodes (4): Buffer, Denier, ProcessManager, Process

### Community 69 - "confirm_dialog"
Cohesion: 0.07
Nodes (8): DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton, confirm_dialog()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 76 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 78 - "VariableOverlay"
Cohesion: 0.17
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): ThemeEditorPage, preview(), message(), PopupWindow

### Community 83 - "ap_commands.py"
Cohesion: 0.16
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+8 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "window_chrome.py"
Cohesion: 0.17
Nodes (5): draw_window_bar_line(), _Strip, window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "sys"
Cohesion: 0.26
Nodes (3): build_name(), main(), write_build_info()

### Community 98 - "WorkspaceSorter"
Cohesion: 0.17
Nodes (3): WorkspaceSorter, create(), DragPayload

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 111 - "menu_bar.py"
Cohesion: 0.04
Nodes (13): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage (+5 more)

### Community 113 - "_Dim"
Cohesion: 0.11
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 119 - "record_schema.py"
Cohesion: 0.17
Nodes (10): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+2 more)

### Community 120 - "WorkspaceChip"
Cohesion: 0.18
Nodes (3): checkbox(), WorkspaceChip, edit()

### Community 122 - "WindowDrag"
Cohesion: 0.15
Nodes (3): SquareButtons, toggle_maximized(), WindowDrag

### Community 129 - "NMapper"
Cohesion: 0.12
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 131 - "SelectRegisterPreset"
Cohesion: 0.17
Nodes (3): SelectBackground, SelectRegisterPreset, background_choices()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "geometry.py"
Cohesion: 0.07
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+6 more)

### Community 141 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (17): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+9 more)

### Community 150 - "ContextManager"
Cohesion: 0.12
Nodes (4): ContextManager, apply_scale_about(), developer_text(), compile_packet_filter()

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

### Community 163 - "Canvas"
Cohesion: 0.12
Nodes (4): Canvas, DefenderWorldMap, House, TriangleCanvas

### Community 171 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (26): NetworkDiagramCanvas, StripChart, WorldMap, Scrollable, panel(), Builder, ChartsExample, ControlsExample (+18 more)

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 178 - "NoteBrowser"
Cohesion: 0.18
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 179 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 189 - "overlay.py"
Cohesion: 0.13
Nodes (6): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SettingsOverlayButton

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.15
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

## Knowledge Gaps
- **42 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1633 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **131 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `router.py`, `host.py`, `PageManager`, `important_buttons/__init__.py`, `Visual`, `hvac_view.py`, `FilterOverlay`, `.start_session`, `threading`, `CheckboxOverlay`, `Performance`, `ClickManager`, `Canvas`, `LocalizationManager`, `widgets/__init__.py`, `InputManager`, `Json`, `KeyBinds`, `pyside6_qtwidgets`, `overlay.py`, `open_favorite_page.py`, `Process`, `confirm_dialog`, `AnimationManager`, `Preferences`, `VariableOverlay`, `window_chrome.py`, `.reload_preferences`, `menu_bar.py`, `Style`?**
  _High betweenness centrality (0.267) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07215686274509804 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.apply_theme`, `SettingsSection`, `.preset_name`, `._build_stylesheet`, `important_buttons/__init__.py`, `.theme_family`, `menu_bar.py`, `.discard_changes`, `.start_session`, `QWidget`, `ContextManager`, `Overlay`, `.link_color`, `overlay.py`, `open_favorite_page.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `router.py` be split into smaller, more focused modules?**
  _Cohesion score 0.056051587301587304 - nodes in this community are weakly interconnected._