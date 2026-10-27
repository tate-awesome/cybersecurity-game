# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 323 files · ~275,313 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4862 nodes · 10046 edges · 221 communities (79 shown, 142 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5146d67c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- _base_button.py
- important_buttons/__init__.py
- MetaPacket
- _in_nm_context
- SummaryDrawer
- describe.py
- save_columns_as_default.py
- paint_mark
- Visual
- Footer
- FilterModal
- MenuBar
- ap_commands.py
- Packet
- open_in_browser
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
- SelectBackground
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- .columnconfigure
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
- App
- PageManager
- filter_overlay.py
- json.py
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
- WindowControls
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- ModbusBuffer
- .collapsed
- _Indicator
- VariableModal
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- transformations.py
- Proximity
- ArpSpoofer
- Process
- ToggleButton
- _DropPreview
- StripChartBase
- KalmanToggleForm
- ModeForm
- QWidget
- SelectRegisterPreset
- PopupEntrance
- _Proxy
- QWidget
- ConfigureThisWorkspace
- time_core/transforms.py
- LinkToPage
- table.py
- Builder
- .refresh_usage
- .play
- ClickManager
- EditBackgroundChoices
- Wifi
- Meter
- MitmTable
- Denier
- threading
- StripChartLayout
- GrowingButton
- _Drawer
- DenseMesh
- Attack
- ToggleLightDarkMode
- .connect_to_saved_wifi
- ShiftWheel
- .collect
- .integer
- Builder
- Kalman
- ._scan_for_networks
- APPoller
- FlagsForm
- Master
- Slave
- ChoiceList
- ListZone
- PopupWindow
- VisualPalette
- MainWindow
- ButtonModal
- AppearEffect
- NoteBrowser
- _Chip
- Loader
- NewWorkspaceDialog
- _RightZoneRoom
- .save_current_page
- CallbackRegistry
- AnimationManager
- DragPayload
- .authored_weights
- .page_panel_keys
- .__init__
- PooledCanvasMixin
- .__init__
- .fill_base
- open_favorite_page.py
- paint_panel
- SettingsSection
- confirm_dialog
- time
- EncryptionForm
- .__init__
- PreferencesData
- Telemetry
- CLAUDE.md
- router.py

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

## Communities (221 total, 142 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.08
Nodes (12): ContextManager, House, WorldMap, BaseForm, APConnectForm, APTunnelForm, ArpForm, DosForm (+4 more)

### Community 1 - "_base_button.py"
Cohesion: 0.09
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (28): AbortAllNetworkActions, ImportantButton, ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole, EditModbusRegisterDisplay (+20 more)

### Community 3 - "MetaPacket"
Cohesion: 0.06
Nodes (5): Channel, NetworkGraph, Transaction, TransactionManager, MetaPacket

### Community 7 - "SummaryDrawer"
Cohesion: 0.06
Nodes (4): fade_in(), SummaryDrawer, WorkspaceButton, update()

### Community 8 - "describe.py"
Cohesion: 0.14
Nodes (5): modbus_function(), modbus_info(), modbus_summary(), register_values(), tags()

### Community 9 - "save_columns_as_default.py"
Cohesion: 0.07
Nodes (9): column_position(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault, _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ShowHelpMessage (+1 more)

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 11 - "Visual"
Cohesion: 0.09
Nodes (3): draw_vessel(), draw_glow(), Visual

### Community 12 - "Footer"
Cohesion: 0.06
Nodes (9): BuildInfo, git(), _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text() (+1 more)

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "MenuBar"
Cohesion: 0.03
Nodes (15): ButtonGroup, offered_sections(), bare_icon(), _FollowResize, global_buttons(), icon_button(), MenuBar, bar_button_height() (+7 more)

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "Packet"
Cohesion: 0.21
Nodes (13): dhcp_type(), dns_answers(), dns_question(), frame_kind(), info(), name(), payload_length(), ports() (+5 more)

### Community 17 - "open_in_browser"
Cohesion: 0.14
Nodes (5): open_in_browser(), ImportThemes, OpenAccessPointConfigInBrowser, OpenProjectRepository, ReportAnIssue

### Community 24 - "WorkspaceSorter"
Cohesion: 0.11
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 27 - "link_info"
Cohesion: 0.16
Nodes (9): handshake_message(), is_dot11_control(), is_filler(), is_lldp(), link_info(), link_summary(), meaningful_layer(), protocol() (+1 more)

### Community 28 - "ThemeEditorPage"
Cohesion: 0.05
Nodes (3): LookOnly, preview(), ThemeEditorPage

### Community 29 - "PacketColumnsModal"
Cohesion: 0.12
Nodes (5): RowZone, column_category(), is_column_available(), PacketColumnsModal, autosave()

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
Cohesion: 0.04
Nodes (14): NetworkDiagramCanvas, StripChart, form_order(), Scrollable, TextArea, panel(), HVACSlidersForm, SubmarineSlidersForm (+6 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "SelectBackground"
Cohesion: 0.18
Nodes (3): SelectBackground, SelectColorTheme, background_choices()

### Community 46 - "HVACChart"
Cohesion: 0.08
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.11
Nodes (4): NetFilterQueue, InterfaceManager, NMapper, job()

### Community 50 - "CombinedTable"
Cohesion: 0.05
Nodes (15): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+7 more)

### Community 53 - ".columnconfigure"
Cohesion: 0.06
Nodes (5): _Gaps, Builder, Builder, Builder, Builder

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
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 65 - "DefenderModbusBuffer"
Cohesion: 0.06
Nodes (3): DefenderMapBuffer, DefenderModbusBuffer, _PollUnpacker

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.09
Nodes (14): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient() (+6 more)

### Community 80 - "filter_overlay.py"
Cohesion: 0.12
Nodes (13): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+5 more)

