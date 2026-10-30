# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~277,803 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4881 nodes · 10403 edges · 238 communities (79 shown, 159 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 478 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d8149126`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- config_editor.py
- _base_button.py
- important_buttons/__init__.py
- MetaPacket
- menu_bar.py
- Style
- Wifi
- SummaryDrawer
- describe.py
- confirm_dialog
- paint_mark
- pyside6_qtcore
- Footer
- FilterModal
- _SashCorners
- Dev/Host_API.py
- ButtonModal
- MenuBar
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- DockArea
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
- blurred_shape
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- TabStrip
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
- QWidget
- Modify
- KeyBinds
- SettingsPage
- Router
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
- WrapLayout
- packet_filter.py
- launch.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- ModbusBuffer
- .apply_theme
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- NewWorkspaceDialog
- Camera
- VectorField
- palette_generator.py
- .__init__
- compile_filter
- Replay
- pyside6_qtwidgets
- open_in_browser
- walk
- ListZone
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- .__init__
- ArpSpoofer
- ap_commands.py
- Process
- Prod/Host_API.py
- StripChartBase
- FlagsForm
- MaterialEditor
- QWidget
- Draw
- PopupEntrance
- host.py
- .add_setting_row
- .integer
- .strip_chart_layout
- ContextManager
- .build_advanced_tab
- core/transforms.py
- Builder
- .refresh_usage
- .add_deadspace
- AnimationManager
- .columnconfigure
- Meter
- MitmTable
- Denier
- _PollUnpacker
- .__init__
- Table
- APPoller
- Attack
- app_core/__init__.py
- filter_overlay.py
- ShiftWheel
- .collect
- .new_tab
- WindowBarButton
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- Master
- Slave
- ChoiceList
- Proximity
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- WindowEdges
- version.py
- AppearEffect
- NoteBrowser
- .workspace_button
- QPoint
- LookOnly
- CornerControls
- .save_current_page
- .build_menu_bar_section
- SectionCard
- WindowControls
- _Gaps
- DragPayload
- frame_callback
- .authored_weights
- .page_panel_keys
- .__init__
- PooledCanvasMixin
- frame_callback
- fade_in
- ToggleBookmark
- .setText
- paint_panel
- QRect
- SelectRegisterPreset
- window_chrome.py
- .theme_info
- SettingsSection
- ConfigureThisWorkspace
- time
- LinkToPage
- ModeForm
- ToggleButton
- ProcessManager
- BaseForm
- _Drawer
- DenseMesh
- Telemetry
- random
- Cyber-ICS Training Module
- message
- GrowingButton

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

## Communities (238 total, 159 thin omitted)

### Community 0 - "config_editor.py"
Cohesion: 0.07
Nodes (19): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+11 more)

### Community 1 - "_base_button.py"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, EditNetworkHosts

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (21): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay (+13 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "menu_bar.py"
Cohesion: 0.08
Nodes (8): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, bare_icon(), global_buttons(), icon_button()

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "confirm_dialog"
Cohesion: 0.06
Nodes (11): ClearSavedWorkspaceInputs, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, EditWorkspaceAvailability (+3 more)

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.10
Nodes (3): FilterModal, label_key(), value_key()

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.16
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 20 - "PacketBuffer"
Cohesion: 0.08
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (8): Visuals, paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise(), VisualBackground

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+5 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.12
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.09
Nodes (8): BinZone, RowZone, ChooseShownPacketConsoleColumns, column_category(), is_column_available(), PacketColumnsModal, autosave(), shown_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (13): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+5 more)

### Community 43 - "WifiForm"
Cohesion: 0.08
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.13
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

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

### Community 59 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.21
Nodes (7): empty_state(), Field, join_pair(), normal_value(), split_outside_quotes(), to_state(), unquote()

### Community 81 - "launch.py"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 87 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.05
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Replay"
Cohesion: 0.08
Nodes (3): _dialog_parent(), file_dialog(), Replay

### Community 103 - "pyside6_qtwidgets"
Cohesion: 0.08
Nodes (7): apply_scale_about(), Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, TriangleCanvas, WorldMap

### Community 104 - "open_in_browser"
Cohesion: 0.14
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 105 - "walk"
Cohesion: 0.10
Nodes (6): visit(), DropTarget, is_split(), tidy(), panel_ids(), walk()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 117 - "Process"
Cohesion: 0.07
Nodes (6): Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "ContextManager"
Cohesion: 0.12
Nodes (4): ContextManager, PreferencesData, SmoothWheel, gradient_points()

### Community 133 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 150 - "app_core/__init__.py"
Cohesion: 0.07
Nodes (12): StripChart, form_order(), Scrollable, TextArea, panel(), Builder, EncryptionForm, Builder (+4 more)

### Community 151 - "filter_overlay.py"
Cohesion: 0.24
Nodes (3): draw_vessel(), conjugate(), quote()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 168 - "PopupWindow"
Cohesion: 0.08
Nodes (3): ModalWindow, PopupWindow, Scrim

### Community 180 - "CornerControls"
Cohesion: 0.16
Nodes (3): CornerControls, draw_window_bar_line(), _Strip

### Community 189 - "WindowControls"
Cohesion: 0.11
Nodes (4): SquareButtons, toggle_maximized(), WindowControls, WindowDrag

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
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 211 - "window_chrome.py"
Cohesion: 0.33
Nodes (3): window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 216 - "time"
Cohesion: 0.06
Nodes (3): flush(), flush_all(), run()

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 226 - "BaseForm"
Cohesion: 0.07
Nodes (19): BaseForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm, HVACSlidersForm, SubmarineSlidersForm (+11 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "message"
Cohesion: 0.07
Nodes (9): make(), column_position(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage (+1 more)

### Community 261 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **159 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `config_editor.py`, `_base_button.py`, `menu_bar.py`, `Style`, `AnimationManager`, `confirm_dialog`, `pyside6_qtcore`, `PacketBuffer`, `app_core/__init__.py`, `filter_overlay.py`, `ShiftWheel`, `docking.py`, `LocalizationManager`, `Preferences`, `.save_current_page`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `.setText`, `PageManager`, `window_chrome.py`, `PrivilegedHelper`, `ConfigureThisWorkspace`, `.apply_theme`, `time`, `LinkToPage`, `ProcessManager`, `BaseForm`, `pyside6_qtwidgets`, `Json`, `message`, `Process`, `host.py`?**
  _High betweenness centrality (0.253) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `config_editor.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06512890094979647 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `_base_button.py`, `.brush`, `._build_stylesheet`, `ContextManager`, `.lift_button`, `menu_bar.py`, `.theme_family`, `pyside6_qtcore`, `.setText`, `_DressedWidgets`, `.theme_info`, `.apply_theme`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `_base_button.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08636977058029689 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `config_editor.py`, `.add_setting_row`, `Rows`, `.leaf`, `.section`, `.refresh_usage`, `.new_tab`, `NoteBrowser`, `LayoutEditor`, `app_core/__init__.py`, `ConfigureThisWorkspace`, `WorkspaceSorter`, `.collect`, `.build_menu_bar_section`, `FindBar`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._