# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~277,165 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4866 nodes · 10374 edges · 221 communities (78 shown, 143 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c61fda22`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- config_editor.py
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- pause_menu.py
- Style
- Wifi
- SummaryDrawer
- describe.py
- modal.py
- paint_mark
- VisualPalette
- Footer
- FilterModal
- draw_window_bar_line
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
- .__init__
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- .brush
- ._build_stylesheet
- Kernel
- .field_options
- ConfigEditor
- docking.py
- LocalizationManager
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
- KalmanToggleForm
- Router
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- Draw
- SlidersForm
- InputManager
- FlowLayout
- CycleBox
- themes.py
- Camera
- Panes
- Constellation
- App
- PageManager
- filter_overlay.py
- launch.py
- DragHandle
- _MapCanvas
- .fill_base
- PrivilegedHelper
- SettingsPage
- MapBuffer
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
- .record
- compile_filter
- Replay
- Canvas
- RecordFilter
- .collapsed
- drag_drop.py
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- _DrawerLayout
- ArpSpoofer
- ap_commands.py
- Process
- .connect_to_saved_wifi
- Prod/Host_API.py
- StripChartBase
- MaterialEditor
- QWidget
- GrowingButton
- PopupEntrance
- _Proxy
- QWidget
- record_schema.py
- .strip_chart_layout
- SmoothWheel
- align_decimals
- Scanlines
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
- Attack
- .__init__
- TextArea
- SquareButtons
- ShiftWheel
- .collect
- dumps
- RetentionPolicy
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- WorkspaceSelectPage
- Master
- Slave
- ChoiceList
- leaf_of
- MaterialEditorPopup
- DragPayload
- PopupWindow
- WindowEdges
- NativeFrame
- AppearEffect
- .arrow
- NoteBrowser
- NetFilterQueue
- _Chip
- LookOnly
- Loader
- CornerControls
- .save_current_page
- panel
- InterfaceManager
- SectionCard
- WindowControls
- DropZone
- frame_callback
- .authored_weights
- .page_panel_keys
- APPoller
- PooledCanvasMixin
- frame_callback
- .__init__
- paint_panel
- _DropPreview
- _OnHide
- ModalWindow
- StreamIncomingPacketsToMcap
- PreferencesData
- ContextManager
- Telemetry
- Cyber-ICS Training Module
- .make_built_in
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
9. `DockArea` - 53 edges
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

## Communities (221 total, 143 thin omitted)

### Community 0 - "config_editor.py"
Cohesion: 0.05
Nodes (20): random_spline_path(), BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+12 more)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (36): AbortAllNetworkActions, ImportantButton, open_in_browser(), ToggleButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole (+28 more)

### Community 3 - "MetaPacket"
Cohesion: 0.04
Nodes (10): HouseBuffer, Channel, ModbusBuffer, _is_global(), Transaction, TransactionManager, MetaPacket, _resolve_local_mac() (+2 more)

### Community 4 - "pause_menu.py"
Cohesion: 0.08
Nodes (7): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark, ShowHelpMessage

### Community 6 - "Wifi"
Cohesion: 0.13
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 7 - "SummaryDrawer"
Cohesion: 0.07
Nodes (4): fade_in(), SummaryDrawer, WorkspaceButton, update()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "modal.py"
Cohesion: 0.04
Nodes (16): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+8 more)

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 11 - "VisualPalette"
Cohesion: 0.11
Nodes (4): draw_vessel(), draw_glow(), Visual, VisualPalette

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.16
Nodes (5): column_position(), is_column_available(), shown_columns(), tray_columns(), ButtonModal

