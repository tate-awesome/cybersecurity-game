# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 320 files · ~268,549 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4760 nodes · 9834 edges · 250 communities (69 shown, 181 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 471 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f4b555b7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- window_chrome.py
- important_buttons/__init__.py
- MetaPacket
- QWidget
- threading
- _in_nm_context
- pyside6_qtcore
- describe.py
- Overlay
- VisualPalette
- Footer
- _SaveLayoutAsDefault
- menu_bar.py
- ap_commands.py
- FilterOverlay
- ElidingLabel
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- DockArea
- SettingsSection
- time
- ThemeEditorPage
- PacketColumnsOverlay
- AttackHMI_relay_ramp_attack.py
- FindBar
- MapBuffer
- server.py
- Style
- ._build_stylesheet
- CheckboxOverlay
- ConfigEditor
- docking.py
- LocalizationManager
- _DrawerLayout
- WifiForm
- .start_session
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- Kernel
- Preferences
- config_editor.py
- edit_workspace_availability.py
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
- Router
- FadeIn
- buffer_manager.py
- .add_setting_row
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
- App
- PageManager
- .brush
- packet_filter.py
- launch.py
- DragHandle
- Map
- typing
- PrivilegedHelper
- SettingsPage
- frame_callback
- Draw
- .__init__
- overlay.py
- PauseMenu
- .fill_base
- WaveGrid
- NewWorkspaceDialog
- Camera
- .__init__
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- walk
- _Peek
- DropZone
- VariableOverlay
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- transformations.py
- ProcessManager
- ArpSpoofer
- WorkspaceChip
- SummaryDrawer
- WorkspaceSelectPage
- StripChartBase
- WindowBarButton
- HouseBuffer
- PageTransition
- _Indicator
- PopupEntrance
- _Proxy
- .new_tab
- QWidget
- time_core/transforms.py
- paint_panel
- MenuBar
- Builder
- MainWindow
- QWidget
- CallbackRegistry
- align_decimals
- Wifi
- Meter
- CornerControls
- Denier
- StripChartLayout
- GrowingButton
- MitmTable
- Attack
- ToggleLightDarkMode
- .connect_to_saved_wifi
- AnimationManager
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
- SectionCard
- SelectRegisterPreset
- .columnconfigure
- SampleNetwork
- Proximity
- NativeFrame
- .material_control
- .__init__
- AppearEffect
- Builder
- NoteBrowser
- _Chip
- select_background.py
- .add_deadspace
- .save_current_page
- Table
- offered_sections
- KalmanToggleForm
- PopupWindow
- _DropPreview
- .authored_weights
- .page_panel_keys
- .build_description_tab
- DragPayload
- .__init__
- PooledCanvasMixin
- .__init__
- _OnHide
- DenseMesh
- OpenFavoritePage
- StreamIncomingPacketsToMcap
- WorkspaceButton
- SettingsSection
- LinkToPage
- ModeForm
- Builder
- .__init__
- FreeScrollStatusConsole
- PausePacketConsole
- ToggleNetworkGraphRingView
- ToggleStripChartAutoFit
- panel
- Builder
- PreferencesData
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 146 edges
2. `ImportantButton` - 114 edges
3. `Style` - 101 edges
4. `Overlay` - 93 edges
5. `BaseForm` - 68 edges
6. `MenuBar` - 65 edges
7. `MetaPacket` - 63 edges
8. `ConfigEditor` - 58 edges
9. `DockArea` - 53 edges
10. `Panel` - 51 edges

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
- 4-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 4-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/transaction_manager.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/__init__.py -> game/src/app_core/app.py -> game/src/app_core/router.py -> game/src/pages/generic/__init__.py -> game/src/pages/generic/workspace.py -> game/src/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/hvac_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/modbus.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/network_graph.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/packet.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/buffer/channels/__init__.py -> game/src/network/buffer/channels/submarine_model.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`
- 5-file cycle: `game/src/network/buffer/__init__.py -> game/src/network/buffer/buffer_manager.py -> game/src/network/saved/__init__.py -> game/src/network/saved/file_stream.py -> game/src/network/buffer/meta_packet.py -> game/src/network/buffer/__init__.py`

## Communities (250 total, 181 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.06
Nodes (29): ContextManager, House, NetworkDiagramCanvas, StripChart, WorldMap, form_order(), Scrollable, BaseForm (+21 more)

### Community 1 - "window_chrome.py"
Cohesion: 0.09
Nodes (8): ask_to_quit(), draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), window_bar_height(), window_bar_room(), WindowDrag

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (47): AbortAllNetworkActions, ImportantButton, open_in_browser(), ToggleButton, ButtonGroup, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts (+39 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 4 - "QWidget"
Cohesion: 0.08
Nodes (9): PassWheel, SampleHouse, SampleHVAC, SampleNetworkDiagram, SamplePackets, SampleSubmarine, SampleWorldMap, StatusExample (+1 more)

### Community 5 - "threading"
Cohesion: 0.04
Nodes (7): flush(), flush_all(), run(), Buffer, NetFilterQueueBaseClass, Process, RetentionPolicy

### Community 7 - "pyside6_qtcore"
Cohesion: 0.04
Nodes (16): Paths, apply_scale_about(), scale(), translate(), conjugate(), quote(), BoatMotion, Sprites (+8 more)

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (8): draw_vessel(), get_arc_points(), get_bearing(), rotate(), draw_glow(), Visual, VisualPalette, Telemetry

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 14 - "menu_bar.py"
Cohesion: 0.07
Nodes (7): PeekArrow, ToggleBookmark, ToggleDebugLabels, ToggleFullscreen, ToggleWorkspaceBackground, bare_icon(), icon_button()

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (5): is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "time"
Cohesion: 0.14
Nodes (11): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+3 more)

### Community 29 - "PacketColumnsOverlay"
Cohesion: 0.10
Nodes (5): RowZone, column_category(), is_column_available(), PacketColumnsOverlay, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 37 - "CheckboxOverlay"
Cohesion: 0.07
Nodes (11): ListZone, PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns (+3 more)

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (14): add_tab(), drain_evenly(), find(), from_tree(), split(), leaf(), leaf_of(), move_panel() (+6 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 53 - "config_editor.py"
Cohesion: 0.06
Nodes (10): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+2 more)

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.08
Nodes (4): _LentPlaceholder, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): ShiftWheelSlider, HVACSlidersForm, SlidersForm, slider_callback(), SubmarineSlidersForm

### Community 71 - "FlowLayout"
Cohesion: 0.06
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

### Community 84 - "typing"
Cohesion: 0.09
Nodes (4): DefenderMapBuffer, ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - ".__init__"
Cohesion: 0.13
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "overlay.py"
Cohesion: 0.10
Nodes (6): SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton

### Community 93 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 97 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Replay"
Cohesion: 0.08
Nodes (3): _dialog_parent(), file_dialog(), Replay

### Community 103 - "Canvas"
Cohesion: 0.11
Nodes (3): Canvas, DefenderWorldMap, TriangleCanvas

### Community 104 - "walk"
Cohesion: 0.13
Nodes (5): visit(), is_split(), tidy(), panel_ids(), walk()

### Community 107 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 116 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 121 - "WindowBarButton"
Cohesion: 0.12
Nodes (4): minimized_thickness(), bar_button_height(), WindowBarButton, WindowControls

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "paint_panel"
Cohesion: 0.11
Nodes (4): bar_inset(), paint_mark(), paint_panel(), surface_shadow()

### Community 136 - "QWidget"
Cohesion: 0.24
Nodes (4): covered(), settle(), uncovered(), WindowReveal

### Community 137 - "CallbackRegistry"
Cohesion: 0.09
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "align_decimals"
Cohesion: 0.31
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

### Community 161 - "FlagsForm"
Cohesion: 0.24
Nodes (3): FlagsForm, HVACFlagsForm, SubmarineFlagsForm

### Community 187 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1940 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **181 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `window_chrome.py`, `important_buttons/__init__.py`, `threading`, `pyside6_qtcore`, `CallbackRegistry`, `VisualPalette`, `menu_bar.py`, `.reload_preferences`, `AnimationManager`, `ShiftWheel`, `Style`, `CheckboxOverlay`, `docking.py`, `LocalizationManager`, `.start_session`, `Preferences`, `config_editor.py`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `typing`, `.reset_page`, `overlay.py`, `.__init__`, `Json`, `ProcessManager`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.060263653483992465 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `important_buttons/__init__.py`, `._build_stylesheet`, `pyside6_qtcore`, `.__init__`, `.make_built_in`, `Overlay`, `.start_session`, `menu_bar.py`, `.brush`, `QWidget`, `.load_imported_themes`, `SettingsSection`, `overlay.py`, `.theme_family`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `window_chrome.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08739495798319327 - nodes in this community are weakly interconnected._