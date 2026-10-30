# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~278,891 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4907 nodes · 10458 edges · 217 communities (74 shown, 143 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 481 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bebc4a80`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- .__init__
- important_buttons/__init__.py
- MetaPacket
- channels/__init__.py
- Style
- Wifi
- CheckboxOverlay
- describe.py
- RefreshCurrentPage
- .__init__
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- ButtonModal
- ToggleBookmark
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- .__init__
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- FindBar
- router.py
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
- WrapLayout
- CycleBox
- style.py
- Camera
- .__init__
- Constellation
- app.py
- PageManager
- FlowLayout
- MapBuffer
- host.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- Kernel
- ModbusBuffer
- NMapper
- Draw
- _Grip
- PauseMenu
- ElidingLabel
- WaveGrid
- .__init__
- Camera
- NetworkGraph
- VectorField
- palette_generator.py
- link.py
- compile_filter
- Replay
- Canvas
- .add_setting_row
- .collapsed
- DropZone
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- WindowEdges
- _PollUnpacker
- Paths
- ArpSpoofer
- ap_commands.py
- threading
- TabStrip
- .connect_to_saved_wifi
- StripChartBase
- Scanlines
- MaterialEditor
- QWidget
- .collect
- PopupEntrance
- _Proxy
- transformations.py
- SettingsSection
- .strip_chart_layout
- .__init__
- DragPayload
- ListZone
- Builder
- .refresh_usage
- .columnconfigure
- AnimationManager
- ModalWindow
- Meter
- MitmTable
- Denier
- Scrim
- CreateToolTip
- Table
- APPoller
- CreateToolTip
- ask_to_quit
- widgets/__init__.py
- config_editor.py
- ShiftWheel
- .new_tab
- DefenderMapBuffer
- ConfigureThisWorkspace
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- Overlay
- Master
- Slave
- ChoiceList
- Visual
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- VisualPalette
- Channel
- modbus_function
- HideEffect
- .arrow
- NoteBrowser
- ResetCurrentPageToDefaults
- _Chip
- LookOnly
- _Drawer
- _DropPreview
- .save_current_page
- DenseMesh
- _Indicator
- MenuBar
- Map
- frame_callback
- .authored_weights
- .page_panel_keys
- .build_menu_bar_section
- .__init__
- PooledCanvasMixin
- _DrawerLayout
- ModeForm
- paint_panel
- DockArea
- SelectRegisterPreset
- arpy2a.py
- WorkspaceSelectPage
- ToggleButton
- ProcessManager
- BaseForm
- Telemetry
- Cyber-ICS Training Module
- WorkspaceSaveResetButton
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

## Communities (217 total, 143 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.08
Nodes (10): ContextManager, PreferencesData, apply_scale_about(), scale(), translate(), _is_global(), DefenderWorldMap, follow_theme() (+2 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (35): make(), AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole (+27 more)

### Community 3 - "MetaPacket"
Cohesion: 0.10
Nodes (3): Transaction, TransactionManager, MetaPacket

### Community 6 - "Wifi"
Cohesion: 0.13
Nodes (3): _in_nm_context(), Wifi, cached()

### Community 7 - "CheckboxOverlay"
Cohesion: 0.08
Nodes (9): PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, HVACSlidersForm (+1 more)

### Community 8 - "describe.py"
Cohesion: 0.10
Nodes (24): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+16 more)

### Community 9 - "RefreshCurrentPage"
Cohesion: 0.24
Nodes (3): RefreshCurrentPage, EditWorkspaceAvailability, RefreshAndCloseOverlay

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.10
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (16): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+8 more)

