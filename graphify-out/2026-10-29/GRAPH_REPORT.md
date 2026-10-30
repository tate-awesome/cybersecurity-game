# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~278,233 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4891 nodes · 10431 edges · 234 communities (81 shown, 153 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 479 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `328717c9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- widgets/__init__.py
- CheckboxOverlay
- ImportantButton
- MetaPacket
- threading
- Style
- Wifi
- SummaryDrawer
- describe.py
- important_buttons/__init__.py
- pyside6_qtcore
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- SettingsOverlayButton
- message
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- WrapLayout
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- ._build_stylesheet
- Kernel
- ConfigEditor
- docking.py
- LocalizationManager
- _base_button.py
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- FilterError
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- Draw
- Modify
- KeyBinds
- SettingsPage
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- SlidersForm
- InputManager
- FlowLayout
- CycleBox
- themes.py
- Camera
- .__init__
- Constellation
- App
- PageManager
- KalmanToggleForm
- sys
- DragHandle
- Map
- ButtonModal
- PrivilegedHelper
- ModbusBuffer
- .apply_theme
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- RecordFilter
- Camera
- VectorField
- palette_generator.py
- ToggleBookmark
- compile_filter
- Replay
- Canvas
- .field_options
- .collapsed
- DropZone
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- packet_filter.py
- paths.py
- ArpSpoofer
- ap_commands.py
- Process
- .record
- Prod/Host_API.py
- StripChartBase
- MaterialEditor
- QWidget
- record_schema.py
- PopupEntrance
- host.py
- core/transforms.py
- .integer
- .strip_chart_layout
- SmoothWheel
- DragPayload
- WorkspaceSaveResetButton
- Builder
- .refresh_usage
- Scrollable
- AnimationManager
- ModalWindow
- Meter
- MitmTable
- Denier
- Scrim
- Paths
- Table
- APPoller
- version.py
- Panel
- config_editor.py
- ShiftWheel
- QWidget
- paint_mark
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- Master
- Slave
- ChoiceList
- Visual
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- transformations.py
- align_decimals
- HideEffect
- NoteBrowser
- WorkspaceButton
- _Chip
- LookOnly
- _DropPreview
- .save_current_page
- ListZone
- MenuBar
- StreamIncomingPacketsToMcap
- Router
- frame_callback
- .authored_weights
- .page_panel_keys
- .build_description_tab
- ConfigureThisWorkspace
- PooledCanvasMixin
- frame_callback
- fade_in
- LinkToPage
- _DrawerLayout
- .setText
- paint_panel
- dumps
- DockArea
- SelectRegisterPreset
- edit_network_hosts.py
- Visualizer.py
- SettingsSection
- conjugate
- arpy2a.py
- _Drawer
- WorkspaceSelectPage
- ToggleButton
- PreferencesData
- ContextManager
- DenseMesh
- Telemetry
- Cyber-ICS Training Module
- confirm_dialog
- TitlePage

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 147 edges
2. `Style` - 123 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 60 edges
9. `DockArea` - 54 edges
10. `VisualPalette` - 53 edges

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
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/network_activity/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/network_hosts/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
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

## Communities (234 total, 153 thin omitted)

### Community 0 - "widgets/__init__.py"
Cohesion: 0.08
Nodes (9): BoatMotion, Sprites, Triangle, Visuals, WorkspacePage, NotFound, Page, TriangleCanvas (+1 more)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 2 - "ImportantButton"
Cohesion: 0.04
Nodes (15): ImportantButton, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, LoadLocalizationLabelsFile, LoadMcapIntoPacketBuffer, LoadPcapIntoPacketBuffer, LoadSettingsPresetFile (+7 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "important_buttons/__init__.py"
Cohesion: 0.06
Nodes (12): AbortAllNetworkActions, ClearAllCapturedBufferData, ClearStatusConsole, EditModbusRegisterDisplay, FilterPacketConsole, OpenMaterialEditor, OpenPauseMenu, OpenThemeEditor (+4 more)

### Community 11 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (3): gradient_points(), random_spline_path(), background_choices()

### Community 12 - "Footer"
Cohesion: 0.05
Nodes (8): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip(), Scanlines

### Community 14 - "Panes"
Cohesion: 0.11
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "SettingsOverlayButton"
Cohesion: 0.14
Nodes (4): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton

### Community 17 - "message"
Cohesion: 0.13
Nodes (5): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (7): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.09
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.12
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 42 - "_base_button.py"
Cohesion: 0.15
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (5): _LentPlaceholder, _SideStrip, _SideTitle, TabbedPane, TabStrip

### Community 48 - "NMapper"
Cohesion: 0.06
Nodes (6): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 53 - "FilterError"
Cohesion: 0.26
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 54 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 58 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.13
Nodes (4): submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 80 - "KalmanToggleForm"
Cohesion: 0.20
Nodes (6): hvac_kalman_enabled(), kalman_enabled(), submarine_kalman_enabled(), HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 81 - "sys"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 84 - "ButtonModal"
Cohesion: 0.15
Nodes (4): VariableModal, autosave(), reset_all(), ButtonModal

### Community 87 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.08
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 95 - "RecordFilter"
Cohesion: 0.15
Nodes (3): decode(), header(), RecordFilter

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "ToggleBookmark"
Cohesion: 0.09
Nodes (4): GoBackToPreviousPage, GoForwardToNextPage, SetCurrentPageAsFavorite, ToggleBookmark

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 112 - "packet_filter.py"
Cohesion: 0.21
Nodes (7): empty_state(), Field, join_pair(), normal_value(), split_outside_quotes(), to_state(), unquote()

### Community 116 - "ap_commands.py"
Cohesion: 0.12
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), _hvac_send(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+9 more)

