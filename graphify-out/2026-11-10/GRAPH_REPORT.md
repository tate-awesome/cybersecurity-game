# Graph Report - cybersecurity-game  (2026-11-10)

## Corpus Check
- 342 files · ~286,600 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5108 nodes · 10488 edges · 259 communities (83 shown, 176 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 518 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `42a12367`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- important_buttons/__init__.py
- MetaPacket
- style.py
- paint_mark
- Wifi
- threading
- describe.py
- map.py
- DockArea
- MapBuffer
- Footer
- FilterModal
- Panes
- ap_commands.py
- MetaStatus
- filter_overlay.py
- Builder
- NetworkMesh
- PacketBuffer
- Visuals
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
- wifi_windows.py
- TabStrip
- Modify
- KeyBinds
- .render_blurred
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
- App
- PageManager
- FlowLayout
- .collapsed
- host.py
- DragHandle
- _MapCanvas
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
- modal.py
- VectorField
- palette_generator.py
- DragPayload
- compile_filter
- Replay
- .apply_theme
- ButtonModal
- DefenderModbusBuffer
- ListZone
- Json
- ._draw_text
- ComboColumn
- Router
- _Grip
- WrapLayout
- ProcessManager
- ArpSpoofer
- FlagsForm
- time
- pause_menu.py
- StripChartBase
- APPoller
- StatusBell
- QWidget
- VisualBackground
- .build_menu_bar_section
- PopupEntrance
- _Proxy
- GoForwardToNextPage
- transformations.py
- time_core/transforms.py
- SmoothWheel
- .add_setting_row
- Report
- Builder
- .refresh_usage
- _Gaps
- ClickManager
- GrowingButton
- .new_tab
- PacketTreeview
- MitmTable
- NetFilterQueue
- PopupWindow
- RowZone
- Kernel
- Table
- KalmanToggleForm
- Denier
- _in_nm_context
- widgets/__init__.py
- kind_color
- ShiftWheel
- Draw
- FileStream
- StripChartLayout
- paint_panel
- MainWindow
- Paths
- Master
- Slave
- SettingsPage
- pyside6_qtcore
- AnimationManager
- Kalman
- IP Forwarding
- menu_bar.py
- file_dialog
- Telemetry
- Builder
- NewWorkspaceDialog
- .connect_to_saved_wifi
- Install NMap
- .get_available_networks
- NMap Scan Failed
- Wi-Fi Control Unavailable
- ToggleBookmark
- .save_current_page
- .prepare_page_config
- ._scan_for_networks
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
- .build_summary
- DoS Attack Didn't Start
- _DropPreview
- NFQ Error
- .columnconfigure
- No Network Connection
- _Chip
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
- Process
- Builder
- NetFilterQueue
- ContextManager
- CheckboxOverlay
- .integer
- _Peek
- ConfigureThisWorkspace
- InterfaceManager
- Cyber-ICS Training Module
- Proximity
- normal_value
- open_favorite_page.py
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

## Communities (259 total, 176 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.12
Nodes (3): Canvas, NetworkDiagramCanvas, Builder

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (30): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, EditModbusRegisterDisplay (+22 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "style.py"
Cohesion: 0.12
Nodes (4): PreferencesData, gradient_points(), random_spline_path(), background_choices()

### Community 5 - "paint_mark"
Cohesion: 0.15
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), bar_button_height()

### Community 7 - "threading"
Cohesion: 0.05
Nodes (3): HouseBuffer, ModbusBuffer, _resolve_local_mac()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "map.py"
Cohesion: 0.07
Nodes (9): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate(), shorten_line(), zoom_and_pan() (+1 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.08
Nodes (4): _SashCorners, _SashLight, _PaneContainer, Panes

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "MetaStatus"
Cohesion: 0.10
Nodes (4): MetaStatus, NoticeContent, _Swallowed, ToastCard

### Community 17 - "filter_overlay.py"
Cohesion: 0.16
Nodes (8): draw_vessel(), conjugate(), empty_state(), join_pair(), quote(), split_pair(), to_state(), unquote()

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 22 - "SummaryDrawer"
Cohesion: 0.14
Nodes (3): fade_in(), SummaryDrawer, update()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): LookOnly, MaterialEditor, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.10
Nodes (7): column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.19
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 33 - "server.py"
Cohesion: 0.09
Nodes (12): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+4 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

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

### Community 48 - "RefreshCurrentPage"
Cohesion: 0.12
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

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 65 - ".collect"
Cohesion: 0.15
Nodes (3): read(), remove_nested(), set_nested()

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): read_note(), refresh_preview(), add(), is_switch()

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
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 81 - "host.py"
Cohesion: 0.07
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Notice"
Cohesion: 0.10
Nodes (3): StatusBuffer, Notice, _BufferShim

