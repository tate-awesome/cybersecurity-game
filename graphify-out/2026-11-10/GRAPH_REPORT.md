# Graph Report - cybersecurity-game  (2026-11-10)

## Corpus Check
- 342 files · ~286,680 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5111 nodes · 10492 edges · 262 communities (85 shown, 177 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 519 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5287834d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- PacketBuffer
- important_buttons/__init__.py
- MetaPacket
- context_manager.py
- save_layout_as_default.py
- Wifi
- threading
- describe.py
- geometry.py
- DockArea
- MapBuffer
- Footer
- FilterModal
- Panes
- ap_commands.py
- ToastCard
- filter_overlay.py
- PacketTreeview
- NetworkMesh
- scapy_all
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
- Sniffer
- ._build_stylesheet
- Style
- ConfigEditor
- docking.py
- LocalizationManager
- SettingsSection
- WifiForm
- WifiBaseClass
- HVACChart
- QWidget
- RefreshCurrentPage
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- FilterError
- frame_callback
- HostModal
- Performance
- ViewPort
- Wifi
- TabStrip
- Modify
- KeyBinds
- HouseBuffer
- FadeIn
- .collect
- Rows
- .leaf
- Meter
- SlidersForm
- InputManager
- Attack
- CycleBox
- style.py
- Camera
- DefenderStatusBuffer
- Constellation
- app.py
- PageManager
- FlowLayout
- walk
- launch.py
- DragHandle
- .field_options
- VariableModal
- PrivilegedHelper
- VisualPalette
- Scanlines
- Notice
- Draw
- .library_nmap
- ChoiceList
- PauseMenu
- BaseForm
- WaveGrid
- Toasts
- Camera
- confirm_dialog
- VectorField
- palette_generator.py
- SectionCard
- compile_filter
- Replay
- .apply_theme
- modal.py
- DefenderModbusBuffer
- .__init__
- Json
- ._draw_text
- ComboColumn
- Router
- _Grip
- WrapLayout
- wifi_windows.py
- ArpSpoofer
- FlagsForm
- record_schema.py
- menu_bar.py
- StripChartBase
- APPoller
- .fill
- transitions.py
- _Dim
- WindowDrag
- PopupEntrance
- _Proxy
- Buffer
- WindowEdges
- time_core/transforms.py
- SmoothWheel
- QWidget
- Report
- Builder
- .build_tabs
- _Gaps
- ClickManager
- GrowingButton
- RecordFilter
- MitmTable
- NetFilterQueue
- PopupWindow
- ListZone
- Kernel
- Table
- KalmanToggleForm
- Denier
- _DrawerLayout
- kind_color
- ShiftWheel
- Draw
- sys
- fade_in
- StripChartLayout
- MenuBar
- _PollUnpacker
- paint_panel
- MainWindow
- TextArea
- Master
- Slave
- SettingsPage
- Visual
- AnimationManager
- Kalman
- IP Forwarding
- window_chrome.py
- WindowBarButton
- Telemetry
- Builder
- NewWorkspaceDialog
- .__init__
- Install NMap
- Loader
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .__init__
- .save_current_page
- .prepare_page_config
- version.py
- DragPayload
- router.py
- ToggleButton
- ModeForm
- .__init__
- .authored_weights
- .add_deadspace
- Can't Reach the Access Point
- StatusBell
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- WorkspaceSelectPage
- DoS Attack Didn't Start
- MetaStatus
- NFQ Error
- .columnconfigure
- No Network Connection
- QRect
- .__init__
- No Wi-Fi Adapter
- Sniffer Didn't Start
- .__init__
- NetFilterQueueBaseClass
- Wi-Fi Connection Failed
- Overlay
- Network Not Found
- No Saved Connection
- NoteBrowser
- ToggleLightDarkMode
- Wi-Fi Is Off
- WinDivert Couldn't Open
- time
- Builder
- NMapper
- ContextManager
- CheckboxOverlay
- .integer
- _Swallowed
- ConfigureThisWorkspace
- InterfaceManager
- Builder
- Cyber-ICS Training Module
- Proximity
- _OnHide
- .build_description_tab
- WorkspaceButton
- LinkToPage
- open_favorite_page.py
- align_decimals
- panel
- random
- .__init__
- DenseMesh
- APTunnelForm
- KalmanForm

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

## Communities (262 total, 177 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.08
Nodes (5): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (29): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, EditModbusRegisterDisplay (+21 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 5 - "save_layout_as_default.py"
Cohesion: 0.13
Nodes (5): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 6 - "Wifi"
Cohesion: 0.07
Nodes (11): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish() (+3 more)

### Community 7 - "threading"
Cohesion: 0.11
Nodes (3): DefenderMapBuffer, ModbusBuffer, _resolve_local_mac()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "geometry.py"
Cohesion: 0.07
Nodes (15): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), get_arc_points(), get_bearing() (+7 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 17 - "filter_overlay.py"
Cohesion: 0.18
Nodes (9): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_pair(), to_state() (+1 more)

### Community 20 - "scapy_all"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, NetworkDiagramCanvas

### Community 21 - "VisualBackground"
Cohesion: 0.06
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 24 - "WorkspaceSorter"
Cohesion: 0.12
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): LookOnly, MaterialEditor, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.09
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.20
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 33 - "Sniffer"
Cohesion: 0.15
Nodes (3): Sniffer, build_capability(), _Echo

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (13): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+5 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 48 - "RefreshCurrentPage"
Cohesion: 0.11
Nodes (6): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, EditWorkspaceAvailability, RefreshAndCloseOverlay, WorkspaceSaveResetButton

### Community 53 - "FilterError"
Cohesion: 0.23
Nodes (5): FilterError, parse(), Parser, split_outside_quotes(), tokenize()

### Community 54 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostModal"
Cohesion: 0.15
Nodes (5): HostModal, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.06
Nodes (5): ViewPort, BoatMotion, Sprites, Map, _MapCanvas

### Community 58 - "Wifi"
Cohesion: 0.10
Nodes (6): _list_item(), Wifi, finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (3): add(), click(), sync()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 80 - "walk"
Cohesion: 0.10
Nodes (6): visit(), DropTarget, is_split(), tidy(), panel_ids(), walk()

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Notice"
Cohesion: 0.09
Nodes (10): Notice, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv(), send() (+2 more)

### Community 93 - "BaseForm"
Cohesion: 0.03
Nodes (8): BaseForm, ElidingLabel, ArpForm, DosForm, EncryptionForm, NFQForm, NmapForm, SniffForm

### Community 97 - "confirm_dialog"
Cohesion: 0.08
Nodes (6): DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), ResetCurrentPageToDefaults, confirm_dialog()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 105 - "modal.py"
Cohesion: 0.09
Nodes (8): SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal, MarkdownModal, background_choices()

