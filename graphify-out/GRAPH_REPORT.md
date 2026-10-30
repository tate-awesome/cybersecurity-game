# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~285,542 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5089 nodes · 10776 edges · 222 communities (83 shown, 139 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df5f98db`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- Style
- important_buttons/__init__.py
- MetaPacket
- message
- developer_text
- Wifi
- describe.py
- WindowEdges
- DockArea
- pyside6_qtcore
- Footer
- FilterModal
- Panes
- Attack
- WorkspaceSelectPage
- menu_bar.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderModbusBuffer
- SessionRecorder
- WorkspaceSorter
- Toast
- SettingsSection
- .__init__
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- Context
- Notice
- ._build_stylesheet
- .collect
- ConfigEditor
- docking.py
- LocalizationManager
- walk
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- .__init__
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- filter_overlay.py
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
- Rows
- .leaf
- align_decimals
- SlidersForm
- InputManager
- WrapLayout
- CycleBox
- style.py
- Camera
- .__init__
- Constellation
- App
- PageManager
- FlowLayout
- channels/__init__.py
- launch.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- VisualPalette
- Dev/Host_API.py
- Report
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- Toasts
- Camera
- confirm_dialog
- VectorField
- palette_generator.py
- workspace_sorter.py
- compile_filter
- Replay
- .apply_theme
- .connect_to_saved_wifi
- paint_panel
- Json
- ._draw_text
- ComboColumn
- _Dim
- Prod/Host_API.py
- .__init__
- Paths
- ArpSpoofer
- ap_commands.py
- os
- TabStrip
- _OnHide
- StripChartBase
- APPoller
- QWidget
- ChoiceList
- json
- PopupEntrance
- _Proxy
- geometry.py
- .strip_chart_layout
- SmoothWheel
- .__init__
- Builder
- .build_tabs
- _Gaps
- context_manager.py
- Scanlines
- .new_tab
- Meter
- MitmTable
- NetFilterQueue
- .add_setting_row
- place
- StatusBell
- Denier
- widgets/__init__.py
- MapBuffer
- ShiftWheel
- window_chrome.py
- MetaStatus
- ToastCard
- ._scan_for_networks
- MainWindow
- Master
- Slave
- Visual
- PopupWindow
- Kalman
- IP Forwarding
- BuildInfo
- .arrow
- NoteBrowser
- Install NMap
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .build_menu_bar_section
- .save_current_page
- .prepare_page_config
- GrowingButton
- DropZone
- MenuBar
- fade_in
- frame_callback
- .authored_weights
- Can't Reach the Access Point
- .build_description_tab
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- WorkspaceButton
- DoS Attack Didn't Start
- NFQ Error
- No Network Connection
- QRect
- No Wi-Fi Adapter
- Sniffer Didn't Start
- frame_callback
- Wi-Fi Connection Failed
- Network Not Found
- No Saved Connection
- SummaryDrawer
- ToggleButton
- Wi-Fi Is Off
- WinDivert Couldn't Open
- time
- ProcessManager
- ContextManager
- CheckboxOverlay
- Telemetry
- CornerControls
- Cyber-ICS Training Module
- _Swallowed
- .__init__

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 148 edges
2. `Style` - 123 edges
3. `ImportantButton` - 116 edges
4. `Overlay` - 88 edges
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

## Communities (222 total, 139 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.06
Nodes (10): Canvas, DefenderWorldMap, follow_theme(), House, NetworkDiagramCanvas, TriangleCanvas, WorldMap, Builder (+2 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (33): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ConfigureThisWorkspace (+25 more)

### Community 3 - "MetaPacket"
Cohesion: 0.06
Nodes (6): Channel, NetworkGraph, Transaction, TransactionManager, MetaPacket, Builder

### Community 4 - "message"
Cohesion: 0.13
Nodes (5): make(), _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, message()

### Community 5 - "developer_text"
Cohesion: 0.13
Nodes (4): save(), on_change(), SettingsSection, developer_text()

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 11 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (9): BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page, MaterialEditor (+1 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.09
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 17 - "menu_bar.py"
Cohesion: 0.07
Nodes (11): ButtonGroup, offered_sections(), GoBackToPreviousPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark, RefreshAndCloseOverlay, ShowHelpMessage (+3 more)

### Community 18 - "PacketTreeview"
Cohesion: 0.06
Nodes (7): FilterError, parse(), Parser, split_outside_quotes(), tokenize(), unquote(), PacketTreeview

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderModbusBuffer"
Cohesion: 0.04
Nodes (6): DefenderMapBuffer, DefenderModbusBuffer, APCommand, DefenderStatusBuffer, StatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+5 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.08
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.10
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "Context"
Cohesion: 0.08
Nodes (12): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+4 more)

### Community 33 - "Notice"
Cohesion: 0.06
Nodes (13): Notice, Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run() (+5 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (13): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+5 more)

### Community 42 - "walk"
Cohesion: 0.10
Nodes (6): visit(), DropTarget, is_split(), tidy(), panel_ids(), walk()

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 46 - "HVACChart"
Cohesion: 0.11
Nodes (3): DefenderHVACChart, HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 53 - "filter_overlay.py"
Cohesion: 0.21
Nodes (7): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), to_state()

