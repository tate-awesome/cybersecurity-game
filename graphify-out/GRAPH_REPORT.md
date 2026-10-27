# Graph Report - cybersecurity-game  (2026-10-26)

## Corpus Check
- 323 files · ~274,708 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4848 nodes · 10005 edges · 259 communities (67 shown, 192 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 466 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5addcdaa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- ButtonModal
- important_buttons/__init__.py
- MetaPacket
- .apply_theme
- _base_button.py
- _in_nm_context
- .build_summary
- describe.py
- message
- paint_mark
- VisualPalette
- Footer
- FilterModal
- MenuBar
- ap_commands.py
- frame_callback
- Panel
- PacketTreeview
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
- server.py
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
- ListZone
- HostOverlay
- Performance
- ViewPort
- wifi_windows.py
- QWidget
- Modify
- KeyBinds
- Router
- FadeOut
- DefenderModbusBuffer
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
- .build_appearance_tab
- SettingsPage
- Draw
- _Grip
- Overlay
- WaveGrid
- Context
- Camera
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
- SectionCard
- FileStream
- ToggleButton
- SummaryDrawer
- StripChartBase
- KalmanToggleForm
- BaseForm
- QWidget
- .shadow_rows
- PopupEntrance
- _Proxy
- .add_setting_row
- .new_tab
- time_core/transforms.py
- place
- Map
- Builder
- .refresh_usage
- .__init__
- CallbackRegistry
- WindowDrag
- Wifi
- Meter
- bare_icon
- Denier
- sys
- StripChartLayout
- GrowingButton
- Style
- Paths
- Attack
- ToggleLightDarkMode
- .connect_to_saved_wifi
- Builder
- ShiftWheel
- .collect
- .integer
- MaterialEditorPopup
- PauseMenu
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
- Proximity
- WindowEdges
- SelectRegisterPreset
- _OnHide
- AppearEffect
- Scanlines
- NoteBrowser
- _Chip
- .build_menu_bar_section
- Process
- NewWorkspaceDialog
- _RightZoneRoom
- .save_current_page
- MaterialEditor
- .columnconfigure
- RefreshAndCloseOverlay
- AnimationManager
- DragPayload
- .__init__
- .authored_weights
- .page_panel_keys
- MainWindow
- .__init__
- PooledCanvasMixin
- .__init__
- WindowBarButton
- background.py
- OpenFavoritePage
- paint_panel
- Builder
- DenseMesh
- SettingsSection
- Draw
- confirm_dialog
- LookOnly
- conjugate
- time
- APConnectForm
- EncryptionForm
- SelectBackground
- .__init__
- ElidingLabel
- PreferencesData
- CLAUDE.md
- ModalWindow
- Scrim
- core/transforms.py

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

## Communities (259 total, 192 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.07
Nodes (15): ContextManager, BoatMotion, Sprites, Triangle, Visuals, TitlePage, WorkspaceSelectPage, WorkspacePage (+7 more)

### Community 1 - "ButtonModal"
Cohesion: 0.16
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.02
Nodes (40): AbortAllNetworkActions, ImportantButton, ButtonGroup, offered_sections(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole (+32 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (4): Channel, Transaction, TransactionManager, MetaPacket

### Community 5 - "_base_button.py"
Cohesion: 0.06
Nodes (12): open_in_browser(), PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ImportThemes (+4 more)

### Community 8 - "describe.py"
Cohesion: 0.06
Nodes (31): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+23 more)

### Community 10 - "paint_mark"
Cohesion: 0.18
Nodes (4): bar_inset(), minimized_thickness(), paint_mark(), bar_button_height()

### Community 11 - "VisualPalette"
Cohesion: 0.07
Nodes (5): draw_vessel(), draw_glow(), Visual, VisualPalette, Telemetry

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 15 - "ap_commands.py"
Cohesion: 0.07
Nodes (33): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status() (+25 more)

### Community 16 - "frame_callback"
Cohesion: 0.16
Nodes (8): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), ring_spots()

### Community 17 - "Panel"
Cohesion: 0.11
Nodes (6): StripChart, TextArea, panel(), Panel, Builder, Builder

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
Cohesion: 0.08
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.09
Nodes (8): RowZone, column_category(), column_position(), is_column_available(), PacketColumnsModal, autosave(), shown_columns(), tray_columns()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 33 - "server.py"
Cohesion: 0.06
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.07
Nodes (3): at_opacity(), shaded(), face()

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

### Community 50 - "CombinedTable"
Cohesion: 0.06
Nodes (6): CombinedTable, entry(), align_decimals(), format_number(), fraction_width(), MitmTable

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 58 - "wifi_windows.py"
Cohesion: 0.06
Nodes (22): DOT11_SSID, GUID, _guid_bytes(), _list_item(), Wifi, finish(), on_notification(), on_notification() (+14 more)

### Community 59 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeOut"
Cohesion: 0.13
Nodes (5): DesktopFade, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.14
Nodes (3): ShiftWheelSlider, SlidersForm, slider_callback()

### Community 71 - "FlowLayout"
Cohesion: 0.05
Nodes (4): FlowLayout, WrapLayout, _Gaps, Builder

### Community 73 - "themes.py"
Cohesion: 0.11
Nodes (11): button_radius(), is_hex(), mode_info(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade() (+3 more)

### Community 77 - "app.py"
Cohesion: 0.15
Nodes (3): App, FadeIn, __getattr__()

### Community 80 - "packet_filter.py"
Cohesion: 0.13
Nodes (11): empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser, split_outside_quotes() (+3 more)

### Community 81 - "launch.py"
Cohesion: 0.09
Nodes (12): build_name(), main(), write_build_info(), BuildInfo, git(), HelperHandle, _PopenHandle, spawn() (+4 more)

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

### Community 107 - "VariableModal"
Cohesion: 0.20
Nodes (3): VariableModal, autosave(), reset_all()

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 113 - "geometry.py"
Cohesion: 0.08
Nodes (13): canvas_fit(), padded_fit(), padded_fit_uniform(), zoom_and_pan(), affine(), apply_scale_about(), get_arc_points(), get_bearing() (+5 more)

### Community 114 - "threading"
Cohesion: 0.08
Nodes (3): ModbusBuffer, _is_global(), _resolve_local_mac()

### Community 118 - "ToggleButton"
Cohesion: 0.03
Nodes (11): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, SetCurrentPageAsFavorite, ToggleBookmark, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen (+3 more)

### Community 122 - "BaseForm"
Cohesion: 0.09
Nodes (15): form_order(), Scrollable, BaseForm, HVACKalmanToggleForm, SubmarineKalmanToggleForm, ModeForm, HVACSlidersForm, SubmarineSlidersForm (+7 more)

### Community 130 - "time_core/transforms.py"
Cohesion: 0.17
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 131 - "place"
Cohesion: 0.22
Nodes (5): place(), Table, fill_order(), key(), spread_order()

### Community 137 - "CallbackRegistry"
Cohesion: 0.09
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 138 - "WindowDrag"
Cohesion: 0.12
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowDrag

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

### Community 167 - "WorkspaceChip"
Cohesion: 0.16
Nodes (3): CategoryChip, checkbox(), WorkspaceChip

### Community 179 - "Process"
Cohesion: 0.06
Nodes (4): NetFilterQueueBaseClass, ProcessManager, Process, Loader

### Community 180 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - ".__init__"
Cohesion: 0.33
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 203 - "WindowBarButton"
Cohesion: 0.13
Nodes (3): CornerControls, WindowBarButton, WindowControls

### Community 204 - "background.py"
Cohesion: 0.13
Nodes (6): paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise()

### Community 206 - "paint_panel"
Cohesion: 0.12
Nodes (3): blurred_shape(), paint_panel(), surface_shadow()

### Community 212 - "confirm_dialog"
Cohesion: 0.05
Nodes (11): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication, ResetCurrentPageToDefaults, SaveLayoutShapeAsDefault (+3 more)

### Community 216 - "time"
Cohesion: 0.08
Nodes (15): flush(), flush_all(), run(), Buffer, action(), decode(), dumps(), header() (+7 more)

## Knowledge Gaps
- **15 isolated node(s):** `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST`, `WLAN_AVAILABLE_NETWORK`, `WLAN_AVAILABLE_NETWORK_LIST` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1982 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **192 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `important_buttons/__init__.py`, `_base_button.py`, `CallbackRegistry`, `Panel`, `Style`, `Paths`, `ShiftWheel`, `.start_session`, `server.py`, `SmoothWheel`, `docking.py`, `LocalizationManager`, `Process`, `Preferences`, `Performance`, `KeyBinds`, `AnimationManager`, `Router`, `InputManager`, `background.py`, `PageManager`, `confirm_dialog`, `.reset_page`, `PrivilegedHelper`, `time`, `Json`, `threading`, `BaseForm`?**
  _High betweenness centrality (0.239) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DOT11_SSID`, `WLAN_INTERFACE_INFO`, `WLAN_INTERFACE_INFO_LIST` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07048054919908467 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `important_buttons/__init__.py`, `._build_stylesheet`, `.apply_theme`, `_base_button.py`, `.discard_changes`, `Overlay`, `.brush`, `_DressedWidgets`, `.lift_button`, `SettingsSection`, `.start_session`, `.theme_family`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `important_buttons/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.023990683229813663 - nodes in this community are weakly interconnected._