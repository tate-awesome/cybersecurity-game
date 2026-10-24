# Graph Report - cybersecurity-game  (2026-10-24)

## Corpus Check
- 327 files · ~279,664 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4848 nodes · 10196 edges · 231 communities (89 shown, 142 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 494 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bee73dfa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- server.py
- MetaPacket
- open_in_browser
- Footer
- InputManager
- SettingsSection
- PauseMenu
- VisualBackground
- FilterOverlay
- ._build_stylesheet
- PageManager
- channels/__init__.py
- window_chrome.py
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
- router.py
- PacketTreeview
- filter_overlay.py
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
- align_decimals
- Runtime Requirements
- TabStrip
- DefenderStatusBuffer
- launch.py
- ConfigEditor
- Overlay
- ViewPort
- threading
- .__init__
- WifiBaseClass
- VectorField
- Json
- KeyBinds
- MaterialEditorPopup
- .__init__
- Modify
- .strip_chart_layout
- .__init__
- DefenderModbusBuffer
- docking.py
- Attack
- StripChartBase
- SettingsPage
- palette_generator.py
- ElidingLabel
- NetFilterQueue
- PrivilegedHelper
- Constellation
- Preferences
- ChoiceList
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
- FadeIn
- SlidersForm
- Replay
- _Dim
- Full Attacker Exercise Workspace Screenshot
- DoS Attack Workspace Screenshot
- QWidget
- StatusBuffer
- AnimationManager
- WorkspaceChip
- ModBus HVAC Exercise Screenshot
- DockArea
- ModbusBuffer
- Kalman
- MaterialEditor
- DropZone
- Defender Full Suite Exercise Screenshot
- ArpSpoofer
- PacketBuffer
- CheckboxOverlay
- TitlePage
- SectionCard
- WorkspaceSelectPage
- Draw
- on_activated
- QWidget
- CycleBox
- NoteBrowser
- config_editor.py
- Camera
- Panes
- Canvas
- Master
- .apply_theme
- AppearEffect
- Wifi
- Slave
- MainWindow
- ProcessManager
- NMapper
- .__init__
- pyside6_qtcore
- paint_mark
- ListZone
- DragPayload
- style.py
- PooledCanvasMixin
- WindowEdges
- _base_button.py
- WindowControls
- defender_hvac_chart.py
- SummaryDrawer
- _SaveLayoutAsDefault
- important_buttons/__init__.py
- .play
- bare_icon
- Meter
- widgets/__init__.py
- sys
- Scrollable
- ShiftWheel
- paint_panel
- ComboColumn
- compile_filter
- Utah Smart Energy Lab
- Utah Smart Energy Lab (U-SMART)
- Visual
- Skull Hacker Image (skull.png)
- Dev Requirements (pyright)
- RecordFilter
- _MapCanvas
- .save_current_page
- _Chip
- .target_at
- CLAUDE.md
- _Drawer
- dumps
- ._scan_for_networks
- .record
- DenseMesh
- SettingsSection
- blurred_shape
- .page_panel_keys
- .authored_weights
- ap_commands.py
- .integer
- _Grip
- record_schema.py
- Draw
- place
- tray_columns
- GrowingButton
- Style
- ContextManager
- core/transforms.py
- ToggleButton
- .__init__
- _RightZoneRoom
- version.py
- Loader
- WifiForm
- .__init__
- _DressedWidgets
- _Proxy
- fade_in
- _Echo
- _BufferShim
- WorkspaceButton
- LookOnly
- .arrow
- Telemetry
- WindowBarButton
- MitmTable
- .__init__
- .describe
- flusher.py
- frame_callback
- frame_callback

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 142 edges
2. `Style` - 119 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 99 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 58 edges
8. `BaseForm` - 56 edges
9. `DockArea` - 53 edges
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
- 3-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 4-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/theme_editor.py -> game/src/__init__.py`
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

## Communities (231 total, 142 thin omitted)

### Community 0 - "server.py"
Cohesion: 0.19
Nodes (8): build_capability(), _ContextStub, _dispatch(), run(), flusher(), run_from_argv(), send(), status_heartbeat()

### Community 1 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 2 - "open_in_browser"
Cohesion: 0.08
Nodes (7): open_in_browser(), DeleteAllUserData, ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 3 - "Footer"
Cohesion: 0.05
Nodes (8): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip(), Scanlines

### Community 5 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 10 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 15 - "window_chrome.py"
Cohesion: 0.10
Nodes (8): bar_button_height(), draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_height(), window_bar_room(), WindowDrag

### Community 16 - "FilterError"
Cohesion: 0.21
Nodes (6): FilterError, parse(), Parser, split_outside_quotes(), tokenize(), unquote()

### Community 17 - "PacketColumnsOverlay"
Cohesion: 0.10
Nodes (5): RowZone, column_category(), is_column_available(), PacketColumnsOverlay, autosave()

### Community 24 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 26 - "background.py"
Cohesion: 0.13
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 28 - "router.py"
Cohesion: 0.06
Nodes (15): canvas_fit(), padded_fit(), affine(), apply_scale_about(), scale(), translate(), BoatMotion, Sprites (+7 more)

### Community 30 - "filter_overlay.py"
Cohesion: 0.18
Nodes (8): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_pair(), to_state()

### Community 34 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 35 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 36 - "CombinedTable"
Cohesion: 0.08
Nodes (5): VariableOverlay, autosave(), reset_all(), CombinedTable, entry()

### Community 37 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 40 - "menu_bar.py"
Cohesion: 0.07
Nodes (9): developer_text(), ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark (+1 more)

### Community 41 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 44 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 45 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 46 - "Runtime Requirements"
Cohesion: 0.10
Nodes (17): Game Architecture Outline, Modbus Master, Modbus Register/Frame Protocol, Network Interface Layer, Modbus Slave, Game GUI Design README, Metapacket Object, Runtime Requirements (+9 more)

### Community 49 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 51 - "Overlay"
Cohesion: 0.04
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 52 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 53 - "threading"
Cohesion: 0.05
Nodes (5): Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 57 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 62 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 64 - ".__init__"
Cohesion: 0.05
Nodes (3): OpenFavoritePage, ToggleDebugLabels, icon_button()

### Community 66 - "docking.py"
Cohesion: 0.12
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 67 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 70 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 76 - "ChoiceList"
Cohesion: 0.13
Nodes (3): _ComboLists, _StyledComboItems, ChoiceList

### Community 78 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 80 - ".leaf"
Cohesion: 0.14
Nodes (3): add(), click(), sync()

### Community 85 - "QWidget"
Cohesion: 0.16
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 88 - "ModBus Submarine Exercise Screenshot"
Cohesion: 0.16
Nodes (14): ModBus Submarine Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (Submarine position grid), ModBus Monitors Panel (Speed/Rudder time series), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing), Network Graph Panel (Packets per Second) (+6 more)

### Community 89 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 90 - "SlidersForm"
Cohesion: 0.13
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

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
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 99 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 100 - "ModBus HVAC Exercise Screenshot"
Cohesion: 0.19
Nodes (13): ModBus HVAC Exercise Screenshot, ARP Spoofing Form (Target IP, Host IP), ModBus Man-in-the-Middle Attack Exercise, ModBus Data Panel (Readings and Modifiers), ModBus Model Panel (HVAC visualization), ModBus Modifiers (Mult/Offset per variable), ModBus Monitors Panel (Heater state, Temperature charts), Network Actions Panel (WiFi Connection, NMapping, ARP Spoofing) (+5 more)

### Community 103 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 107 - "Defender Full Suite Exercise Screenshot"
Cohesion: 0.24
Nodes (11): Defender Full Suite Exercise Screenshot, Defender Data Panel (Operation Mode, Submarine Settings sliders), Defender Flags Panel (Submarine Error Detection Flags, Kalman Filter status), Defender Monitors (X/Y Position vs Time plots), Kalman Filter Anomaly Detection, ModBus Model Map (Defender Map, Auto-Switch), Network Access Panel (WiFi Connection, NMapping, Packet Sniffing, AP Connection), Packet Log Panel (last 10; Time, X, Y, Theta, Speed, Rudder) (+3 more)

### Community 109 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 110 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (7): PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 111 - "TitlePage"
Cohesion: 0.15
Nodes (3): TitlePage, TitleFooter, TitleMenu

### Community 115 - "on_activated"
Cohesion: 0.25
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 116 - "QWidget"
Cohesion: 0.12
Nodes (3): _LentPlaceholder, _SideStrip, TabbedPane

### Community 118 - "NoteBrowser"
Cohesion: 0.14
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 119 - "config_editor.py"
Cohesion: 0.08
Nodes (14): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), remove_nested(), rename_workspace() (+6 more)

### Community 122 - "Canvas"
Cohesion: 0.08
Nodes (7): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, WorldMap, Builder, is_on()

### Community 126 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 130 - "NMapper"
Cohesion: 0.07
Nodes (5): NetFilterQueue, NMapper, InterfaceManager, job(), Sniffer

### Community 132 - "pyside6_qtcore"
Cohesion: 0.10
Nodes (3): PreferencesData, Router, shown_columns()

### Community 134 - "paint_mark"
Cohesion: 0.12
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow

### Community 137 - "style.py"
Cohesion: 0.12
Nodes (11): button_radius(), gradient_points(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 140 - "_base_button.py"
Cohesion: 0.05
Nodes (11): make(), ClearSavedWorkspaceInputs, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton (+3 more)

### Community 144 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 145 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (25): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, ConfigureThisWorkspace (+17 more)

### Community 147 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (8): StripChart, panel(), Builder, Builder, _DrawerLayout, Panel, Builder, Builder

### Community 151 - "sys"
Cohesion: 0.22
Nodes (3): build_name(), main(), write_build_info()

### Community 153 - "Scrollable"
Cohesion: 0.06
Nodes (5): _Gaps, Scrollable, Builder, Builder, Builder

### Community 158 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 159 - "Utah Smart Energy Lab"
Cohesion: 0.67
Nodes (4): Smart_Energy2.jpg (Utah SMART Energy Lab logo), Power Grid / Transmission Tower, University of Utah, Utah Smart Energy Lab

### Community 160 - "Utah Smart Energy Lab (U-SMART)"
Cohesion: 0.67
Nodes (4): Utah Smart Energy Lab Logo, Power Grid / Transmission Infrastructure, University of Utah, Utah Smart Energy Lab (U-SMART)

### Community 162 - "Visual"
Cohesion: 0.09
Nodes (6): draw_vessel(), get_arc_points(), get_bearing(), rotate(), draw_glow(), Visual

### Community 167 - "RecordFilter"
Cohesion: 0.15
Nodes (3): decode(), header(), RecordFilter

### Community 175 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 177 - ".record"
Cohesion: 0.15
Nodes (4): action(), mark(), poll(), status()

### Community 182 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 186 - "ap_commands.py"
Cohesion: 0.13
Nodes (14): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+6 more)

### Community 189 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 191 - "record_schema.py"
Cohesion: 0.25
Nodes (4): link_of(), packet(), packet_from_meta(), raw_bytes()

### Community 195 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 197 - "tray_columns"
Cohesion: 0.20
Nodes (3): column_position(), tray_columns(), SavePacketColumnsAsDefault

### Community 200 - "ContextManager"
Cohesion: 0.13
Nodes (11): ContextManager, BaseForm, ModeForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm (+3 more)

### Community 201 - "core/transforms.py"
Cohesion: 0.28
Nodes (4): padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 202 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 203 - ".__init__"
Cohesion: 0.16
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), ring_spots()

### Community 207 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 208 - ".__init__"
Cohesion: 0.32
Nodes (4): encryption_enabled(), set_encryption(), start_encryption(), stop_encryption()

### Community 225 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 226 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 227 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **27 isolated node(s):** `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)`, `Top Toolbar (Quit, Back to Title, Refresh, Reset Page, Help, Toggle Theme, Select Theme, Favorite Page, Load Labels)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1922 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **142 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `ProcessManager`, `pyside6_qtcore`, `InputManager`, `style.py`, `PageManager`, `channels/__init__.py`, `_base_button.py`, `defender_hvac_chart.py`, `window_chrome.py`, `important_buttons/__init__.py`, `widgets/__init__.py`, `ShiftWheel`, `background.py`, `router.py`, `filter_overlay.py`, `Performance`, `.start_session`, `menu_bar.py`, `.save_current_page`, `LocalizationManager`, `Overlay`, `threading`, `Json`, `KeyBinds`, `.__init__`, `docking.py`, `Style`, `PrivilegedHelper`, `Preferences`, `host.py`, `AnimationManager`, `CheckboxOverlay`, `config_editor.py`, `Canvas`, `.apply_theme`?**
  _High betweenness centrality (0.245) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ModBus Man-in-the-Middle Attack Exercise`, `Three-column Minimizable Panel Layout`, `Status Log Panel` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MetaPacket` be split into smaller, more focused modules?**
  _Cohesion score 0.0792156862745098 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.__init__`, `.start_session`, `pyside6_qtcore`, `SettingsSection`, `ContextManager`, `style.py`, `._build_stylesheet`, `menu_bar.py`, `_base_button.py`, `.theme_family`, `_DressedWidgets`, `.brush`, `.discard_changes`, `Overlay`, `.apply_theme`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `open_in_browser` be split into smaller, more focused modules?**
  _Cohesion score 0.082010582010582 - nodes in this community are weakly interconnected._