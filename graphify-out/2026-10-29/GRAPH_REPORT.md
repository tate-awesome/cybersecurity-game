# Graph Report - cybersecurity-game  (2026-10-29)

## Corpus Check
- 323 files · ~276,276 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .ino 8, .pcap 5, .pcapng 4)

## Summary
- 4863 nodes · 10368 edges · 245 communities (72 shown, 173 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 478 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c45640fa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContextManager
- CheckboxOverlay
- important_buttons/__init__.py
- MetaPacket
- Style
- Wifi
- SummaryDrawer
- describe.py
- modal.py
- paint_mark
- pyside6_qtcore
- Footer
- FilterModal
- QWidget
- Dev/Host_API.py
- ButtonModal
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
- .__init__
- ThemeEditorPage
- PacketColumnsModal
- AttackHMI_relay_ramp_attack.py
- FindBar
- geometry.py
- server.py
- .theme_family
- ._build_stylesheet
- Paths
- ConfigEditor
- docking.py
- LocalizationManager
- WifiForm
- wifi_windows.py
- WifiBaseClass
- HVACChart
- TabStrip
- NMapper
- LayoutEditor
- CombinedTable
- _DressedWidgets
- Preferences
- _Gaps
- .__init__
- HostOverlay
- Performance
- ViewPort
- Wifi
- QWidget
- Modify
- KeyBinds
- WrapLayout
- Router
- FadeIn
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
- App
- PageManager
- .brush
- packet_filter.py
- launch.py
- DragHandle
- _MapCanvas
- Draw
- PrivilegedHelper
- SettingsPage
- MapBuffer
- .start_session
- Draw
- _Grip
- Overlay
- PauseMenu
- .fixed_width_wrapper
- WaveGrid
- Context
- Camera
- VectorField
- palette_generator.py
- StatusBuffer
- compile_filter
- Replay
- Canvas
- .collapsed
- ListZone
- VariableModal
- Json
- ._draw_text
- ComboColumn
- _Dim
- NetFilterQueue
- .__init__
- ArpSpoofer
- ap_commands.py
- threading
- ToggleButton
- Prod/Host_API.py
- StripChartBase
- FlagsForm
- MaterialEditor
- QWidget
- AnimationManager
- PopupEntrance
- _Proxy
- .add_setting_row
- ConfigureThisWorkspace
- .strip_chart_layout
- .__init__
- combined.py
- Scanlines
- Builder
- .refresh_usage
- .columnconfigure
- CallbackRegistry
- .add_deadspace
- Meter
- MitmTable
- Denier
- time
- .__init__
- Table
- Builder
- Attack
- .__init__
- WindowDrag
- ShiftWheel
- .collect
- dist.py
- .build_description_tab
- Builder
- Kalman
- ._scan_for_networks
- MainWindow
- Master
- Slave
- ChoiceList
- leaf_of
- MaterialEditorPopup
- DragPayload
- PopupWindow
- VisualPalette
- WindowEdges
- NativeFrame
- AppearEffect
- NoteBrowser
- _Chip
- LookOnly
- .__init__
- CornerControls
- _RightZoneRoom
- .save_current_page
- panel
- ToggleLightDarkMode
- SectionCard
- WindowControls
- Map
- DropZone
- .new_tab
- .authored_weights
- .page_panel_keys
- transformations.py
- APPoller
- core/transforms.py
- .__init__
- PooledCanvasMixin
- frame_callback
- Proximity
- .setText
- paint_panel
- version.py
- _DropPreview
- SelectRegisterPreset
- _OnHide
- RefreshAndCloseOverlay
- ProcessManager
- ModalWindow
- fade_in
- os
- Scrim
- OpenFavoritePage
- StreamIncomingPacketsToMcap
- DenseMesh
- .workspace_button
- PreferencesData
- pyside6_qtwidgets
- .__init__
- Telemetry
- .play
- FreeScrollStatusConsole
- PausePacketConsole
- ToggleFullscreen
- ToggleNetworkGraphRingView
- Cyber-ICS Training Module
- .make_built_in
- GrowingButton

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

## Communities (245 total, 173 thin omitted)

### Community 0 - "ContextManager"
Cohesion: 0.08
Nodes (13): ContextManager, BoatMotion, make_workspace(), write_config_values(), Sprites, Triangle, TitlePage, WorkspaceSelectPage (+5 more)

### Community 1 - "CheckboxOverlay"
Cohesion: 0.10
Nodes (7): PanelButton, CheckboxOverlay, ChooseShownDefenderFlagForms, ChooseShownDefenderModbusForms, ChooseShownModbusTableForms, ChooseShownNetworkActionForms, ChooseShownPacketConsoleColumns

### Community 2 - "important_buttons/__init__.py"
Cohesion: 0.03
Nodes (38): AbortAllNetworkActions, ImportantButton, open_in_browser(), ClearAllCapturedBufferData, ClearModbusAndModelData, ClearNetworkHosts, ClearPacketConsole, ClearSavedWorkspaceInputs (+30 more)

### Community 3 - "MetaPacket"
Cohesion: 0.07
Nodes (5): Channel, Transaction, TransactionManager, MetaPacket, Builder

### Community 6 - "Wifi"
Cohesion: 0.11
Nodes (7): _in_nm_context(), Wifi, finish(), on_activated(), on_state_changed(), on_timeout(), cached()

### Community 8 - "describe.py"
Cohesion: 0.07
Nodes (30): dhcp_type(), dns_answers(), dns_question(), endpoints(), frame_kind(), handshake_message(), info(), is_dot11_control() (+22 more)

### Community 9 - "modal.py"
Cohesion: 0.05
Nodes (14): DeleteAllWorkspaceSavedData, column_position(), is_column_available(), shown_columns(), tray_columns(), SavePacketColumnsAsDefault, ask_to_quit(), QuitApplication (+6 more)

### Community 10 - "paint_mark"
Cohesion: 0.17
Nodes (3): bar_inset(), minimized_thickness(), paint_mark()

### Community 11 - "pyside6_qtcore"
Cohesion: 0.07
Nodes (5): draw_vessel(), apply_scale_about(), draw_glow(), Visual, background_choices()

### Community 12 - "Footer"
Cohesion: 0.07
Nodes (7): _FollowResize, Footer, on_off(), on_off(), _Quiet, set_text(), tooltip()

### Community 13 - "FilterModal"
Cohesion: 0.08
Nodes (3): FilterModal, label_key(), value_key()

### Community 15 - "Dev/Host_API.py"
Cohesion: 0.22
Nodes (8): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), set_target(), status()

