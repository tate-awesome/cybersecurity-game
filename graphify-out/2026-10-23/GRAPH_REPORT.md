# Graph Report - cybersecurity-game  (2026-10-23)

## Corpus Check
- 327 files · ~278,569 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4855 nodes · 10260 edges · 230 communities (73 shown, 157 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 510 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `50dc9ea6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- server.py
- MetaPacket
- buffer_manager.py
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- Draw
- FilterOverlay
- ._build_stylesheet
- PageManager
- .__init__
- WindowDrag
- packet_filter.py
- PacketColumnsOverlay
- app.py
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- MenuBar
- FindBar
- VisualPalette
- background.py
- time
- ViewPort
- PacketTreeview
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- describe.py
- APPoller
- Camera
- menu_bar.py
- Dev/Host_API.py
- LocalizationManager
- PopupEntrance
- HostOverlay
- BaseForm
- Runtime Requirements
- TabStrip
- MapBuffer
- host.py
- ConfigEditor
- Overlay
- context_manager.py
- DefenderStatusBuffer
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- MaterialEditorPopup
- .add_header
- Modify
- .strip_chart_layout
- Router
- .setText
- DefenderModbusBuffer
- docking.py
- arpy2a.py
- StripChartBase
- SettingsPage
- palette_generator.py
- .add_labeled_entry
- NetFilterQueue
- PrivilegedHelper
- Constellation
- Preferences
- .apply_theme
- ._draw_text
- WorkspaceSorter
- BinZone
- .build_workspace_section
- WaveGrid
- Denier
- .add_setting_row
- Rows
- Builder
- ModBus Submarine Exercise Screenshot
- FadeIn
- SlidersForm
- Replay
- _Dim
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- Buffer
- CallbackRegistry
- .__init__
- SectionCard
- ModBus HVAC Exercise Screenshot
- DockArea
- ModbusBuffer
- Kalman
- SampleNetwork
- DropZone
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- PacketBuffer
- CheckboxOverlay
- TitleMenu
- network_graph.py
- WorkspaceSelectPage
- Draw
- WindowBarButton
- QWidget
- CycleBox
- NoteBrowser
- NewWorkspaceDialog
- Camera
- Panes
- Master
- Style
- AppearEffect
- Wifi
- Slave
- MainWindow
- ProcessManager
- NMapper
- MaterialEditor
- ContextManager
- Builder
- _Indicator
- bare_icon
- themes.py
- PooledCanvasMixin
- WindowEdges
- PopupWindow
- _Peek
- DefenderHVACChart
- paint_mark
- .collect
- important_buttons/__init__.py
- .play
- os
- Meter
- widgets/__init__.py
- _Chip
- .__init__
- ShiftWheel
- SummaryDrawer
- ComboColumn
- compile_filter
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Visual
- Prod/Host_API.py
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- paint_panel
- Map
- .save_current_page
- AnimationManager
- .target_at
- CLAUDE.md
- TransactionManager
- FileStream
- ._scan_for_networks
- .build_description_tab
- SettingsSection
- Scanlines
- .page_panel_keys
- .authored_weights
- WindowControls
- ap_commands.py
- .integer
- .brush
- _Grip
- _SaveLayoutAsDefault
- fade_in
- SampleSubmarine
- .leaf
- _PollUnpacker
- WorkspaceButton
- GrowingButton
- ModeForm
- core/transforms.py
- ToggleButton
- .__init__
- Builder
- Builder
- .__init__
- WifiForm
- _DressedWidgets
- _Proxy
- .__init__
- .__init__
- _OnHide
- _DrawerLayout
- Channel
- TopLayout
- ask_to_quit
- visuals/__init__.py
- confirm_dialog
- frame_callback
- MitmTable
- .__init__
- ShiftWheelSlider
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 142 edges
2. `ImportantButton` - 114 edges
3. `Style` - 110 edges
4. `Overlay` - 93 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
7. `MetaPacket` - 63 edges
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

## Communities (230 total, 157 thin omitted)

### Community 0 - "server.py"
Cohesion: 0.09
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 3 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 5 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 10 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 12 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 15 - "WindowDrag"
Cohesion: 0.12
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowDrag

### Community 16 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.07
Nodes (12): DragHandle, DragPayload, RowZone, ChooseShownPacketConsoleColumns, column_category(), column_position(), is_column_available(), PacketColumnsOverlay (+4 more)

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "background.py"
Cohesion: 0.13
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 27 - "time"
Cohesion: 0.06
Nodes (14): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+6 more)

### Community 28 - "ViewPort"
Cohesion: 0.06
Nodes (12): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine(), apply_scale_about(), get_arc_points() (+4 more)

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.06
Nodes (9): Table, fill_order(), key(), spread_order(), VariableOverlay, autosave(), reset_all(), CombinedTable (+1 more)

### Community 37 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 40 - "menu_bar.py"
Cohesion: 0.06
Nodes (14): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ToggleBookmark (+6 more)

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "BaseForm"
Cohesion: 0.12
Nodes (12): BaseForm, align_decimals(), format_number(), fraction_width(), APTunnelForm, ArpForm, DosForm, EncryptionForm (+4 more)

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "host.py"
Cohesion: 0.08
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 51 - "Overlay"
Cohesion: 0.07
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 53 - "context_manager.py"
Cohesion: 0.08
Nodes (4): _dialog_parent(), file_dialog(), NetFilterQueueBaseClass, Process

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 67 - "arpy2a.py"
Cohesion: 0.09
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 78 - "WorkspaceSorter"
Cohesion: 0.13
Nodes (3): WorkspaceSorter, create(), rename()

### Community 80 - ".build_workspace_section"
Cohesion: 0.24
Nodes (3): add(), click(), sync()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.15
Nodes (4): push_submarine_settings(), submarine_settings_synced(), SlidersForm, slider_callback()

### Community 92 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 96 - "Buffer"
Cohesion: 0.11
Nodes (3): Buffer, StatusBuffer, MetaStatus

### Community 97 - "CallbackRegistry"
Cohesion: 0.13
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - ".__init__"
Cohesion: 0.10
Nodes (6): PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SamplePackets, SampleWorldMap

### Community 99 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 110 - "CheckboxOverlay"
Cohesion: 0.06
Nodes (6): ListZone, PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 111 - "TitleMenu"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

### Community 112 - "network_graph.py"
Cohesion: 0.14
Nodes (3): _default_gateway_ip(), _is_global(), NetworkGraph

### Community 116 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 119 - "NewWorkspaceDialog"
Cohesion: 0.10
Nodes (5): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems(), delete()

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 130 - "NMapper"
Cohesion: 0.13
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 132 - "ContextManager"
Cohesion: 0.07
Nodes (18): ContextManager, conjugate(), quote(), BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace() (+10 more)

### Community 137 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 143 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (38): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs (+30 more)

### Community 147 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 148 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (25): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, WorldMap, form_order() (+17 more)

### Community 158 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 163 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 167 - "paint_panel"
Cohesion: 0.13
Nodes (3): _one_shadow(), paint_panel(), surface_shadow()

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.20
Nodes (14): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+6 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 201 - "core/transforms.py"
Cohesion: 0.15
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 202 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 203 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 212 - ".__init__"
Cohesion: 0.33
Nodes (3): encryption_enabled(), start_encryption(), stop_encryption()

### Community 219 - "visuals/__init__.py"
Cohesion: 0.13
Nodes (4): draw_vessel(), draw_glow(), DenseMesh, Telemetry

### Community 221 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1921 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **157 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `ProcessManager`, `buffer_manager.py`, `InputManager`, `PageManager`, `important_buttons/__init__.py`, `PacketColumnsOverlay`, `widgets/__init__.py`, `ShiftWheel`, `background.py`, `Performance`, `menu_bar.py`, `AnimationManager`, `LocalizationManager`, `BaseForm`, `host.py`, `Overlay`, `context_manager.py`, `Json`, `KeyBinds`, `Router`, `docking.py`, `PrivilegedHelper`, `Preferences`, `CallbackRegistry`, `CheckboxOverlay`, `network_graph.py`, `.start_session`, `Style`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08669354838709678 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `SettingsSection`, `.lift_button`, `menu_bar.py`, `._build_stylesheet`, `.apply_theme`, `.theme_family`, `_DressedWidgets`, `.discard_changes`, `important_buttons/__init__.py`, `Overlay`, `context_manager.py`, `.start_session`, `.brush`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.11261261261261261 - nodes in this community are weakly interconnected._