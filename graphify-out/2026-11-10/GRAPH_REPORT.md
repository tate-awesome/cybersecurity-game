# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~286,296 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5102 nodes · 10800 edges · 230 communities (81 shown, 149 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 520 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `70f00def`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- Style
- important_buttons/__init__.py
- MetaPacket
- pyside6_qtcore
- WindowBarButton
- Wifi
- walk
- describe.py
- WindowEdges
- DockArea
- MapBuffer
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- toasts.py
- .field_options
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- SummaryDrawer
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
- Sniffer
- ._build_stylesheet
- Draw
- ConfigEditor
- docking.py
- LocalizationManager
- SettingsSection
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- .setText
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
- TabStrip
- Modify
- KeyBinds
- SettingsPage
- Router
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
- channels/__init__.py
- Constellation
- App
- PageManager
- FlowLayout
- ModbusBuffer
- launch.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- VisualPalette
- Scanlines
- Report
- Draw
- NMapper
- ChoiceList
- PauseMenu
- .fixed_width_wrapper
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
- hvac_chart.py
- ListZone
- Json
- ._draw_text
- ComboColumn
- _Dim
- _Grip
- .__init__
- Loader
- ArpSpoofer
- ap_commands.py
- os
- _OnHide
- StripChartBase
- APPoller
- .fill
- QWidget
- CornerControls
- .build_menu_bar_section
- PopupEntrance
- _Proxy
- .__init__
- geometry.py
- .strip_chart_layout
- SmoothWheel
- .add_setting_row
- MetaStatus
- Builder
- .refresh_usage
- .__init__
- AnimationManager
- title.py
- .new_tab
- align_decimals
- MitmTable
- NetFilterQueue
- MaterialEditorPopup
- place
- StatusBell
- Denier
- MaterialEditor
- widgets/__init__.py
- ShiftWheel
- window_bar_height
- fade_in
- ToastCard
- LookOnly
- ._scan_for_networks
- MainWindow
- WorkspaceButton
- Master
- Slave
- Visual
- PopupWindow
- Kalman
- IP Forwarding
- WindowDrag
- Telemetry
- Builder
- .arrow
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
- frame_callback
- .authored_weights
- Can't Reach the Access Point
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- WorkspaceSelectPage
- DoS Attack Didn't Start
- NFQ Error
- No Network Connection
- QRect
- No Wi-Fi Adapter
- Sniffer Didn't Start
- frame_callback
- Wi-Fi Connection Failed
- Overlay
- Network Not Found
- No Saved Connection
- NoteBrowser
- Wi-Fi Is Off
- WinDivert Couldn't Open
- time
- ProcessManager
- ContextManager
- CheckboxOverlay
- paint_panel
- Cyber-ICS Training Module
- _Swallowed
- ModalWindow
- Scrim
- menu_bar.py
- PreferencesData

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 148 edges
2. `Style` - 123 edges
3. `ImportantButton` - 116 edges
4. `Overlay` - 89 edges
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

## Communities (230 total, 149 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.10
Nodes (6): Canvas, DefenderWorldMap, NetworkDiagramCanvas, TriangleCanvas, WorldMap, Builder

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (33): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ConfigureThisWorkspace (+25 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "pyside6_qtcore"
Cohesion: 0.07
Nodes (9): conjugate(), quote(), BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page (+1 more)

### Community 5 - "WindowBarButton"
Cohesion: 0.13
Nodes (3): bar_button_height(), WindowBarButton, WindowControls

### Community 6 - "Wifi"
Cohesion: 0.08
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 7 - "walk"
Cohesion: 0.10
Nodes (6): visit(), DropTarget, is_split(), tidy(), panel_ids(), walk()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 16 - "toasts.py"
Cohesion: 0.12
Nodes (8): status(), _escape(), kind_color(), clicked(), sheet(), open_notice(), session_stamp(), MarkdownModal

### Community 20 - "PacketBuffer"
Cohesion: 0.08
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - ".__init__"
Cohesion: 0.07
Nodes (5): ap_tunnel_enabled(), encryption_enabled(), set_encryption(), start_encryption(), stop_encryption()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.10
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "Context"
Cohesion: 0.08
Nodes (12): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+4 more)

### Community 33 - "Sniffer"
Cohesion: 0.15
Nodes (3): Sniffer, build_capability(), _Echo

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (13): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+5 more)

