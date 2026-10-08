from ....app_core import Context
from ._base_button import ImportantButton


class ConfigureThisWorkspace(ImportantButton):
    '''Opens the workspace editor on the workspace currently showing (Back returns here).'''
    LABEL = "menu_bar_buttons_configure_workspace_button"
    TOOLTIP = "menu_bar_tooltips_configure_workspace_button"

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return context.pages.get_build_type(context.router.current_page) == "workspace"

    def on_click(self):
        # Imported here - the editor page imports widgets, which import this
        from ....pages.demo.config_editor import ConfigEditor
        ConfigEditor.selected_key = self.context.router.current_page
        ConfigEditor.selected_tab = 0
        self.context.router.show("demo/config_editor")