### Community 108 - "Json"
Cohesion: 0.07
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 114 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 116 - "FlagsForm"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 117 - "record_schema.py"
Cohesion: 0.16
Nodes (10): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+2 more)

### Community 119 - "menu_bar.py"
Cohesion: 0.06
Nodes (11): developer_text(), ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, QuitApplication, ToggleBookmark (+3 more)

### Community 122 - ".fill"
Cohesion: 0.33
Nodes (7): page_tokens(), build_nav(), go(), on_filter(), refresh(), render(), shown()

### Community 123 - "transitions.py"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 124 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 125 - "WindowDrag"
Cohesion: 0.17
Nodes (3): SquareButtons, toggle_maximized(), WindowDrag

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "QWidget"
Cohesion: 0.11
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 133 - "Report"
Cohesion: 0.15
Nodes (3): Report, _escape(), open_notice()

### Community 138 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 143 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 147 - "KalmanToggleForm"
Cohesion: 0.23
Nodes (3): HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 151 - "kind_color"
Cohesion: 0.13
Nodes (5): status(), kind_color(), clicked(), sheet(), session_stamp()

### Community 154 - "sys"
Cohesion: 0.27
Nodes (3): build_name(), main(), write_build_info()

### Community 159 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 165 - "Visual"
Cohesion: 0.07
Nodes (8): draw_vessel(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), value_noise(), draw_glow(), Visual

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "window_chrome.py"
Cohesion: 0.12
Nodes (7): bar_button_height(), CornerControls, draw_window_bar_line(), _Strip, window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 174 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 175 - ".__init__"
Cohesion: 0.22
Nodes (3): covered(), settle(), uncovered()

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 189 - "router.py"
Cohesion: 0.10
Nodes (5): Triangle, TitlePage, WorkspacePage, NotFound, Page

### Community 190 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 213 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "Overlay"
Cohesion: 0.05
Nodes (3): SelectBackground, SelectRegisterPreset, Overlay

### Community 223 - "time"
Cohesion: 0.05
Nodes (6): flush(), flush_all(), run(), ProcessManager, Process, FileStream

### Community 226 - "ContextManager"
Cohesion: 0.09
Nodes (10): ContextManager, StripChart, form_order(), Scrollable, HVACSlidersForm, SubmarineSlidersForm, format_number(), Builder (+2 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.08
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

## Knowledge Gaps
- **41 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2107 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **177 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `SmoothWheel`, `context_manager.py`, `save_layout_as_default.py`, `threading`, `ClickManager`, `filter_overlay.py`, `scapy_all`, `ShiftWheel`, `config_editor.py`, `Style`, `AnimationManager`, `docking.py`, `LocalizationManager`, `Visual`, `window_chrome.py`, `RefreshCurrentPage`, `Preferences`, `Performance`, `KeyBinds`, `router.py`, `InputManager`, `style.py`, `PageManager`, `open_favorite_page.py`, `Toasts`, `time`, `confirm_dialog`, `CheckboxOverlay`, `.apply_theme`, `modal.py`, `ConfigureThisWorkspace`, `Json`, `.reload_preferences`, `Router`, `host.py`, `LinkToPage`, `menu_bar.py`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `context_manager.py`, `.brush`, `important_buttons/__init__.py`, `.apply_theme`, `style.py`, `.theme_family`, `modal.py`, `.lift_button`, `_DressedWidgets`, `menu_bar.py`, `open_favorite_page.py`, `Overlay`, `SettingsSection`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `PacketBuffer` be split into smaller, more focused modules?**
  _Cohesion score 0.09486166007905138 - nodes in this community are weakly interconnected._