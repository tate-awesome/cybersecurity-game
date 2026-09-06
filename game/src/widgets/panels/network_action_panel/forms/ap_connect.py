from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel
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

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="ap_connect")
        self.process = self.get_process(APPoller)

        self.add_header()

        label, entry = self.add_labeled_entry("AP URL:")
        self.url_entry = entry

        def do_connect():
            url = self.url_entry.text().strip().rstrip("/")
            if url:
                self.process.url = url
            if not self.process.is_running():
                self.process.start()

        self.add_process_row(do_connect, self.process.stop, self.process.is_running)

        self.conn_label = QLabel("")
        self.conn_label.setFont(self.style.get_font("small"))
        self.conn_label.setStyleSheet("color: gray;")
        self.conn_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.grid_layout.addWidget(self.conn_label, self.current_row, 1, 1, 2)
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
            self.conn_label.setText("⬤  Connected")
            self.conn_label.setStyleSheet("color: green;")
        elif self.process.is_running():
            self.conn_label.setText("⬤  Waiting for response...")
            self.conn_label.setStyleSheet("color: orange;")
        else:
            self.conn_label.setText("")
