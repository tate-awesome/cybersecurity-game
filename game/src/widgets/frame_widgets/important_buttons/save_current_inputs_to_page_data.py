from ._base_button import ImportantButton


class SaveCurrentInputsToPageData(ImportantButton):
    '''Saves the current page's checkboxes and entries to its user_data inputs.json.'''
    LABEL = "menu_bar_buttons_fields_button"
    TOOLTIP = "menu_bar_tooltips_fields_button"

    def on_click(self):
        self.context.states.save_inputs()
