# Graph Report - cybersecurity-game  (2026-11-10)

## Corpus Check
- 342 files · ~287,310 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5131 nodes · 10536 edges · 263 communities (90 shown, 173 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 522 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d1ffc183`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TriangleCanvas
- Canvas
- important_buttons/__init__.py
- MetaPacket
- context_manager.py
- Process
- Wifi
- buffer_manager.py
- describe.py
- geometry.py
- .collapsed
- Replay
- Footer
- FilterModal
- Panes
- ap_commands.py
- ToastCard
- packet_filter.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- WorkspaceSelectPage
- SessionRecorder
- WorkspaceSorter
- Toast
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- Kernel
- time
- ._build_stylesheet
- Style
- ConfigEditor
- docking.py
- LocalizationManager
- .setting
- WifiForm
- WifiBaseClass
- HVACChart
- QWidget
- SettingsPage
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- FilterError
- frame_callback
- HostModal
- Performance
- ViewPort
- wifi_windows.py
- TabStrip
- Modify
- KeyBinds
- ModbusBuffer
- FadeIn
- .collect
- Rows
- .leaf
- Meter
- SlidersForm
- InputManager
- Attack
- CycleBox
- themes.py
- Camera
- DefenderStatusBuffer
- Constellation
- app.py
- PageManager
- FlowLayout
- ElidingLabel
- launch.py
- DragHandle
- ButtonModal
- VariableModal
- PrivilegedHelper
- VisualPalette
- Scanlines
- Notice
- Draw
- transformations.py
- .restyle
- PauseMenu
- WaveGrid
- Toasts
- Camera
- confirm_dialog
- VectorField
- palette_generator.py
- WorkspaceChip
- compile_filter
- _Peek
- Overlay
- DefenderModbusBuffer
- _FollowResize
- Json
- ._draw_text
- ComboColumn
- Router
- _Grip
- WrapLayout
- ListZone
- ArpSpoofer
- FlagsForm
- SmoothWheel
- StripChartBase
- APPoller
- .fill
- QWidget
- _Dim
- .columnconfigure
- PopupEntrance
- _Proxy
- MetaStatus
- WindowEdges
- time_core/transforms.py
- .connect_to_saved_wifi
- QWidget
- Report
- Builder
- SettingsSection
- _Gaps
- CallbackRegistry
- GrowingButton
- paint_mark
- ToggleLightDarkMode
- MitmTable
- NetFilterQueue
- PopupWindow
- _Indicator
- Builder
- .integer
- KalmanToggleForm
- Denier
- _DrawerLayout
- kind_color
- ShiftWheel
- Draw
- StripChartLayout
- MenuBar
- paint_panel
- MainWindow
- TextArea
- Master
- Slave
- Map
- pyside6_qtcore
- AnimationManager
- Kalman
- IP Forwarding
- WindowBarButton
- _MapCanvas
- is_column_available
- Builder
- NewWorkspaceDialog
- Install NMap
- Loader
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .save_current_page
- .prepare_page_config
- BuildInfo
- _Chip
- DropZone
- config_editor.py
- ToggleButton
- ModeForm
- .__init__
- .authored_weights
- DragPayload
- Can't Reach the Access Point
- StatusBell
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- DoS Attack Didn't Start
- ._scan_for_networks
- NFQ Error
- .add_deadspace
- No Network Connection
- DockArea
- _DropPreview
- No Wi-Fi Adapter
- Sniffer Didn't Start
- .__init__
- threading
- Wi-Fi Connection Failed
- Network Not Found
- No Saved Connection
- NoteBrowser
- Wi-Fi Is Off
- WinDivert Couldn't Open
- Buffer
- _RightZoneRoom
- NetFilterQueue
- ContextManager
- Telemetry
- NMapper
- .play
- Cyber-ICS Training Module
- HideEffect
- Proximity
- .global_rows
- .build_description_tab
- panel
- LinkToPage
- OpenFavoritePage
- align_decimals
- PreferencesData
- .__init__
- DenseMesh

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 147 edges
2. `Style` - 123 edges
3. `ImportantButton` - 116 edges
4. `Overlay` - 85 edges
5. `MenuBar` - 67 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 62 edges
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
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/widgets/__init__.py -> game/src/widgets/frame_widgets/menu_bar.py -> game/src/widgets/frame_widgets/toasts.py -> game/src/__init__.py`
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/hvac_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/modbus.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/network_graph.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/packet.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/submarine_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/saved/__init__.py -> game/src/network/saved/file_stream.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`

## Communities (263 total, 173 thin omitted)

### Community 1 - "Canvas"
Cohesion: 0.08
Nodes (6): Canvas, DefenderWorldMap, NetworkDiagramCanvas, WorldMap, ToggleNetworkGraphRingView, Builder

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (39): AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms (+31 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "context_manager.py"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 7 - "buffer_manager.py"
Cohesion: 0.12
Nodes (3): DefenderMapBuffer, _is_global(), _resolve_local_mac()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "geometry.py"
Cohesion: 0.10
Nodes (8): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate(), shorten_line(), zoom_and_pan()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.09
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.08
Nodes (4): _SashCorners, _SashLight, _PaneContainer, Panes

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "ToastCard"
Cohesion: 0.14
Nodes (3): NoticeContent, _Swallowed, ToastCard

### Community 17 - "packet_filter.py"
Cohesion: 0.21
Nodes (7): empty_state(), Field, join_pair(), normal_value(), split_outside_quotes(), to_state(), unquote()

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (7): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise(), VisualBackground

### Community 22 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): LookOnly, MaterialEditor, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "time"
Cohesion: 0.13
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 38 - "ConfigEditor"
Cohesion: 0.09
Nodes (3): ConfigEditor, walk(), in_layout()

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 50 - "CombinedTable"
Cohesion: 0.11
Nodes (3): key(), CombinedTable, entry()

### Community 53 - "FilterError"
Cohesion: 0.26
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 54 - "frame_callback"
Cohesion: 0.10
Nodes (12): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+4 more)

### Community 55 - "HostModal"
Cohesion: 0.16
Nodes (5): HostModal, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 63 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 65 - ".collect"
Cohesion: 0.18
Nodes (3): read(), remove_nested(), set_nested()

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 75 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 81 - "launch.py"
Cohesion: 0.12
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 83 - "ButtonModal"
Cohesion: 0.16
Nodes (3): EditModelStyle, EditStripChartStyle, ButtonModal

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Notice"
Cohesion: 0.05
Nodes (12): Notice, Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run() (+4 more)

### Community 90 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 91 - ".restyle"
Cohesion: 0.10
Nodes (4): _ComboLists, _StyledComboItems, StyleSignals, ChoiceList

### Community 97 - "confirm_dialog"
Cohesion: 0.05
Nodes (12): ClearSavedWorkspaceInputs, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetSavedWorkspaceLayout, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault (+4 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 105 - "Overlay"
Cohesion: 0.03
Nodes (20): developer_text(), ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, RefreshCurrentPage, SelectBackground (+12 more)

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 116 - "FlagsForm"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 122 - ".fill"
Cohesion: 0.23
Nodes (9): page_tokens(), build_nav(), go(), on_filter(), refresh(), render(), shown(), start() (+1 more)

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 124 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 132 - "QWidget"
Cohesion: 0.12
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 133 - "Report"
Cohesion: 0.15
Nodes (3): Report, _escape(), open_notice()

### Community 137 - "CallbackRegistry"
Cohesion: 0.10
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 139 - "paint_mark"
Cohesion: 0.15
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), bar_button_height()

### Community 143 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 147 - "KalmanToggleForm"
Cohesion: 0.23
Nodes (3): HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 151 - "kind_color"
Cohesion: 0.22
Nodes (3): kind_color(), sheet(), session_stamp()

### Community 157 - "MenuBar"
Cohesion: 0.05
Nodes (4): bare_icon(), global_buttons(), icon_button(), MenuBar

### Community 159 - "paint_panel"
Cohesion: 0.16
Nodes (3): blurred_shape(), paint_panel(), surface_shadow()

### Community 165 - "pyside6_qtcore"
Cohesion: 0.06
Nodes (5): draw_vessel(), gradient_points(), conjugate(), quote(), Visual

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "WindowBarButton"
Cohesion: 0.06
Nodes (10): CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_height(), window_bar_room(), WindowBarButton (+2 more)

### Community 172 - "is_column_available"
Cohesion: 0.28
Nodes (4): column_position(), is_column_available(), shown_columns(), tray_columns()

### Community 174 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 189 - "config_editor.py"
Cohesion: 0.06
Nodes (17): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+9 more)

### Community 190 - "ToggleButton"
Cohesion: 0.06
Nodes (6): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleStripChartAutoFit

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 204 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 213 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 223 - "Buffer"
Cohesion: 0.07
Nodes (7): flush(), flush_all(), run(), Buffer, StatusBuffer, FileStream, RetentionPolicy

### Community 226 - "ContextManager"
Cohesion: 0.07
Nodes (20): ContextManager, House, StripChart, form_order(), Scrollable, BaseForm, HVACSlidersForm, SubmarineSlidersForm (+12 more)

### Community 235 - "NMapper"
Cohesion: 0.13
Nodes (3): InterfaceManager, NMapper, job()

### Community 237 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 248 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

## Knowledge Gaps
- **41 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2117 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **173 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `important_buttons/__init__.py`, `context_manager.py`, `Process`, `buffer_manager.py`, `CallbackRegistry`, `ShiftWheel`, `Style`, `AnimationManager`, `pyside6_qtcore`, `LocalizationManager`, `docking.py`, `Preferences`, `.reset_page`, `Performance`, `KeyBinds`, `config_editor.py`, `InputManager`, `PageManager`, `Notice`, `Toasts`, `Buffer`, `confirm_dialog`, `.start_session`, `Overlay`, `Json`, `Router`, `SmoothWheel`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.07816091954022988 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `context_manager.py`, `pyside6_qtcore`, `.brush`, `.start_session`, `.preset_name`, `.theme_family`, `.setting`, `important_buttons/__init__.py`, `.lift_button`, `Overlay`, `_DressedWidgets`, `SettingsSection`, `.restyle`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.02399516063987095 - nodes in this community are weakly interconnected._