### Community 16 - "ButtonModal"
Cohesion: 0.13
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 17 - "ToggleBookmark"
Cohesion: 0.09
Nodes (4): GoBackToPreviousPage, GoForwardToNextPage, SetCurrentPageAsFavorite, ToggleBookmark

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (12): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 25 - ".__init__"
Cohesion: 0.06
Nodes (7): OpenPauseMenu, ShowHelpMessage, bare_icon(), _FollowResize, global_buttons(), icon_button(), _RightZoneRoom

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.09
Nodes (9): RowZone, ChooseShownPacketConsoleColumns, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns() (+1 more)

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "router.py"
Cohesion: 0.11
Nodes (8): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "menu_bar.py"
Cohesion: 0.06
Nodes (14): ButtonGroup, offered_sections(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized() (+6 more)

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 42 - "os"
Cohesion: 0.09
Nodes (4): flush(), flush_all(), run(), RetentionPolicy

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.11
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.11
Nodes (3): DefenderHVACChart, HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.06
Nodes (8): bar_inset(), _LentPlaceholder, minimized_thickness(), paint_mark(), PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 53 - "filter_overlay.py"
Cohesion: 0.12
Nodes (14): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+6 more)

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
Cohesion: 0.06
Nodes (3): SettingsPage, DeleteAllUserData, DeleteAllWorkspaceSavedData

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.09
Nodes (14): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient() (+6 more)

### Community 81 - "host.py"
Cohesion: 0.08
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 88 - "NMapper"
Cohesion: 0.13
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.16
Nodes (8): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 114 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 116 - "ap_commands.py"
Cohesion: 0.10
Nodes (17): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), read_hvac_state() (+9 more)

### Community 117 - "threading"
Cohesion: 0.07
Nodes (4): Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 119 - ".connect_to_saved_wifi"
Cohesion: 0.23
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 128 - "transformations.py"
Cohesion: 0.14
Nodes (7): canvas_fit(), padded_fit(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 129 - "SettingsSection"
Cohesion: 0.15
Nodes (3): save(), on_change(), SettingsSection

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 136 - ".columnconfigure"
Cohesion: 0.10
Nodes (3): Builder, Builder, Builder

### Community 137 - "AnimationManager"
Cohesion: 0.08
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 150 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (13): NetworkDiagramCanvas, StripChart, Scrollable, TextArea, panel(), Builder, Builder, Builder (+5 more)

### Community 151 - "config_editor.py"
Cohesion: 0.09
Nodes (13): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), make_workspace(), NewWorkspaceDialog, relist_workspace(), rename_workspace(), RenameWorkspaceDialog (+5 more)

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 161 - "Overlay"
Cohesion: 0.08
Nodes (4): SelectBackground, SelectColorTheme, Overlay, background_choices()

### Community 165 - "Visual"
Cohesion: 0.06
Nodes (12): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through() (+4 more)

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

### Community 199 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 216 - "arpy2a.py"
Cohesion: 0.09
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 219 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 220 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView (+1 more)

### Community 226 - "BaseForm"
Cohesion: 0.05
Nodes (19): BaseForm, FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm, align_decimals() (+11 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "WorkspaceSaveResetButton"
Cohesion: 0.12
Nodes (3): ClearSavedWorkspaceInputs, SavePacketColumnsAsDefault, WorkspaceSaveResetButton

### Community 261 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **143 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `.__init__`, `important_buttons/__init__.py`, `.__init__`, `channels/__init__.py`, `Style`, `CheckboxOverlay`, `AnimationManager`, `ButtonModal`, `ToggleBookmark`, `widgets/__init__.py`, `config_editor.py`, `ShiftWheel`, `ConfigureThisWorkspace`, `PacketColumnsModal`, `router.py`, `menu_bar.py`, `Visual`, `docking.py`, `LocalizationManager`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `style.py`, `PageManager`, `host.py`, `PrivilegedHelper`, `ProcessManager`, `BaseForm`, `Canvas`, `Json`, `Paths`, `threading`?**
  _High betweenness centrality (0.231) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07591553060678963 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.__init__`, `.brush`, `.__init__`, `._build_stylesheet`, `.lift_button`, `important_buttons/__init__.py`, `menu_bar.py`, `Overlay`, `style.py`, `.discard_changes`, `.theme_family`, `ButtonModal`, `_DressedWidgets`, `SettingsSection`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.06156156156156156 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `router.py`, `Rows`, `.leaf`, `.build_menu_bar_section`, `.section`, `.refresh_usage`, `.add_setting_row`, `NoteBrowser`, `LayoutEditor`, `MenuBar`, `widgets/__init__.py`, `config_editor.py`, `WorkspaceSorter`, `.new_tab`, `WorkspaceSelectPage`, `ConfigureThisWorkspace`, `.collect`, `FindBar`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._