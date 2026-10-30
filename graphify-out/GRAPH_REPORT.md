# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~284,869 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5086 nodes · 10771 edges · 240 communities (93 shown, 147 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `af2a826c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app_core/__init__.py
- edit_network_hosts.py
- ImportantButton
- MetaPacket
- important_buttons/__init__.py
- SettingsSection
- Wifi
- describe.py
- WindowEdges
- DockArea
- ContextManager
- Footer
- FilterModal
- Panes
- arp_poisoner.py
- WorkspaceSelectPage
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
- .__init__
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- workspace_sorter.py
- server.py
- ._build_stylesheet
- window_chrome.py
- Style
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
- DefenderModbusBuffer
- Rows
- .leaf
- DropZone
- SlidersForm
- InputManager
- CycleBox
- themes.py
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
- Dev/Host_API.py
- Report
- Draw
- _Grip
- PauseMenu
- ElidingLabel
- WaveGrid
- Toasts
- Camera
- message
- VectorField
- palette_generator.py
- SectionCard
- compile_filter
- Replay
- .apply_theme
- .connect_to_saved_wifi
- paint_panel
- DragPayload
- bare_icon
- Json
- ._draw_text
- ComboColumn
- _Dim
- Prod/Host_API.py
- .__init__
- file_dialog
- ArpSpoofer
- ap_commands.py
- os
- TabStrip
- CornerControls
- StripChartBase
- APPoller
- FilterError
- QWidget
- .collect
- sys
- PopupEntrance
- _Proxy
- packet_console/_builder.py
- geometry.py
- .strip_chart_layout
- SmoothWheel
- kind_color
- Builder
- .build_tabs
- Scrollable
- AnimationManager
- Scanlines
- .new_tab
- Meter
- MitmTable
- NetFilterQueue
- .add_setting_row
- Visual
- Table
- StatusBell
- Denier
- confirm_dialog
- widgets/__init__.py
- modbus_panel/_builder.py
- ShiftWheel
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
- visuals/__init__.py
- PopupWindow
- RecordFilter
- Kalman
- IP Forwarding
- Map
- version.py
- .arrow
- NoteBrowser
- Install NMap
- dumps
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .build_menu_bar_section
- .save_current_page
- .prepare_page_config
- .__init__
- ListZone
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
- No Network Connection
- QRect
- SelectRegisterPreset
- EditBackgroundChoices
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
- PreferencesData
- BaseForm
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
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `status()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Prod/Host_API.py → game/src/network/hardware/ap_commands.py
- `receive_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py
- `api_data()` --indirect_call--> `encryption_key()`  [INFERRED]
  firmware/REST_API/Dev/Host_API.py → game/src/network/hardware/ap_commands.py

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

## Communities (240 total, 147 thin omitted)

### Community 0 - "app_core/__init__.py"
Cohesion: 0.09
Nodes (7): Canvas, padded_fit_uniform_reverse(), zoom_and_pan_reverse(), DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 2 - "ImportantButton"
Cohesion: 0.04
Nodes (23): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearPacketConsole, EditModbusRegisterDisplay, FilterPacketConsole (+15 more)

### Community 3 - "MetaPacket"
Cohesion: 0.05
Nodes (7): Channel, _is_global(), NetworkGraph, Transaction, MetaPacket, _resolve_local_mac(), NetFilterQueueBaseClass

### Community 4 - "important_buttons/__init__.py"
Cohesion: 0.06
Nodes (11): ClearNetworkHosts, ClearSavedWorkspaceInputs, OpenThemeEditor, OpenWorkspaceSelect, RefreshCurrentPage, ResetSavedWorkspaceLayout, SaveToastPositionAsDefault, EditWorkspaceAvailability (+3 more)

### Community 5 - "SettingsSection"
Cohesion: 0.15
Nodes (3): save(), on_change(), SettingsSection

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 11 - "ContextManager"
Cohesion: 0.08
Nodes (10): ContextManager, BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page (+2 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "arp_poisoner.py"
Cohesion: 0.15
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 17 - "menu_bar.py"
Cohesion: 0.08
Nodes (7): developer_text(), ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (3): _default_gateway_ip(), PacketBuffer, TransactionManager

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (5): checked_value(), is_checked(), SettingsSection, save(), save()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.11
Nodes (6): RowZone, ChooseShownPacketConsoleColumns, column_category(), PacketColumnsModal, autosave(), on_change()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "workspace_sorter.py"
Cohesion: 0.09
Nodes (12): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+4 more)

### Community 33 - "server.py"
Cohesion: 0.10
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "window_chrome.py"
Cohesion: 0.09
Nodes (9): bar_button_height(), draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_height(), window_bar_room(), WindowBarButton (+1 more)

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

### Community 48 - ".__init__"
Cohesion: 0.06
Nodes (3): LinkToPage, OpenFavoritePage, icon_button()

### Community 53 - "filter_overlay.py"
Cohesion: 0.13
Nodes (12): conjugate(), empty_state(), Field, join_pair(), normal_value(), quote(), split_outside_quotes(), split_pair() (+4 more)

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

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 80 - "ModbusBuffer"
Cohesion: 0.06
Nodes (4): DefenderMapBuffer, HouseBuffer, ModbusBuffer, MapBuffer

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 86 - "VisualPalette"
Cohesion: 0.07
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 87 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (9): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+1 more)

