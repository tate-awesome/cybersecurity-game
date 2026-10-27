# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 322 files · ~269,740 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4783 nodes · 9903 edges · 240 communities (68 shown, 172 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 478 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dd2c700b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- WindowControls
- important_buttons/__init__.py
- MetaPacket
- _Gaps
- _in_nm_context
- WorkspaceSelectPage
- describe.py
- _SaveLayoutAsDefault
- paint_mark
- VisualPalette
- Footer
- geometry.py
- ap_commands.py
- FilterOverlay
- widgets/__init__.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- .target_at
- SettingsSection
- time
- ThemeEditorPage
- PacketColumnsOverlay
- AttackHMI_relay_ramp_attack.py
- FindBar
- ModbusBuffer
- server.py
- .restyle
- ._build_stylesheet
- SmoothWheel
- ImportantButton
- ConfigEditor
- docking.py
- LocalizationManager
- WifiForm
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- Kernel
- Preferences
- ListZone
- RefreshCurrentPage
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
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
- Panes
- Constellation
- App
- PageManager
- .css
- packet_filter.py
- launch.py
- DragHandle
- Map
- FileStream
- PrivilegedHelper
- SettingsPage
- frame_callback
- Draw
- _Grip
- Overlay
- PauseMenu
- ElidingLabel
- WaveGrid
- pyside6_qtcore
- Camera
- menu_bar.py
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- MapBuffer
- DockArea
- DropZone
- VariableOverlay
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- transformations.py
- threading
- ArpSpoofer
- WorkspaceChip
- ToggleButton
- SummaryDrawer
- StripChartBase
- .build_advanced_tab
- align_decimals
- QWidget
- MaterialEditor
- PopupEntrance
- host.py
- .add_setting_row
- .new_tab
- time_core/transforms.py
- paint_panel
- MenuBar
- Builder
- .build_tabs
- ClickManager
- CallbackRegistry
- WindowDrag
- Wifi
- Meter
- Denier
- sys
- StripChartLayout
- GrowingButton
- Style
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
- defender_flag_panel/_builder.py
- Master
- Slave
- fade_in
- BuildInfo
- SampleNetwork
- Proximity
- WindowEdges
- ConfigureThisWorkspace
- DragPayload
- AppearEffect
- NoteBrowser
- _Chip
- Process
- NewWorkspaceDialog
- ToggleBookmark
- .save_current_page
- Table
- CheckboxOverlay
- SectionCard
- popup.py
- .build_description_tab
- WorkspaceButton
- .authored_weights
- .page_panel_keys
- MainWindow
- .__init__
- PooledCanvasMixin
- .__init__
- CornerControls
- NativeFrame
- open_favorite_page.py
- surface_shadow
- Telemetry
- LinkToPage
- ModeForm
- SettingsSection
- draw_window_bar_line
- ProcessManager
- NetFilterQueueBaseClass
- _DrawerLayout
- EncryptionForm
- SampleSubmarine
- .__init__
- _GlobalClickFilter
- _Drawer
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 148 edges
2. `ImportantButton` - 114 edges
3. `Style` - 101 edges
4. `Overlay` - 93 edges
5. `BaseForm` - 68 edges
6. `MenuBar` - 65 edges
7. `MetaPacket` - 63 edges
8. `ConfigEditor` - 62 edges
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