### Community 117 - "Process"
Cohesion: 0.06
Nodes (8): flush(), flush_all(), run(), Buffer, ProcessManager, Process, FileStream, RetentionPolicy

### Community 118 - ".record"
Cohesion: 0.15
Nodes (4): action(), mark(), poll(), status()

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 125 - "record_schema.py"
Cohesion: 0.25
Nodes (4): link_of(), packet(), packet_from_meta(), raw_bytes()

### Community 128 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 136 - "Scrollable"
Cohesion: 0.06
Nodes (6): _Gaps, Scrollable, Builder, Builder, Builder, Builder

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 150 - "Panel"
Cohesion: 0.04
Nodes (9): NetworkDiagramCanvas, StripChart, TextArea, Builder, Builder, Builder, Panel, Builder (+1 more)

### Community 151 - "config_editor.py"
Cohesion: 0.08
Nodes (15): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), remove_nested(), rename_workspace() (+7 more)

### Community 154 - "QWidget"
Cohesion: 0.12
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 160 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 170 - "transformations.py"
Cohesion: 0.32
Nodes (3): canvas_fit(), padded_fit(), affine()

### Community 172 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 189 - "MenuBar"
Cohesion: 0.02
Nodes (22): minimized_thickness(), PeekArrow, ButtonGroup, offered_sections(), bare_icon(), _FollowResize, global_buttons(), icon_button() (+14 more)

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 201 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 206 - "paint_panel"
Cohesion: 0.11
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 216 - "arpy2a.py"
Cohesion: 0.08
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 226 - "ContextManager"
Cohesion: 0.08
Nodes (20): ContextManager, DefenderWorldMap, House, WorldMap, form_order(), BaseForm, FlagsForm, HVACFlagsForm (+12 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "confirm_dialog"
Cohesion: 0.06
Nodes (8): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog()

### Community 261 - "TitlePage"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **153 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `widgets/__init__.py`, `CheckboxOverlay`, `SmoothWheel`, `threading`, `Style`, `WorkspaceSaveResetButton`, `AnimationManager`, `pyside6_qtcore`, `Paths`, `message`, `Panel`, `config_editor.py`, `ShiftWheel`, `docking.py`, `LocalizationManager`, `_base_button.py`, `Preferences`, `Performance`, `KeyBinds`, `MenuBar`, `Router`, `InputManager`, `ConfigureThisWorkspace`, `LinkToPage`, `.setText`, `PageManager`, `edit_network_hosts.py`, `PrivilegedHelper`, `.__init__`, `.reset_page`, `ToggleBookmark`, `Json`, `confirm_dialog`, `Process`, `host.py`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `widgets/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07673469387755102 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `.brush`, `.lift_button`, `.discard_changes`, `.theme_family`, `pyside6_qtcore`, `_base_button.py`, `.setText`, `_DressedWidgets`, `.__init__`, `.apply_theme`, `SettingsSection`, `Overlay`, `MenuBar`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.08888888888888889 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `widgets/__init__.py`, `Rows`, `.leaf`, `.build_description_tab`, `.add_setting_row`, `ConfigureThisWorkspace`, `.refresh_usage`, `pyside6_qtcore`, `NoteBrowser`, `LayoutEditor`, `config_editor.py`, `WorkspaceSorter`, `QWidget`, `WorkspaceSelectPage`, `FindBar`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._