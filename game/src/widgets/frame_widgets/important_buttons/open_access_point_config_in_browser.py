from ._base_button import ImportantButton, open_in_browser


class OpenAccessPointConfigInBrowser(ImportantButton):
    '''Opens the AP's config web page in the user's browser.'''
    LABEL = "title_buttons_ap_page"
    TOOLTIP = "menu_bar_tooltips_ap_config_button"
    URL = "http://192.168.4.1"
    POPOUT = True

    def on_click(self):
        open_in_browser(self.URL)
