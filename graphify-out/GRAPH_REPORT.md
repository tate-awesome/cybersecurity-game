# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 334 files · ~283,813 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4840 nodes · 9986 edges · 276 communities (65 shown, 211 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 466 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ab88947`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- ButtonModal
- important_buttons/__init__.py
- MetaPacket
- CheckboxOverlay
- _in_nm_context
- WorkspaceSelectPage
- describe.py
- _SaveLayoutAsDefault
- .__init__
- VisualPalette
- Footer
- FilterModal
- MenuBar
- Dev/Host_API.py
- .field_options
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
- RecordFilter
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- ModbusBuffer
- run
- .restyle
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
- RowZone
- ButtonGroup
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
- .brush
- packet_filter.py
- launch.py
- DragHandle
- _MapCanvas
- .add_deadspace
- PrivilegedHelper
- SettingsPage
- Draw
- _Grip
- Overlay
- PauseMenu
- WaveGrid
- Context
- Camera
- GoForwardToNextPage
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
- time
- ArpSpoofer
- SectionCard
- .__init__
- ToggleButton
- SummaryDrawer
- StripChartBase
- KalmanToggleForm
- BaseForm
- QWidget
- TransactionManager
- PopupEntrance
- host.py
- .add_setting_row
- .new_tab
- time_core/transforms.py
- NetworkGraph
- Map
- Builder
- .refresh_usage
- ClickManager
- WindowBarButton
- Wifi
- Meter
- menu_bar.py
- Denier
- sys
- StripChartLayout
- TitlePage
- Style
- MitmTable
- arpy2a.py
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
- BuildInfo
- DragPayload
- PopupWindow
- Proximity
- WindowEdges
- SelectBackground
- AppearEffect
- Scanlines
- NoteBrowser
- _Chip
- .collapsed
- Loader
- NewWorkspaceDialog
- .__init__
- .save_current_page
- _PollUnpacker
- .columnconfigure
- EditWorkspaceAvailability
- AnimationManager
- .build_description_tab
- WorkspaceButton
- .authored_weights
- .page_panel_keys
- MainWindow
- CallbackRegistry
- .__init__
- PooledCanvasMixin
- .__init__
- window_chrome.py
- .fill_base
- OpenFavoritePage
- paint_panel
- DenseMesh
- ModeForm
- SettingsSection
- ask_to_quit
- ProcessManager
- .play
- .build_appearance_tab
- flusher.py
- APConnectForm
- EncryptionForm
- NetFilterQueueBaseClass
- .__init__
- EditBackgroundChoices
- ElidingLabel
- PreferencesData
- CLAUDE.md
- ModalWindow
- DefenderMapBuffer
- _Echo
- _BufferShim
- StreamIncomingPacketsToMcap
- ToggleDebugLabels
- message
- Scrim
- Channel
- FreeScrollStatusConsole
- LinkToPage
- PausePacketConsole
- ToggleFullscreen
- ToggleNetworkGraphRingView
- ToggleStripChartAutoFit
- ToggleWorkspaceBackground
- shorten_line

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 146 edges
2. `Style` - 119 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 60 edges
9. `DockArea` - 53 edges
10. `VisualPalette` - 48 edges

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

## Communities (276 total, 211 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.06
Nodes (13): ContextManager, apply_scale_about(), conjugate(), quote(), BoatMotion, Sprites, Triangle, WorkspacePage (+5 more)

### Community 1 - "ButtonModal"
Cohesion: 0.20
Nodes (4): EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (42): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs (+34 more)

### Community 5 - "CheckboxOverlay"
Cohesion: 0.11
Nodes (8): ListZone, PanelButton, CheckboxOverlay, form_order(), ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (32): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+24 more)

### Community 9 - "_SaveLayoutAsDefault"
Cohesion: 0.16
Nodes (3): _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault

### Community 10 - ".__init__"
Cohesion: 0.24
Nodes (3): bar_inset(), minimized_thickness(), bar_button_height()

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, Telemetry

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.07
Nodes (28): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+20 more)

