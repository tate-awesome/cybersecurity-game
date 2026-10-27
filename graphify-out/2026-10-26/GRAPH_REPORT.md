# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 322 files · ~269,789 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4784 nodes · 9913 edges · 240 communities (71 shown, 169 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 479 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `14e022c9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- settings_overlay_button.py
- important_buttons/__init__.py
- MetaPacket
- Builder
- _in_nm_context
- WorkspaceSelectPage
- describe.py
- _SaveLayoutAsDefault
- paint_mark
- VisualPalette
- Footer
- PopupWindow
- MenuBar
- ap_commands.py
- FilterPopup
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
- PacketColumnsPopup
- AttackHMI_relay_ramp_attack.py
- FindBar
- HouseBuffer
- server.py
- .apply_theme
- ._build_stylesheet
- SmoothWheel
- ConfigEditor
- docking.py
- LocalizationManager
- _DrawerLayout
- WifiForm
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- WrapLayout
- Preferences
- _Indicator
- global_buttons
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
- app.py
- PageManager
- .brush
- packet_filter.py
- launch.py
- DragHandle
- _MapCanvas
- Builder
- PrivilegedHelper
- SettingsPage
- frame_callback
- Draw
- _Grip
- Overlay
- PauseMenu
- ElidingLabel
- WaveGrid
- config_editor.py
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
- DragPayload
- VariablePopup
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- geometry.py
- threading
- ArpSpoofer
- SectionCard
- _Gaps
- ToggleButton
- SummaryDrawer
- StripChartBase
- KalmanToggleForm
- align_decimals
- QWidget
- MaterialEditor
- PopupEntrance
- host.py
- .add_setting_row
- .new_tab
- time_core/transforms.py
- paint_panel
- router.py
- Builder
- .build_tabs
- AnimationManager
- WindowBarButton
- Wifi
- Meter
- bare_icon
- Denier
- sys
- StripChartLayout
- GrowingButton
- Style
- MitmTable
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
- defender_flag_panel/_builder.py
- Master
- Slave
- fade_in
- version.py
- SampleNetwork
- Proximity
- WindowEdges
- SelectRegisterPreset
- _OnHide
- AppearEffect
- NoteBrowser
- _Chip
- .__init__
- NewWorkspaceDialog
- .__init__
- .save_current_page
- Table
- .columnconfigure
- EditWorkspaceAvailability
- confirm_dialog
- .build_description_tab
- WorkspaceButton
- .authored_weights
- .page_panel_keys
- MainWindow
- .__init__
- PooledCanvasMixin
- .__init__
- CornerControls
- paint_noise_gradient
- OpenFavoritePage
- surface_shadow
- Telemetry
- DenseMesh
- ModeForm
- SettingsSection
- Draw
- window_chrome.py
- ProcessManager
- .play
- Visualizer.py
- flusher.py
- SampleSubmarine
- .__init__
- EditBackgroundChoices
- PreferencesData
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 145 edges
2. `ImportantButton` - 114 edges
3. `Style` - 101 edges
4. `Overlay` - 76 edges
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

## Communities (240 total, 169 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.07
Nodes (15): ContextManager, apply_scale_about(), conjugate(), quote(), DefenderWorldMap, BaseForm, APConnectForm, APTunnelForm (+7 more)

### Community 1 - "settings_overlay_button.py"
Cohesion: 0.16
Nodes (5): EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton, ButtonPopup

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (43): ListZone, AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderFlagForms (+35 more)

### Community 3 - "MetaPacket"
Cohesion: 0.06
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 11 - "VisualPalette"
Cohesion: 0.08
Nodes (4): draw_glow(), Visual, VisualPalette, Kernel

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterPopup"
Cohesion: 0.07
Nodes (4): read(), FilterPopup, label_key(), value_key()

### Community 17 - "widgets/__init__.py"
Cohesion: 0.04
Nodes (26): House, StripChart, WorldMap, Scrollable, TextArea, panel(), Builder, ChartsExample (+18 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (5): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer, NetworkDiagramCanvas

### Community 21 - "VisualBackground"
Cohesion: 0.06
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (3): WorkspaceSorter, create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.11
Nodes (5): is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "time"
Cohesion: 0.07
Nodes (12): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 29 - "PacketColumnsPopup"
Cohesion: 0.09
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsPopup, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

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

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 65 - "buffer_manager.py"
Cohesion: 0.05
Nodes (4): DefenderMapBuffer, DefenderModbusBuffer, ModbusBuffer, _resolve_local_mac()

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), is_switch()

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
Cohesion: 0.12
Nodes (3): App, WindowReveal, __getattr__()

### Community 80 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.06
Nodes (4): SelectBackground, SelectColorTheme, Overlay, background_choices()

### Community 95 - "config_editor.py"
Cohesion: 0.19
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), write_config_values() (+1 more)

### Community 97 - "menu_bar.py"
Cohesion: 0.07
Nodes (7): ButtonGroup, GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Replay"
Cohesion: 0.07
Nodes (3): _dialog_parent(), file_dialog(), Replay

### Community 107 - "VariablePopup"
Cohesion: 0.20
Nodes (3): VariablePopup, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "geometry.py"
Cohesion: 0.07
Nodes (14): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+6 more)

### Community 114 - "threading"
Cohesion: 0.05
Nodes (4): Buffer, NetFilterQueueBaseClass, Process, FileStream

### Community 116 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 118 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 122 - "align_decimals"
Cohesion: 0.24
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "router.py"
Cohesion: 0.07
Nodes (9): BoatMotion, Sprites, Triangle, TitlePage, WorkspacePage, NotFound, Page, TriangleCanvas (+1 more)

### Community 137 - "AnimationManager"
Cohesion: 0.06
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "WindowBarButton"
Cohesion: 0.10
Nodes (5): SquareButtons, toggle_maximized(), WindowBarButton, WindowControls, WindowDrag

### Community 143 - "sys"
Cohesion: 0.22
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
Cohesion: 0.18
Nodes (5): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, SubmarineKalmanToggleForm

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.10
Nodes (5): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems(), delete()

### Community 181 - ".__init__"
Cohesion: 0.11
Nodes (3): ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 187 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 190 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout, WorkspaceSaveResetButton (+1 more)

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 212 - "window_chrome.py"
Cohesion: 0.13
Nodes (6): ask_to_quit(), bar_button_height(), draw_window_bar_line(), _Strip, window_bar_height(), window_bar_room()

### Community 214 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 216 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1949 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **169 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `settings_overlay_button.py`, `important_buttons/__init__.py`, `router.py`, `AnimationManager`, `VisualPalette`, `widgets/__init__.py`, `Style`, `PacketBuffer`, `ShiftWheel`, `PacketColumnsPopup`, `defender_flag_panel/_builder.py`, `.apply_theme`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `.start_session`, `Preferences`, `.save_current_page`, `Performance`, `KeyBinds`, `confirm_dialog`, `Router`, `buffer_manager.py`, `InputManager`, `PageManager`, `window_chrome.py`, `ProcessManager`, `config_editor.py`, `menu_bar.py`, `Json`, `threading`, `host.py`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07239382239382239 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `settings_overlay_button.py`, `.apply_theme`, `._build_stylesheet`, `.theme_modes`, `important_buttons/__init__.py`, `menu_bar.py`, `.discard_changes`, `.start_session`, `.brush`, `SettingsSection`, `Overlay`, `.theme_family`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.022098120458776196 - nodes in this community are weakly interconnected._