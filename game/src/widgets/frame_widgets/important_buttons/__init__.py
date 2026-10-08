'''
Every important button, each the single source of truth for its label,
tooltip, and behavior - see ImportantButton. Place one with
MenuBar.add_important / TitleMenu.add_important, or add it to any layout.
'''
from ._base_button import ImportantButton, ToggleButton

from .quit_application import QuitApplication
from .go_back_to_previous_page import GoBackToPreviousPage
from .refresh_current_page import RefreshCurrentPage
from .reset_current_page_to_defaults import ResetCurrentPageToDefaults
from .toggle_light_dark_mode import ToggleLightDarkMode
from .select_color_theme import SelectColorTheme
from .load_pcap_into_packet_buffer import LoadPcapIntoPacketBuffer
from .save_current_packet_buffer_to_mcap import SaveCurrentPacketBufferToMcap
from .load_packet_buffer_from_mcap import LoadPacketBufferFromMcap
from .stream_incoming_packets_to_mcap import StreamIncomingPacketsToMcap
from .load_settings_preset_file import LoadSettingsPresetFile
from .load_localization_labels_file import LoadLocalizationLabelsFile
from .show_help_message import ShowHelpMessage
from .save_current_inputs_to_page_data import SaveCurrentInputsToPageData
from .set_current_page_as_favorite import SetCurrentPageAsFavorite
from .delete_all_workspace_saved_data import DeleteAllWorkspaceSavedData
from .open_workspace_editor import OpenWorkspaceEditor

from .link_to_page import LinkToPage
from .open_favorite_page import OpenFavoritePage
from .open_access_point_config_in_browser import OpenAccessPointConfigInBrowser
from .delete_all_user_data import DeleteAllUserData

from .clear_modbus_and_model_data import ClearModbusAndModelData
from .toggle_strip_chart_auto_fit import ToggleStripChartAutoFit
from .abort_all_network_actions import AbortAllNetworkActions
from .pause_packet_console import PausePacketConsole
from .free_scroll_status_console import FreeScrollStatusConsole
from .clear_all_captured_buffer_data import ClearAllCapturedBufferData
from .checkbox_overlay.choose_shown_network_action_forms import ChooseShownNetworkActionForms
from .checkbox_overlay.choose_shown_modbus_table_forms import ChooseShownModbusTableForms
from .checkbox_overlay.choose_shown_defender_modbus_forms import ChooseShownDefenderModbusForms
from .checkbox_overlay.choose_shown_packet_console_columns import ChooseShownPacketConsoleColumns
from .edit_modbus_register_display.edit_modbus_register_display import EditModbusRegisterDisplay
from .filter_packet_console.filter_packet_console import FilterPacketConsole

from .clear_saved_workspace_inputs import ClearSavedWorkspaceInputs
from .reset_saved_workspace_layout import ResetSavedWorkspaceLayout
from .toggle_debug_labels import ToggleDebugLabels
from .settings_overlays.edit_model_style import EditModelStyle
from .settings_overlays.edit_strip_chart_style import EditStripChartStyle
from .settings_overlays.edit_workspace_availability import EditWorkspaceAvailability

# The names a page config's "menu_bar" list uses, in the standard
# left-to-right order: preferences, data tools, page actions, then
# navigation (back, quit) on the right. Leftmost buttons are squashed into
# the overflow menu first.
MENU_BAR_BUTTONS: dict[str, type[ImportantButton]] = {
    "toggle_button": ToggleLightDarkMode,
    "theme_button": SelectColorTheme,
    "labels_button": LoadLocalizationLabelsFile,
    "page_button": SetCurrentPageAsFavorite,
    "pcap_button": LoadPcapIntoPacketBuffer,
    "save_button": SaveCurrentPacketBufferToMcap,
    "load_button": LoadPacketBufferFromMcap,
    "stream_button": StreamIncomingPacketsToMcap,
    "preset_button": LoadSettingsPresetFile,
    "data_button": SaveCurrentInputsToPageData,
    "workspace_editor_button": OpenWorkspaceEditor,
    "delete_all_workspace_data_button": DeleteAllWorkspaceSavedData,
    "model_style_button": EditModelStyle,
    "strip_chart_style_button": EditStripChartStyle,
    "debug_labels_button": ToggleDebugLabels,
    "debug_availability_button": EditWorkspaceAvailability,
    "clear_inputs_button": ClearSavedWorkspaceInputs,
    "reset_layout_button": ResetSavedWorkspaceLayout,
    "refresh_button": RefreshCurrentPage,
    "reset_button": ResetCurrentPageToDefaults,
    "help_button": ShowHelpMessage,
    "back_button": GoBackToPreviousPage,
    "quit_button": QuitApplication,
}

# Every menu bar button a standard game page gets (see MenuBar.page_buttons)
PAGE_BUTTONS: tuple[type[ImportantButton], ...] = tuple(
    button for button in MENU_BAR_BUTTONS.values()
    if button not in (OpenWorkspaceEditor, DeleteAllWorkspaceSavedData, EditModelStyle, EditStripChartStyle,
                      ToggleDebugLabels, EditWorkspaceAvailability, ClearSavedWorkspaceInputs, ResetSavedWorkspaceLayout)
)

# The names a title page config's {"action": ...} buttons use
TITLE_ACTIONS: dict[str, type[ImportantButton]] = {
    "back": GoBackToPreviousPage,
    "quit": QuitApplication,
    "resume": OpenFavoritePage,
    "open_ap_config": OpenAccessPointConfigInBrowser,
    "delete_user_data": DeleteAllUserData,
}
