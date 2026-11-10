# Graph Report - cybersecurity-game  (2026-11-10)

## Corpus Check
- 342 files · ~286,283 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5102 nodes · 10477 edges · 275 communities (79 shown, 196 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 518 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `48923066`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- important_buttons/__init__.py
- MetaPacket
- ContextManager
- WindowBarButton
- Wifi
- threading
- describe.py
- WindowEdges
- DockArea
- MapBuffer
- Footer
- FilterModal
- Panes
- ap_commands.py
- toasts.py
- filter_overlay.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- SummaryDrawer
- SessionRecorder
- WorkspaceSorter
- Toast
- SettingsSection
- APConnectForm
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- config_editor.py
- server.py
- .brush
- ._build_stylesheet
- ConfigEditor
- docking.py
- LocalizationManager
- SettingsSection
- WifiForm
- WifiBaseClass
- HVACChart
- QWidget
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
- .build_appearance_tab
- .fill_base
- FadeOut
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
- Router
- PageManager
- FlowLayout
- HouseBuffer
- launch.py
- DragHandle
- Map
- VariableModal
- PrivilegedHelper
- VisualPalette
- Scanlines
- Notice
- Draw
- NMapper
- ChoiceList
- PauseMenu
- ElidingLabel
- WaveGrid
- Toasts
- Camera
- save_layout_as_default.py
- VectorField
- palette_generator.py
- WorkspaceChip
- compile_filter
- Replay
- Style
- ButtonModal
- DefenderModbusBuffer
- SectionCard
- Json
- ._draw_text
- ComboColumn
- _Dim
- _Grip
- _RightZoneRoom
- Loader
- ArpSpoofer
- FlagsForm
- time
- .global_rows
- StripChartBase
- APPoller
- StatusBell
- transitions.py
- CornerControls
- .build_menu_bar_section
- PopupEntrance
- host.py
- geometry.py
- time_core/transforms.py
- SmoothWheel
- .add_setting_row
- Report
- Builder
- .build_tabs
- _Gaps
- ClickManager
- TitlePage
- .new_tab
- align_decimals
- MitmTable
- NetFilterQueue
- PopupWindow
- ListZone
- Table
- sys
- Denier
- MaterialEditor
- widgets/__init__.py
- ShiftWheel
- Draw
- FileStream
- fade_in
- StripChartLayout
- blurred_shape
- MainWindow
- WorkspaceButton
- Master
- Slave
- SettingsPage
- Visual
- AnimationManager
- Kalman
- IP Forwarding
- WindowControls
- Telemetry
- Builder
- RenameWorkspaceDialog
- Install NMap
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .save_current_page
- .prepare_page_config
- GrowingButton
- DropZone
- MenuBar
- ToggleButton
- ModeForm
- .__init__
- .authored_weights
- .add_deadspace
- Can't Reach the Access Point
- CallbackRegistry
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- WorkspaceSelectPage
- DoS Attack Didn't Start
- NFQ Error
- .columnconfigure
- No Network Connection
- QRect
- version.py
- No Wi-Fi Adapter
- Sniffer Didn't Start
- .__init__
- is_column_available
- Wi-Fi Connection Failed
- Overlay
- Network Not Found
- No Saved Connection
- NoteBrowser
- ToggleLightDarkMode
- Wi-Fi Is Off
- WinDivert Couldn't Open
- Process
- Builder
- NetFilterQueue
- BaseForm
- CheckboxOverlay
- .integer
- paint_panel
- quit_application.py
- Builder
- Cyber-ICS Training Module
- _Swallowed
- Proximity
- DragPayload
- .build_description_tab
- LookOnly
- OpenFavoritePage
- _DrawerLayout
- PreferencesData
- .__init__
- EditBackgroundChoices
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

## Communities (275 total, 196 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.08
Nodes (5): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (45): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs (+37 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "ContextManager"
Cohesion: 0.07
Nodes (12): ContextManager, apply_scale_about(), BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page (+4 more)

### Community 5 - "WindowBarButton"
Cohesion: 0.09
Nodes (6): bar_inset(), minimized_thickness(), bare_icon(), icon_button(), bar_button_height(), WindowBarButton

### Community 6 - "Wifi"
Cohesion: 0.06
Nodes (11): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish() (+3 more)

### Community 7 - "threading"
Cohesion: 0.06
Nodes (4): ModbusBuffer, _is_global(), _resolve_local_mac(), NetFilterQueueBaseClass

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.07
Nodes (4): _SashCorners, _SashLight, _PaneContainer, Panes

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "toasts.py"
Cohesion: 0.09
Nodes (9): MetaStatus, _escape(), kind_color(), NoticeContent, sheet(), open_notice(), session_stamp(), ToastCard (+1 more)

### Community 17 - "filter_overlay.py"
Cohesion: 0.13
Nodes (12): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_outside_quotes(), split_pair() (+4 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.19
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 33 - "server.py"
Cohesion: 0.10
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.05
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.12
Nodes (18): add_tab(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf(), leaf_of() (+10 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.07
Nodes (6): _LentPlaceholder, paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 51 - "_DressedWidgets"
Cohesion: 0.11
Nodes (3): _DressedWidgets, _StyledComboItems, StyleSignals

### Community 53 - "FilterError"
Cohesion: 0.25
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 54 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostModal"
Cohesion: 0.16
Nodes (5): HostModal, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 63 - ".fill_base"
Cohesion: 0.12
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 75 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 77 - "Router"
Cohesion: 0.07
Nodes (4): App, Router, FadeIn, __getattr__()

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Notice"
Cohesion: 0.09
Nodes (4): StatusBuffer, Notice, _BufferShim, read()

### Community 90 - "NMapper"
Cohesion: 0.16
Nodes (3): InterfaceManager, NMapper, job()

### Community 97 - "save_layout_as_default.py"
Cohesion: 0.10
Nodes (6): SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 105 - "ButtonModal"
Cohesion: 0.15
Nodes (4): EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 108 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 116 - "FlagsForm"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 117 - "time"
Cohesion: 0.08
Nodes (12): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 122 - "StatusBell"
Cohesion: 0.14
Nodes (7): page_tokens(), StatusBell, build_nav(), go(), on_filter(), render(), shown()

### Community 123 - "transitions.py"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 126 - "PopupEntrance"
Cohesion: 0.16
Nodes (5): covered(), settle(), uncovered(), PopupEntrance, WindowReveal

### Community 129 - "geometry.py"
Cohesion: 0.08
Nodes (12): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+4 more)

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 138 - "TitlePage"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

### Community 140 - "align_decimals"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 143 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 147 - "sys"
Cohesion: 0.23
Nodes (3): build_name(), main(), write_build_info()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (11): NetworkDiagramCanvas, StripChart, form_order(), Scrollable, TextArea, panel(), Builder, Builder (+3 more)

### Community 165 - "Visual"
Cohesion: 0.08
Nodes (3): draw_vessel(), draw_glow(), Visual

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "WindowControls"
Cohesion: 0.09
Nodes (5): draw_window_bar_line(), SquareButtons, _Strip, WindowControls, WindowDrag

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 189 - "MenuBar"
Cohesion: 0.04
Nodes (7): ButtonGroup, offered_sections(), _FollowResize, global_buttons(), MenuBar, window_bar_height(), window_bar_room()

### Community 190 - "ToggleButton"
Cohesion: 0.04
Nodes (8): ToggleButton, PausePacketConsole, ToggleBookmark, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 208 - "QRect"
Cohesion: 0.08
Nodes (3): _Chip, _DropPreview, DropTarget

### Community 213 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 214 - "is_column_available"
Cohesion: 0.28
Nodes (4): column_position(), is_column_available(), shown_columns(), tray_columns()

### Community 216 - "Overlay"
Cohesion: 0.09
Nodes (4): SelectBackground, SelectColorTheme, SelectRegisterPreset, Overlay

### Community 223 - "Process"
Cohesion: 0.07
Nodes (7): flush(), flush_all(), run(), Buffer, ProcessManager, Process, RetentionPolicy

### Community 226 - "BaseForm"
Cohesion: 0.09
Nodes (14): BaseForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm, HVACSlidersForm, SubmarineSlidersForm, APTunnelForm, ArpForm (+6 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

## Knowledge Gaps
- **41 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2103 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **196 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `.start_session`, `important_buttons/__init__.py`, `SmoothWheel`, `Wifi`, `threading`, `ClickManager`, `toasts.py`, `filter_overlay.py`, `widgets/__init__.py`, `ShiftWheel`, `config_editor.py`, `Visual`, `AnimationManager`, `docking.py`, `LocalizationManager`, `Preferences`, `Performance`, `KeyBinds`, `InputManager`, `Router`, `PageManager`, `PrivilegedHelper`, `Toasts`, `Process`, `save_layout_as_default.py`, `BaseForm`, `CheckboxOverlay`, `Style`, `quit_application.py`, `Json`, `.apply`, `host.py`?**
  _High betweenness centrality (0.254) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.08266129032258064 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.theme_family`, `.start_session`, `.brush`, `._build_stylesheet`, `ContextManager`, `.lift_button`, `important_buttons/__init__.py`, `.discard_changes`, `_DressedWidgets`, `Overlay`, `SettingsSection`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.02208660273176402 - nodes in this community are weakly interconnected._