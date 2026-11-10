# Graph Report - cybersecurity-game  (2026-11-10)

## Corpus Check
- 342 files · ~286,906 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5118 nodes · 10507 edges · 260 communities (82 shown, 178 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 521 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5911516c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TransactionManager
- ImportantButton
- MetaPacket
- context_manager.py
- save_layout_as_default.py
- Wifi
- channels/__init__.py
- describe.py
- geometry.py
- DockArea
- MapBuffer
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
- background.py
- Sniffer
- ._build_stylesheet
- Style
- ConfigEditor
- docking.py
- LocalizationManager
- WifiForm
- WifiBaseClass
- HVACChart
- QWidget
- .add_setting_row
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- parse
- frame_callback
- HostModal
- Performance
- ViewPort
- wifi_windows.py
- TabStrip
- Modify
- KeyBinds
- SettingsPage
- ModbusBuffer
- FadeOut
- .collect
- Rows
- .leaf
- Meter
- SlidersForm
- InputManager
- arp_poisoner.py
- CycleBox
- style.py
- Camera
- DefenderStatusBuffer
- Constellation
- app.py
- PageManager
- FlowLayout
- ElidingLabel
- launch.py
- DragHandle
- .field_options
- VariableModal
- PrivilegedHelper
- .color
- Scanlines
- server.py
- Draw
- ChoiceList
- PauseMenu
- WaveGrid
- Toasts
- Camera
- confirm_dialog
- VectorField
- palette_generator.py
- WorkspaceChip
- compile_filter
- Prod/Host_API.py
- Dev/Host_API.py
- important_buttons/__init__.py
- DefenderModbusBuffer
- .__init__
- Json
- ._draw_text
- ComboColumn
- Router
- _Grip
- WrapLayout
- ListZone
- ArpSpoofer
- flags.py
- .add_chip
- StripChartBase
- APPoller
- .fill
- transitions.py
- _Dim
- PopupEntrance
- host.py
- buffer_manager.py
- WindowEdges
- time_core/transforms.py
- .connect_to_saved_wifi
- .new_tab
- Report
- Builder
- .build_tabs
- _Gaps
- ClickManager
- GrowingButton
- paint_mark
- MitmTable
- NetFilterQueue
- PopupWindow
- _Indicator
- Table
- KalmanToggleForm
- Denier
- _DrawerLayout
- toasts.py
- ShiftWheel
- Draw
- sys
- .__init__
- StripChartLayout
- MenuBar
- _PollUnpacker
- paint_panel
- MainWindow
- TextArea
- Master
- Slave
- Map
- VisualPalette
- AnimationManager
- Kalman
- IP Forwarding
- menu_bar.py
- _MapCanvas
- columns_overlay.py
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
- BinZone
- Can't Reach the Access Point
- StatusBell
- Host Not Found
- ARP Spoof Error
- PooledCanvasMixin
- Capture File Error
- DoS Attack Didn't Start
- ._scan_for_networks
- NFQ Error
- .__init__
- No Network Connection
- QRect
- .__init__
- .build_menu_bar_section
- No Wi-Fi Adapter
- Sniffer Didn't Start
- .__init__
- NetFilterQueueBaseClass
- Wi-Fi Connection Failed
- Overlay
- Network Not Found
- No Saved Connection
- NoteCache
- NoteBrowser
- Wi-Fi Is Off
- WinDivert Couldn't Open
- time
- _RightZoneRoom
- NMapper
- ContextManager
- CheckboxOverlay
- SniffedHVACChart
- Channel
- InterfaceManager
- Cyber-ICS Training Module
- .start
- Proximity
- _OnHide
- .build_description_tab
- .build_summary
- LinkToPage
- open_favorite_page.py
- pyside6_qtwidgets
- submarine_settings_synced
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

## Communities (260 total, 178 thin omitted)

### Community 2 - "ImportantButton"
Cohesion: 0.02
Nodes (30): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ConfigureThisWorkspace (+22 more)

### Community 4 - "context_manager.py"
Cohesion: 0.05
Nodes (7): CallbackRegistry, _dialog_parent(), file_dialog(), Paths, PreferencesData, SmoothWheel, ProcessManager

### Community 5 - "save_layout_as_default.py"
Cohesion: 0.10
Nodes (6): SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 8 - "describe.py"
Cohesion: 0.05
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "geometry.py"
Cohesion: 0.07
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), affine(), apply_scale_about(), get_arc_points(), get_bearing(), rotate() (+6 more)

### Community 10 - "DockArea"
Cohesion: 0.07
Nodes (3): DockArea, visit(), drain_evenly()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "ap_commands.py"
Cohesion: 0.18
Nodes (15): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+7 more)

### Community 16 - "ToastCard"
Cohesion: 0.14
Nodes (3): NoticeContent, _Swallowed, ToastCard

### Community 17 - "packet_filter.py"
Cohesion: 0.19
Nodes (7): empty_state(), Field, normal_value(), split_outside_quotes(), to_state(), tokenize(), unquote()

