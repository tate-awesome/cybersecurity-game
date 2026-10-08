from ._base_button import ImportantButton


class LoadLocalizationLabelsFile(ImportantButton):
    '''Asks for a labels JSON file, merges it over the current labels, and remembers it.'''
    LABEL = "menu_bar_buttons_labels_button"
    TOOLTIP = "menu_bar_tooltips_labels_button"

    def on_click(self):
        self.context.labels.select()
