# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~277,969 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4886 nodes · 10412 edges · 214 communities (79 shown, 135 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 479 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d8149126`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- router.py
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- GoForwardToNextPage
- Style
- Wifi
- SummaryDrawer
- describe.py
- RefreshCurrentPage
- pyside6_qtcore
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- ButtonModal
- MenuBar
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- map.py
- server.py
- ._build_stylesheet
- Kernel
- ConfigEditor
- docking.py
- LocalizationManager
- blurred_shape
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
- packet_filter.py
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- QWidget
- Modify
- KeyBinds
- SettingsPage
- Router
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- Draw
- SlidersForm
- InputManager
- FlowLayout
- CycleBox
- themes.py
- Camera
- .__init__
- Constellation
- App
- PageManager
- MapBuffer
- launch.py
- DragHandle
- Map
- VariableModal
- PrivilegedHelper
- ModbusBuffer
- .apply_theme
- Draw
- _Grip
- Overlay
- PauseMenu
- ElidingLabel
- WaveGrid
- NewWorkspaceDialog
- Camera
- VectorField
- palette_generator.py
- .__init__
- compile_filter
- Replay
- Canvas
- .field_options
- DockArea
- RowZone
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- GrowingButton
- file_dialog
- ArpSpoofer
- ap_commands.py
- time
- Prod/Host_API.py
- StripChartBase
- FlagsForm
- MaterialEditor
- QWidget
- Scanlines
- PopupEntrance
- host.py
- .add_setting_row
- .integer
- .strip_chart_layout
- style.py
- DragPayload
- _OnHide
- Builder
- .refresh_usage
- .columnconfigure
- AnimationManager
- ModalWindow
- Meter
- MitmTable
- Denier
- Scrim
- .play
- Table
- APPoller
- Attack
- widgets/__init__.py
- config_editor.py
- ShiftWheel
- .collect
- .new_tab
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- Master
- Slave
- ChoiceList
- Proximity
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- AppearEffect
- .arrow
- NoteBrowser
- .build_summary
- _Chip
- LookOnly
- .save_current_page
- .build_menu_bar_section
- ListZone
- menu_bar.py
- DropZone
- frame_callback
- .authored_weights
- .page_panel_keys
- PooledCanvasMixin
- frame_callback
- fade_in
- .setText
- paint_panel
- QRect
- SelectRegisterPreset
- SettingsSection
- os
- ModeForm
- ToggleButton
- ProcessManager
- ContextManager
- DenseMesh
- Telemetry
- Cyber-ICS Training Module
- confirm_dialog
- TitleMenu

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 147 edges
2. `Style` - 123 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 60 edges
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

## Communities (214 total, 135 thin omitted)

### Community 0 - "router.py"
Cohesion: 0.13
Nodes (9): BoatMotion, Sprites, Triangle, TitlePage, WorkspaceSelectPage, WorkspacePage, NotFound, Page (+1 more)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.07
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (32): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole (+24 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (3): Channel, Transaction, MetaPacket

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 9 - "RefreshCurrentPage"
Cohesion: 0.12
Nodes (6): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, EditWorkspaceAvailability, RefreshAndCloseOverlay, WorkspaceSaveResetButton

### Community 11 - "pyside6_qtcore"
Cohesion: 0.09
Nodes (4): draw_vessel(), draw_glow(), Visual, background_choices()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.11
Nodes (3): empty_state(), to_state(), FilterModal

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.14
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 17 - "MenuBar"
Cohesion: 0.05
Nodes (3): bare_icon(), icon_button(), MenuBar

### Community 20 - "PacketBuffer"
Cohesion: 0.08
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (8): Visuals, paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise(), VisualBackground

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

### Community 29 - "PacketColumnsModal"
Cohesion: 0.12
Nodes (4): column_category(), is_column_available(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "map.py"
Cohesion: 0.12
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (13): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), move_panel(), new_id() (+5 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "TabStrip"
Cohesion: 0.07
Nodes (5): _LentPlaceholder, paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 48 - "NMapper"
Cohesion: 0.05
Nodes (6): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue, NMapper, InterfaceManager, job()

### Community 53 - "packet_filter.py"
Cohesion: 0.15
Nodes (9): Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes(), tokenize() (+1 more)

### Community 54 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.10
Nodes (6): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), ViewPort, affine()

### Community 58 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "FlowLayout"
Cohesion: 0.05
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 87 - "ModbusBuffer"
Cohesion: 0.08
Nodes (3): DefenderMapBuffer, HouseBuffer, ModbusBuffer

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.07
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 96 - "Camera"
Cohesion: 0.12
Nodes (5): Camera, padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - ".__init__"
Cohesion: 0.07
Nodes (5): GoBackToPreviousPage, OpenPauseMenu, ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.09
Nodes (7): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, TriangleCanvas, WorldMap, Builder

### Community 105 - "DockArea"
Cohesion: 0.08
Nodes (7): DockArea, visit(), is_split(), leaf_of(), tidy(), panel_ids(), walk()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 116 - "ap_commands.py"
Cohesion: 0.09
Nodes (21): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+13 more)

