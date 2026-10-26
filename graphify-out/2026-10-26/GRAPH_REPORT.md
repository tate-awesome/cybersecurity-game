# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 317 files · ~267,210 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4731 nodes · 9763 edges · 231 communities (71 shown, 160 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 469 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `acc71208`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- menu_bar.py
- important_buttons/__init__.py
- MetaPacket
- examples.py
- Process
- _in_nm_context
- MenuBar
- describe.py
- Overlay
- style.py
- Visual
- Footer
- confirm_dialog
- ToggleButton
- ap_commands.py
- FilterOverlay
- BaseForm
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
- Style
- ._build_stylesheet
- network_diagram/_builder.py
- CheckboxOverlay
- ConfigEditor
- docking.py
- LocalizationManager
- Panel
- WifiForm
- .start_session
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- VisualPalette
- Preferences
- _base_button.py
- edit_workspace_availability.py
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
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
- _MapCanvas
- threading
- PrivilegedHelper
- SettingsPage
- frame_callback
- Draw
- _Grip
- settings_overlay_button.py
- PauseMenu
- .fill_base
- WaveGrid
- NewWorkspaceDialog
- Camera
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- DockArea
- paint_panel
- DropZone
- VariableOverlay
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- geometry.py
- ProcessManager
- ArpSpoofer
- DragPayload
- SummaryDrawer
- WorkspaceSelectPage
- StripChartBase
- Router
- QWidget
- conjugate
- PopupEntrance
- host.py
- .new_tab
- QWidget
- time_core/transforms.py
- paint_mark
- Builder
- MainWindow
- dist.py
- CallbackRegistry
- combined.py
- Wifi
- Meter
- surface_shadow
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
- Map
- Builder
- Kalman
- ._scan_for_networks
- APPoller
- Loader
- Master
- Slave
- SectionCard
- SelectRegisterPreset
- Builder
- SampleNetwork
- Proximity
- Visuals
- SelectColorTheme
- FileStream
- AppearEffect
- BuildInfo
- NoteBrowser
- _Chip
- ToggleBookmark
- select_background.py
- Scrollable
- to_state
- .save_current_page
- Table
- pause_menu.py
- _Gaps
- _DrawerLayout
- Telemetry
- .authored_weights
- .page_panel_keys
- .build_description_tab
- fade_in
- .__init__
- PooledCanvasMixin
- .__init__
- _Drawer
- DenseMesh
- open_favorite_page.py
- WorkspaceButton
- SettingsSection
- ConfigureThisWorkspace
- LinkToPage
- ModeForm
- APConnectForm
- EncryptionForm
- Builder
- APTunnelForm
- KalmanForm
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

## Communities (231 total, 160 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.10
Nodes (4): ContextManager, form_order(), HVACSlidersForm, SubmarineSlidersForm

### Community 1 - "menu_bar.py"
Cohesion: 0.04
Nodes (17): bare_icon(), _FollowResize, global_buttons(), icon_button(), _RightZoneRoom, bar_button_height(), CornerControls, draw_window_bar_line() (+9 more)

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (27): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs, ClearStatusConsole (+19 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "examples.py"
Cohesion: 0.06
Nodes (17): House, NetworkDiagramCanvas, WorldMap, ControlsExample, HouseExample, MapExample, NetworkExample, PassWheel (+9 more)

### Community 5 - "Process"
Cohesion: 0.07
Nodes (6): flush(), flush_all(), run(), Buffer, Process, RetentionPolicy

### Community 7 - "MenuBar"
Cohesion: 0.04
Nodes (18): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+10 more)

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 11 - "Visual"
Cohesion: 0.07
Nodes (7): draw_vessel(), get_arc_points(), get_bearing(), rotate(), value_noise(), draw_glow(), Visual

### Community 12 - "Footer"
Cohesion: 0.06
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "confirm_dialog"
Cohesion: 0.05
Nodes (10): DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ResetCurrentPageToDefaults, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage, confirm_dialog() (+2 more)

