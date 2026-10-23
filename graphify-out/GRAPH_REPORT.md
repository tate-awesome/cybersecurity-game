# Graph Report - cybersecurity-game  (2026-10-23)

## Corpus Check
- 314 files · ~265,436 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4784 nodes · 10107 edges · 224 communities (85 shown, 139 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 507 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f05858dd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Process
- MetaPacket
- PacketBuffer
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- router.py
- FilterOverlay
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- .__init__
- packet_filter.py
- PacketColumnsOverlay
- App
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- server.py
- FindBar
- Kernel
- MenuBar
- SessionRecorder
- ViewPort
- PacketTreeview
- ContextManager
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- describe.py
- WorkspaceSelectPage
- Camera
- time
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- Draw
- Runtime Requirements
- TabStrip
- ModbusBuffer
- os
- ConfigEditor
- _base_button.py
- DropZone
- .fill_base
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- Scrollable
- .add_header
- Modify
- .strip_chart_layout
- Router
- RefreshCurrentPage
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- AnimationManager
- palette_generator.py
- config_editor.py
- QWidget
- PrivilegedHelper
- Constellation
- Preferences
- _Proxy
- ._draw_text
- WorkspaceSorter
- DragHandle
- .leaf
- DragPayload
- WaveGrid
- QWidget
- Overlay
- .add_setting_row
- Rows
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- SlidersForm
- Replay
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- StatusBuffer
- CallbackRegistry
- pyside6_qtgui
- .__init__
- ModBus HVAC Exercise Screenshot
- affine
- walk
- Kalman
- SampleNetwork
- WorkspaceChip
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- Camera
- .__init__
- NewWorkspaceDialog
- Draw
- ListZone
- paint_panel
- CycleBox
- NoteBrowser
- GrowingButton
- Panes
- .apply_theme
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- Denier
- NMapper
- ToggleButton
- SelectRegisterPreset
- VariableOverlay
- _Dim
- on_activated
- themes.py
- PooledCanvasMixin
- Visual
- DockArea
- DefenderHVACChart
- SelectBackground
- .css
- important_buttons/__init__.py
- frame_callback
- ConfigureThisWorkspace
- Meter
- widgets/__init__.py
- _Chip
- MitmTable
- .arrow
- ShiftWheel
- SummaryDrawer
- ComboColumn
- compile_filter
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- defender_hvac_chart.py
- _Gaps
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- _MapCanvas
- .save_current_page
- WindowEdges
- _DropPreview
- CLAUDE.md
- LinkToPage
- .collect
- ._scan_for_networks
- Builder
- DenseMesh
- .authored_weights
- .prepare_page_config
- WindowControls
- edit_modbus_register_display.py
- ap_commands.py
- filter_packet_console.py
- GoForwardToNextPage
- .__init__
- confirm_dialog
- .build_description_tab
- fade_in
- ResetCurrentPageToDefaults
- CheckboxOverlay
- _Indicator
- WorkspaceButton
- APPoller
- SampleHVAC
- table.py
- Table
- WifiForm
- _OnHide
- settings_overlay_button.py
- ToggleLightDarkMode
- SampleSubmarine
- _DrawerLayout
- VisualPalette
- ask_to_quit
- ToggleBookmark
- ElidingLabel
- .new_tab
- frame_callback
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 141 edges
2. `ImportantButton` - 112 edges
3. `Style` - 100 edges
4. `Overlay` - 93 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
7. `MetaPacket` - 63 edges
8. `ConfigEditor` - 58 edges
9. `DockArea` - 53 edges
10. `Panel` - 51 edges

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

## Communities (224 total, 139 thin omitted)

### Community 0 - "Process"
Cohesion: 0.05
Nodes (7): file_dialog(), random_spline_path(), Buffer, ProcessManager, Process, FileStream, Loader

### Community 1 - "MetaPacket"
Cohesion: 0.06
Nodes (7): Channel, _default_gateway_ip(), NetworkGraph, Transaction, TransactionManager, MetaPacket, NetFilterQueueBaseClass

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (8): BuildInfo, _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (5): checked_value(), SettingsSection, save(), save(), on_change()

### Community 8 - "router.py"
Cohesion: 0.07
Nodes (10): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page (+2 more)

### Community 9 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 14 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 16 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.12
Nodes (4): column_category(), is_column_available(), PacketColumnsOverlay, autosave()

### Community 19 - "App"
Cohesion: 0.11
Nodes (5): App, covered(), settle(), uncovered(), __getattr__()

### Community 20 - "ThemeEditorPage"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, MaterialEditor, preview(), ThemeEditorPage

### Community 23 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "MenuBar"
Cohesion: 0.03
Nodes (14): ButtonGroup, offered_sections(), bare_icon(), _FollowResize, global_buttons(), MenuBar, _RightZoneRoom, bar_button_height() (+6 more)

### Community 27 - "SessionRecorder"
Cohesion: 0.05
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 30 - "ContextManager"
Cohesion: 0.11
Nodes (13): ContextManager, shown_columns(), BaseForm, ModeForm, APConnectForm, APTunnelForm, ArpForm, DosForm (+5 more)

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
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 48 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 49 - "os"
Cohesion: 0.05
Nodes (15): build_name(), main(), write_build_info(), flush(), flush_all(), run(), _dialog_parent(), git() (+7 more)

### Community 51 - "_base_button.py"
Cohesion: 0.11
Nodes (6): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 53 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 59 - "Scrollable"
Cohesion: 0.08
Nodes (9): Scrollable, ChartsExample, ControlsExample, FlagsExample, PassWheel, SampleHouse, SampleNetworkDiagram, SamplePackets (+1 more)

### Community 60 - ".add_header"
Cohesion: 0.05
Nodes (3): encryption_enabled(), start_encryption(), stop_encryption()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - "RefreshCurrentPage"
Cohesion: 0.15
Nodes (4): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (14): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+6 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "config_editor.py"
Cohesion: 0.14
Nodes (11): conjugate(), quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+3 more)

