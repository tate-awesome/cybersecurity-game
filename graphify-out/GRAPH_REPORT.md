# Graph Report - cybersecurity-game  (2026-10-30)

## Corpus Check
- 324 files · ~278,972 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4908 nodes · 10461 edges · 228 communities (85 shown, 143 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 481 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f54b8655`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Canvas
- .__init__
- important_buttons/__init__.py
- MetaPacket
- context_manager.py
- Style
- Wifi
- PanelButton
- describe.py
- RefreshCurrentPage
- DockArea
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- ButtonModal
- .__init__
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- _RightZoneRoom
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- config_editor.py
- server.py
- ._build_stylesheet
- menu_bar.py
- ConfigEditor
- docking.py
- LocalizationManager
- os
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- NetFilterQueue
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
- WrapLayout
- CycleBox
- themes.py
- Camera
- .__init__
- Constellation
- App
- PageManager
- FlowLayout
- MapBuffer
- sys
- CheckboxOverlay
- _MapCanvas
- VariableModal
- PrivilegedHelper
- Kernel
- ModbusBuffer
- NMapper
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- _Gaps
- Camera
- NetworkGraph
- VectorField
- palette_generator.py
- link.py
- compile_filter
- Replay
- .apply_theme
- Prod/Host_API.py
- walk
- DragPayload
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- defender_flag_panel/_builder.py
- _PollUnpacker
- FileStream
- ArpSpoofer
- ap_commands.py
- threading
- TabStrip
- StripChartBase
- Scanlines
- MaterialEditor
- QWidget
- .collect
- PopupEntrance
- _Proxy
- geometry.py
- core/transforms.py
- .strip_chart_layout
- SmoothWheel
- filter_overlay.py
- .columnconfigure
- Builder
- .build_tabs
- .add_deadspace
- AnimationManager
- ModalWindow
- Meter
- MitmTable
- Denier
- Scrim
- Proximity
- Table
- .__init__
- APPoller
- confirm_dialog
- widgets/__init__.py
- NewWorkspaceDialog
- ShiftWheel
- QWidget
- DefenderMapBuffer
- .build_advanced_tab
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- SelectBackground
- Master
- Slave
- ChoiceList
- pyside6_qtcore
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- Channel
- modbus_function
- HideEffect
- NoteBrowser
- .__init__
- LookOnly
- _Drawer
- .save_current_page
- DenseMesh
- _Indicator
- MenuBar
- Map
- frame_callback
- .authored_weights
- .page_panel_keys
- .__init__
- .build_description_tab
- .__init__
- PooledCanvasMixin
- fade_in
- tray_columns
- .__init__
- paint_panel
- QRect
- SelectRegisterPreset
- _BufferShim
- frame_callback
- EditBackgroundChoices
- arpy2a.py
- SummaryDrawer
- ToggleButton
- ContextManager
- Telemetry
- Cyber-ICS Training Module
- message
- GrowingButton

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 147 edges
2. `Style` - 123 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
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

## Communities (228 total, 143 thin omitted)

### Community 0 - "Canvas"
Cohesion: 0.07
Nodes (8): apply_scale_about(), Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, TriangleCanvas, WorldMap, Builder

### Community 1 - ".__init__"
Cohesion: 0.06
Nodes (4): OpenFavoritePage, ToggleDebugLabels, bare_icon(), icon_button()

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (29): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole (+21 more)

### Community 3 - "MetaPacket"
Cohesion: 0.09
Nodes (3): Transaction, TransactionManager, MetaPacket

### Community 4 - "context_manager.py"
Cohesion: 0.09
Nodes (3): PreferencesData, _is_global(), _resolve_local_mac()

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 7 - "PanelButton"
Cohesion: 0.09
Nodes (5): PanelButton, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 8 - "describe.py"
Cohesion: 0.10
Nodes (24): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+16 more)

### Community 9 - "RefreshCurrentPage"
Cohesion: 0.12
Nodes (6): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, EditWorkspaceAvailability, RefreshAndCloseOverlay, WorkspaceSaveResetButton

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (4): read(), FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.17
Nodes (4): EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 17 - ".__init__"
Cohesion: 0.07
Nodes (5): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ToggleBookmark, _FollowResize

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), value_noise(), VisualBackground

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (6): SectionCard, WorkspaceSorter, delete(), create(), rename(), ListZone

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (5): RowZone, column_category(), is_column_available(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "config_editor.py"
Cohesion: 0.08
Nodes (19): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+11 more)

### Community 33 - "server.py"
Cohesion: 0.10
Nodes (10): Sniffer, build_capability(), _Echo, _ContextStub, _dispatch(), run(), flusher(), run_from_argv() (+2 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "menu_bar.py"
Cohesion: 0.06
Nodes (15): ButtonGroup, offered_sections(), global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip (+7 more)

### Community 39 - "docking.py"
Cohesion: 0.16
Nodes (12): add_tab(), find(), from_tree(), split(), leaf(), move_panel(), new_id(), normalize() (+4 more)

### Community 42 - "os"
Cohesion: 0.14
Nodes (3): flush(), flush_all(), run()

### Community 43 - "WifiForm"
Cohesion: 0.08
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 48 - "NetFilterQueue"
Cohesion: 0.09
Nodes (3): NetFilterQueueBaseClass, NetFilterQueue, NetFilterQueue

### Community 50 - "CombinedTable"
Cohesion: 0.09
Nodes (5): CombinedTable, entry(), align_decimals(), format_number(), fraction_width()

### Community 53 - "packet_filter.py"
Cohesion: 0.14
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

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

### Community 62 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.14
Nodes (3): add(), click(), sync()

### Community 69 - "SlidersForm"
Cohesion: 0.10
Nodes (7): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, HVACSlidersForm, SlidersForm, slider_callback(), SubmarineSlidersForm

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 81 - "sys"
Cohesion: 0.07
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "NMapper"
Cohesion: 0.17
Nodes (3): NMapper, InterfaceManager, job()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 104 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 105 - "walk"
Cohesion: 0.11
Nodes (6): visit(), drain_evenly(), is_split(), tidy(), panel_ids(), walk()

### Community 106 - "DragPayload"
Cohesion: 0.08
Nodes (3): BinZone, DragPayload, DropZone

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 112 - "defender_flag_panel/_builder.py"
Cohesion: 0.22
Nodes (6): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 114 - "FileStream"
Cohesion: 0.12
Nodes (3): _dialog_parent(), file_dialog(), FileStream

### Community 116 - "ap_commands.py"
Cohesion: 0.11
Nodes (18): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+10 more)

### Community 117 - "threading"
Cohesion: 0.07
Nodes (4): Buffer, ProcessManager, Process, RetentionPolicy

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 128 - "geometry.py"
Cohesion: 0.11
Nodes (8): canvas_fit(), padded_fit(), affine(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 129 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "filter_overlay.py"
Cohesion: 0.24
Nodes (3): draw_vessel(), conjugate(), quote()

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 149 - "confirm_dialog"
Cohesion: 0.06
Nodes (8): make(), DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (13): StripChart, form_order(), ChooseShownModbusTableForms, Scrollable, TextArea, panel(), Builder, Builder (+5 more)

### Community 151 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 154 - "QWidget"
Cohesion: 0.11
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 160 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 165 - "pyside6_qtcore"
Cohesion: 0.08
Nodes (4): gradient_points(), random_spline_path(), Visual, background_choices()

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 172 - "modbus_function"
Cohesion: 0.50
Nodes (4): modbus_function(), modbus_info(), modbus_summary(), register_values()

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 202 - "tray_columns"
Cohesion: 0.33
Nodes (3): column_position(), shown_columns(), tray_columns()

### Community 206 - "paint_panel"
Cohesion: 0.10
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 208 - "QRect"
Cohesion: 0.08
Nodes (3): _Chip, _DropPreview, DropTarget

### Community 213 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "arpy2a.py"
Cohesion: 0.09
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 219 - "SummaryDrawer"
Cohesion: 0.07
Nodes (3): SummaryDrawer, WorkspaceButton, update()

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 226 - "ContextManager"
Cohesion: 0.11
Nodes (12): ContextManager, BaseForm, ModeForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm (+4 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "message"
Cohesion: 0.13
Nodes (5): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, message()

## Knowledge Gaps
- **143 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `Canvas`, `.__init__`, `important_buttons/__init__.py`, `SmoothWheel`, `context_manager.py`, `Style`, `filter_overlay.py`, `PanelButton`, `AnimationManager`, `RefreshCurrentPage`, `.__init__`, `confirm_dialog`, `widgets/__init__.py`, `ShiftWheel`, `config_editor.py`, `menu_bar.py`, `pyside6_qtcore`, `docking.py`, `LocalizationManager`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `sys`, `PrivilegedHelper`, `.reset_page`, `Json`, `message`, `defender_flag_panel/_builder.py`, `threading`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `Canvas` be split into smaller, more focused modules?**
  _Cohesion score 0.07307692307692308 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `.__init__`, `ContextManager`, `._build_stylesheet`, `context_manager.py`, `pyside6_qtcore`, `.brush`, `.apply_theme`, `.lift_button`, `.theme_family`, `important_buttons/__init__.py`, `menu_bar.py`, `.preset_name`, `_DressedWidgets`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.05609756097560976 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `config_editor.py`, `Rows`, `.leaf`, `.build_description_tab`, `.add_setting_row`, `important_buttons/__init__.py`, `.build_tabs`, `NoteBrowser`, `LayoutEditor`, `widgets/__init__.py`, `WorkspaceSorter`, `QWidget`, `.collect`, `FindBar`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._