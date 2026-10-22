# Graph Report - cybersecurity-game  (2026-10-22)

## Corpus Check
- 312 files · ~258,259 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4630 nodes · 9764 edges · 216 communities (77 shown, 139 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 490 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a1b4ee6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- os
- MetaPacket
- PacketBuffer
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- config_editor.py
- .columnconfigure
- ._build_stylesheet
- PageManager
- .__init__
- SettingsPage
- .__init__
- geometry.py
- PacketColumnsOverlay
- app.py
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
- Buffer
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- Draw
- Runtime Requirements
- .__init__
- MapBuffer
- launch.py
- ConfigEditor
- NMapper
- DropZone
- .fill_base
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- .__init__
- .add_header
- Modify
- .strip_chart_layout
- Router
- _PollUnpacker
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- VariableOverlay
- palette_generator.py
- Context
- WindowBarButton
- PrivilegedHelper
- Constellation
- Preferences
- host.py
- ._draw_text
- WorkspaceSorter
- DragHandle
- .build_workspace_section
- CheckboxOverlay
- WaveGrid
- QWidget
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
- Table
- AnimationManager
- time
- surface_shadow
- ModBus HVAC Exercise Screenshot
- bare_icon
- DockArea
- .__init__
- Kalman
- SampleNetwork
- SectionCard
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- Camera
- GrowingButton
- NewWorkspaceDialog
- MaterialEditor
- Draw
- .__init__
- .collapsed
- .populate_filter_overlay
- NoteBrowser
- BinZone
- Panes
- .apply_theme
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- .__init__
- NetFilterQueue
- StreamIncomingPacketsToMcap
- SampleSubmarine
- _Dim
- CornerControls
- themes.py
- PooledCanvasMixin
- VisualPalette
- MaterialEditorPopup
- .target_at
- DefenderHVACChart
- FileStream
- .css
- important_buttons/__init__.py
- .__init__
- frame_callback
- .leaf
- Meter
- panel
- _Chip
- MitmTable
- .arrow
- ShiftWheel
- SummaryDrawer
- TabStrip
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- SampleHVAC
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- Map
- .save_current_page
- WindowEdges
- CLAUDE.md
- .collect
- ._scan_for_networks
- Builder
- .__init__
- .authored_weights
- .prepare_page_config
- on_activated
- Loader
- ap_commands.py
- _SaveLayoutAsDefault
- _Grip
- PopupWindow
- .build_description_tab
- fade_in
- _OnHide
- _Indicator
- WorkspaceButton
- Process
- ToggleButton
- Canvas
- align_decimals
- WifiForm
- _DrawerLayout
- Overlay
- ModeForm
- .make_built_in
- Builder
- PreferencesData
- TopLayout
- Telemetry
- .add_labeled_entry

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

## Communities (216 total, 139 thin omitted)

### Community 0 - "os"
Cohesion: 0.08
Nodes (3): flush(), flush_all(), run()

### Community 1 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 2 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 8 - "config_editor.py"
Cohesion: 0.11
Nodes (9): BoatMotion, make_workspace(), Sprites, Triangle, WorkspacePage, NotFound, Page, TriangleCanvas (+1 more)

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 14 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 15 - ".__init__"
Cohesion: 0.05
Nodes (3): FilterOverlay, FilterPacketConsole, OpenFavoritePage

### Community 16 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.08
Nodes (10): DragPayload, RowZone, column_category(), column_position(), is_column_available(), PacketColumnsOverlay, autosave(), shown_columns() (+2 more)

### Community 23 - "server.py"
Cohesion: 0.10
Nodes (10): build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.10
Nodes (6): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine()

### Community 30 - "ContextManager"
Cohesion: 0.06
Nodes (29): ContextManager, apply_scale_about(), House, NetworkDiagramCanvas, StripChart, WorldMap, ListZone, form_order() (+21 more)

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 37 - "describe.py"
Cohesion: 0.12
Nodes (18): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), info(), modbus_function(), modbus_info() (+10 more)