### Community 20 - "PacketBuffer"
Cohesion: 0.09
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (3): RecordFilter, RetentionPolicy, SessionRecorder

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): column_category(), is_column_available(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "background.py"
Cohesion: 0.13
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 33 - "Sniffer"
Cohesion: 0.15
Nodes (3): Sniffer, build_capability(), _Echo

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
Cohesion: 0.11
Nodes (3): DefenderHVACChart, follow_theme(), HVACChart

### Community 47 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 54 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostModal"
Cohesion: 0.15
Nodes (5): HostModal, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 62 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 64 - "FadeOut"
Cohesion: 0.13
Nodes (5): DesktopFade, covered(), settle(), uncovered(), FadeOut

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "arp_poisoner.py"
Cohesion: 0.15
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 73 - "style.py"
Cohesion: 0.09
Nodes (14): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient() (+6 more)

### Community 77 - "app.py"
Cohesion: 0.13
Nodes (3): App, FadeIn, __getattr__()

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "server.py"
Cohesion: 0.13
Nodes (8): _BufferShim, _ContextStub, _dispatch(), run(), flusher(), run_from_argv(), send(), status_heartbeat()

### Community 97 - "confirm_dialog"
Cohesion: 0.05
Nodes (11): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+3 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Prod/Host_API.py"
Cohesion: 0.19
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status(), encryption_enabled() (+1 more)

### Community 103 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 105 - "important_buttons/__init__.py"
Cohesion: 0.09
Nodes (8): LoadLocalizationLabelsFile, OpenWorkspaceEditor, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, SettingsOverlayButton, ButtonModal

### Community 112 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 116 - "flags.py"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 117 - ".add_chip"
Cohesion: 0.19
Nodes (3): delete(), create(), rename()

### Community 122 - ".fill"
Cohesion: 0.23
Nodes (9): page_tokens(), build_nav(), go(), on_filter(), refresh(), render(), shown(), start() (+1 more)

### Community 123 - "transitions.py"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 124 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 128 - "buffer_manager.py"
Cohesion: 0.09
Nodes (5): Buffer, StatusBuffer, MetaStatus, Notice, read()

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 138 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 139 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 143 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 147 - "KalmanToggleForm"
Cohesion: 0.23
Nodes (3): HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 151 - "toasts.py"
Cohesion: 0.11
Nodes (8): status(), _escape(), kind_color(), clicked(), sheet(), open_notice(), session_stamp(), MarkdownModal

### Community 154 - "sys"
Cohesion: 0.18
Nodes (3): build_name(), main(), write_build_info()

### Community 159 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 164 - "Map"
Cohesion: 0.22
Nodes (3): BoatMotion, Sprites, Map

### Community 165 - "VisualPalette"
Cohesion: 0.08
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, Telemetry

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 170 - "menu_bar.py"
Cohesion: 0.05
Nodes (17): ButtonGroup, offered_sections(), bare_icon(), global_buttons(), icon_button(), bar_button_height(), CornerControls, draw_window_bar_line() (+9 more)

### Community 172 - "columns_overlay.py"
Cohesion: 0.27
Nodes (3): column_position(), shown_columns(), tray_columns()

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
Nodes (19): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+11 more)

### Community 190 - "ToggleButton"
Cohesion: 0.04
Nodes (10): ToggleButton, PausePacketConsole, SetCurrentPageAsFavorite, ToggleBookmark, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode (+2 more)

### Community 192 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 204 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 206 - ".__init__"
Cohesion: 0.06
Nodes (3): Builder, Builder, Builder

### Community 213 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "Overlay"
Cohesion: 0.04
Nodes (5): SelectBackground, SelectColorTheme, SelectRegisterPreset, Overlay, background_choices()

### Community 223 - "time"
Cohesion: 0.03
Nodes (17): flush(), flush_all(), run(), random_spline_path(), link_of(), Process, FileStream, action() (+9 more)

### Community 226 - "ContextManager"
Cohesion: 0.05
Nodes (19): ContextManager, zoom_and_pan(), FilterError, Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart (+11 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.08
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 248 - "pyside6_qtwidgets"
Cohesion: 0.06
Nodes (16): conjugate(), quote(), BaseForm, HVACSlidersForm, SubmarineSlidersForm, align_decimals(), format_number(), fraction_width() (+8 more)

## Knowledge Gaps
- **41 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2111 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **178 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `buffer_manager.py`, `ImportantButton`, `context_manager.py`, `save_layout_as_default.py`, `channels/__init__.py`, `ClickManager`, `geometry.py`, `toasts.py`, `ShiftWheel`, `background.py`, `Style`, `AnimationManager`, `docking.py`, `LocalizationManager`, `menu_bar.py`, `columns_overlay.py`, `Preferences`, `.reset_page`, `Performance`, `KeyBinds`, `config_editor.py`, `InputManager`, `style.py`, `PageManager`, `PrivilegedHelper`, `Toasts`, `time`, `confirm_dialog`, `CheckboxOverlay`, `important_buttons/__init__.py`, `Json`, `Router`, `flags.py`, `LinkToPage`, `open_favorite_page.py`, `pyside6_qtwidgets`, `.apply`, `host.py`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TransactionManager` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `context_manager.py`, `.brush`, `ImportantButton`, `style.py`, `.theme_family`, `.discard_changes`, `.lift_button`, `important_buttons/__init__.py`, `menu_bar.py`, `_DressedWidgets`, `open_favorite_page.py`, `Overlay`, `SettingsSection`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `ImportantButton` be split into smaller, more focused modules?**
  _Cohesion score 0.023695602642971065 - nodes in this community are weakly interconnected._