## Communities (240 total, 172 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.07
Nodes (19): ContextManager, apply_scale_about(), shorten_line(), zoom_and_pan(), DefenderWorldMap, TriangleCanvas, PanelButton, ChooseShownModbusTableForms (+11 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (18): open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, EditModbusRegisterDisplay, ImportThemes, LoadLocalizationLabelsFile (+10 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 9 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 10 - "paint_mark"
Cohesion: 0.12
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (7): draw_vessel(), paint_noise_gradient(), value_noise(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterOverlay"
Cohesion: 0.07
Nodes (4): read(), FilterOverlay, label_key(), value_key()

### Community 17 - "widgets/__init__.py"
Cohesion: 0.03
Nodes (29): House, NetworkDiagramCanvas, StripChart, Scrollable, TextArea, panel(), Builder, HVACSlidersForm (+21 more)

### Community 18 - "PacketTreeview"
Cohesion: 0.08
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 23 - "SessionRecorder"
Cohesion: 0.07
Nodes (3): RecordFilter, RetentionPolicy, SessionRecorder

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "time"
Cohesion: 0.08
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

### Community 37 - "ImportantButton"
Cohesion: 0.05
Nodes (9): AbortAllNetworkActions, ImportantButton, ClearStatusConsole, EditNetworkHosts, FilterPacketConsole, LoadMcapIntoPacketBuffer, OpenTitlePage, StreamMcapIntoPacketBuffer (+1 more)

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

### Community 54 - "RefreshCurrentPage"
Cohesion: 0.15
Nodes (4): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (4): _LentPlaceholder, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 65 - "DefenderModbusBuffer"
Cohesion: 0.06
Nodes (3): DefenderMapBuffer, DefenderModbusBuffer, _PollUnpacker

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.15
Nodes (8): git(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "FileStream"
Cohesion: 0.12
Nodes (3): _dialog_parent(), file_dialog(), FileStream

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.04
Nodes (11): SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SelectRegisterPreset (+3 more)

### Community 95 - "pyside6_qtcore"
Cohesion: 0.07
Nodes (15): PreferencesData, conjugate(), quote(), delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace() (+7 more)

### Community 97 - "menu_bar.py"
Cohesion: 0.04
Nodes (13): ButtonGroup, offered_sections(), GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, ShowHelpMessage, bare_icon(), _FollowResize (+5 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 107 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 113 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 116 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 118 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 122 - "align_decimals"
Cohesion: 0.32
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "MenuBar"
Cohesion: 0.04
Nodes (11): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspacePage, NotFound, Page (+3 more)

### Community 138 - "WindowDrag"
Cohesion: 0.16
Nodes (3): SquareButtons, toggle_maximized(), WindowDrag

### Community 143 - "sys"
Cohesion: 0.27
Nodes (3): build_name(), main(), write_build_info()

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

### Community 161 - "defender_flag_panel/_builder.py"
Cohesion: 0.12
Nodes (6): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 179 - "Process"
Cohesion: 0.07
Nodes (6): flush(), flush_all(), run(), Buffer, Process, Loader

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.13
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 187 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 188 - "CheckboxOverlay"
Cohesion: 0.07
Nodes (6): CheckboxOverlay, form_order(), ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, Builder, Builder

### Community 190 - "popup.py"
Cohesion: 0.05
Nodes (10): DeleteAllWorkspaceSavedData, column_position(), tray_columns(), SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, confirm_dialog() (+2 more)

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1951 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **172 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `MenuBar`, `ClickManager`, `VisualPalette`, `widgets/__init__.py`, `Style`, `AnimationManager`, `ShiftWheel`, `defender_flag_panel/_builder.py`, `.restyle`, `SmoothWheel`, `ImportantButton`, `.apply`, `LocalizationManager`, `docking.py`, `ConfigureThisWorkspace`, `.start_session`, `Process`, `Preferences`, `.save_current_page`, `Performance`, `KeyBinds`, `popup.py`, `Router`, `InputManager`, `open_favorite_page.py`, `PageManager`, `LinkToPage`, `PrivilegedHelper`, `ProcessManager`, `Overlay`, `pyside6_qtcore`, `menu_bar.py`, `Json`, `threading`, `host.py`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.06606353881758889 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `menu_bar.py`, `.restyle`, `._build_stylesheet`, `.apply_theme`, `important_buttons/__init__.py`, `.discard_changes`, `.start_session`, `open_favorite_page.py`, `.css`, `SettingsSection`, `Overlay`, `.theme_family`, `pyside6_qtcore`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.044668008048289735 - nodes in this community are weakly interconnected._