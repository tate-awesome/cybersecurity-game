# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~284,664 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5082 nodes · 10763 edges · 235 communities (84 shown, 151 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `218d7289`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- buffer_manager.py
- Wifi
- .fill_base
- describe.py
- WindowEdges
- DockArea
- .__init__
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- menu_bar.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- Toast
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- config_editor.py
- server.py
- .brush
- ._build_stylesheet
- WindowControls
- ConfigEditor
- docking.py
- LocalizationManager
- Style
- flusher.py
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- NetFilterQueue
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- packet_filter.py
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- Draw
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
- CycleBox
- themes.py
- Camera
- .__init__
- Constellation
- app.py
- PageManager
- FlowLayout
- MapBuffer
- host.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- .color
- HouseBuffer
- Report
- Draw
- _Grip
- PauseMenu
- .add_labeled_entry
- WaveGrid
- Toasts
- Camera
- NetworkGraph
- VectorField
- palette_generator.py
- ListZone
- compile_filter
- Replay
- .apply_theme
- .connect_to_saved_wifi
- blurred_shape
- DropZone
- .__init__
- Json
- ._draw_text
- ComboColumn
- _Dim
- KalmanToggleForm
- _PollUnpacker
- file_dialog
- ArpSpoofer
- .__init__
- threading
- TabStrip
- GrowingButton
- StripChartBase
- NoticeContent
- MaterialEditor
- QWidget
- .collect
- PopupEntrance
- _Proxy
- pyside6_qtcore
- affine
- .strip_chart_layout
- SmoothWheel
- kind_color
- Builder
- .refresh_usage
- Scrollable
- AnimationManager
- ModalWindow
- .new_tab
- Meter
- MitmTable
- Denier
- Scrim
- Proximity
- Table
- StatusBell
- APPoller
- modal.py
- widgets/__init__.py
- align_decimals
- ShiftWheel
- .add_setting_row
- MetaStatus
- _OnHide
- Builder
- toasts.py
- ._scan_for_networks
- MainWindow
- Overlay
- Master
- Slave
- ChoiceList
- VisualPalette
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- IP Forwarding
- Channel
- .arrow
- NoteBrowser
- Install NMap
- LookOnly
- NMap Scan Failed
- Wi-Fi Control Unavailable
- random
- .save_current_page
- .prepare_page_config
- _Indicator
- MenuBar
- Map
- frame_callback
- .authored_weights
- Can't Reach the Access Point
- .build_description_tab
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- is_column_available
- DoS Attack Didn't Start
- Panel
- NFQ Error
- paint_panel
- No Network Connection
- QRect
- SelectRegisterPreset
- Buffer
- No Wi-Fi Adapter
- Sniffer Didn't Start
- frame_callback
- EditBackgroundChoices
- Wi-Fi Connection Failed
- Attack
- Network Not Found
- No Saved Connection
- WorkspaceSelectPage
- ToggleButton
- Wi-Fi Is Off
- WinDivert Couldn't Open
- ProcessManager
- .key_column_width
- .make_built_in
- ContextManager
- Telemetry
- Cyber-ICS Training Module
- TitlePage

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 148 edges
2. `Style` - 123 edges
3. `ImportantButton` - 116 edges
4. `Overlay` - 88 edges
5. `MenuBar` - 67 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 61 edges
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

## Communities (235 total, 151 thin omitted)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.04
Nodes (9): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, EditNetworkHosts, OpenFavoritePage (+1 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (36): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ConfigureThisWorkspace (+28 more)

### Community 3 - "MetaPacket"
Cohesion: 0.09
Nodes (3): Transaction, TransactionManager, MetaPacket

### Community 4 - "buffer_manager.py"
Cohesion: 0.11
Nodes (3): DefenderMapBuffer, ModbusBuffer, _resolve_local_mac()

### Community 6 - "Wifi"
Cohesion: 0.12
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 7 - ".fill_base"
Cohesion: 0.12
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 9 - "WindowEdges"
Cohesion: 0.11
Nodes (3): SquareButtons, WindowDrag, WindowEdges

### Community 10 - "DockArea"
Cohesion: 0.07
Nodes (3): DockArea, visit(), drain_evenly()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 17 - "menu_bar.py"
Cohesion: 0.04
Nodes (16): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage (+8 more)

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.10
Nodes (6): BinZone, DragPayload, RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.06
Nodes (20): BoatMotion, delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace() (+12 more)

### Community 33 - "server.py"
Cohesion: 0.10
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.05
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "WindowControls"
Cohesion: 0.09
Nodes (6): CornerControls, draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room(), WindowControls

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 42 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

### Community 43 - "WifiForm"
Cohesion: 0.08
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.07
Nodes (6): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane, bare_icon()

### Community 53 - "packet_filter.py"
Cohesion: 0.11
Nodes (13): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+5 more)

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
Cohesion: 0.11
Nodes (6): _list_item(), Wifi, finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 62 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 77 - "app.py"
Cohesion: 0.12
Nodes (5): App, covered(), settle(), uncovered(), __getattr__()