### Community 40 - "Buffer"
Cohesion: 0.06
Nodes (5): Buffer, HouseBuffer, ModbusBuffer, StatusBuffer, MetaStatus

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 47 - ".__init__"
Cohesion: 0.09
Nodes (6): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideTitle

### Community 49 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 51 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 53 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 59 - ".__init__"
Cohesion: 0.12
Nodes (7): PassWheel, SampleHouse, SampleNetworkDiagram, SamplePackets, SampleWorldMap, StatusExample, TabsExample

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 69 - "VariableOverlay"
Cohesion: 0.22
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 71 - "Context"
Cohesion: 0.18
Nodes (7): delete_workspace(), drop_unused_labels(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), write_config_values()

### Community 72 - "WindowBarButton"
Cohesion: 0.09
Nodes (5): bar_button_height(), SquareButtons, WindowBarButton, WindowControls, WindowDrag

### Community 78 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".build_workspace_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 81 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 83 - "QWidget"
Cohesion: 0.09
Nodes (4): _Peek, _SideStrip, TabbedPane, paint_panel()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.14
Nodes (4): push_submarine_settings(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 97 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "time"
Cohesion: 0.10
Nodes (3): _is_global(), _resolve_local_mac(), RetentionPolicy

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 106 - "SectionCard"
Cohesion: 0.10
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 110 - "Camera"
Cohesion: 0.12
Nodes (5): Camera, padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 112 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 117 - ".populate_filter_overlay"
Cohesion: 0.20
Nodes (4): _checkbox_value(), packet_filter(), activate(), save_filter_summary()

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 129 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 130 - "NetFilterQueue"
Cohesion: 0.09
Nodes (3): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue

### Community 135 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 136 - "CornerControls"
Cohesion: 0.13
Nodes (5): CornerControls, draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 137 - "themes.py"
Cohesion: 0.15
Nodes (9): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+1 more)

### Community 139 - "VisualPalette"
Cohesion: 0.10
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (43): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+35 more)

### Community 147 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

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

### Community 184 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 186 - "ap_commands.py"
Cohesion: 0.12
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+10 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 200 - "Process"
Cohesion: 0.04
Nodes (6): random_spline_path(), APPoller, Denier, Sniffer, ProcessManager, Process

### Community 202 - "ToggleButton"
Cohesion: 0.04
Nodes (10): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleBookmark, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView (+2 more)

### Community 203 - "Canvas"
Cohesion: 0.07
Nodes (5): Canvas, DefenderWorldMap, frame_callback(), sprite(), sprite_enabled()

### Community 204 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 210 - "Overlay"
Cohesion: 0.05
Nodes (17): ButtonGroup, offered_sections(), compile_packet_filter(), RefreshCurrentPage, SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle (+9 more)

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1843 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `InputManager`, `config_editor.py`, `PageManager`, `VisualPalette`, `.__init__`, `important_buttons/__init__.py`, `PacketColumnsOverlay`, `ShiftWheel`, `Performance`, `.start_session`, `LocalizationManager`, `.reset_page`, `Json`, `KeyBinds`, `Router`, `docking.py`, `Process`, `PrivilegedHelper`, `Preferences`, `host.py`, `CheckboxOverlay`, `Overlay`, `AnimationManager`, `time`, `Style`?**
  _High betweenness centrality (0.232) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `os` be split into smaller, more focused modules?**
  _Cohesion score 0.0846774193548387 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `SettingsSection`, `.start_session`, `config_editor.py`, `._build_stylesheet`, `.theme_family`, `QWidget`, `.__init__`, `.css`, `important_buttons/__init__.py`, `.discard_changes`, `Overlay`, `.preset_name`, `.apply_theme`, `ContextManager`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.07329462989840348 - nodes in this community are weakly interconnected._