### Community 92 - "PauseMenu"
Cohesion: 0.05
Nodes (5): _Dim, _Drawer, _FollowResize, _OnHide, PauseMenu

### Community 97 - "modal.py"
Cohesion: 0.06
Nodes (10): DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault (+2 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "DragPayload"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), WorkspaceChip, DragPayload

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 105 - "ButtonModal"
Cohesion: 0.12
Nodes (7): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 116 - "FlagsForm"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 117 - "time"
Cohesion: 0.08
Nodes (10): link_of(), action(), header(), mark(), packet(), packet_from_meta(), poll(), raw_bytes() (+2 more)

### Community 119 - "pause_menu.py"
Cohesion: 0.13
Nodes (5): developer_text(), ButtonGroup, offered_sections(), QuitApplication, ShowHelpMessage

### Community 122 - "StatusBell"
Cohesion: 0.14
Nodes (7): page_tokens(), StatusBell, build_nav(), go(), on_filter(), render(), shown()

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 129 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

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

### Community 150 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (12): StripChart, form_order(), Scrollable, TextArea, panel(), HVACSlidersForm, SubmarineSlidersForm, Builder (+4 more)

### Community 151 - "kind_color"
Cohesion: 0.22
Nodes (3): kind_color(), sheet(), session_stamp()

### Community 159 - "paint_panel"
Cohesion: 0.16
Nodes (3): blurred_shape(), paint_panel(), surface_shadow()

### Community 160 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 165 - "pyside6_qtcore"
Cohesion: 0.06
Nodes (7): MarkdownModal, paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), value_noise(), Visual

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "menu_bar.py"
Cohesion: 0.04
Nodes (16): bare_icon(), _FollowResize, global_buttons(), icon_button(), _RightZoneRoom, CornerControls, draw_window_bar_line(), SquareButtons (+8 more)

### Community 174 - "NewWorkspaceDialog"
Cohesion: 0.09
Nodes (6): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, delete(), create(), rename()

### Community 175 - ".connect_to_saved_wifi"
Cohesion: 0.33
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 186 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 189 - "MenuBar"
Cohesion: 0.04
Nodes (10): BoatMotion, Sprites, Triangle, TitlePage, WorkspaceSelectPage, WorkspacePage, NotFound, Page (+2 more)

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

### Community 223 - "Process"
Cohesion: 0.06
Nodes (7): flush(), flush_all(), run(), Buffer, Process, Loader, RetentionPolicy

### Community 226 - "ContextManager"
Cohesion: 0.09
Nodes (16): ContextManager, DefenderWorldMap, House, WorldMap, BaseForm, align_decimals(), format_number(), fraction_width() (+8 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

## Knowledge Gaps
- **41 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2106 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **176 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `.start_session`, `important_buttons/__init__.py`, `SmoothWheel`, `style.py`, `GoForwardToNextPage`, `threading`, `ClickManager`, `map.py`, `filter_overlay.py`, `PacketBuffer`, `widgets/__init__.py`, `ShiftWheel`, `PacketColumnsModal`, `config_editor.py`, `Paths`, `Style`, `AnimationManager`, `pyside6_qtcore`, `LocalizationManager`, `docking.py`, `menu_bar.py`, `RefreshCurrentPage`, `Preferences`, `Performance`, `KeyBinds`, `MenuBar`, `InputManager`, `PageManager`, `host.py`, `open_favorite_page.py`, `Toasts`, `Process`, `modal.py`, `CheckboxOverlay`, `ButtonModal`, `ConfigureThisWorkspace`, `Json`, `.reload_preferences`, `Router`, `ProcessManager`, `pause_menu.py`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.start_session`, `ContextManager`, `._build_stylesheet`, `style.py`, `.brush`, `important_buttons/__init__.py`, `.apply_theme`, `pyside6_qtcore`, `.theme_family`, `ButtonModal`, `menu_bar.py`, `_DressedWidgets`, `open_favorite_page.py`, `Overlay`, `SettingsSection`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `.start_session` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._