### Community 16 - "ButtonModal"
Cohesion: 0.16
Nodes (5): EditBackgroundChoices, EditModelStyle, EditStripChartStyle, SettingsOverlayButton, ButtonModal

### Community 17 - "MenuBar"
Cohesion: 0.03
Nodes (15): ButtonGroup, offered_sections(), GoForwardToNextPage, ToggleBookmark, bare_icon(), _FollowResize, global_buttons(), icon_button() (+7 more)

### Community 20 - "PacketBuffer"
Cohesion: 0.06
Nodes (4): _default_gateway_ip(), _is_global(), NetworkGraph, PacketBuffer

### Community 21 - "VisualBackground"
Cohesion: 0.05
Nodes (8): Visuals, paint_abyss(), paint_noise_gradient(), paint_plasma(), _paint_through(), pyramid_blur(), value_noise(), VisualBackground

### Community 22 - "DefenderStatusBuffer"
Cohesion: 0.09
Nodes (3): APCommand, DefenderStatusBuffer, _PollUnpacker

### Community 23 - "SessionRecorder"
Cohesion: 0.06
Nodes (13): link_of(), action(), decode(), dumps(), header(), mark(), packet(), packet_from_meta() (+5 more)

### Community 24 - "WorkspaceSorter"
Cohesion: 0.09
Nodes (4): WorkspaceSorter, delete(), create(), rename()

### Community 26 - "SettingsSection"
Cohesion: 0.09
Nodes (6): checked_value(), is_checked(), SettingsSection, save(), save(), on_change()

### Community 29 - "PacketColumnsModal"
Cohesion: 0.13
Nodes (4): RowZone, column_category(), PacketColumnsModal, autosave()

### Community 31 - "FindBar"
Cohesion: 0.09
Nodes (3): FindBar, walk(), FindField

### Community 32 - "geometry.py"
Cohesion: 0.15
Nodes (5): get_arc_points(), get_bearing(), rotate(), scale(), translate()

### Community 33 - "server.py"
Cohesion: 0.08
Nodes (11): Sniffer, build_capability(), _Echo, _BufferShim, _ContextStub, _dispatch(), run(), flusher() (+3 more)

### Community 35 - "._build_stylesheet"
Cohesion: 0.08
Nodes (3): at_opacity(), shaded(), face()

### Community 36 - "Paths"
Cohesion: 0.14
Nodes (3): _dialog_parent(), file_dialog(), Paths

