import os, subprocess, webbrowser
from ._base_button import ImportantButton


class OpenAccessPointConfigInBrowser(ImportantButton):
    '''Opens the AP's config web page in the user's browser.'''
    LABEL = "title_buttons_ap_page"
    TOOLTIP = "menu_bar_tooltips_ap_config_button"
    URL = "http://192.168.4.1"
    POPOUT = True

    def on_click(self):
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user:
            # Open browser as not sudo
            subprocess.Popen(["sudo", "-u", sudo_user, "xdg-open", self.URL])
        else:
            # Fallback when not running under sudo
            webbrowser.open(self.URL)
