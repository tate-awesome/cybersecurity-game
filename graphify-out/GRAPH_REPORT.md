# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~284,728 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5085 nodes · 10770 edges · 238 communities (92 shown, 146 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `218d7289`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- .__init__
- important_buttons/__init__.py
- MetaPacket
- channels/__init__.py
- settings.py
- Wifi
- .fill_base
- describe.py
- WindowEdges
- DockArea
- router.py
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
- ._build_stylesheet
- window_chrome.py
- ConfigEditor
- docking.py
- LocalizationManager
- Style
- walk
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
- DefenderModbusBuffer
- Rows
- .leaf
- SlidersForm
- InputManager
- CycleBox
- style.py
- Camera
- .__init__
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
- .restyle
- Report
- Draw
- _Grip
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- Toasts
- Camera
- message
- VectorField
- palette_generator.py
- workspace_sorter.py
- compile_filter
- Replay
- .connect_to_saved_wifi
- paint_panel
- DragPayload
- bare_icon
- Json
- ._draw_text
- ComboColumn
- _Dim
- defender_flag_panel/_builder.py
- .__init__
- Paths
- ArpSpoofer
- ap_commands.py
- os
- TabStrip
- WindowControls
- StripChartBase
- _Swallowed
- FilterError
- QWidget
- json
- PopupEntrance
- _Proxy
- pyside6_qtcore
- geometry.py
- .strip_chart_layout
- SmoothWheel
- .record
- kind_color
- Builder
- .refresh_usage
- Scrollable
- context_manager.py
- Scanlines
- Meter
- MitmTable
- APPoller
- Proximity
- place
- StatusBell
- Denier
- confirm_dialog
- widgets/__init__.py
- align_decimals
- ShiftWheel
- SettingCell
- MetaStatus
- ToastCard
- Builder
- record_schema.py
- ._scan_for_networks
- MainWindow
- Overlay
- Master
- Slave
- ChoiceList
- Visual
- PopupWindow
- RecordFilter
- Kalman
- IP Forwarding
- _RightZoneRoom
- version.py
- .arrow
- NoteCache
- Install NMap
- dumps
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .build_menu_bar_section
- .save_current_page
- .prepare_page_config
- NoteBrowser
- _Indicator
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
- ConfigureThisWorkspace
- NFQ Error
- WindowBarButton
- No Network Connection
- QRect
- SelectRegisterPreset
- Notice
- No Wi-Fi Adapter
- Sniffer Didn't Start
- frame_callback
- ButtonModal
- Wi-Fi Connection Failed
- Network Not Found
- No Saved Connection
- SummaryDrawer
- ToggleButton
- Wi-Fi Is Off
- WinDivert Couldn't Open
- threading
- .play
- HideEffect
- ContextManager
- CheckboxOverlay
- Telemetry
- _Drawer
- Cyber-ICS Training Module
- GrowingButton

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

## Communities (238 total, 146 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.11
Nodes (5): Canvas, DefenderWorldMap, NetworkDiagramCanvas, WorldMap, Builder

### Community 1 - ".__init__"
Cohesion: 0.07
Nodes (6): PanelButton, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, EditNetworkHosts, LinkToPage, ChooseShownPacketConsoleColumns

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (26): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, EditModbusRegisterDisplay (+18 more)

### Community 3 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 5 - "settings.py"
Cohesion: 0.07
Nodes (8): save(), on_change(), SettingsSection, developer_text(), LoadLocalizationLabelsFile, OpenThemeEditor, OpenWorkspaceEditor, background_choices()

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 7 - ".fill_base"
Cohesion: 0.12
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 11 - "router.py"
Cohesion: 0.04
Nodes (10): BoatMotion, Sprites, Triangle, TitlePage, WorkspaceSelectPage, WorkspacePage, NotFound, Page (+2 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.07
Nodes (19): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+11 more)

### Community 17 - "menu_bar.py"
Cohesion: 0.08
Nodes (7): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, RefreshCurrentPage, ToggleBookmark

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.08
Nodes (13): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+5 more)

### Community 33 - "server.py"
Cohesion: 0.10
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "window_chrome.py"
Cohesion: 0.10
Nodes (8): bar_button_height(), draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_height(), window_bar_room(), WindowDrag

### Community 38 - "ConfigEditor"
Cohesion: 0.11
Nodes (4): ConfigEditor, walk(), remove_nested(), set_nested()

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
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 48 - ".setText"
Cohesion: 0.07
Nodes (3): OpenFavoritePage, ToggleDebugLabels, icon_button()

### Community 53 - "filter_overlay.py"
Cohesion: 0.13
Nodes (12): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_outside_quotes(), split_pair() (+4 more)

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
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 80 - "ModbusBuffer"
Cohesion: 0.06
Nodes (4): DefenderMapBuffer, HouseBuffer, ModbusBuffer, MapBuffer

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 87 - ".restyle"
Cohesion: 0.09
Nodes (3): _ComboLists, _StyledComboItems, StyleSignals