### Community 39 - "docking.py"
Cohesion: 0.13
Nodes (16): add_tab(), find(), from_tree(), split(), is_split(), leaf(), move_panel(), new_id() (+8 more)

### Community 43 - "WifiForm"
Cohesion: 0.11
Nodes (4): set_enabled(), set_read_only(), set_text(), WifiForm

### Community 44 - "wifi_windows.py"
Cohesion: 0.12
Nodes (17): DOT11_SSID, GUID, _guid_bytes(), WLAN_ASSOCIATION_ATTRIBUTES, WLAN_AVAILABLE_NETWORK, WLAN_AVAILABLE_NETWORK_LIST, WLAN_CONNECTION_ATTRIBUTES, WLAN_CONNECTION_NOTIFICATION_DATA (+9 more)

### Community 46 - "HVACChart"
Cohesion: 0.10
Nodes (4): DefenderHVACChart, follow_theme(), HVACChart, SniffedHVACChart

### Community 48 - "NMapper"
Cohesion: 0.09
Nodes (4): NetFilterQueue, NMapper, InterfaceManager, job()

### Community 54 - ".__init__"
Cohesion: 0.15
Nodes (9): _edge_distance(), display_name(), draw_arrow(), draw_chip(), draw_label(), frame_callback(), label_size(), place() (+1 more)

### Community 55 - "HostOverlay"
Cohesion: 0.14
Nodes (5): HostOverlay, autosave(), autosave(), reset_all(), shown()

### Community 57 - "ViewPort"
Cohesion: 0.13
Nodes (3): padded_fit_uniform(), zoom_and_pan(), ViewPort

### Community 58 - "Wifi"
Cohesion: 0.12
Nodes (5): _list_item(), Wifi, finish(), on_notification(), on_notification()

### Community 59 - "QWidget"
Cohesion: 0.09
Nodes (5): _LentPlaceholder, PeekArrow, _SideStrip, _SideTitle, TabbedPane

### Community 64 - "FadeIn"
Cohesion: 0.14
Nodes (3): DesktopFade, FadeIn, FadeOut

### Community 67 - ".leaf"
Cohesion: 0.13
Nodes (4): add(), click(), sync(), read()

### Community 69 - "SlidersForm"
Cohesion: 0.12
Nodes (5): push_submarine_settings(), submarine_settings_synced(), ShiftWheelSlider, SlidersForm, slider_callback()

### Community 73 - "themes.py"
Cohesion: 0.13
Nodes (10): button_radius(), is_hex(), _old_palette(), read_gradient(), read_theme(), resolve_materials(), shade(), style_setting() (+2 more)

### Community 80 - "packet_filter.py"
Cohesion: 0.11
Nodes (13): conjugate(), empty_state(), Field, FilterError, join_pair(), normal_value(), parse(), Parser (+5 more)

### Community 81 - "launch.py"
Cohesion: 0.18
Nodes (7): HelperHandle, _PopenHandle, spawn(), _spawn_linux(), _spawn_mac(), _spawn_windows(), _WindowsHandle

### Community 86 - "SettingsPage"
Cohesion: 0.05
Nodes (4): SettingsPage, save(), on_change(), SettingsSection

### Community 90 - "_Grip"
Cohesion: 0.15
Nodes (3): _Grip, _SashGrip, _ShadowWatch

### Community 91 - "Overlay"
Cohesion: 0.07
Nodes (3): SelectBackground, SelectColorTheme, Overlay

### Community 95 - "Context"
Cohesion: 0.11
Nodes (9): delete_workspace(), DeleteWorkspaceDialog, drop_unused_labels(), relist_workspace(), rename_workspace(), RenameWorkspaceDialog, workspace_folder(), workspace_labels() (+1 more)

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

### Community 116 - "ap_commands.py"
Cohesion: 0.09
Nodes (22): ap_tunnel_enabled(), ap_tunnel_key(), encryption_enabled(), encryption_key(), hvac_kalman_enabled(), _hvac_send(), kalman_enabled(), push_hvac_settings() (+14 more)

### Community 117 - "threading"
Cohesion: 0.07
Nodes (5): Buffer, _resolve_local_mac(), NetFilterQueueBaseClass, Process, RetentionPolicy

### Community 119 - "Prod/Host_API.py"
Cohesion: 0.21
Nodes (7): api_data(), dashboard(), _parse_packet(), receive_data(), send_command(), set_encryption(), status()

### Community 130 - ".strip_chart_layout"
Cohesion: 0.18
Nodes (6): choose_time_step(), decimals_for_step(), format_max_decimals(), format_tick(), nice_number(), nice_ticks()