### Community 42 - "SettingsSection"
Cohesion: 0.15
Nodes (3): save(), on_change(), SettingsSection

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

### Community 53 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

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

### Community 65 - ".collect"
Cohesion: 0.15
Nodes (3): read(), remove_nested(), set_nested()

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): read_note(), refresh_preview(), add(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 75 - "channels/__init__.py"
Cohesion: 0.04
Nodes (6): DefenderMapBuffer, DefenderModbusBuffer, APCommand, DefenderStatusBuffer, StatusBuffer, _PollUnpacker

### Community 81 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "Report"
Cohesion: 0.06
Nodes (10): Notice, Report, _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 90 - "NMapper"
Cohesion: 0.09
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 91 - "ChoiceList"
Cohesion: 0.13
Nodes (3): _ComboLists, _StyledComboItems, ChoiceList

### Community 97 - "modal.py"
Cohesion: 0.04
Nodes (15): make(), ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults (+7 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "DragPayload"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), WorkspaceChip, DragPayload

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 108 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 116 - "ap_commands.py"
Cohesion: 0.10
Nodes (17): ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), set_ap_tunnel(), set_hvac_kalman(), set_kalman() (+9 more)

### Community 117 - "os"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 122 - ".fill"
Cohesion: 0.36
Nodes (6): page_tokens(), build_nav(), go(), on_filter(), render(), shown()

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 129 - "geometry.py"
Cohesion: 0.09
Nodes (11): canvas_fit(), padded_fit(), padded_fit_uniform(), affine(), apply_scale_about(), scale(), translate(), padded_fit_uniform() (+3 more)

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "title.py"
Cohesion: 0.11
Nodes (3): TitlePage, TitleFooter, TitleMenu

### Community 140 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 146 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.03
Nodes (12): StripChart, Scrollable, TextArea, panel(), Builder, Builder, Builder, Builder (+4 more)

### Community 159 - "._scan_for_networks"
Cohesion: 0.53
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 165 - "Visual"
Cohesion: 0.07
Nodes (11): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through() (+3 more)

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "WindowDrag"
Cohesion: 0.12
Nodes (5): draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), WindowDrag

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 190 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "Overlay"
Cohesion: 0.04
Nodes (12): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+4 more)

### Community 223 - "time"
Cohesion: 0.05
Nodes (7): random_spline_path(), Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process, FileStream, RetentionPolicy

### Community 226 - "ContextManager"
Cohesion: 0.10
Nodes (15): ContextManager, House, form_order(), BaseForm, HVACSlidersForm, SubmarineSlidersForm, APConnectForm, APTunnelForm (+7 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.07
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 231 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 250 - "menu_bar.py"
Cohesion: 0.07
Nodes (9): ButtonGroup, offered_sections(), GoForwardToNextPage, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage, bare_icon(), global_buttons() (+1 more)

## Knowledge Gaps
- **149 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `Style`, `important_buttons/__init__.py`, `SmoothWheel`, `pyside6_qtcore`, `AnimationManager`, `title.py`, `toasts.py`, `PacketBuffer`, `widgets/__init__.py`, `ShiftWheel`, `PacketColumnsModal`, `Visual`, `docking.py`, `LocalizationManager`, `.setText`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `style.py`, `PageManager`, `ModbusBuffer`, `PrivilegedHelper`, `Overlay`, `time`, `Toasts`, `ProcessManager`, `modal.py`, `CheckboxOverlay`, `.apply_theme`, `hvac_chart.py`, `Json`, `ap_commands.py`, `os`, `menu_bar.py`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.09666666666666666 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `pyside6_qtcore`, `.brush`, `.lift_button`, `.apply_theme`, `important_buttons/__init__.py`, `style.py`, `.theme_family`, `menu_bar.py`, `.setText`, `_DressedWidgets`, `Overlay`, `SettingsSection`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Style` be split into smaller, more focused modules?**
  _Cohesion score 0.06463414634146342 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `ContextManager`, `.__init__`, `pyside6_qtcore`, `WindowBarButton`, `window_bar_height`, `WindowDrag`, `.show_body`, `QWidget`, `CornerControls`, `.__init__`, `StatusBell`, `widgets/__init__.py`, `Overlay`, `menu_bar.py`, `PauseMenu`, `QPushButton`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._