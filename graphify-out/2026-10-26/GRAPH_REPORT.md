# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 323 files · ~275,231 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4860 nodes · 10042 edges · 249 communities (65 shown, 184 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5146d67c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- ButtonModal
- important_buttons/__init__.py
- MetaPacket
- WrapLayout
- _in_nm_context
- WorkspaceSelectPage
- describe.py
- message
- paint_panel
- VisualPalette
- Footer
- FilterModal
- MenuBar
- ap_commands.py
- frame_callback
- TextArea
- Builder
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
- HouseBuffer
- Process
- _Peek
- ._build_stylesheet
- SmoothWheel
- ConfigEditor
- docking.py
- LocalizationManager
- _DrawerLayout
- WifiForm
- Kernel
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- _Gaps
- PacketTreeview
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
- .theme_family
- Router
- FadeOut
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
- Panes
- Constellation
- app.py
- PageManager
- .brush
- FilterError
- sys
- DragHandle
- Map
- .add_deadspace
- PrivilegedHelper
- SettingsPage
- Style
- Draw
- _Grip
- PauseMenu
- WaveGrid
- config_editor.py
- Camera
- WindowControls
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- MapBuffer
- DockArea
- DropZone
- VariableModal
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- geometry.py
- threading
- ArpSpoofer
- ListZone
- Buffer
- ToggleButton
- SummaryDrawer
- StripChartBase
- KalmanToggleForm
- ModeForm
- QWidget
- MaterialEditor
- PopupEntrance
- host.py
- .add_setting_row
- .new_tab
- time_core/transforms.py
- Table
- table.py
- Builder
- .refresh_usage
- ClickManager
- WindowDrag
- Wifi
- Meter
- MitmTable
- Denier
- scapy_all
- StripChartLayout
- GrowingButton
- Paths
- Attack
- ToggleLightDarkMode
- .connect_to_saved_wifi
- Builder
- ShiftWheel
- .collect
- .integer
- MaterialEditorPopup
- Builder
- Kalman
- ._scan_for_networks
- APPoller
- FlagsForm
- Master
- Slave
- ChoiceList
- file_dialog
- WorkspaceChip
- PopupWindow
- .color
- WindowEdges
- Overlay
- _OnHide
- AppearEffect
- NoteBrowser
- _Chip
- .build_menu_bar_section
- Loader
- NewWorkspaceDialog
- _RightZoneRoom
- .save_current_page
- NativeFrame
- .columnconfigure
- CallbackRegistry
- AnimationManager
- BinZone
- is_column_available
- .authored_weights
- .page_panel_keys
- MainWindow
- LookOnly
- .__init__
- PooledCanvasMixin
- WorldMap
- CornerControls
- background.py
- open_favorite_page.py
- blurred_shape
- draw_window_bar_line
- SettingsSection
- confirm_dialog
- BuildInfo
- packet_filter.py
- time
- APConnectForm
- EncryptionForm
- WorkspaceButton
- .__init__
- StreamIncomingPacketsToMcap
- DefenderWorldMap
- ElidingLabel
- PreferencesData
- BaseForm
- APTunnelForm
- Telemetry
- KalmanForm
- panel
- CLAUDE.md
- ModalWindow
- Scrim
- router.py

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 146 edges
2. `Style` - 122 edges
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

