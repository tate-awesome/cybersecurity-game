# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 317 files · ~266,903 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4725 nodes · 9752 edges · 244 communities (66 shown, 178 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 469 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9c3b4a4b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- MenuBar
- important_buttons/__init__.py
- MetaPacket
- examples.py
- threading
- Wifi
- router.py
- describe.py
- Overlay
- config_editor.py
- VisualPalette
- Footer
- popup.py
- ToggleButton
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
- ModbusBuffer
- server.py
- Style
- ._build_stylesheet
- widgets/__init__.py
- CheckboxOverlay
- ConfigEditor
- docking.py
- LocalizationManager
- _DrawerLayout
- WifiForm
- .restyle
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- Kernel
- Preferences
- _base_button.py
- RefreshCurrentPage
- HostOverlay
- Performance
- ViewPort
- Wifi
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
- .css
- FilterError
- launch.py
- DragHandle
- Map
- wifi_windows.py
- PrivilegedHelper
- SettingsPage
- frame_callback
- Draw
- .__init__
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
- MaterialEditorPopup
- .collapsed
- paint_panel
- ListZone
- VariableOverlay
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- transformations.py
- geometry.py
- ArpSpoofer
- WorkspaceChip
- DropZone
- SummaryDrawer
- WorkspaceSelectPage
- StripChartBase
- WrapLayout
- _SaveLayoutAsDefault
- QWidget
- filter_overlay.py
- PopupEntrance
- host.py
- .new_tab
- QWidget
- time_core/transforms.py
- paint_mark
- QWidget
- Builder
- WindowEdges
- sys
- CallbackRegistry
- Meter
- Denier
- .connect_to_saved_wifi
- StripChartLayout
- GrowingButton
- WindowDrag
- MitmTable
- Attack
- ToggleLightDarkMode
- MainWindow
- AnimationManager
- ShiftWheel
- .collect
- .integer
- leaf_of
- Builder
- Kalman
- NativeFrame
- APPoller
- Loader
- Master
- Slave
- SectionCard
- CornerControls
- Builder
- SampleNetwork
- Proximity
- ClickManager
- Paths
- file_dialog
- AppearEffect
- version.py
- NoteBrowser
- _Chip
- ToggleBookmark
- _RightZoneRoom
- Builder
- WindowControls
- .save_current_page
- Table
- quit_application.py
- _Gaps
- Builder
- Telemetry
- .authored_weights
- .page_panel_keys
- .build_description_tab
- fade_in
- .__init__
- PooledCanvasMixin
- .__init__
- _DropPreview
- DragPayload
- open_favorite_page.py
- StreamIncomingPacketsToMcap
- _OnHide
- WorkspaceButton
- SettingsSection
- ConfigureThisWorkspace
- GoForwardToNextPage
- LinkToPage
- ModeForm
- SampleSubmarine
- Builder
- _GlobalClickFilter
- .__init__
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 143 edges
2. `ImportantButton` - 114 edges
3. `Style` - 101 edges
4. `Overlay` - 93 edges
5. `MenuBar` - 65 edges
6. `BaseForm` - 64 edges
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

## Communities (244 total, 178 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.07
Nodes (18): ContextManager, shorten_line(), zoom_and_pan(), FilterPacketConsole, shown_columns(), BaseForm, align_decimals(), format_number() (+10 more)

### Community 1 - "MenuBar"
Cohesion: 0.04
Nodes (14): PeekArrow, ButtonGroup, offered_sections(), bare_icon(), _FollowResize, global_buttons(), icon_button(), MenuBar (+6 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.04
Nodes (22): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay (+14 more)

### Community 3 - "MetaPacket"
Cohesion: 0.05
Nodes (6): HouseBuffer, Channel, Transaction, TransactionManager, MetaPacket, _resolve_local_mac()

### Community 4 - "examples.py"
Cohesion: 0.04
Nodes (22): Canvas, DefenderWorldMap, House, NetworkDiagramCanvas, WorldMap, Scrollable, ChartsExample, ControlsExample (+14 more)

### Community 5 - "threading"
Cohesion: 0.05
Nodes (7): flush(), flush_all(), run(), Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 6 - "Wifi"
Cohesion: 0.05
Nodes (12): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached(), finish() (+4 more)

### Community 7 - "router.py"
Cohesion: 0.04
Nodes (11): BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page, TriangleCanvas (+3 more)

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 9 - "Overlay"
Cohesion: 0.05
Nodes (6): SelectBackground, SelectColorTheme, EditModelStyle, EditStripChartStyle, SelectRegisterPreset, Overlay

### Community 10 - "config_editor.py"
Cohesion: 0.09
Nodes (13): PreferencesData, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+5 more)

