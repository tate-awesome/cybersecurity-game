from ._base_button import ImportantButton


class SaveToastPositionAsDefault(ImportantButton):
    '''
    Makes where the status toasts are on this page - wherever a toast was
    dragged to here - where they go on every page (see Toasts.save_anchor_as_default).
    Says so in a toast of its own.
    '''
    LABEL = "menu_bar_buttons_save_toast_position_button"
    TOOLTIP = "menu_bar_tooltips_save_toast_position_button"

    def on_click(self):
        self.context.toasts.save_anchor_as_default()
        self.context.buffer.put("toasts", self.context.labels.get("status_toasts_position_saved"))
