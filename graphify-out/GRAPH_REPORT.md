# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 307 files · ~248,103 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4438 nodes · 9335 edges · 216 communities (77 shown, 139 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 473 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06d93875`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MetaPacket
- server.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- overlay.py
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- ToggleButton
- geometry.py
- menu_bar.py
- _RightZoneRoom
- scrollable.py
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- time
- FindBar
- VisualPalette
- .__init__
- SessionRecorder
- ViewPort
- PacketTreeview
- ToggleBookmark
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
- QWidget
- HostOverlay
- APPoller
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
- Modify
- .strip_chart_layout
- Router
- _PollUnpacker
- DefenderModbusBuffer
- docking.py
- os
- StripChartBase
- Canvas
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
- RefreshCurrentPage
- Replay
- DropZone
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- PageTransition
- Panes
- AnimationManager
- FileStream
- Denier
- ModBus HVAC Exercise Screenshot
- MitmTable
- .__init__
- Map
- Kalman
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- Camera
- GrowingButton
- ProcessManager
- Draw
- align_decimals
- DockArea
- Overlay
- ContextManager
- WorkspaceChip
- .__init__
- .setText
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- .collapsed
- .__init__
- paint_mark
- _DropPreview
- place
- .slider
- _Dim
- .__init__
- themes.py
- PooledCanvasMixin
- Visual
- .__init__
- ConfigureThisWorkspace
- DefenderHVACChart
- NoteBrowser
- .css
- important_buttons/__init__.py
- .add_section
- Meter
- GoForwardToNextPage
- .populate_filter_overlay
- examples.py
- _Chip
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
- FilterOverlay
- .__init__
- .save_current_page
- MenuBar
- CLAUDE.md
- Attack
- .collect
- ._scan_for_networks
- paint_panel
- LinkToPage
- .authored_weights
- .prepare_page_config
- PacketBuffer
- .integer
- ap_commands.py
- .material_control
- SampleNetwork
- .__init__
- confirm_dialog
- frame_callback
- Builder
- Telemetry
- version.py
- DragHandle
- DenseMesh
- .build_description_tab
- random
- SelectRegisterPreset
- _OnHide
- WifiForm
- push_submarine_settings
- pyside6_qtwidgets
- frame_callback
- widgets/__init__.py
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

## Communities (216 total, 139 thin omitted)

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
Cohesion: 0.09
Nodes (6): on_change(), checked_value(), SettingsSection, save(), save(), on_change()

### Community 7 - "VisualBackground"
Cohesion: 0.06
Nodes (3): paint_noise_gradient(), pyramid_blur(), VisualBackground

### Community 9 - "overlay.py"
Cohesion: 0.13
Nodes (7): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, is_checked(), SettingsOverlayButton

### Community 12 - ".__init__"
Cohesion: 0.16
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), ring_spots()

### Community 15 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 16 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 17 - "menu_bar.py"
Cohesion: 0.04
Nodes (19): ButtonGroup, offered_sections(), OpenPauseMenu, bare_icon(), _FollowResize, global_buttons(), icon_button(), bar_button_height() (+11 more)

### Community 23 - "time"
Cohesion: 0.08
Nodes (4): Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - ".__init__"
Cohesion: 0.11
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+5 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

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

### Community 43 - "QWidget"
Cohesion: 0.18
Nodes (4): covered(), settle(), uncovered(), PopupEntrance

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - "QWidget"
Cohesion: 0.10
Nodes (3): _LentPlaceholder, _Peek, TabbedPane

### Community 49 - "launch.py"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 52 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - "SlidersForm"
Cohesion: 0.14
Nodes (4): submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.14
Nodes (15): add_tab(), find(), is_split(), leaf(), leaf_of(), move_panel(), new_id(), normalize() (+7 more)

### Community 67 - "os"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 69 - "Canvas"
Cohesion: 0.08
Nodes (6): Canvas, DefenderWorldMap, TriangleCanvas, WorldMap, Builder, is_on()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 77 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 81 - "config_editor.py"
Cohesion: 0.19
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 83 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "RefreshCurrentPage"
Cohesion: 0.18
Nodes (3): RefreshCurrentPage, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 92 - "DropZone"
Cohesion: 0.11
Nodes (3): DropZone, _Indicator, ListZone

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 115 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 117 - "Overlay"
Cohesion: 0.07
Nodes (4): SelectBackground, SelectColorTheme, Overlay, background_choices()

### Community 118 - "ContextManager"
Cohesion: 0.07
Nodes (13): ContextManager, WindowReveal, apply_scale_about(), BoatMotion, Sprites, Triangle, Visuals, TitlePage (+5 more)

### Community 126 - "Wifi"
Cohesion: 0.10
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 128 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 131 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 133 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "Visual"
Cohesion: 0.10
Nodes (4): draw_vessel(), value_noise(), draw_glow(), Visual

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (27): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+19 more)

### Community 149 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 150 - "examples.py"
Cohesion: 0.05
Nodes (18): House, ControlsExample, FlagsExample, HouseExample, MapExample, NetworkExample, PacketsExample, PassWheel (+10 more)

### Community 153 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 156 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 157 - "TabStrip"
Cohesion: 0.08
Nodes (4): PeekArrow, _SideStrip, _SideTitle, TabStrip

### Community 158 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 173 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 184 - "PacketBuffer"
Cohesion: 0.07
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 186 - "ap_commands.py"
Cohesion: 0.14
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+8 more)

### Community 189 - ".__init__"
Cohesion: 0.12
Nodes (5): from_tree(), split(), _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.04
Nodes (13): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault (+5 more)

### Community 191 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.13
Nodes (3): set_enabled(), set_read_only(), WifiForm

### Community 210 - "pyside6_qtwidgets"
Cohesion: 0.17
Nodes (9): BaseForm, ModeForm, APTunnelForm, ArpForm, DosForm, KalmanForm, NFQForm, NmapForm (+1 more)

### Community 214 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 215 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (10): StripChart, compile_packet_filter(), Scrollable, panel(), Builder, ChartsExample, Builder, Panel (+2 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1767 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `overlay.py`, `PageManager`, `Visual`, `ConfigureThisWorkspace`, `important_buttons/__init__.py`, `menu_bar.py`, `GoForwardToNextPage`, `scrollable.py`, `examples.py`, `time`, `ShiftWheel`, `.__init__`, `Performance`, `FilterOverlay`, `LocalizationManager`, `.start_session`, `.reset_page`, `LinkToPage`, `Json`, `KeyBinds`, `confirm_dialog`, `Router`, `docking.py`, `os`, `Canvas`, `PrivilegedHelper`, `Preferences`, `config_editor.py`, `pyside6_qtwidgets`, `widgets/__init__.py`, `AnimationManager`, `.apply_theme`, `ProcessManager`, `.setText`, `Style`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.click_open` be split into smaller, more focused modules?**
  _Cohesion score 0.11052631578947368 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.restyle`, `SettingsSection`, `overlay.py`, `._build_stylesheet`, `.apply_theme`, `.theme_family`, `.css`, `important_buttons/__init__.py`, `.start_session`, `.discard_changes`, `menu_bar.py`, `Overlay`, `ContextManager`, `.setText`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07616892911010557 - nodes in this community are weakly interconnected._