### Community 81 - "json.py"
Cohesion: 0.09
Nodes (10): build_name(), main(), write_build_info(), HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac() (+2 more)

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 95 - "config_editor.py"
Cohesion: 0.20
Nodes (9): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), workspace_name_problems() (+1 more)

### Community 97 - "WindowControls"
Cohesion: 0.08
Nodes (4): CornerControls, SquareButtons, _Strip, WindowControls

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 103 - "Canvas"
Cohesion: 0.08
Nodes (3): Canvas, DefenderWorldMap, TriangleCanvas

### Community 104 - "ModbusBuffer"
Cohesion: 0.07
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 107 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.15
Nodes (3): _Dim, _FollowResize, _OnHide

### Community 113 - "transformations.py"
Cohesion: 0.11
Nodes (9): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line() (+1 more)

### Community 117 - "Process"
Cohesion: 0.04
Nodes (10): flush(), flush_all(), run(), _dialog_parent(), file_dialog(), Buffer, ProcessManager, Process (+2 more)

### Community 118 - "ToggleButton"
Cohesion: 0.04
Nodes (9): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleNetworkGraphRingView, ToggleStripChartAutoFit (+1 more)

### Community 121 - "KalmanToggleForm"
Cohesion: 0.23
Nodes (3): HVACKalmanToggleForm, KalmanToggleForm, SubmarineKalmanToggleForm

### Community 128 - "QWidget"
Cohesion: 0.11
Nodes (3): is_switch(), SettingCell, TopLayout

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "table.py"
Cohesion: 0.33
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 136 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 143 - "threading"
Cohesion: 0.06
Nodes (3): _is_global(), _resolve_local_mac(), NetFilterQueueBaseClass

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

### Community 167 - "ListZone"
Cohesion: 0.10
Nodes (5): CategoryChip, checkbox(), SectionCard, WorkspaceChip, ListZone

### Community 168 - "PopupWindow"
Cohesion: 0.06
Nodes (4): MaterialEditorPopup, ModalWindow, PopupWindow, Scrim

### Community 170 - "MainWindow"
Cohesion: 0.08
Nodes (3): MainWindow, NativeFrame, WindowEdges

### Community 171 - "ButtonModal"
Cohesion: 0.12
Nodes (6): EditModelStyle, EditStripChartStyle, EditWorkspaceAvailability, RefreshAndCloseOverlay, SettingsOverlayButton, ButtonModal

### Community 175 - "NoteBrowser"
Cohesion: 0.13
Nodes (3): read_note(), refresh_preview(), NoteBrowser

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.15
Nodes (3): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

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
Cohesion: 0.07
Nodes (8): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, WorkspaceSaveResetButton, confirm_dialog()

### Community 216 - "time"
Cohesion: 0.08
Nodes (11): random_spline_path(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+3 more)

### Community 261 - "router.py"
Cohesion: 0.05
Nodes (14): BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspaceSelectPage, WorkspacePage, NotFound (+6 more)

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1989 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **142 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `_base_button.py`, `ConfigureThisWorkspace`, `important_buttons/__init__.py`, `.start_session`, `router.py`, `LinkToPage`, `table.py`, `ClickManager`, `save_columns_as_default.py`, `Visual`, `MenuBar`, `threading`, `ShiftWheel`, `geometry.py`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `widgets/__init__.py`, `ButtonModal`, `.reload_preferences`, `Preferences`, `Performance`, `KeyBinds`, `AnimationManager`, `Router`, `InputManager`, `style.py`, `open_favorite_page.py`, `PageManager`, `filter_overlay.py`, `json.py`, `confirm_dialog`, `.reset_page`, `Style`, `config_editor.py`, `Json`, `Process`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.08419126058110273 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `_base_button.py`, `._build_stylesheet`, `.start_session`, `.lift_button`, `style.py`, `.theme_family`, `ButtonModal`, `open_favorite_page.py`, `MenuBar`, `.brush`, `_DressedWidgets`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `_base_button.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._