### Community 72 - "QWidget"
Cohesion: 0.14
Nodes (3): draw_window_bar_line(), SquareButtons, _Strip

### Community 78 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 83 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 91 - "Replay"
Cohesion: 0.07
Nodes (4): dissect(), link_of(), RecordFilter, Replay

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "CallbackRegistry"
Cohesion: 0.13
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "pyside6_qtgui"
Cohesion: 0.08
Nodes (8): apply_scale_about(), scale(), translate(), Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 99 - ".__init__"
Cohesion: 0.14
Nodes (3): Builder, Builder, Builder

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 101 - "affine"
Cohesion: 0.14
Nodes (7): canvas_fit(), padded_fit(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 102 - "walk"
Cohesion: 0.13
Nodes (4): visit(), is_split(), panel_ids(), walk()

### Community 106 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 112 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 116 - "paint_panel"
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 130 - "NMapper"
Cohesion: 0.07
Nodes (5): NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 131 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 134 - "VariableOverlay"
Cohesion: 0.29
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 136 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 141 - "DockArea"
Cohesion: 0.09
Nodes (3): DockArea, DropTarget, leaf_of()

### Community 143 - "SelectBackground"
Cohesion: 0.18
Nodes (3): SelectBackground, SelectColorTheme, background_choices()

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.05
Nodes (19): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearStatusConsole, EditNetworkHosts, LoadLocalizationLabelsFile (+11 more)

### Community 147 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.07
Nodes (16): NetworkDiagramCanvas, StripChart, form_order(), panel(), Builder, HouseExample, MapExample, NetworkExample (+8 more)

### Community 158 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 175 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.14
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+7 more)

### Community 188 - "GoForwardToNextPage"
Cohesion: 0.11
Nodes (3): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu

### Community 189 - ".__init__"
Cohesion: 0.12
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.04
Nodes (13): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, column_position(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault (+5 more)

### Community 195 - "CheckboxOverlay"
Cohesion: 0.12
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 204 - "table.py"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 206 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 207 - "WifiForm"
Cohesion: 0.06
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "settings_overlay_button.py"
Cohesion: 0.09
Nodes (7): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, is_checked(), SettingsOverlayButton

### Community 219 - "VisualPalette"
Cohesion: 0.10
Nodes (7): draw_vessel(), get_arc_points(), get_bearing(), rotate(), draw_glow(), VisualPalette, Telemetry

### Community 232 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1892 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Process`, `InputManager`, `router.py`, `PageManager`, `.__init__`, `important_buttons/__init__.py`, `.start_session`, `ConfigureThisWorkspace`, `widgets/__init__.py`, `ShiftWheel`, `MenuBar`, `Performance`, `defender_hvac_chart.py`, `time`, `LocalizationManager`, `LinkToPage`, `os`, `.reset_page`, `_base_button.py`, `Json`, `KeyBinds`, `edit_modbus_register_display.py`, `filter_packet_console.py`, `GoForwardToNextPage`, `confirm_dialog`, `Router`, `docking.py`, `CheckboxOverlay`, `AnimationManager`, `config_editor.py`, `PrivilegedHelper`, `Preferences`, `table.py`, `settings_overlay_button.py`, `VisualPalette`, `CallbackRegistry`, `pyside6_qtgui`, `.__init__`, `Style`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Process` be split into smaller, more focused modules?**
  _Cohesion score 0.05446853516657853 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `MenuBar`, `SettingsSection`, `._build_stylesheet`, `.theme_family`, `QWidget`, `.__init__`, `.css`, `.start_session`, `.discard_changes`, `_base_button.py`, `settings_overlay_button.py`, `Overlay`, `.preset_name`, `.apply_theme`, `ContextManager`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.05721153846153846 - nodes in this community are weakly interconnected._