### Community 14 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterOverlay"
Cohesion: 0.13
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 17 - "BaseForm"
Cohesion: 0.04
Nodes (7): BaseForm, ElidingLabel, ArpForm, DosForm, NFQForm, NmapForm, SniffForm

### Community 18 - "PacketTreeview"
Cohesion: 0.07
Nodes (3): PacketsExample, Builder, PacketTreeview

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.07
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (5): is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "time"
Cohesion: 0.06
Nodes (11): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+3 more)

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): MaterialEditorPopup, MaterialEditor, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsOverlay"
Cohesion: 0.09
Nodes (7): column_category(), column_position(), is_column_available(), PacketColumnsOverlay, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 36 - "network_diagram/_builder.py"
Cohesion: 0.08
Nodes (5): StripChart, frame_callback(), Builder, Builder, Builder

### Community 37 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (6): PanelButton, CheckboxOverlay, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 39 - "docking.py"
Cohesion: 0.12
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

### Community 53 - "_base_button.py"
Cohesion: 0.08
Nodes (8): open_in_browser(), DeleteAllUserData, ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue, OpenThemeEditor, OpenTitlePage

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.10
Nodes (4): _LentPlaceholder, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.17
Nodes (5): DesktopFade, FadeIn, covered(), settle(), uncovered()

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.15
Nodes (9): Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes(), tokenize() (+1 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "threading"
Cohesion: 0.09
Nodes (3): _is_global(), _resolve_local_mac(), NetFilterQueueBaseClass

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "settings_overlay_button.py"
Cohesion: 0.14
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 106 - "DropZone"
Cohesion: 0.08
Nodes (4): DropZone, _Indicator, ListZone, RowZone

### Community 107 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 113 - "geometry.py"
Cohesion: 0.08
Nodes (12): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), scale(), translate() (+4 more)

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "paint_mark"
Cohesion: 0.12
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), PeekArrow

### Community 135 - "MainWindow"
Cohesion: 0.07
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 136 - "dist.py"
Cohesion: 0.27
Nodes (3): build_name(), main(), write_build_info()

### Community 137 - "CallbackRegistry"
Cohesion: 0.10
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "combined.py"
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

### Community 164 - "SectionCard"
Cohesion: 0.14
Nodes (3): CategoryChip, checkbox(), SectionCard

### Community 172 - "FileStream"
Cohesion: 0.10
Nodes (3): _dialog_parent(), file_dialog(), FileStream

### Community 180 - "Scrollable"
Cohesion: 0.10
Nodes (5): Scrollable, Builder, ChartsExample, FlagsExample, Builder

### Community 187 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 188 - "pause_menu.py"
Cohesion: 0.10
Nodes (6): developer_text(), ButtonGroup, offered_sections(), OpenPauseMenu, ask_to_quit(), QuitApplication

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1928 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **160 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `menu_bar.py`, `important_buttons/__init__.py`, `examples.py`, `Process`, `MenuBar`, `CallbackRegistry`, `style.py`, `combined.py`, `Visual`, `confirm_dialog`, `.reload_preferences`, `AnimationManager`, `ShiftWheel`, `Style`, `network_diagram/_builder.py`, `CheckboxOverlay`, `docking.py`, `LocalizationManager`, `.start_session`, `Preferences`, `_base_button.py`, `Performance`, `pause_menu.py`, `KeyBinds`, `InputManager`, `open_favorite_page.py`, `PageManager`, `threading`, `ConfigureThisWorkspace`, `LinkToPage`, `settings_overlay_button.py`, `Json`, `ProcessManager`, `Router`, `host.py`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.10277777777777777 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `menu_bar.py`, `._build_stylesheet`, `.make_built_in`, `style.py`, `Overlay`, `.start_session`, `open_favorite_page.py`, `.brush`, `QWidget`, `.load_imported_themes`, `_base_button.py`, `SettingsSection`, `settings_overlay_button.py`, `.theme_family`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `menu_bar.py` be split into smaller, more focused modules?**
  _Cohesion score 0.037719298245614034 - nodes in this community are weakly interconnected._