### Community 117 - "time"
Cohesion: 0.05
Nodes (6): Buffer, TransactionManager, _resolve_local_mac(), Process, FileStream, RetentionPolicy

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "style.py"
Cohesion: 0.07
Nodes (5): Paths, PreferencesData, SmoothWheel, gradient_points(), random_spline_path()

### Community 136 - ".columnconfigure"
Cohesion: 0.10
Nodes (3): Builder, Builder, Builder

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 144 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 150 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (10): StripChart, Scrollable, TextArea, panel(), Builder, Builder, _DrawerLayout, Panel (+2 more)

### Community 151 - "config_editor.py"
Cohesion: 0.14
Nodes (11): conjugate(), quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder() (+3 more)

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 160 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 189 - "menu_bar.py"
Cohesion: 0.06
Nodes (15): ButtonGroup, offered_sections(), global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip (+7 more)

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 201 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 206 - "paint_panel"
Cohesion: 0.11
Nodes (4): bar_inset(), minimized_thickness(), _Peek, paint_panel()

### Community 216 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 226 - "ContextManager"
Cohesion: 0.08
Nodes (20): ContextManager, form_order(), shown_columns(), BaseForm, HVACFlagsForm, SubmarineFlagsForm, HVACSlidersForm, SubmarineSlidersForm (+12 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "confirm_dialog"
Cohesion: 0.04
Nodes (15): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, column_position(), tray_columns(), SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication (+7 more)

## Knowledge Gaps
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `router.py`, `CheckboxOverlay`, `important_buttons/__init__.py`, `style.py`, `GoForwardToNextPage`, `Style`, `AnimationManager`, `RefreshCurrentPage`, `pyside6_qtcore`, `widgets/__init__.py`, `config_editor.py`, `ShiftWheel`, `map.py`, `docking.py`, `LocalizationManager`, `Preferences`, `Performance`, `KeyBinds`, `menu_bar.py`, `Router`, `InputManager`, `.setText`, `PageManager`, `PrivilegedHelper`, `ProcessManager`, `Canvas`, `Json`, `confirm_dialog`, `time`, `host.py`?**
  _High betweenness centrality (0.258) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `router.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1265597147950089 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `._build_stylesheet`, `style.py`, `.brush`, `.lift_button`, `important_buttons/__init__.py`, `.discard_changes`, `.theme_family`, `pyside6_qtcore`, `.setText`, `_DressedWidgets`, `.apply_theme`, `SettingsSection`, `Overlay`, `menu_bar.py`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.07200929152148665 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `router.py`, `.add_setting_row`, `Rows`, `.leaf`, `important_buttons/__init__.py`, `.section`, `.new_tab`, `.refresh_usage`, `NoteBrowser`, `LayoutEditor`, `widgets/__init__.py`, `config_editor.py`, `WorkspaceSorter`, `.collect`, `.build_menu_bar_section`, `FindBar`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._