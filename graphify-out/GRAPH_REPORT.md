# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 320 files · ~269,056 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4768 nodes · 9851 edges · 247 communities (71 shown, 176 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 471 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `09e1c2c1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- WindowDrag
- important_buttons/__init__.py
- MetaPacket
- Scrollable
- os
- _in_nm_context
- config_editor.py
- describe.py
- paint_mark
- VisualPalette
- Footer
- _SaveLayoutAsDefault
- bare_icon
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
- .apply_theme
- ._build_stylesheet
- CheckboxOverlay
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
- Kernel
- Preferences
- confirm_dialog
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
- Router
- FadeOut
- buffer_manager.py
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
- .css
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
- Overlay
- PauseMenu
- _PollUnpacker
- WaveGrid
- NewWorkspaceDialog
- Camera
- .__init__
- VectorField
- palette_generator.py
- Buffer
- compile_filter
- Replay
- Canvas
- .collapsed
- leaf_of
- DropZone
- VariableOverlay
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- transformations.py
- Process
- ArpSpoofer
- WorkspaceChip
- WrapLayout
- ToggleButton
- WorkspaceSelectPage
- StripChartBase
- WindowBarButton
- HouseBuffer
- QWidget
- geometry.py
- PopupEntrance
- host.py
- QWidget
- time_core/transforms.py
- paint_panel
- MenuBar
- Builder
- WindowEdges
- .__init__
- CallbackRegistry
- Wifi
- Meter
- WindowControls
- Denier
- dist.py
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
- FlagsForm
- Master
- Slave
- ListZone
- platform
- .columnconfigure
- SampleNetwork
- Proximity
- MainWindow
- MaterialEditor
- FileStream
- AppearEffect
- Builder
- NoteBrowser
- _Chip
- core/draw.py
- Loader
- Builder
- ToggleBookmark
- .save_current_page
- Table
- Builder
- KalmanToggleForm
- PopupWindow
- _Gaps
- _DropPreview
- .authored_weights
- .page_panel_keys
- DragPayload
- .__init__
- PooledCanvasMixin
- .__init__
- ToggleDebugLabels
- SampleSubmarine
- OpenFavoritePage
- Telemetry
- StreamIncomingPacketsToMcap
- GoForwardToNextPage
- SettingsSection
- LinkToPage
- ModeForm
- ToggleFullscreen
- Builder
- .__init__
- FreeScrollStatusConsole
- PausePacketConsole
- ToggleNetworkGraphRingView
- ToggleStripChartAutoFit
- panel
- ToggleWorkspaceBackground
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

## Communities (247 total, 176 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.05
Nodes (39): ContextManager, DefenderWorldMap, House, NetworkDiagramCanvas, StripChart, TriangleCanvas, WorldMap, form_order() (+31 more)

### Community 1 - "WindowDrag"
Cohesion: 0.12
Nodes (5): draw_window_bar_line(), SquareButtons, _Strip, toggle_maximized(), WindowDrag

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (44): AbortAllNetworkActions, ImportantButton, open_in_browser(), PanelButton, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms (+36 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 4 - "Scrollable"
Cohesion: 0.09
Nodes (6): Scrollable, ControlsExample, FlagsExample, RegistersExample, SampleHVAC, SamplePackets

### Community 5 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 7 - "config_editor.py"
Cohesion: 0.05
Nodes (18): BoatMotion, delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels() (+10 more)

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 10 - "paint_mark"
Cohesion: 0.12
Nodes (4): bar_inset(), paint_mark(), PeekArrow, _SideTitle

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (7): draw_vessel(), paint_noise_gradient(), value_noise(), draw_glow(), Visual, VisualPalette, DenseMesh

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "FilterOverlay"
Cohesion: 0.08
Nodes (3): FilterOverlay, label_key(), value_key()

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "time"
Cohesion: 0.10
Nodes (12): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+4 more)

### Community 29 - "PacketColumnsOverlay"
Cohesion: 0.09
Nodes (7): column_category(), column_position(), is_column_available(), PacketColumnsOverlay, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 38 - "ConfigEditor"
Cohesion: 0.10
Nodes (3): ConfigEditor, walk(), in_layout()

### Community 39 - "docking.py"
Cohesion: 0.11
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), move_panel(), new_id() (+8 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 54 - "confirm_dialog"
Cohesion: 0.06
Nodes (9): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), RefreshCurrentPage, ResetSavedWorkspaceLayout, RefreshAndCloseOverlay, WorkspaceSaveResetButton (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.10
Nodes (3): _LentPlaceholder, _SideStrip, TabbedPane

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

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
Cohesion: 0.16
Nodes (3): App, WindowReveal, __getattr__()

### Community 80 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "threading"
Cohesion: 0.07
Nodes (3): ModbusBuffer, _resolve_local_mac(), NetFilterQueueBaseClass

### Community 88 - "frame_callback"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.04
Nodes (17): conjugate(), quote(), ButtonGroup, offered_sections(), SelectBackground, SelectColorTheme, EditBackgroundChoices, EditModelStyle (+9 more)

### Community 95 - "NewWorkspaceDialog"
Cohesion: 0.13
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 97 - ".__init__"
Cohesion: 0.11
Nodes (3): _FollowResize, global_buttons(), _RightZoneRoom

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 100 - "Buffer"
Cohesion: 0.12
Nodes (3): Buffer, StatusBuffer, MetaStatus

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 106 - "DropZone"
Cohesion: 0.09
Nodes (3): DropZone, _Indicator, RowZone

### Community 107 - "VariableOverlay"
Cohesion: 0.24
Nodes (3): VariableOverlay, autosave(), reset_all()

### Community 108 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.11
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 113 - "transformations.py"
Cohesion: 0.16
Nodes (7): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse()

### Community 116 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 119 - "WorkspaceSelectPage"
Cohesion: 0.06
Nodes (5): fade_in(), SummaryDrawer, WorkspaceButton, WorkspaceSelectPage, update()

### Community 121 - "WindowBarButton"
Cohesion: 0.18
Nodes (3): minimized_thickness(), bar_button_height(), WindowBarButton

### Community 125 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 129 - "QWidget"
Cohesion: 0.12
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "paint_panel"
Cohesion: 0.12
Nodes (3): _Peek, paint_panel(), surface_shadow()

### Community 136 - ".__init__"
Cohesion: 0.21
Nodes (4): FadeIn, covered(), settle(), uncovered()

### Community 137 - "CallbackRegistry"
Cohesion: 0.10
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 143 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 145 - "GrowingButton"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

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

### Community 175 - "NoteBrowser"
Cohesion: 0.14
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 178 - "core/draw.py"
Cohesion: 0.22
Nodes (3): apply_scale_about(), shorten_line(), zoom_and_pan()

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1943 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **176 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `config_editor.py`, `CallbackRegistry`, `.apply`, `VisualPalette`, `Style`, `AnimationManager`, `ShiftWheel`, `.apply_theme`, `docking.py`, `LocalizationManager`, `.start_session`, `core/draw.py`, `Preferences`, `confirm_dialog`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `threading`, `PrivilegedHelper`, `.reset_page`, `Overlay`, `Json`, `Process`, `host.py`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.05184108527131783 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.apply_theme`, `._build_stylesheet`, `important_buttons/__init__.py`, `config_editor.py`, `.discard_changes`, `.start_session`, `.css`, `SettingsSection`, `Overlay`, `.theme_family`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `WindowDrag` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._