from ...popup import confirm_dialog
from ._base_button import ImportantButton


class ResetCurrentPageToDefaults(ImportantButton):
    '''
    Wipes this session back to defaults: the current page's autosaved
    settings/panes (see PageManager.save_current_page) and session-level
    state. Refreshes without re-autosaving first (save=False), so the
    current page's now-deleted data isn't immediately recreated from
    whatever was on screen - the rebuilt page picks up its own config.json
    defaults instead (see PageManager.prepare_page_config).
    '''
    LABEL = "menu_bar_buttons_reset_button"
    TOOLTIP = "menu_bar_tooltips_reset_button"
    MESSAGE = ("Reset this page to its defaults?\n"
               "Everything you changed here - inputs, layout, settings - goes back to how it started.")

    def on_click(self):
        '''Asks first - there's no undoing it.'''
        confirm_dialog(self.window(), self.context, self.MESSAGE, "Yes, reset", "No, cancel", self.reset)

    def reset(self):
        context = self.context
        if context.router.current_page is not None:
            context.pages.delete_saved_page(context.router.current_page)
        context.reset_session()
        # context.preferences.clear()
        context.router.refresh(save=False)
