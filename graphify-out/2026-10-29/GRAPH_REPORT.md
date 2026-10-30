# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 324 files · ~278,496 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4901 nodes · 10446 edges · 229 communities (77 shown, 152 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 481 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `328717c9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- context_manager.py
- Style
- Wifi
- SummaryDrawer
- describe.py
- edit_workspace_availability.py
- .__init__
- Footer
- FilterModal
- Panes
- Dev/Host_API.py
- ButtonModal
- menu_bar.py
- PacketTreeview
- NetworkMesh
- PacketBuffer
- VisualBackground
- DefenderStatusBuffer
- SessionRecorder
- WorkspaceSorter
- .__init__
- SettingsSection
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- ._build_stylesheet
- WindowDrag
- ConfigEditor
- docking.py
- LocalizationManager
- network_activity/_builder.py
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- QWidget
- NetFilterQueue
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- filter_overlay.py
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- Draw
- Modify
- KeyBinds
- SettingsPage
- Router
- FadeIn
- DefenderModbusBuffer
- Rows
- .leaf
- SlidersForm
- InputManager
- FlowLayout
- CycleBox
- style.py
- Camera
- .__init__
- Constellation
- App
- PageManager
- NewWorkspaceDialog
- columns_overlay.py
- launch.py
- DragHandle
- _MapCanvas
- VariableModal
- PrivilegedHelper
- ModbusBuffer
- NMapper
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- .__init__
- Camera
- VectorField
- palette_generator.py
- compile_filter
- Replay
- Canvas
- .add_setting_row
- .collapsed
- DropZone
- StatusBuffer
- Json
- ._draw_text
- ComboColumn
- _Dim
- WindowEdges
- pathlib
- ArpSpoofer
- ap_commands.py
- Process
- TabStrip
- Prod/Host_API.py
- StripChartBase
- Scanlines
- MaterialEditor
- QWidget
- .collect
- PopupEntrance
- host.py
- transformations.py
- .integer
- .strip_chart_layout
- SmoothWheel
- DragPayload
- sys
- Builder
- .refresh_usage
- Scrollable
- AnimationManager
- ModalWindow
- Meter
- MitmTable
- Denier
- Scrim
- Paths
- Table
- Loader
- version.py
- APPoller
- Panel
- config_editor.py
- ShiftWheel
- .new_tab
- WindowBarButton
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- select_background.py
- Master
- Slave
- ChoiceList
- Visual
- MaterialEditorPopup
- SectionCard
- PopupWindow
- VisualPalette
- TextArea
- table.py
- HideEffect
- .arrow
- NoteBrowser
- WorkspaceButton
- _Chip
- LookOnly
- CornerControls
- .__init__
- _DropPreview
- .save_current_page
- panel
- ListZone
- MenuBar
- Map
- Builder
- frame_callback
- .authored_weights
- .page_panel_keys
- .build_menu_bar_section
- _OnHide
- .__init__
- PooledCanvasMixin
- NetworkDiagramCanvas
- fade_in
- bare_icon
- _DrawerLayout
- ModeForm
- paint_panel
- DockArea
- SelectRegisterPreset
- SettingsSection
- .make_built_in
- Attack
- WorkspaceSelectPage
- ToggleButton
- BaseForm
- Telemetry
- Cyber-ICS Training Module
- confirm_dialog
- TitlePage

## God Nodes (most connected - your core abstractions)
1. `ContextManager` - 147 edges
2. `Style` - 123 edges
3. `ImportantButton` - 114 edges
4. `Overlay` - 84 edges
5. `MenuBar` - 65 edges
6. `MetaPacket` - 63 edges
7. `ConfigEditor` - 62 edges
8. `BaseForm` - 60 edges
9. `DockArea` - 54 edges
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
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/network_activity/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
- 3-file cycle: `game/src/widgets/__init__.py -> game/src/widgets/panels/network_hosts/_builder.py -> game/src/widgets/panels/panel.py -> game/src/widgets/__init__.py`
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

## Communities (229 total, 152 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.08
Nodes (10): ContextManager, BoatMotion, Sprites, Triangle, WorkspacePage, NotFound, Page, House (+2 more)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.05
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, OpenFavoritePage

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (37): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearStatusConsole (+29 more)

