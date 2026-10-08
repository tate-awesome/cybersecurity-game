'''
Every important button, each the single source of truth for its label,
tooltip, and behavior - see ImportantButton. Place one with
MenuBar.add_important / TitleMenu.add_important, or add it to any layout.
'''
from ._base_button import ImportantButton, ToggleButton
from .button_group import ButtonGroup

# Help
from .show_help_message import ShowHelpMessage
from .load_localization_labels_file import LoadLocalizationLabelsFile

# Navigation
from .set_current_page_as_favorite import SetCurrentPageAsFavorite
from .open_access_point_config_in_browser import OpenAccessPointConfigInBrowser
from .go_back_to_previous_page import GoBackToPreviousPage
from .open_workspace_select import OpenWorkspaceSelect
from .open_title_page import OpenTitlePage
from .quit_application import QuitApplication
from .link_to_page import LinkToPage
from .open_favorite_page import OpenFavoritePage

# Workspace
from .refresh_current_page import RefreshCurrentPage
from .clear_saved_workspace_inputs import ClearSavedWorkspaceInputs
from .reset_saved_workspace_layout import ResetSavedWorkspaceLayout
from .reset_current_page_to_defaults import ResetCurrentPageToDefaults
from .load_settings_preset_file import LoadSettingsPresetFile
from .checkbox_overlay.choose_shown_network_action_forms import ChooseShownNetworkActionForms
from .checkbox_overlay.choose_shown_modbus_table_forms import ChooseShownModbusTableForms
from .checkbox_overlay.choose_shown_defender_modbus_forms import ChooseShownDefenderModbusForms
from .checkbox_overlay.choose_shown_packet_console_columns import ChooseShownPacketConsoleColumns

# Style
from .toggle_light_dark_mode import ToggleLightDarkMode
from .select_color_theme import SelectColorTheme
from .settings_overlays.edit_model_style import EditModelStyle
from .settings_overlays.edit_strip_chart_style import EditStripChartStyle

# Captures
from .load_pcap_into_packet_buffer import LoadPcapIntoPacketBuffer
from .load_mcap_into_packet_buffer import LoadMcapIntoPacketBuffer
from .stream_pcap_into_packet_buffer import StreamPcapIntoPacketBuffer
from .stream_mcap_into_packet_buffer import StreamMcapIntoPacketBuffer
from .save_current_packet_buffer_to_mcap import SaveCurrentPacketBufferToMcap
from .stream_incoming_packets_to_mcap import StreamIncomingPacketsToMcap
from .clear_status_console import ClearStatusConsole
from .clear_packet_console import ClearPacketConsole
from .clear_modbus_and_model_data import ClearModbusAndModelData
from .clear_all_captured_buffer_data import ClearAllCapturedBufferData

# ModBus
from .edit_modbus_register_display.edit_modbus_register_display import EditModbusRegisterDisplay
from .settings_overlays.select_register_preset import SelectRegisterPreset

# Debug
from .delete_all_user_data import DeleteAllUserData
from .delete_all_workspace_saved_data import DeleteAllWorkspaceSavedData
from .open_workspace_editor import OpenWorkspaceEditor
from .configure_this_workspace import ConfigureThisWorkspace
from .settings_overlays.edit_workspace_availability import EditWorkspaceAvailability
from .toggle_debug_labels import ToggleDebugLabels

# Panel menu bars only
from .toggle_strip_chart_auto_fit import ToggleStripChartAutoFit
from .abort_all_network_actions import AbortAllNetworkActions
from .pause_packet_console import PausePacketConsole
from .free_scroll_status_console import FreeScrollStatusConsole
from .filter_packet_console.filter_packet_console import FilterPacketConsole

# The names a page config's "menu_bar" list uses. Where each one goes - its
# group and order - is MenuBar.MENU_BAR_GROUPS.
MENU_BAR_BUTTONS: dict[str, type[ImportantButton]] = {
    # Help
    "help_button": ShowHelpMessage,
    "labels_button": LoadLocalizationLabelsFile,
    # Navigation
    "page_button": SetCurrentPageAsFavorite,
    "ap_config_button": OpenAccessPointConfigInBrowser,
    "back_button": GoBackToPreviousPage,
    "workspaces_button": OpenWorkspaceSelect,
    "title_button": OpenTitlePage,
    "quit_button": QuitApplication,
    # Workspace
    "refresh_button": RefreshCurrentPage,
    "clear_inputs_button": ClearSavedWorkspaceInputs,
    "reset_layout_button": ResetSavedWorkspaceLayout,
    "reset_button": ResetCurrentPageToDefaults,
    "preset_button": LoadSettingsPresetFile,
    "network_forms_button": ChooseShownNetworkActionForms,
    "modbus_forms_button": ChooseShownModbusTableForms,
    "defender_forms_button": ChooseShownDefenderModbusForms,
    "packet_columns_button": ChooseShownPacketConsoleColumns,
    # Style
    "toggle_button": ToggleLightDarkMode,
    "theme_button": SelectColorTheme,
    "model_style_button": EditModelStyle,
    "strip_chart_style_button": EditStripChartStyle,
    # Captures
    "pcap_button": LoadPcapIntoPacketBuffer,
    "load_json_fast_button": LoadMcapIntoPacketBuffer,
    "stream_pcap_button": StreamPcapIntoPacketBuffer,
    "load_button": StreamMcapIntoPacketBuffer,
    "save_button": SaveCurrentPacketBufferToMcap,
    "stream_button": StreamIncomingPacketsToMcap,
    "clear_status_button": ClearStatusConsole,
    "clear_packet_console_button": ClearPacketConsole,
    "clear_modbus_button": ClearModbusAndModelData,
    "clear_all_button": ClearAllCapturedBufferData,
    # ModBus
    "registers_button": EditModbusRegisterDisplay,
    "register_preset_button": SelectRegisterPreset,
    # Debug
    "delete_all_user_data_button": DeleteAllUserData,
    "delete_all_workspace_data_button": DeleteAllWorkspaceSavedData,
    "workspace_editor_button": OpenWorkspaceEditor,
    "configure_workspace_button": ConfigureThisWorkspace,
    "debug_availability_button": EditWorkspaceAvailability,
    "debug_labels_button": ToggleDebugLabels,
}

# The names a title page config's {"action": ...} buttons use
TITLE_ACTIONS: dict[str, type[ImportantButton]] = {
    "back": GoBackToPreviousPage,
    "quit": QuitApplication,
    "resume": OpenFavoritePage,
    "open_ap_config": OpenAccessPointConfigInBrowser,
    "delete_user_data": DeleteAllUserData,
}
