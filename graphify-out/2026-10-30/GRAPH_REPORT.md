# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 342 files · ~285,444 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 5087 nodes · 10771 edges · 253 communities (88 shown, 165 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eeef27f4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- edit_network_hosts.py
- important_buttons/__init__.py
- MetaPacket
- RefreshCurrentPage
- .integer
- Wifi
- SettingsPage
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
- ConfigEditor
- docking.py
- LocalizationManager
- Style
- .collapsed
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
- Router
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- _base_button.py
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
- Map
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
- SectionCard
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
- Prod/Host_API.py
- .__init__
- Paths
- ArpSpoofer
- ap_commands.py
- os
- TabStrip
- CornerControls
- StripChartBase
- APPoller
- FilterError
- QWidget
- .restyle
- json
- PopupEntrance
- _Proxy
- is_column_available
- geometry.py
- .strip_chart_layout
- SmoothWheel
- kind_color
- Builder
- .build_tabs
- .__init__
- AnimationManager
- Scanlines
- .new_tab
- Meter
- MitmTable
- NetFilterQueue
- .add_setting_row
- place
- StatusBell
- Denier
- quit_application.py
- widgets/__init__.py
- MapBuffer
- ShiftWheel
- WindowDrag
- MetaStatus
- ToastCard
- Builder
- MaterialEditor
- ._scan_for_networks
- MainWindow
- SelectBackground
- Master
- Slave
- ChoiceList
- Visual
- MaterialEditorPopup
- Kalman
- IP Forwarding
- PopupWindow
- version.py
- LookOnly
- .arrow
- NoteBrowser
- Install NMap
- leaf_of
- NMap Scan Failed
- Wi-Fi Control Unavailable
- .build_menu_bar_section
- .save_current_page
- .prepare_page_config
- GrowingButton
- Scrim
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
- FileStream
- No Network Connection
- _Chip
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
- time
- defender_flag_panel/_builder.py
- ProcessManager
- ContextManager
- CheckboxOverlay
- Telemetry
- window_bar_height
- _Drawer
- Cyber-ICS Training Module
- _Swallowed
- _DropPreview
- open_favorite_page.py
- ModalWindow
- SettingsSection
- LinkToPage
- config_editor.py

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
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/hvac_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/modbus.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/network_graph.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/packet.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/submarine_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/saved/__init__.py -> game/src/network/saved/file_stream.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`

## Communities (253 total, 165 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.10
Nodes (6): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, WorldMap, Builder

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (22): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, EditModbusRegisterDisplay, FilterPacketConsole (+14 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 4 - "RefreshCurrentPage"
Cohesion: 0.12
Nodes (6): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, EditWorkspaceAvailability, RefreshAndCloseOverlay, WorkspaceSaveResetButton

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 11 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (4): PreferencesData, follow_theme(), MarkdownModal, background_choices()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 14 - "Panes"
Cohesion: 0.11
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 17 - "menu_bar.py"
Cohesion: 0.08
Nodes (7): developer_text(), ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+5 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.08
Nodes (5): WorkspaceSorter, delete(), create(), rename(), DropZone

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "workspace_sorter.py"
Cohesion: 0.09
Nodes (12): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+4 more)

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "window_chrome.py"
Cohesion: 0.15
Nodes (4): minimized_thickness(), bar_button_height(), WindowBarButton, WindowControls

### Community 38 - "ConfigEditor"
Cohesion: 0.11
Nodes (4): ConfigEditor, walk(), remove_nested(), set_nested()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), move_panel(), new_id() (+8 more)

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
Cohesion: 0.10
Nodes (3): _LentPlaceholder, _SideStrip, TabbedPane

### Community 50 - "CombinedTable"
Cohesion: 0.09
Nodes (5): CombinedTable, entry(), align_decimals(), format_number(), fraction_width()

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
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 68 - "_base_button.py"
Cohesion: 0.09
Nodes (7): open_in_browser(), DeleteAllUserData, ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 80 - "ModbusBuffer"
Cohesion: 0.08
Nodes (3): HouseBuffer, ModbusBuffer, Loader

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
Cohesion: 0.07
Nodes (5): Report, NMapper, InterfaceManager, job(), _BufferShim

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 97 - "confirm_dialog"
Cohesion: 0.06
Nodes (10): make(), DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage (+2 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "SectionCard"
Cohesion: 0.13
Nodes (3): CategoryChip, checkbox(), SectionCard

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 104 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 105 - "paint_panel"
Cohesion: 0.11
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

### Community 114 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (19): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+11 more)

### Community 117 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

### Community 118 - "TabStrip"
Cohesion: 0.08
Nodes (5): bar_inset(), paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 122 - "FilterError"
Cohesion: 0.25
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 123 - "QWidget"
Cohesion: 0.13
Nodes (4): HideEffect, Layer, PageTransition, TransitionOverlay

### Community 124 - ".restyle"
Cohesion: 0.09
Nodes (3): _ComboLists, _StyledComboItems, StyleSignals

### Community 125 - "json"
Cohesion: 0.22
Nodes (3): build_name(), main(), write_build_info()

### Community 128 - "is_column_available"
Cohesion: 0.27
Nodes (4): column_position(), is_column_available(), shown_columns(), tray_columns()

### Community 129 - "geometry.py"
Cohesion: 0.12
Nodes (7): apply_scale_about(), scale(), translate(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 133 - "kind_color"
Cohesion: 0.18
Nodes (6): status(), _escape(), kind_color(), clicked(), sheet(), open_notice()

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 142 - "NetFilterQueue"
Cohesion: 0.09
Nodes (3): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue

### Community 146 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.03
Nodes (12): StripChart, Scrollable, TextArea, panel(), Builder, Builder, Builder, Builder (+4 more)

### Community 154 - "WindowDrag"
Cohesion: 0.17
Nodes (3): SquareButtons, toggle_maximized(), WindowDrag

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 165 - "Visual"
Cohesion: 0.07
Nodes (11): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through() (+3 more)

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

### Community 214 - "ButtonModal"
Cohesion: 0.19
Nodes (4): EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (7): ToggleButton, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 223 - "time"
Cohesion: 0.05
Nodes (7): random_spline_path(), Buffer, StatusBuffer, _resolve_local_mac(), Notice, Process, read()

### Community 224 - "defender_flag_panel/_builder.py"
Cohesion: 0.24
Nodes (5): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, SubmarineKalmanToggleForm

### Community 226 - "ContextManager"
Cohesion: 0.10
Nodes (14): ContextManager, form_order(), BaseForm, ModeForm, HVACSlidersForm, SubmarineSlidersForm, APTunnelForm, ArpForm (+6 more)

### Community 227 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 231 - "window_bar_height"
Cohesion: 0.14
Nodes (4): draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "config_editor.py"
Cohesion: 0.04
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), affine(), BoatMotion, Sprites, Triangle, TitlePage (+6 more)

## Knowledge Gaps
- **165 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `edit_network_hosts.py`, `SmoothWheel`, `RefreshCurrentPage`, `config_editor.py`, `AnimationManager`, `pyside6_qtcore`, `menu_bar.py`, `PacketBuffer`, `quit_application.py`, `widgets/__init__.py`, `ShiftWheel`, `workspace_sorter.py`, `window_chrome.py`, `Visual`, `docking.py`, `LocalizationManager`, `Style`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `host.py`, `_base_button.py`, `InputManager`, `style.py`, `ConfigureThisWorkspace`, `PageManager`, `PrivilegedHelper`, `.reset_page`, `Toasts`, `time`, `ProcessManager`, `confirm_dialog`, `CheckboxOverlay`, `defender_flag_panel/_builder.py`, `.start_session`, `Json`, `Paths`, `open_favorite_page.py`, `LinkToPage`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.setting`, `._build_stylesheet`, `.lift_button`, `_base_button.py`, `.start_session`, `style.py`, `pyside6_qtcore`, `.theme_family`, `menu_bar.py`, `open_favorite_page.py`, `_DressedWidgets`, `SettingsSection`, `Overlay`, `.restyle`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.041176470588235294 - nodes in this community are weakly interconnected._
- **Why does `MenuBar` connect `MenuBar` to `workspace_sorter.py`, `window_chrome.py`, `config_editor.py`, `ConfigEditor`, `SettingsPage`, `window_bar_height`, `pyside6_qtcore`, `menu_bar.py`, `.__init__`, `StatusBell`, `CornerControls`, `TabStrip`, `.show_body`, `WorkspaceSorter`, `widgets/__init__.py`, `WindowDrag`, `Overlay`, `PauseMenu`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._