### Community 132 - "combined.py"
Cohesion: 0.33
Nodes (3): align_decimals(), format_number(), fraction_width()

### Community 137 - "CallbackRegistry"
Cohesion: 0.13
Nodes (3): CallbackRegistry, ClickManager, _GlobalClickFilter

### Community 143 - "time"
Cohesion: 0.06
Nodes (3): DefenderMapBuffer, HouseBuffer, ModbusBuffer

### Community 146 - "Table"
Cohesion: 0.29
Nodes (4): Table, fill_order(), key(), spread_order()

### Community 148 - "Attack"
Cohesion: 0.18
Nodes (3): Attack, PreAttack, toggle_IP_Forward

### Community 155 - "dist.py"
Cohesion: 0.29
Nodes (3): build_name(), main(), write_build_info()

### Community 159 - "._scan_for_networks"
Cohesion: 0.36
Nodes (4): finish(), on_last_scan_changed(), on_scanned(), on_timeout()

### Community 167 - "DragPayload"
Cohesion: 0.11
Nodes (4): CategoryChip, checkbox(), WorkspaceChip, DragPayload

### Community 193 - ".authored_weights"
Cohesion: 0.33
Nodes (3): valid(), walk(), walk()

### Community 195 - "transformations.py"
Cohesion: 0.32
Nodes (3): canvas_fit(), padded_fit(), affine()

### Community 198 - "core/transforms.py"
Cohesion: 0.22
Nodes (5): padded_fit_uniform(), padded_fit_uniform_reverse(), shorten_line(), zoom_and_pan(), zoom_and_pan_reverse()

### Community 199 - ".__init__"
Cohesion: 0.11
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 201 - "frame_callback"
Cohesion: 0.67
Nodes (3): frame_callback(), sprite(), sprite_enabled()

### Community 206 - "paint_panel"
Cohesion: 0.10
Nodes (4): _Peek, blurred_shape(), paint_panel(), surface_shadow()

### Community 216 - "os"
Cohesion: 0.07
Nodes (3): flush(), flush_all(), run()

### Community 226 - "pyside6_qtwidgets"
Cohesion: 0.05
Nodes (26): DefenderWorldMap, House, StripChart, TriangleCanvas, WorldMap, form_order(), ToggleStripChartAutoFit, Scrollable (+18 more)

### Community 231 - ".play"
Cohesion: 0.60
Nodes (3): covered(), settle(), uncovered()

### Community 238 - "Cyber-ICS Training Module"
Cohesion: 0.25
Nodes (5): graphify, Cyber-ICS Training Module, Intended use, Repository layout, The game lives in [`game/`](game/)

## Knowledge Gaps
- **173 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextManager` connect `ContextManager` to `CheckboxOverlay`, `important_buttons/__init__.py`, `.__init__`, `combined.py`, `Style`, `CallbackRegistry`, `modal.py`, `pyside6_qtcore`, `time`, `MenuBar`, `PacketBuffer`, `ShiftWheel`, `Paths`, `docking.py`, `LocalizationManager`, `Preferences`, `Performance`, `KeyBinds`, `Router`, `InputManager`, `PageManager`, `PrivilegedHelper`, `ProcessManager`, `.start_session`, `os`, `.reset_page`, `pyside6_qtwidgets`, `Json`, `threading`, `AnimationManager`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ContextManager` (e.g. with `AnimationManager` and `ClickManager`) actually correct?**
  _`ContextManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `ContextManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07711711711711712 - nodes in this community are weakly interconnected._
- **Why does `Style` connect `Style` to `ContextManager`, `.theme_family`, `.__init__`, `._build_stylesheet`, `.theme_modes`, `important_buttons/__init__.py`, `.setting`, `.discard_changes`, `pyside6_qtcore`, `.brush`, `MenuBar`, `_DressedWidgets`, `.start_session`, `SettingsSection`, `Overlay`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Style` (e.g. with `ContextManager` and `SettingsSection`) actually correct?**
  _`Style` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `CheckboxOverlay` be split into smaller, more focused modules?**
  _Cohesion score 0.10160427807486631 - nodes in this community are weakly interconnected._
- **Why does `ConfigEditor` connect `ConfigEditor` to `ContextManager`, `.add_setting_row`, `.new_tab`, `.leaf`, `Rows`, `.section`, `pyside6_qtwidgets`, `.refresh_usage`, `ConfigureThisWorkspace`, `NoteBrowser`, `LayoutEditor`, `WorkspaceSorter`, `.collect`, `.build_description_tab`, `FindBar`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._