### Community 17 - "widgets/__init__.py"
Cohesion: 0.08
Nodes (12): NetworkDiagramCanvas, StripChart, SelectRegisterPreset, Scrollable, TextArea, panel(), HVACKalmanToggleForm, Builder (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.11
Nodes (3): WorkspaceSorter, create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (4): LookOnly, MaterialEditor, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.10
Nodes (7): column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "run"
Cohesion: 0.27
Nodes (7): _ContextStub, _dispatch(), run(), flusher(), run_from_argv(), send(), status_heartbeat()

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.10
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "TabStrip"
Cohesion: 0.09
Nodes (4): paint_mark(), PeekArrow, _SideTitle, TabStrip

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 50 - "CombinedTable"
Cohesion: 0.05
Nodes (15): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+7 more)

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (4): _LentPlaceholder, _Peek, _SideStrip, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "FlowLayout"
Cohesion: 0.05
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.14
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 95 - "Context"
Cohesion: 0.18
Nodes (8): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), write_config_values()

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.10
Nodes (4): Canvas, DefenderWorldMap, TriangleCanvas, WorldMap

### Community 107 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 108 - "Json"
Cohesion: 0.08
Nodes (4): Json, _dialog_parent(), file_dialog(), Paths

### Community 111 - "_Dim"
Cohesion: 0.11
Nodes (4): _Dim, _Drawer, _FollowResize, _OnHide

### Community 113 - "geometry.py"
Cohesion: 0.08
Nodes (12): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), get_arc_points(), get_bearing(), rotate() (+4 more)

### Community 114 - "time"
Cohesion: 0.04
Nodes (16): random_spline_path(), Buffer, _is_global(), _resolve_local_mac(), Sniffer, build_capability(), Process, action() (+8 more)

### Community 116 - "SectionCard"
Cohesion: 0.14
Nodes (3): CategoryChip, checkbox(), SectionCard

### Community 122 - "BaseForm"
Cohesion: 0.08
Nodes (19): hvac_kalman_enabled(), kalman_enabled(), push_submarine_settings(), submarine_kalman_enabled(), submarine_settings_synced(), BaseForm, SubmarineKalmanToggleForm, HVACSlidersForm (+11 more)

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 138 - "WindowBarButton"
Cohesion: 0.11
Nodes (5): SquareButtons, toggle_maximized(), WindowBarButton, WindowControls, WindowDrag

### Community 141 - "menu_bar.py"
Cohesion: 0.14
Nodes (5): ConfigureThisWorkspace, ShowHelpMessage, bare_icon(), global_buttons(), icon_button()

### Community 143 - "sys"
Cohesion: 0.16
Nodes (3): build_name(), main(), write_build_info()

### Community 145 - "TitlePage"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

### Community 148 - "arpy2a.py"
Cohesion: 0.10
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

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.09
Nodes (5): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems(), delete()

### Community 181 - ".__init__"
Cohesion: 0.11
Nodes (3): ToggleBookmark, _FollowResize, _RightZoneRoom

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 203 - "window_chrome.py"
Cohesion: 0.13
Nodes (6): CornerControls, draw_window_bar_line(), _Strip, window_bar_button_height(), window_bar_height(), window_bar_room()

### Community 204 - ".fill_base"
Cohesion: 0.12
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 206 - "paint_panel"
Cohesion: 0.12
Nodes (3): blurred_shape(), paint_panel(), surface_shadow()

### Community 214 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 216 - "flusher.py"
Cohesion: 0.83
Nodes (3): flush(), flush_all(), run()

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1978 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **211 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `CheckboxOverlay`, `ClickManager`, `VisualPalette`, `menu_bar.py`, `widgets/__init__.py`, `Style`, `ShiftWheel`, `PacketColumnsModal`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `Preferences`, `.save_current_page`, `Performance`, `KeyBinds`, `AnimationManager`, `Router`, `InputManager`, `window_chrome.py`, `PageManager`, `ProcessManager`, `PrivilegedHelper`, `.apply`, `Json`, `time`, `BaseForm`, `host.py`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.06016240157480315 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.restyle`, `._build_stylesheet`, `.apply_theme`, `important_buttons/__init__.py`, `.discard_changes`, `menu_bar.py`, `.brush`, `_DressedWidgets`, `.lift_button`, `SettingsSection`, `Overlay`, `.theme_family`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.022609706480674223 - nodes in this community are weakly interconnected._