### Community 11 - "VisualPalette"
Cohesion: 0.08
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "popup.py"
Cohesion: 0.05
Nodes (10): DeleteAllUserData, DeleteAllWorkspaceSavedData, column_position(), tray_columns(), SavePacketColumnsAsDefault, ResetCurrentPageToDefaults, ShowHelpMessage, confirm_dialog() (+2 more)

### Community 14 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit, ToggleWorkspaceBackground

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

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

### Community 36 - "widgets/__init__.py"
Cohesion: 0.14
Nodes (6): StripChart, panel(), Builder, Builder, Panel, Builder

### Community 37 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (7): PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (14): add_tab(), find(), is_split(), leaf(), move_panel(), new_id(), normalize(), tidy() (+6 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "TabStrip"
Cohesion: 0.10
Nodes (3): _LentPlaceholder, _SideTitle, TabStrip

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 53 - "_base_button.py"
Cohesion: 0.11
Nodes (6): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor

### Community 54 - "RefreshCurrentPage"
Cohesion: 0.11
Nodes (6): ClearSavedWorkspaceInputs, RefreshCurrentPage, ResetSavedWorkspaceLayout, EditWorkspaceAvailability, RefreshAndCloseOverlay, WorkspaceSaveResetButton

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.16
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "FilterError"
Cohesion: 0.18
Nodes (7): Field, FilterError, normal_value(), parse(), Parser, split_outside_quotes(), tokenize()

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "wifi_windows.py"
Cohesion: 0.12
Nodes (16): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+8 more)

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - ".__init__"
Cohesion: 0.12
Nodes (5): from_tree(), split(), _Grip, _SashGrip, _ShadowWatch

### Community 93 - ".fill_base"
Cohesion: 0.14
Nodes (3): paint_noise_gradient(), pyramid_blur(), value_noise()

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 105 - "paint_panel"
Cohesion: 0.12
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 107 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 114 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 116 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 122 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 125 - "filter_overlay.py"
Cohesion: 0.24
Nodes (6): conjugate(), empty_state(), join_pair(), quote(), to_state(), unquote()

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "paint_mark"
Cohesion: 0.15
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 136 - "sys"
Cohesion: 0.26
Nodes (3): build_name(), main(), write_build_info()

### Community 143 - ".connect_to_saved_wifi"
Cohesion: 0.18
Nodes (4): finish(), on_notification(), on_notification(), WLAN_CONNECTION_PARAMETERS

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1925 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **178 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `MenuBar`, `important_buttons/__init__.py`, `MetaPacket`, `examples.py`, `threading`, `Wifi`, `router.py`, `config_editor.py`, `.start_session`, `.apply`, `popup.py`, `VisualPalette`, `PacketBuffer`, `AnimationManager`, `ShiftWheel`, `Style`, `widgets/__init__.py`, `CheckboxOverlay`, `docking.py`, `LocalizationManager`, `ClickManager`, `Paths`, `.restyle`, `Preferences`, `_base_button.py`, `RefreshCurrentPage`, `Performance`, `quit_application.py`, `KeyBinds`, `Router`, `InputManager`, `open_favorite_page.py`, `PageManager`, `ConfigureThisWorkspace`, `PrivilegedHelper`, `GoForwardToNextPage`, `LinkToPage`, `Json`, `filter_overlay.py`, `host.py`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.06575963718820861 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `MenuBar`, `._build_stylesheet`, `.discard_changes`, `config_editor.py`, `.start_session`, `.restyle`, `.apply_theme`, `open_favorite_page.py`, `.css`, `Overlay`, `_base_button.py`, `SettingsSection`, `.theme_family`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `MenuBar` be split into smaller, more focused modules?**
  _Cohesion score 0.036818851251840944 - nodes in this community are weakly interconnected._