## Communities (249 total, 184 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.07
Nodes (19): ContextManager, House, StripChart, form_order(), Scrollable, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm (+11 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (44): AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms (+36 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 10 - "paint_panel"
Cohesion: 0.09
Nodes (5): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow, paint_panel()

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.09
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "MenuBar"
Cohesion: 0.03
Nodes (15): ButtonGroup, offered_sections(), GoForwardToNextPage, RefreshCurrentPage, ToggleBookmark, ShowHelpMessage, bare_icon(), _FollowResize (+7 more)

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (5): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer, NetworkDiagramCanvas

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.14
Nodes (4): DragPayload, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "Process"
Cohesion: 0.05
Nodes (13): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+5 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.10
Nodes (19): add_tab(), visit(), drain_evenly(), find(), from_tree(), split(), is_split(), leaf() (+11 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (4): _LentPlaceholder, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeOut"
Cohesion: 0.13
Nodes (5): DesktopFade, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 75 - "Panes"
Cohesion: 0.09
Nodes (3): _PaneContainer, Panes, Builder

### Community 77 - "app.py"
Cohesion: 0.15
Nodes (3): App, FadeIn, __getattr__()

### Community 80 - "FilterError"
Cohesion: 0.26
Nodes (4): FilterError, parse(), Parser, tokenize()

### Community 81 - "sys"
Cohesion: 0.10
Nodes (11): build_name(), main(), write_build_info(), git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux() (+3 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 95 - "config_editor.py"
Cohesion: 0.10
Nodes (10): quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+2 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 106 - "DropZone"
Cohesion: 0.09
Nodes (3): DropZone, _Indicator, RowZone

### Community 107 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "geometry.py"
Cohesion: 0.07
Nodes (15): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), get_arc_points(), get_bearing() (+7 more)

### Community 114 - "threading"
Cohesion: 0.10
Nodes (3): DefenderMapBuffer, ModbusBuffer, _resolve_local_mac()

### Community 117 - "Buffer"
Cohesion: 0.09
Nodes (6): flush(), flush_all(), run(), Buffer, FileStream, RetentionPolicy

### Community 118 - "ToggleButton"
Cohesion: 0.04
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 132 - "table.py"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 145 - "GrowingButton"
Cohesion: 0.09
Nodes (3): TitleFooter, GrowingButton, TitleMenu

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 150 - ".connect_to_saved_wifi"
Cohesion: 0.33
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 164 - "ChoiceList"
Cohesion: 0.11
Nodes (4): _ComboLists, _StyledComboItems, StyleSignals, ChoiceList

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 171 - "Overlay"
Cohesion: 0.06
Nodes (10): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset, SettingsOverlayButton (+2 more)

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 192 - "is_column_available"
Cohesion: 0.27
Nodes (4): column_position(), is_column_available(), shown_columns(), tray_columns()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - "WorldMap"
Cohesion: 0.25
Nodes (4): WorldMap, frame_callback(), sprite(), sprite_enabled()

### Community 204 - "background.py"
Cohesion: 0.13
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 212 - "confirm_dialog"
Cohesion: 0.06
Nodes (8): DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, confirm_dialog()

### Community 215 - "packet_filter.py"
Cohesion: 0.17
Nodes (8): conjugate(), empty_state(), Field, join_pair(), normal_value(), split_outside_quotes(), to_state(), unquote()

### Community 216 - "time"
Cohesion: 0.13
Nodes (10): action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+2 more)

### Community 261 - "router.py"
Cohesion: 0.07
Nodes (9): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page (+1 more)

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1988 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **184 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `.apply_theme`, `router.py`, `table.py`, `ClickManager`, `MenuBar`, `Paths`, `PacketBuffer`, `ShiftWheel`, `.start_session`, `Process`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `Overlay`, `.reload_preferences`, `Preferences`, `Performance`, `KeyBinds`, `AnimationManager`, `Router`, `InputManager`, `background.py`, `open_favorite_page.py`, `PageManager`, `confirm_dialog`, `.reset_page`, `Style`, `config_editor.py`, `Json`, `threading`, `Buffer`, `host.py`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.06675508399646331 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `important_buttons/__init__.py`, `._build_stylesheet`, `.apply_theme`, `.discard_changes`, `Overlay`, `open_favorite_page.py`, `MenuBar`, `.brush`, `.setting`, `_DressedWidgets`, `SettingsSection`, `.start_session`, `.theme_family`, `config_editor.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.02035421623050489 - nodes in this community are weakly interconnected._