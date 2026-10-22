from ._base_button import ImportantButton


class OpenMaterialEditor(ImportantButton):
    '''Developers: opens the theme editor's Materials tab in a popup window over the current page (see MaterialEditorPopup).'''
    LABEL = "menu_bar_buttons_material_editor_button"
    TOOLTIP = "menu_bar_tooltips_material_editor_button"
    OPENS = "popup"

    def on_click(self):
        from ....pages.material_editor import MaterialEditorPopup  # here - pages import this package
        MaterialEditorPopup.show_for(self.context)