### Community 88 - "Report"
Cohesion: 0.10
Nodes (6): Report, NMapper, InterfaceManager, job(), _escape(), open_notice()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 97 - "message"
Cohesion: 0.13
Nodes (5): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "workspace_sorter.py"
Cohesion: 0.14
Nodes (4): CategoryChip, checkbox(), SectionCard, ListZone

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 104 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 105 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 106 - "DragPayload"
Cohesion: 0.10
Nodes (3): WorkspaceChip, DragPayload, DropZone

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 112 - "defender_flag_panel/_builder.py"
Cohesion: 0.22
Nodes (6): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 114 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+9 more)

### Community 117 - "os"
Cohesion: 0.04
Nodes (6): flush(), flush_all(), run(), NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue

### Community 122 - "FilterError"
Cohesion: 0.25
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 125 - "json"
Cohesion: 0.22
Nodes (3): build_name(), main(), write_build_info()

### Community 128 - "pyside6_qtcore"
Cohesion: 0.09
Nodes (7): __getattr__(), MaterialEditor, column_position(), is_column_available(), shown_columns(), tray_columns(), MarkdownModal

### Community 129 - "geometry.py"
Cohesion: 0.09
Nodes (11): canvas_fit(), padded_fit(), padded_fit_uniform(), affine(), apply_scale_about(), scale(), translate(), padded_fit_uniform() (+3 more)

### Community 130 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 132 - ".record"
Cohesion: 0.13
Nodes (5): action(), mark(), poll(), status(), clicked()

### Community 136 - "Scrollable"
Cohesion: 0.05
Nodes (6): _Gaps, Scrollable, Builder, Builder, Builder, Builder

### Community 137 - "context_manager.py"
Cohesion: 0.06
Nodes (5): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter, PreferencesData

### Community 146 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 149 - "confirm_dialog"
Cohesion: 0.05
Nodes (10): make(), ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults (+2 more)

### Community 150 - "widgets/__init__.py"
Cohesion: 0.05
Nodes (8): StripChart, TextArea, panel(), Builder, Builder, _DrawerLayout, Panel, Builder

### Community 151 - "align_decimals"
Cohesion: 0.31
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 158 - "record_schema.py"
Cohesion: 0.25
Nodes (4): link_of(), packet(), packet_from_meta(), raw_bytes()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 161 - "Overlay"
Cohesion: 0.08
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 165 - "Visual"
Cohesion: 0.08
Nodes (8): draw_vessel(), get_arc_points(), get_bearing(), rotate(), nice_number(), nice_ticks(), draw_glow(), Visual

### Community 166 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 169 - "IP Forwarding"
Cohesion: 0.40
Nodes (4): IP Forwarding, Linux, macOS / other systems, Windows

### Community 176 - "Install NMap"
Cohesion: 0.50
Nodes (3): Fix, Install NMap, Still not found?

### Community 178 - "dumps"
Cohesion: 0.32
Nodes (3): decode(), dumps(), header()

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

### Community 210 - "Notice"
Cohesion: 0.08
Nodes (4): StatusBuffer, Notice, _BufferShim, read()

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 214 - "ButtonModal"
Cohesion: 0.11
Nodes (7): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SettingsOverlayButton, ButtonModal

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 223 - "threading"
Cohesion: 0.05
Nodes (6): random_spline_path(), Buffer, ProcessManager, Process, FileStream, RetentionPolicy

### Community 224 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 226 - "ContextManager"
Cohesion: 0.09
Nodes (15): ContextManager, House, BaseForm, ModeForm, HVACSlidersForm, SubmarineSlidersForm, APConnectForm, APTunnelForm (+7 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.13
Nodes (4): CheckboxOverlay, form_order(), ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **146 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `pyside6_qtcore`, `Canvas`, `important_buttons/__init__.py`, `SmoothWheel`, `channels/__init__.py`, `settings.py`, `.__init__`, `context_manager.py`, `router.py`, `menu_bar.py`, `confirm_dialog`, `widgets/__init__.py`, `ShiftWheel`, `config_editor.py`, `window_chrome.py`, `Visual`, `docking.py`, `LocalizationManager`, `Style`, `.setText`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `host.py`, `InputManager`, `style.py`, `ConfigureThisWorkspace`, `PageManager`, `PrivilegedHelper`, `ButtonModal`, `.reset_page`, `threading`, `Toasts`, `message`, `workspace_sorter.py`, `.start_session`, `Json`, `defender_flag_panel/_builder.py`, `Paths`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.1067193675889328 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `pyside6_qtcore`, `Overlay`, `ContextManager`, `.setting`, `._build_stylesheet`, `.lift_button`, `important_buttons/__init__.py`, `.start_session`, `style.py`, `context_manager.py`, `.theme_family`, `.setText`, `menu_bar.py`, `_DressedWidgets`, `ButtonModal`, `.restyle`, `SettingsSection`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.0677361853832442 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `pyside6_qtcore`, `settings.py`, `router.py`, `menu_bar.py`, `StatusBell`, `widgets/__init__.py`, `WorkspaceSorter`, `config_editor.py`, `Overlay`, `window_chrome.py`, `ConfigEditor`, `QWidget`, `WindowBarButton`, `PauseMenu`, `workspace_sorter.py`, `.bar_height`, `bare_icon`, `.__init__`, `WindowControls`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._