from ._base_button import ImportantButton


class AbortAllNetworkActions(ImportantButton):
    '''
    Stops every process in the process manager (wifi last - see its
    "stop_last" tag). Each form's process button catches up on its own,
    from its refresh_process_button animation callback.
    '''
    LABEL = "menu_bar_buttons_abort_all"

    def on_click(self):
        self.context.process_manager.abort_all()