### Community 17 - "MenuBar"
Cohesion: 0.03
Nodes (12): bare_icon(), _FollowResize, global_buttons(), icon_button(), MenuBar, _RightZoneRoom, bar_button_height(), window_bar_button_height() (+4 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.06
Nodes (5): DefenderMapBuffer, APCommand, DefenderStatusBuffer, StatusBuffer, MetaStatus

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.12
Nodes (5): RowZone, ChooseShownPacketConsoleColumns, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.06
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), move_panel(), new_id() (+8 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 50 - "CombinedTable"
Cohesion: 0.08
Nodes (5): VariableModal, autosave(), reset_all(), CombinedTable, entry()

### Community 53 - "FilterError"
Cohesion: 0.25
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 54 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.10
Nodes (6): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine()

### Community 58 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 62 - "KalmanToggleForm"
Cohesion: 0.20
Nodes (6): hvac_kalman_enabled(), kalman_enabled(), submarine_kalman_enabled(), HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "FlowLayout"
Cohesion: 0.05
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 80 - "filter_overlay.py"
Cohesion: 0.18
Nodes (9): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_outside_quotes(), to_state() (+1 more)

### Community 81 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - ".fill_base"
Cohesion: 0.21
Nodes (5): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), value_noise()

### Community 86 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.04
Nodes (9): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SelectRegisterPreset, SettingsOverlayButton, Overlay (+1 more)

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 96 - "Camera"
Cohesion: 0.12
Nodes (5): Camera, padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - ".record"
Cohesion: 0.15
Nodes (4): action(), mark(), poll(), status()

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.12
Nodes (5): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 108 - "Json"
Cohesion: 0.07
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 116 - "ap_commands.py"
Cohesion: 0.15
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), _hvac_send(), push_hvac_settings(), read_hvac_state(), set_ap_tunnel() (+7 more)

### Community 117 - "Process"
Cohesion: 0.06
Nodes (7): flush(), flush_all(), run(), Buffer, ProcessManager, Process, FileStream

### Community 118 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 128 - "QWidget"
Cohesion: 0.11
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 129 - "record_schema.py"
Cohesion: 0.25
Nodes (4): link_of(), packet(), packet_from_meta(), raw_bytes()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 154 - "dumps"
Cohesion: 0.32
Nodes (3): decode(), dumps(), header()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 167 - "DragPayload"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), WorkspaceChip, DragPayload

### Community 175 - "NoteBrowser"
Cohesion: 0.15
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 201 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 205 - ".__init__"
Cohesion: 0.05
Nodes (3): OpenFavoritePage, ToggleDebugLabels, ToggleLightDarkMode

### Community 206 - "paint_panel"
Cohesion: 0.10
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 226 - "ContextManager"
Cohesion: 0.06
Nodes (25): ContextManager, apply_scale_about(), StripChart, form_order(), EditNetworkHosts, Scrollable, BaseForm, FlagsForm (+17 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "TitlePage"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

## Knowledge Gaps
- **143 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `config_editor.py`, `CheckboxOverlay`, `important_buttons/__init__.py`, `SmoothWheel`, `MetaPacket`, `Style`, `pause_menu.py`, `AnimationManager`, `modal.py`, `VisualPalette`, `ButtonModal`, `MenuBar`, `ShiftWheel`, `server.py`, `docking.py`, `LocalizationManager`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `filter_overlay.py`, `PrivilegedHelper`, `.apply_theme`, `Overlay`, `.reset_page`, `drag_drop.py`, `.start_session`, `Json`, `Process`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `config_editor.py` be split into smaller, more focused modules?**
  _Cohesion score 0.053313587560162905 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `.brush`, `important_buttons/__init__.py`, `.theme_family`, `.start_session`, `.texture_brush`, `MenuBar`, `_DressedWidgets`, `.apply_theme`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.0989247311827957 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `config_editor.py`, `QWidget`, `Rows`, `.leaf`, `WorkspaceSelectPage`, `.add_setting_row`, `ContextManager`, `.refresh_usage`, `important_buttons/__init__.py`, `modal.py`, `NoteBrowser`, `MenuBar`, `LayoutEditor`, `WorkspaceSorter`, `.collect`, `FindBar`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._