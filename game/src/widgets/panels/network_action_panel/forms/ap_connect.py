from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel
from .....app_core import Context
from .....network.hardware import APPoller, AP_POLLER_KEY
from ...base_form import BaseForm


class APConnectForm(BaseForm):
    '''
    Starts/stops the AP poller process and reports its live connected
    status - the panels-based counterpart to DefenderV0's URL entry +
    Connect button + connected dot. This is the one AP poller every
    defender widget shares (process_manager key AP_POLLER_KEY - DefenderV0
    reclaims the same one); the other defender forms never touch it
    directly, they queue commands on context.buffer.defender_status for it
    to send.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="ap_connect")
        # get_process() registers under this form's key - which has to be
        # the shared poller's key, or this would start a second poller.
        assert self.key == AP_POLLER_KEY
        self.process = self.get_process(APPoller)

        self.add_header()

        label, entry = self.add_labeled_entry("AP URL:")
        self.url_entry = entry

        # Slot 0 is the URL entry above (add_labeled_entry); slot 1 is
        # whether the poller is switched on, which decides whether it
        # auto-connects on startup.
        self.save_slots = self.context.states.get("network_action_form_inputs", self.key)
        if len(self.save_slots) < 2:  # saves from before slot 1 existed
            self.save_slots.append(0)

        def do_connect():
            self.save_slots[1] = 1
            url = self.url_entry.text().strip().rstrip("/")
            if url:
                self.process.url = url
            if not self.process.is_running():
                self.process.start()

        def do_disconnect():
            self.save_slots[1] = 0
            self.process.stop()

        self.add_process_row(do_connect, do_disconnect, self.process.is_running)

        self.conn_label = QLabel("")
        self.conn_label.setFont(self.style.get_font("small"))
        self.conn_label.setStyleSheet("color: gray;")
        self.conn_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.grid_layout.addWidget(self.conn_label, self.current_row, 1, 1, 2)
        self.current_row += 1

        self.context.animation_manager.add_callback(f"APConnectForm_{id(self)}", self._refresh_status)

        # Auto-connect on startup only if switched on in settings - skipped
        # if regained already-running across a refresh, so refreshing never
        # double-starts or interrupts it.
        if self.save_slots[1] and not self.process.is_running():
            self.click_start()

    def _refresh_status(self):
        if self.process.is_running() and self.process.connected:
            self.conn_label.setText("⬤  Connected")
            self.conn_label.setStyleSheet("color: green;")
        elif self.process.is_running():
            self.conn_label.setText("⬤  Waiting for response...")
            self.conn_label.setStyleSheet("color: orange;")
        else:
            self.conn_label.setText("")