### Community 88 - "Report"
Cohesion: 0.07
Nodes (5): Report, NMapper, InterfaceManager, job(), _BufferShim

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 96 - "Camera"
Cohesion: 0.13
Nodes (3): Camera, padded_fit_uniform(), zoom_and_pan()

### Community 97 - "message"
Cohesion: 0.08
Nodes (8): column_position(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "SectionCard"
Cohesion: 0.14
Nodes (3): CategoryChip, checkbox(), SectionCard

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 104 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 105 - "paint_panel"
Cohesion: 0.09
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 112 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 113 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (17): ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), set_ap_tunnel(), set_hvac_kalman(), set_kalman() (+9 more)

### Community 117 - "os"
Cohesion: 0.08
Nodes (3): flush(), flush_all(), run()

### Community 122 - "FilterError"
Cohesion: 0.25
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 125 - "sys"
Cohesion: 0.23
Nodes (3): build_name(), main(), write_build_info()

### Community 129 - "geometry.py"
Cohesion: 0.14
Nodes (6): canvas_fit(), padded_fit(), affine(), apply_scale_about(), scale(), translate()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.20
Nodes (4): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick()

### Community 133 - "kind_color"
Cohesion: 0.19
Nodes (5): _escape(), kind_color(), clicked(), sheet(), open_notice()

### Community 136 - "Scrollable"
Cohesion: 0.06
Nodes (6): _Gaps, Scrollable, Builder, Builder, Builder, Builder

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 142 - "NetFilterQueue"
Cohesion: 0.06
Nodes (3): NetFilterQueue, NetFilterQueue, Loader

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 149 - "confirm_dialog"
Cohesion: 0.08
Nodes (7): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (10): NetworkDiagramCanvas, StripChart, TextArea, panel(), Builder, Builder, Builder, _DrawerLayout (+2 more)

### Community 151 - "modbus_panel/_builder.py"
Cohesion: 0.29
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 156 - "ToastCard"
Cohesion: 0.12
Nodes (3): NoticeContent, _Swallowed, ToastCard

### Community 158 - "record_schema.py"
Cohesion: 0.16
Nodes (8): link_of(), action(), mark(), packet(), packet_from_meta(), poll(), raw_bytes(), status()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 161 - "Overlay"
Cohesion: 0.08
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 165 - "visuals/__init__.py"
Cohesion: 0.07
Nodes (14): draw_vessel(), gradient_points(), random_spline_path(), get_arc_points(), get_bearing(), rotate(), nice_number(), nice_ticks() (+6 more)

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
Cohesion: 0.25
Nodes (3): decode(), dumps(), header()

### Community 179 - "NMap Scan Failed"
Cohesion: 0.50
Nodes (3): Common causes, NMap Scan Failed, Then

### Community 180 - "Wi-Fi Control Unavailable"
Cohesion: 0.50
Nodes (3): Linux, Wi-Fi Control Unavailable, Windows

### Community 186 - ".__init__"
Cohesion: 0.32
Nodes (4): encryption_enabled(), set_encryption(), start_encryption(), stop_encryption()

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 214 - "ButtonModal"
Cohesion: 0.17
Nodes (4): EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 223 - "threading"
Cohesion: 0.05
Nodes (8): Buffer, StatusBuffer, Notice, ProcessManager, Process, FileStream, RetentionPolicy, read()

### Community 226 - "BaseForm"
Cohesion: 0.12
Nodes (13): BaseForm, ModeForm, HVACSlidersForm, SubmarineSlidersForm, APConnectForm, APTunnelForm, ArpForm, DosForm (+5 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (7): PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **147 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `app_core/__init__.py`, `edit_network_hosts.py`, `ImportantButton`, `SmoothWheel`, `MetaPacket`, `packet_console/_builder.py`, `important_buttons/__init__.py`, `Scrollable`, `AnimationManager`, `menu_bar.py`, `confirm_dialog`, `widgets/__init__.py`, `modbus_panel/_builder.py`, `ShiftWheel`, `.start_session`, `workspace_sorter.py`, `window_chrome.py`, `Style`, `visuals/__init__.py`, `docking.py`, `LocalizationManager`, `.__init__`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `host.py`, `InputManager`, `ConfigureThisWorkspace`, `PageManager`, `PrivilegedHelper`, `.reset_page`, `threading`, `Toasts`, `message`, `BaseForm`, `CheckboxOverlay`, `.apply_theme`, `Json`, `ap_commands.py`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `app_core/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08974358974358974 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `Overlay`, `.brush`, `._build_stylesheet`, `ImportantButton`, `SettingsSection`, `.apply_theme`, `.theme_family`, `ContextManager`, `.__init__`, `menu_bar.py`, `_DressedWidgets`, `.start_session`, `.preset_name`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `ImportantButton` be split into smaller, more focused modules?**
  _Cohesion score 0.036662106703146374 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `app_core/__init__.py`, `workspace_sorter.py`, `Overlay`, `window_chrome.py`, `ConfigEditor`, `.__init__`, `.bar_height`, `WindowEdges`, `ContextManager`, `bare_icon`, `QWidget`, `menu_bar.py`, `.__init__`, `StatusBell`, `widgets/__init__.py`, `CornerControls`, `WorkspaceSorter`, `PauseMenu`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._