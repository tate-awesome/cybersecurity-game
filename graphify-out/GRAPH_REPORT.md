# Graph Report - cybersecurity-game  (2026-10-23)

## Corpus Check
- 327 files · ~277,927 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4853 nodes · 10254 edges · 226 communities (85 shown, 141 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 510 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1e33268`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- threading
- MetaPacket
- time
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
- FilterError
- PacketColumnsOverlay
- App
- ThemeEditorPage
- NetworkMesh
- AttackHMI_relay_ramp_attack.py
- MenuBar
- FindBar
- VisualPalette
- background.py
- SessionRecorder
- ViewPort
- PacketTreeview
- Builder
- FlowLayout
- LayoutEditor
- Performance
- wifi_windows.py
- Wifi
- CombinedTable
- describe.py
- packet_filter.py
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
- sys
- ConfigEditor
- settings_overlay_button.py
- Overlay
- Process
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
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- SettingsPage
- palette_generator.py
- .fixed_width_wrapper
- NetFilterQueue
- PrivilegedHelper
- Constellation
- Preferences
- geometry.py
- ._draw_text
- WorkspaceSorter
- DragHandle
- .leaf
- WaveGrid
- Denier
- QWidget
- .add_setting_row
- Builder
- ModBus Submarine Exercise Screenshot
- app.py
- SlidersForm
- Replay
- _Dim
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- StatusBuffer
- AnimationManager
- QWidget
- SectionCard
- ModBus HVAC Exercise Screenshot
- .__init__
- DockArea
- Kalman
- SampleNetwork
- DragPayload
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- transformations.py
- CheckboxOverlay
- GrowingButton
- SelectRegisterPreset
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
- NMapper
- MaterialEditor
- ContextManager
- .columnconfigure
- DropZone
- bare_icon
- style.py
- PooledCanvasMixin
- WindowEdges
- PopupWindow
- _Peek
- DefenderHVACChart
- paint_mark
- .collect
- important_buttons/__init__.py
- .play
- Meter
- Panel
- _Chip
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
- _MapCanvas
- .save_current_page
- .__init__
- .target_at
- CLAUDE.md
- Map
- table.py
- ._scan_for_networks
- .build_description_tab
- SettingsSection
- Scanlines
- .page_panel_keys
- .authored_weights
- CornerControls
- ap_commands.py
- .integer
- _Grip
- confirm_dialog
- fade_in
- SampleSubmarine
- SelectColorTheme
- select_background.py
- WorkspaceButton
- ModeForm
- core/transforms.py
- ToggleButton
- Builder
- Builder
- Table
- WifiForm
- _DressedWidgets
- _Proxy
- _Drawer
- .__init__
- visuals/__init__.py
- .make_built_in
- frame_callback
- MitmTable
- .__init__
- .new_tab
- frame_callback

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

## Communities (226 total, 141 thin omitted)

### Community 0 - "threading"
Cohesion: 0.04
Nodes (15): flush(), flush_all(), run(), NetFilterQueueBaseClass, Sniffer, build_capability(), _Echo, _BufferShim (+7 more)

### Community 1 - "MetaPacket"
Cohesion: 0.04
Nodes (6): Channel, _default_gateway_ip(), NetworkGraph, PacketBuffer, Transaction, MetaPacket

### Community 2 - "time"
Cohesion: 0.08
Nodes (4): PreferencesData, ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 3 - "Footer"
Cohesion: 0.06
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 5 - "SettingsSection"
Cohesion: 0.10
Nodes (5): is_checked(), SettingsSection, save(), save(), on_change()

### Community 9 - "FilterOverlay"
Cohesion: 0.13
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

### Community 16 - "FilterError"
Cohesion: 0.26
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.14
Nodes (3): column_category(), PacketColumnsOverlay, autosave()

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "background.py"
Cohesion: 0.14
Nodes (5): paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 27 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 28 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 31 - "FlowLayout"
Cohesion: 0.06
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 34 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.08
Nodes (5): VariableOverlay, autosave(), reset_all(), CombinedTable, entry()

### Community 37 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 38 - "packet_filter.py"
Cohesion: 0.15
Nodes (9): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_outside_quotes(), to_state() (+1 more)

### Community 40 - "menu_bar.py"
Cohesion: 0.07
Nodes (12): ButtonGroup, offered_sections(), ask_to_quit(), QuitApplication, ToggleBookmark, ShowHelpMessage, global_buttons(), icon_button() (+4 more)

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "BaseForm"
Cohesion: 0.08
Nodes (9): BaseForm, APConnectForm, APTunnelForm, ArpForm, EncryptionForm, KalmanForm, NFQForm, NmapForm (+1 more)

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "sys"
Cohesion: 0.10
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 51 - "settings_overlay_button.py"
Cohesion: 0.11
Nodes (7): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, checked_value(), SettingsOverlayButton

### Community 53 - "Process"
Cohesion: 0.05
Nodes (9): _dialog_parent(), file_dialog(), Buffer, TransactionManager, ProcessManager, Process, FileStream, Loader (+1 more)

### Community 54 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 60 - ".add_header"
Cohesion: 0.07
Nodes (3): DosForm, start_encryption(), stop_encryption()

### Community 62 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 76 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 78 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "app.py"
Cohesion: 0.17
Nodes (4): DesktopFade, FadeIn, FadeOut, WindowReveal

### Community 90 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 91 - "Replay"
Cohesion: 0.09
Nodes (3): dissect(), RecordFilter, Replay

### Community 92 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 93 - "Full Attacker Exercise Workspace Screenshot"
Cohesion: 0.19
Nodes (14): Full Attacker Exercise Workspace Screenshot, ARP Spoofing Form (Target IP / Host IP), ModBus Holding Registers (HReg 1-7), Minimizable Panel Layout Pattern, ModBus Data Panel (ModBus Readings table of HRegs), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (HReg time-series plots), Network Access Panel (WiFi Connection, NMapping, ARP Spoofing) (+6 more)

### Community 94 - "DoS Attack Workspace Screenshot"
Cohesion: 0.20
Nodes (13): DoS Attack Workspace Screenshot, ARP Spoofing Form (Target/Host IP), Denial-of-Service Exercise, ModBus Data Panel (HReg Readings), ModBus Model Panel (Submarine), ModBus Monitors Panel (HReg time-series), Network Actions Panel, Network Graph Panel (Packets per Second) (+5 more)

### Community 97 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 98 - "QWidget"
Cohesion: 0.11
Nodes (6): WorldMap, ControlsExample, FlagsExample, RegistersExample, SampleHVAC, SampleWorldMap

### Community 99 - "SectionCard"
Cohesion: 0.14
Nodes (3): CategoryChip, checkbox(), SectionCard

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 105 - "SampleNetwork"
Cohesion: 0.15
Nodes (3): SampleNetwork, SamplePacket, SamplePackets

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "transformations.py"
Cohesion: 0.32
Nodes (3): canvas_fit(), padded_fit(), affine()

### Community 110 - "CheckboxOverlay"
Cohesion: 0.04
Nodes (8): PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, OpenFavoritePage, ChooseShownPacketConsoleColumns

### Community 111 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 115 - "WindowBarButton"
Cohesion: 0.19
Nodes (3): bar_button_height(), WindowBarButton, WindowControls

### Community 116 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 119 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 130 - "NMapper"
Cohesion: 0.07
Nodes (5): APPoller, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 132 - "ContextManager"
Cohesion: 0.07
Nodes (19): ContextManager, BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+11 more)

### Community 135 - "DropZone"
Cohesion: 0.08
Nodes (4): DropZone, _Indicator, ListZone, RowZone

### Community 137 - "style.py"
Cohesion: 0.09
Nodes (13): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme() (+5 more)

### Community 143 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (36): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole (+28 more)

### Community 147 - ".play"
Cohesion: 0.24
Nodes (3): covered(), settle(), uncovered()

### Community 150 - "Panel"
Cohesion: 0.06
Nodes (17): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, panel(), Builder, ChartsExample (+9 more)

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

### Community 174 - "table.py"
Cohesion: 0.33
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 175 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.13
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+9 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 190 - "confirm_dialog"
Cohesion: 0.04
Nodes (15): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, column_position(), is_column_available(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault (+7 more)

### Community 201 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 202 - "ToggleButton"
Cohesion: 0.04
Nodes (10): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView (+2 more)

### Community 206 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 214 - ".__init__"
Cohesion: 0.12
Nodes (3): StatusExample, TabsExample, _DrawerLayout

### Community 219 - "visuals/__init__.py"
Cohesion: 0.11
Nodes (6): draw_vessel(), nice_number(), nice_ticks(), draw_glow(), DenseMesh, Telemetry

### Community 221 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 225 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1920 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **141 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `threading`, `.reset_page`, `time`, `Footer`, `InputManager`, `style.py`, `PageManager`, `important_buttons/__init__.py`, `Panel`, `ShiftWheel`, `background.py`, `Performance`, `menu_bar.py`, `LocalizationManager`, `BaseForm`, `table.py`, `settings_overlay_button.py`, `Process`, `Json`, `KeyBinds`, `confirm_dialog`, `Router`, `docking.py`, `PrivilegedHelper`, `Preferences`, `WifiForm`, `AnimationManager`, `CheckboxOverlay`, `.start_session`, `Style`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `threading` be split into smaller, more focused modules?**
  _Cohesion score 0.03677221654749745 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `time`, `ContextManager`, `SettingsSection`, `.lift_button`, `menu_bar.py`, `style.py`, `._build_stylesheet`, `.theme_family`, `CheckboxOverlay`, `_DressedWidgets`, `.discard_changes`, `important_buttons/__init__.py`, `settings_overlay_button.py`, `Overlay`, `.start_session`, `.brush`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.04130808950086059 - nodes in this community are weakly interconnected._