### Community 81 - "host.py"
Cohesion: 0.06
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Report"
Cohesion: 0.11
Nodes (5): Report, NMapper, InterfaceManager, job(), _escape()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Replay"
Cohesion: 0.08
Nodes (3): dissect(), RecordFilter, Replay

### Community 104 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 112 - "KalmanToggleForm"
Cohesion: 0.23
Nodes (7): hvac_kalman_enabled(), kalman_enabled(), set_hvac_kalman(), set_kalman(), set_submarine_kalman(), submarine_kalman_enabled(), KalmanToggleForm

### Community 116 - ".__init__"
Cohesion: 0.11
Nodes (10): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), _hvac_send(), push_hvac_settings(), set_ap_tunnel(), set_encryption(), submarine_mode() (+2 more)

### Community 117 - "threading"
Cohesion: 0.06
Nodes (3): NetFilterQueueBaseClass, Process, FileStream

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 128 - "pyside6_qtcore"
Cohesion: 0.07
Nodes (8): CallbackRegistry, ClickManager, PreferencesData, apply_scale_about(), scale(), translate(), _is_global(), background_choices()

### Community 129 - "affine"
Cohesion: 0.14
Nodes (7): canvas_fit(), padded_fit(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 133 - "kind_color"
Cohesion: 0.24
Nodes (4): status(), kind_color(), clicked(), sheet()

### Community 136 - "Scrollable"
Cohesion: 0.05
Nodes (6): _Gaps, Scrollable, Builder, Builder, Builder, Builder

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 149 - "modal.py"
Cohesion: 0.04
Nodes (14): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+6 more)

### Community 150 - "widgets/__init__.py"
Cohesion: 0.07
Nodes (7): StripChart, ToggleStripChartAutoFit, TextArea, panel(), Builder, Builder, Builder

### Community 151 - "align_decimals"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 161 - "Overlay"
Cohesion: 0.11
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 165 - "VisualPalette"
Cohesion: 0.08
Nodes (7): draw_vessel(), get_arc_points(), get_bearing(), rotate(), Visual, VisualPalette, Kalman

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 202 - "is_column_available"
Cohesion: 0.28
Nodes (4): column_position(), is_column_available(), shown_columns(), tray_columns()

### Community 204 - "Panel"
Cohesion: 0.09
Nodes (4): NetworkDiagramCanvas, Builder, _DrawerLayout, Panel

### Community 206 - "paint_panel"
Cohesion: 0.09
Nodes (5): bar_inset(), minimized_thickness(), paint_mark(), _Peek, paint_panel()

### Community 208 - "QRect"
Cohesion: 0.08
Nodes (3): _Chip, _DropPreview, DropTarget

### Community 210 - "Buffer"
Cohesion: 0.08
Nodes (4): Buffer, Notice, _BufferShim, read()

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 219 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView

### Community 226 - "ContextManager"
Cohesion: 0.06
Nodes (23): ContextManager, DefenderWorldMap, House, WorldMap, form_order(), BaseForm, FlagsForm, HVACFlagsForm (+15 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "TitlePage"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

## Knowledge Gaps
- **151 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `pyside6_qtcore`, `CheckboxOverlay`, `important_buttons/__init__.py`, `SmoothWheel`, `buffer_manager.py`, `.start_session`, `AnimationManager`, `menu_bar.py`, `modal.py`, `widgets/__init__.py`, `ShiftWheel`, `toasts.py`, `config_editor.py`, `VisualPalette`, `docking.py`, `LocalizationManager`, `Style`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `host.py`, `PrivilegedHelper`, `Toasts`, `ProcessManager`, `.apply_theme`, `Json`, `threading`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.04117063492063492 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `pyside6_qtcore`, `CheckboxOverlay`, `ContextManager`, `._build_stylesheet`, `.brush`, `.start_session`, `.lift_button`, `.apply_theme`, `important_buttons/__init__.py`, `Overlay`, `.theme_family`, `menu_bar.py`, `_DressedWidgets`, `SettingsSection`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.027622865109794354 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `config_editor.py`, `pyside6_qtcore`, `Overlay`, `ContextManager`, `WindowControls`, `WindowEdges`, `.__init__`, `Panel`, `QWidget`, `menu_bar.py`, `StatusBell`, `widgets/__init__.py`, `WorkspaceSorter`, `PauseMenu`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._