from ._base_button import ImportantButton


class AbortAllNetworkActions(ImportantButton):
    '''
    Stops every process in the process manager (wifi last - see its
    "stop_last" tag), then switches back to the home network even if this
    page has no Wi-Fi form (see ProcessManager.return_wifi_home). Each
    form's process button catches up on its own, from its
    refresh_process_button animation callback.
    '''
    LABEL = "menu_bar_buttons_abort_all"

    def on_click(self):
        self.context.process_manager.abort_all()
        self.context.process_manager.return_wifi_home()
