# Graph Report - cybersecurity-game  (2026-10-27)

## Corpus Check
- 322 files · ~275,233 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4856 nodes · 10035 edges · 242 communities (75 shown, 167 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24af8708`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- important_buttons/__init__.py
- ImportantButton
- MetaPacket
- .apply_theme
- _in_nm_context
- SummaryDrawer
- describe.py
- save_columns_as_default.py
- paint_mark
- VisualPalette
- Footer
- FilterModal
- menu_bar.py
- Dev/Host_API.py
- Packet
- MenuBar
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- DockArea
- SettingsSection
- link_info
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- leaf_of
- ._build_stylesheet
- SmoothWheel
- Scanlines
- ConfigEditor
- docking.py
- LocalizationManager
- widgets/__init__.py
- WifiForm
- SelectColorTheme
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- Scrollable
- endpoints
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
- ToggleBookmark
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
- style.py
- Camera
- Panes
- Constellation
- app.py
- PageManager
- filter_overlay.py
- launch.py
- DragHandle
- _MapCanvas
- PrivilegedHelper
- SettingsPage
- Style
- Draw
- _Grip
- Overlay
- PauseMenu
- ElidingLabel
- WaveGrid
- config_editor.py
- Camera
- NativeFrame
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- MapBuffer
- .collapsed
- RowZone
- VariableModal
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- boat_motion.py
- _DrawerLayout
- ArpSpoofer
- ap_commands.py
- time
- ToggleButton
- _DropPreview
- StripChartBase
- defender_flag_panel/_builder.py
- defender_modbus_panel/_builder.py
- QWidget
- SelectRegisterPreset
- PopupEntrance
- host.py
- .add_setting_row
- ConfigureThisWorkspace
- time_core/transforms.py
- LinkToPage
- align_decimals
- Builder
- .refresh_usage
- Page
- ClickManager
- Kernel
- Wifi
- Meter
- MitmTable
- Denier
- buffer_manager.py
- StripChartLayout
- GrowingButton
- json.py
- DenseMesh
- Attack
- ToggleLightDarkMode
- .connect_to_saved_wifi
- Map
- ShiftWheel
- .collect
- .integer
- GoForwardToNextPage
- Builder
- Kalman
- ._scan_for_networks
- APPoller
- WorkspaceSelectPage
- Master
- Slave
- ChoiceList
- MaterialEditorPopup
- WorkspaceChip
- PopupWindow
- .color
- MainWindow
- ButtonModal
- MaterialEditor
- AppearEffect
- NoteBrowser
- _Chip
- FileStream
- Loader
- NewWorkspaceDialog
- _RightZoneRoom
- .save_current_page
- LookOnly
- ListZone
- CallbackRegistry
- AnimationManager
- DropZone
- .new_tab
- .authored_weights
- .page_panel_keys
- Paths
- file_dialog
- core/transforms.py
- .__init__
- PooledCanvasMixin
- .__init__
- hvac_chart.py
- .fill_base
- open_favorite_page.py
- paint_panel
- BuildInfo
- .build_menu_bar_section
- DragPayload
- SettingsSection
- confirm_dialog
- ProcessManager
- fade_in
- os
- select_background.py
- _OnHide
- ModalWindow
- .__init__
- Scrim
- WorkspaceButton
- PreferencesData
- BaseForm
- NotFound
- Telemetry
- CLAUDE.md
- TitlePage

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 146 edges
2. `Style` - 123 edges
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

## Communities (242 total, 167 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.11
Nodes (3): ContextManager, _is_global(), format_number()

### Community 1 - "important_buttons/__init__.py"
Cohesion: 0.05
Nodes (14): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, EditNetworkHosts, LoadLocalizationLabelsFile (+6 more)

### Community 2 - "ImportantButton"
Cohesion: 0.03
Nodes (23): AbortAllNetworkActions, developer_text(), ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole (+15 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 8 - "describe.py"
Cohesion: 0.14
Nodes (5): modbus_function(), modbus_info(), modbus_summary(), register_values(), tags()

### Community 9 - "save_columns_as_default.py"
Cohesion: 0.09
Nodes (7): column_position(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, message()

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 11 - "VisualPalette"
Cohesion: 0.09
Nodes (4): draw_vessel(), draw_glow(), Visual, VisualPalette

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "menu_bar.py"
Cohesion: 0.05
Nodes (16): ButtonGroup, offered_sections(), ShowHelpMessage, global_buttons(), bar_button_height(), CornerControls, draw_window_bar_line(), SquareButtons (+8 more)

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.11
Nodes (17): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+9 more)

### Community 16 - "Packet"
Cohesion: 0.21
Nodes (13): dhcp_type(), dns_answers(), dns_question(), frame_kind(), info(), name(), payload_length(), ports() (+5 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.07
Nodes (3): _default_gateway_ip(), NetworkGraph, PacketBuffer

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.06
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (3): RecordFilter, RetentionPolicy, SessionRecorder

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.10
Nodes (5): is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "link_info"
Cohesion: 0.16
Nodes (9): handshake_message(), is_dot11_control(), is_filler(), is_lldp(), link_info(), link_summary(), meaningful_layer(), protocol() (+1 more)

### Community 29 - "PacketColumnsModal"
Cohesion: 0.12
Nodes (4): column_category(), is_column_available(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.13
Nodes (6): apply_scale_about(), get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), move_panel(), new_id() (+8 more)

### Community 42 - "widgets/__init__.py"
Cohesion: 0.06
Nodes (11): NetworkDiagramCanvas, StripChart, shown_columns(), TextArea, panel(), Builder, Builder, Builder (+3 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 46 - "HVACChart"
Cohesion: 0.09
Nodes (3): DefenderHVACChart, HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 50 - "CombinedTable"
Cohesion: 0.05
Nodes (15): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+7 more)

### Community 53 - "Scrollable"
Cohesion: 0.05
Nodes (7): form_order(), _Gaps, Scrollable, Builder, Builder, Builder, Builder

### Community 54 - "endpoints"
Cohesion: 0.22
Nodes (4): endpoints(), dissect(), hardware_addresses(), link_of()

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.11
Nodes (12): button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials() (+4 more)

### Community 80 - "filter_overlay.py"
Cohesion: 0.12
Nodes (13): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+5 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 95 - "config_editor.py"
Cohesion: 0.20
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.10
Nodes (5): Canvas, DefenderWorldMap, House, TriangleCanvas, WorldMap

### Community 107 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "boat_motion.py"
Cohesion: 0.19
Nodes (5): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine()

### Community 116 - "ap_commands.py"
Cohesion: 0.16
Nodes (16): ap_tunnel_enabled(), ap_tunnel_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings(), push_submarine_settings(), read_hvac_state() (+8 more)

### Community 117 - "time"
Cohesion: 0.06
Nodes (12): random_spline_path(), Buffer, Process, action(), dumps(), header(), mark(), packet() (+4 more)

### Community 118 - "ToggleButton"
Cohesion: 0.04
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit

### Community 121 - "defender_flag_panel/_builder.py"
Cohesion: 0.13
Nodes (6): FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 122 - "defender_modbus_panel/_builder.py"
Cohesion: 0.19
Nodes (3): ModeForm, HVACSlidersForm, SubmarineSlidersForm

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 136 - "Page"
Cohesion: 0.11
Nodes (4): Sprites, Triangle, WorkspacePage, Page

### Community 143 - "buffer_manager.py"
Cohesion: 0.07
Nodes (4): HouseBuffer, ModbusBuffer, _resolve_local_mac(), NetFilterQueueBaseClass

### Community 146 - "json.py"
Cohesion: 0.19
Nodes (4): build_name(), main(), write_build_info(), decode()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 150 - ".connect_to_saved_wifi"
Cohesion: 0.33
Nodes (4): finish(), on_activated(), on_state_changed(), on_timeout()

### Community 155 - "GoForwardToNextPage"
Cohesion: 0.12
Nodes (3): GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 171 - "ButtonModal"
Cohesion: 0.14
Nodes (5): EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton, ButtonModal

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 198 - "core/transforms.py"
Cohesion: 0.22
Nodes (4): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 204 - ".fill_base"
Cohesion: 0.12
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 206 - "paint_panel"
Cohesion: 0.10
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 212 - "confirm_dialog"
Cohesion: 0.05
Nodes (12): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, RefreshCurrentPage, ResetCurrentPageToDefaults, ResetSavedWorkspaceLayout (+4 more)

### Community 216 - "os"
Cohesion: 0.09
Nodes (3): flush(), flush_all(), run()

### Community 226 - "BaseForm"
Cohesion: 0.03
Nodes (10): BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm, EncryptionForm, KalmanForm, NFQForm (+2 more)

### Community 261 - "TitlePage"
Cohesion: 0.12
Nodes (3): TitlePage, TitleFooter, TitleMenu

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1985 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **167 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `ImportantButton`, `ConfigureThisWorkspace`, `LinkToPage`, `Page`, `ClickManager`, `save_columns_as_default.py`, `VisualPalette`, `menu_bar.py`, `buffer_manager.py`, `json.py`, `ShiftWheel`, `GoForwardToNextPage`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `widgets/__init__.py`, `ButtonModal`, `Preferences`, `.save_current_page`, `Performance`, `KeyBinds`, `AnimationManager`, `Router`, `Paths`, `InputManager`, `style.py`, `hvac_chart.py`, `open_favorite_page.py`, `PageManager`, `filter_overlay.py`, `confirm_dialog`, `ProcessManager`, `.apply`, `Style`, `.reload_preferences`, `config_editor.py`, `BaseForm`, `Canvas`, `Json`, `boat_motion.py`, `time`, `defender_flag_panel/_builder.py`, `defender_modbus_panel/_builder.py`, `host.py`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.10868079289131921 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `ImportantButton`, `._build_stylesheet`, `.apply_theme`, `.lift_button`, `style.py`, `.theme_family`, `ButtonModal`, `open_favorite_page.py`, `menu_bar.py`, `.brush`, `_DressedWidgets`, `SettingsSection`, `Overlay`, `.preset_name`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.053185271770894216 - nodes in this community are weakly interconnected._