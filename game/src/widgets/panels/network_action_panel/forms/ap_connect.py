from customtkinter import CTkFrame, CTkLabel
from .....app_core import Context
from .....network.hardware import APPoller
from ...base_form import BaseForm


class APConnectForm(BaseForm):
    '''
    Starts/stops the AP poller process and reports its live connected
    status - the panels-based counterpart to DefenderV0's URL entry +
    Connect button + connected dot, but as a network_action_panel form so
    every other defender form can reach the same process by name
    (context.process_manager.get_process("ap_connect")).
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, key="ap_connect")
        self.process = self.get_process(APPoller)

        self.add_header()

        label, entry = self.add_labeled_entry("AP URL:")
        self.url_entry = entry

        def do_connect():
            url = self.url_entry.get().strip().rstrip("/")
            if url:
                self.process.url = url
            if not self.process.is_running():
                self.process.start()

        self.add_attack_button(do_connect, self.process.stop, self.process.is_running)

        self.conn_label = CTkLabel(self, text="", font=self.style.get_font("small"), text_color="gray")
        self.conn_label.grid(row=self.current_row, column=1, columnspan=2, sticky="e",
                              padx=self.style.gap, pady=self.style.gapbot)
        self.current_row += 1

        self.context.animation_manager.add_callback(f"APConnectForm_{id(self)}", self._refresh_status)

        # Auto-connect on first visit, matching the old defender page's
        # behavior of starting the poller immediately on page load - a
        # no-op (via is_running()) if regained already-running across a
        # refresh, so refreshing never double-starts or interrupts it.
        if not self.process.is_running():
            self.click_start()

    def _refresh_status(self):
        if self.process.is_running() and self.process.connected:
            self.conn_label.configure(text="⬤  Connected", text_color="green")
        elif self.process.is_running():
            self.conn_label.configure(text="⬤  Waiting for response...", text_color="orange")
        else:
            self.conn_label.configure(text="")
