# Graph Report - cybersecurity-game  (2026-10-28)

## Corpus Check
- 323 files · ~275,703 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4861 nodes · 10362 edges · 218 communities (82 shown, 136 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 478 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f99295b1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pyside6_qtcore
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- Style
- Wifi
- SummaryDrawer
- describe.py
- message
- paint_mark
- Visual
- Footer
- FilterModal
- menu_bar.py
- Dev/Host_API.py
- time
- MenuBar
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- .target_at
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- .theme_family
- ._build_stylesheet
- _base_button.py
- ConfigEditor
- docking.py
- LocalizationManager
- widgets/__init__.py
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- Scrollable
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- QWidget
- Modify
- KeyBinds
- WrapLayout
- Router
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- SlidersForm
- InputManager
- FlowLayout
- CycleBox
- themes.py
- Camera
- Panes
- Constellation
- App
- PageManager
- .brush
- FilterError
- launch.py
- DragHandle
- Map
- Draw
- PrivilegedHelper
- SettingsPage
- bare_icon
- .start_session
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- config_editor.py
- Camera
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- DockArea
- RowZone
- VariableModal
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- .__init__
- .__init__
- ArpSpoofer
- ap_commands.py
- Process
- ToggleButton
- Prod/Host_API.py
- StripChartBase
- ModeForm
- QWidget
- packet_filter.py
- PopupEntrance
- host.py
- .add_setting_row
- ConfigureThisWorkspace
- .strip_chart_layout
- LinkToPage
- align_decimals
- blurred_shape
- Builder
- .refresh_usage
- .add_deadspace
- AnimationManager
- .columnconfigure
- Meter
- MitmTable
- Denier
- ModbusBuffer
- .__init__
- GrowingButton
- Table
- quit_application.py
- Attack
- .__init__
- ShiftWheel
- .collect
- GoForwardToNextPage
- .build_description_tab
- Builder
- Kalman
- ._scan_for_networks
- WorkspaceSelectPage
- Master
- Slave
- ChoiceList
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- MainWindow
- edit_network_hosts.py
- AppearEffect
- NoteBrowser
- _Chip
- .key_column_width
- Loader
- NewWorkspaceDialog
- .__init__
- .save_current_page
- ListZone
- DropZone
- .new_tab
- .authored_weights
- .page_panel_keys
- core/transforms.py
- .__init__
- PooledCanvasMixin
- frame_callback
- .setText
- paint_panel
- BuildInfo
- DragPayload
- confirm_dialog
- ProcessManager
- fade_in
- os
- WorkspaceButton
- PreferencesData
- ContextManager
- NotFound
- Telemetry
- Cyber-ICS Training Module
- Page

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 146 edges
2. `Style` - 123 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 60 edges
9. `DockArea` - 53 edges
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
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/packet_console/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/status_console/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
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

## Communities (218 total, 136 thin omitted)

### Community 0 - "pyside6_qtcore"
Cohesion: 0.09
Nodes (6): apply_scale_about(), conjugate(), quote(), BoatMotion, Sprites, MaterialEditor

### Community 1 - "CheckboxOverlay"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (22): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay (+14 more)

### Community 3 - "MetaPacket"
Cohesion: 0.08
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 9 - "message"
Cohesion: 0.08
Nodes (8): make(), column_position(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, message()

### Community 10 - "paint_mark"
Cohesion: 0.12
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow

### Community 11 - "Visual"
Cohesion: 0.09
Nodes (7): draw_vessel(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), value_noise(), Visual

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.10
Nodes (4): read(), FilterModal, label_key(), value_key()

### Community 14 - "menu_bar.py"
Cohesion: 0.05
Nodes (16): ButtonGroup, offered_sections(), ShowHelpMessage, global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons (+8 more)

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 17 - "MenuBar"
Cohesion: 0.05
Nodes (5): random_spline_path(), Triangle, TriangleCanvas, developer_text(), MenuBar

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (13): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+5 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.12
Nodes (4): column_category(), is_column_available(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "_base_button.py"
Cohesion: 0.11
Nodes (6): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 39 - "docking.py"
Cohesion: 0.12
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 42 - "widgets/__init__.py"
Cohesion: 0.07
Nodes (9): StripChart, shown_columns(), TextArea, panel(), Builder, Builder, Panel, Builder (+1 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.07
Nodes (5): APPoller, NetFilterQueue, NMapper, InterfaceManager, job()

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
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 59 - "QWidget"
Cohesion: 0.12
Nodes (3): _LentPlaceholder, _SideStrip, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.10
Nodes (7): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, HVACSlidersForm, SlidersForm, slider_callback(), SubmarineSlidersForm

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "FilterError"
Cohesion: 0.26
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 81 - "launch.py"
Cohesion: 0.11
Nodes (11): build_name(), main(), write_build_info(), git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux() (+3 more)

### Community 86 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.05
Nodes (12): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+4 more)

### Community 95 - "config_editor.py"
Cohesion: 0.20
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.14
Nodes (3): Canvas, DefenderWorldMap, WorldMap

### Community 107 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 108 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.10
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 117 - "Process"
Cohesion: 0.07
Nodes (6): Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process, FileStream, NetworkDiagramCanvas

### Community 118 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 125 - "packet_filter.py"
Cohesion: 0.21
Nodes (7): empty_state(), Field, join_pair(), normal_value(), split_outside_quotes(), to_state(), unquote()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "align_decimals"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 137 - "AnimationManager"
Cohesion: 0.05
Nodes (5): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter, SmoothWheel

### Community 143 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 155 - "GoForwardToNextPage"
Cohesion: 0.12
Nodes (3): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 168 - "PopupWindow"
Cohesion: 0.08
Nodes (3): ModalWindow, PopupWindow, Scrim

### Community 169 - "VisualPalette"
Cohesion: 0.07
Nodes (3): draw_glow(), VisualPalette, Kernel

### Community 170 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 181 - ".__init__"
Cohesion: 0.08
Nodes (3): ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 198 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 199 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 212 - "confirm_dialog"
Cohesion: 0.07
Nodes (8): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton, confirm_dialog()

### Community 216 - "os"
Cohesion: 0.08
Nodes (3): flush(), flush_all(), run()

### Community 226 - "ContextManager"
Cohesion: 0.09
Nodes (18): ContextManager, House, form_order(), BaseForm, FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm (+10 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 261 - "Page"
Cohesion: 0.08
Nodes (5): TitlePage, WorkspacePage, Page, TitleFooter, TitleMenu

## Knowledge Gaps
- **136 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `pyside6_qtcore`, `CheckboxOverlay`, `ConfigureThisWorkspace`, `LinkToPage`, `Style`, `Page`, `AnimationManager`, `message`, `Visual`, `menu_bar.py`, `ModbusBuffer`, `time`, `MenuBar`, `quit_application.py`, `PacketBuffer`, `ShiftWheel`, `GoForwardToNextPage`, `_base_button.py`, `docking.py`, `LocalizationManager`, `widgets/__init__.py`, `edit_network_hosts.py`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `.setText`, `PageManager`, `confirm_dialog`, `PrivilegedHelper`, `ProcessManager`, `.start_session`, `Overlay`, `config_editor.py`, `Json`, `Process`, `host.py`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `pyside6_qtcore` be split into smaller, more focused modules?**
  _Cohesion score 0.088841882601798 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `pyside6_qtcore`, `ContextManager`, `.theme_family`, `._build_stylesheet`, `.theme_modes`, `_base_button.py`, `.setting`, `AnimationManager`, `.discard_changes`, `.setText`, `menu_bar.py`, `.brush`, `_DressedWidgets`, `.start_session`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.08888888888888889 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `pyside6_qtcore`, `.add_setting_row`, `ConfigureThisWorkspace`, `Page`, `.refresh_usage`, `MenuBar`, `WorkspaceSorter`, `.collect`, `.build_description_tab`, `FindBar`, `WorkspaceSelectPage`, `widgets/__init__.py`, `NoteBrowser`, `LayoutEditor`, `.key_column_width`, `.new_tab`, `Rows`, `.leaf`, `.section`, `config_editor.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._