### Community 3 - "MetaPacket"
Cohesion: 0.06
Nodes (5): Channel, NetworkGraph, Transaction, TransactionManager, MetaPacket

### Community 4 - "context_manager.py"
Cohesion: 0.05
Nodes (4): PreferencesData, _is_global(), _resolve_local_mac(), NetFilterQueueBaseClass

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (29): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+21 more)

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 14 - "Panes"
Cohesion: 0.11
Nodes (3): _SashCorners, _SashLight, Panes

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.10
Nodes (7): SelectColorTheme, EditBackgroundChoices, EditModelStyle, EditStripChartStyle, checked_value(), SettingsOverlayButton, ButtonModal

### Community 17 - "menu_bar.py"
Cohesion: 0.07
Nodes (11): minimized_thickness(), _SaveLayoutAsDefault, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault, ToggleBookmark, ShowHelpMessage, bar_button_height(), window_bar_button_height() (+3 more)

### Community 21 - "VisualBackground"
Cohesion: 0.07
Nodes (3): Visuals, pyramid_blur(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.08
Nodes (4): DefenderMapBuffer, APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.05
Nodes (12): link_of(), action(), dumps(), header(), mark(), packet(), packet_from_meta(), poll() (+4 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.10
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.11
Nodes (4): is_checked(), SettingsSection, save(), save()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.11
Nodes (6): RowZone, ChooseShownPacketConsoleColumns, column_category(), PacketColumnsModal, autosave(), on_change()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.22
Nodes (3): apply_scale_about(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.06
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "WindowDrag"
Cohesion: 0.12
Nodes (4): draw_window_bar_line(), SquareButtons, _Strip, WindowDrag

### Community 39 - "docking.py"
Cohesion: 0.14
Nodes (17): add_tab(), find(), from_tree(), split(), is_split(), leaf(), leaf_of(), move_panel() (+9 more)

### Community 42 - "network_activity/_builder.py"
Cohesion: 0.13
Nodes (4): StripChart, ToggleStripChartAutoFit, Builder, Builder

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 47 - "QWidget"
Cohesion: 0.08
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 53 - "filter_overlay.py"
Cohesion: 0.12
Nodes (13): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+5 more)

### Community 54 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.15
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 58 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 64 - "FadeIn"
Cohesion: 0.12
Nodes (6): DesktopFade, FadeIn, covered(), settle(), uncovered(), FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (5): read_note(), refresh_preview(), add(), read(), is_switch()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "style.py"
Cohesion: 0.09
Nodes (14): _StyledComboItems, StyleSignals, button_radius(), gradient_points(), is_hex(), mode_info(), _old_palette(), read_gradient() (+6 more)

### Community 79 - "NewWorkspaceDialog"
Cohesion: 0.14
Nodes (4): DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, workspace_name_problems()

### Community 80 - "columns_overlay.py"
Cohesion: 0.17
Nodes (5): column_position(), is_column_available(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 84 - "VariableModal"
Cohesion: 0.24
Nodes (3): VariableModal, autosave(), reset_all()

### Community 87 - "ModbusBuffer"
Cohesion: 0.06
Nodes (3): HouseBuffer, ModbusBuffer, MapBuffer

### Community 88 - "NMapper"
Cohesion: 0.18
Nodes (3): NMapper, InterfaceManager, job()

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 99 - "palette_generator.py"
Cohesion: 0.24
Nodes (9): _at_lightness(), borders(), contrast(), generate(), _hex(), _hls(), inset(), lightness() (+1 more)

### Community 101 - "compile_filter"
Cohesion: 0.14
Nodes (9): compile_filter(), build(), between(), side(), end(), end_matches(), nickname(), is_broadcast() (+1 more)

### Community 102 - "Replay"
Cohesion: 0.10
Nodes (3): dissect(), decode(), Replay

### Community 103 - "Canvas"
Cohesion: 0.14
Nodes (3): Canvas, DefenderWorldMap, WorldMap

### Community 111 - "_Dim"
Cohesion: 0.14
Nodes (3): _Dim, _Drawer, _FollowResize

### Community 116 - "ap_commands.py"
Cohesion: 0.09
Nodes (21): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+13 more)

### Community 117 - "Process"
Cohesion: 0.06
Nodes (8): flush(), flush_all(), run(), Buffer, ProcessManager, Process, FileStream, RetentionPolicy

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 123 - "QWidget"
Cohesion: 0.17
Nodes (3): Layer, PageTransition, TransitionOverlay

### Community 128 - "transformations.py"
Cohesion: 0.14
Nodes (7): canvas_fit(), padded_fit(), affine(), padded_fit_uniform(), padded_fit_uniform_reverse(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 133 - "sys"
Cohesion: 0.27
Nodes (3): build_name(), main(), write_build_info()

### Community 136 - "Scrollable"
Cohesion: 0.10
Nodes (3): Scrollable, Builder, Builder

### Community 137 - "AnimationManager"
Cohesion: 0.07
Nodes (4): AnimationManager, CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 150 - "Panel"
Cohesion: 0.11
Nodes (3): blurred_shape(), Panel, surface_shadow()

### Community 151 - "config_editor.py"
Cohesion: 0.11
Nodes (12): delete_workspace(), drop_unused_labels(), make_workspace(), relist_workspace(), rename_workspace(), workspace_folder(), workspace_labels(), write_config_values() (+4 more)

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 165 - "Visual"
Cohesion: 0.07
Nodes (11): draw_vessel(), get_arc_points(), get_bearing(), rotate(), paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through() (+3 more)

### Community 167 - "SectionCard"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), SectionCard, WorkspaceChip

### Community 172 - "table.py"
Cohesion: 0.33
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 192 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 199 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 206 - "paint_panel"
Cohesion: 0.10
Nodes (4): bar_inset(), paint_mark(), _Peek, paint_panel()

### Community 216 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 220 - "ToggleButton"
Cohesion: 0.05
Nodes (8): ToggleButton, FreeScrollStatusConsole, PausePacketConsole, StreamIncomingPacketsToMcap, ToggleDebugLabels, ToggleFullscreen, ToggleLightDarkMode, ToggleNetworkGraphRingView

### Community 226 - "BaseForm"
Cohesion: 0.11
Nodes (16): form_order(), BaseForm, FlagsForm, HVACFlagsForm, SubmarineFlagsForm, HVACSlidersForm, SubmarineSlidersForm, APConnectForm (+8 more)

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

### Community 239 - "confirm_dialog"
Cohesion: 0.07
Nodes (7): ClearSavedWorkspaceInputs, DeleteAllUserData, DeleteAllWorkspaceSavedData, ask_to_quit(), QuitApplication, WorkspaceSaveResetButton, confirm_dialog()

### Community 261 - "TitlePage"
Cohesion: 0.08
Nodes (4): TitlePage, TitleFooter, GrowingButton, TitleMenu

## Knowledge Gaps
- **152 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `CheckboxOverlay`, `important_buttons/__init__.py`, `SmoothWheel`, `context_manager.py`, `Style`, `AnimationManager`, `Paths`, `menu_bar.py`, `ButtonModal`, `config_editor.py`, `ShiftWheel`, `geometry.py`, `Visual`, `docking.py`, `LocalizationManager`, `network_activity/_builder.py`, `table.py`, `Preferences`, `filter_overlay.py`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `style.py`, `PageManager`, `columns_overlay.py`, `PrivilegedHelper`, `.reset_page`, `BaseForm`, `Json`, `confirm_dialog`, `Process`, `host.py`?**
  _High betweenness centrality (0.239) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07582417582417582 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `CheckboxOverlay`, `.brush`, `._build_stylesheet`, `context_manager.py`, `.lift_button`, `important_buttons/__init__.py`, `style.py`, `.discard_changes`, `.theme_family`, `ButtonModal`, `menu_bar.py`, `_DressedWidgets`, `ShiftWheel`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.04745762711864407 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `ContextManager`, `Rows`, `.leaf`, `.build_menu_bar_section`, `.section`, `important_buttons/__init__.py`, `.refresh_usage`, `.add_setting_row`, `NoteBrowser`, `LayoutEditor`, `config_editor.py`, `WorkspaceSorter`, `.new_tab`, `WorkspaceSelectPage`, `.collect`, `FindBar`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._