### Community 54 - ".__init__"
Cohesion: 0.16
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), ring_spots()

### Community 55 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "Wifi"
Cohesion: 0.11
Nodes (6): _list_item(), Wifi, finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 68 - "align_decimals"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 80 - "channels/__init__.py"
Cohesion: 0.07
Nodes (4): HouseBuffer, ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 87 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 88 - "Report"
Cohesion: 0.08
Nodes (7): Report, NMapper, InterfaceManager, job(), _escape(), clicked(), open_notice()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.04
Nodes (12): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, SelectRegisterPreset, SettingsOverlayButton (+4 more)

### Community 97 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, WorkspaceSaveResetButton (+1 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "workspace_sorter.py"
Cohesion: 0.11
Nodes (5): CategoryChip, checkbox(), SectionCard, WorkspaceChip, ListZone

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 104 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 105 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 112 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 114 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 116 - "ap_commands.py"
Cohesion: 0.12
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+9 more)

### Community 117 - "os"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 124 - "ChoiceList"
Cohesion: 0.13
Nodes (3): _ComboLists, _StyledComboItems, ChoiceList

### Community 125 - "json"
Cohesion: 0.21
Nodes (3): build_name(), main(), write_build_info()

### Community 129 - "geometry.py"
Cohesion: 0.09
Nodes (11): canvas_fit(), padded_fit(), padded_fit_uniform(), affine(), apply_scale_about(), scale(), translate(), padded_fit_uniform() (+3 more)

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 133 - ".__init__"
Cohesion: 0.28
Nodes (3): kind_color(), sheet(), session_stamp()

### Community 137 - "context_manager.py"
Cohesion: 0.06
Nodes (5): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter, PreferencesData

### Community 146 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.03
Nodes (13): StripChart, Scrollable, TextArea, panel(), Builder, Builder, Builder, Builder (+5 more)

### Community 154 - "window_chrome.py"
Cohesion: 0.09
Nodes (7): bar_button_height(), SquareButtons, toggle_maximized(), window_bar_button_height(), WindowBarButton, WindowControls, WindowDrag

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 165 - "Visual"
Cohesion: 0.07
Nodes (11): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through() (+3 more)

### Community 166 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

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

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 223 - "time"
Cohesion: 0.06
Nodes (6): random_spline_path(), Buffer, NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 226 - "ContextManager"
Cohesion: 0.08
Nodes (20): ContextManager, form_order(), BaseForm, FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, SubmarineKalmanToggleForm (+12 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.07
Nodes (8): DragPayload, PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 231 - "CornerControls"
Cohesion: 0.13
Nodes (5): CornerControls, draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

## Knowledge Gaps
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `Style`, `important_buttons/__init__.py`, `SmoothWheel`, `message`, `.__init__`, `context_manager.py`, `pyside6_qtcore`, `menu_bar.py`, `widgets/__init__.py`, `ShiftWheel`, `window_chrome.py`, `Visual`, `docking.py`, `LocalizationManager`, `.__init__`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `style.py`, `PageManager`, `channels/__init__.py`, `PrivilegedHelper`, `Overlay`, `Toasts`, `time`, `ProcessManager`, `confirm_dialog`, `workspace_sorter.py`, `.apply_theme`, `Json`, `Paths`, `os`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.055904961565338925 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `.brush`, `.lift_button`, `important_buttons/__init__.py`, `.apply_theme`, `style.py`, `context_manager.py`, `.theme_family`, `.__init__`, `menu_bar.py`, `_DressedWidgets`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Style` be split into smaller, more focused modules?**
  _Cohesion score 0.06463414634146342 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `workspace_sorter.py`, `.__init__`, `ConfigEditor`, `.minimize_button`, `CornerControls`, `window_chrome.py`, `pyside6_qtcore`, `QWidget`, `menu_bar.py`, `.__init__`, `StatusBell`, `widgets/__init__.py`, `WorkspaceSorter`, `.bar_height`, `Overlay`, `PauseMenu`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._