from PySide6.QtWidgets import QLineEdit, QWidget
from .....app_core import Context
from .....network.hardware import Wifi
from ...base_form import BaseForm


class WifiForm(BaseForm):
    '''
    Switches between two networks: home (where the player normally is) and
    the device's AP. Both live in app-wide preferences rather than the
    page's states - there's one Wi-Fi radio, whichever page switches it.

    The process's "on" state means "on the device" (see
    WifiBaseClass.is_running), so the button toggles Connect to device /
    Connect to home. The entry for whichever network you're on right now is
    read-only - it's a fact, not a choice - and both are while switching.
    '''
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="wifi")
        # Stopped last on page-exit cleanup (ProcessManager.abort_all): other
        # processes' teardown (e.g. ArpSpoofer restoring ARP tables) needs
        # working networking, so switching networks back must happen after.
        self.process = self.get_process(Wifi, tags=["stop_last"])
        self.preferences = context.preferences

        self.add_header()

        _, self.home_entry = self.add_labeled_entry(self.label("home"), autosave=False)
        _, self.device_entry = self.add_labeled_entry(self.label("device"), autosave=False)
        self.device_entry.setText(self.preferences.get("wifi_device") or "")
        self.home_entry.setText(self.default_home())
        for entry in (self.home_entry, self.device_entry):
            entry.editingFinished.connect(self.save_entries)
        # Before the process row's first poll, so a device network the app
        # started on is already recognised (see is_running's detection)
        self.apply_entries()

        self.add_process_row(self.connect_device, self.process.stop, self.process.is_running)

    def label(self, key: str) -> str:
        return self.context.labels.get(f"network_action_forms_wifi_{key}")

    def default_home(self) -> str:
        '''
        The saved home network - or, before one's saved, the network the app
        started on, unless that was the device (starting on the device's AP
        doesn't make it home). The footer keeps both - see Footer.wifi_roles.
        '''
        home, _ = self.context.router.footer.wifi_roles()
        return home or ""

    def apply_entries(self):
        self.process.home_network = self.home_entry.text().strip() or None
        self.process.match_name = self.device_entry.text().strip() or None

    def save_entries(self):
        home = self.home_entry.text().strip()
        device = self.device_entry.text().strip()
        if home and Wifi._matches(home, device or None):
            self.context.buffer.put("wifi", f"'{home}' {self.label('home_is_device')}")
            self.home_entry.setText("")
            home = ""
        for key, value in (("wifi_home", home), ("wifi_device", device)):
            if self.preferences.get(key) != value:
                self.preferences.set(key, value)
        self.apply_entries()

    def connect_device(self):
        self.save_entries()
        self.process.start(self.device_entry.text())

    def refresh_process_button(self):
        '''
        On top of the base's on/off reconcile: which network the status
        names, which entry is locked, and whether "home" has anywhere to go.
        '''
        super().refresh_process_button()
        process = self.process
        switching = process._connecting
        on_device = process.is_connected
        current = process.current_ssid
        on_home = not on_device and Wifi._equal_ci(current, self.home_entry.text().strip())

        set_read_only(self.device_entry, switching or on_device)
        set_read_only(self.home_entry, switching or on_home)

        if switching:
            # The button already shows the optimistic text (see click_start/click_stop)
            set_text(self.process_status, self.label("switching"))
            return
        if on_device:
            status = self.status_on_text
            set_text(self.process_button, self.stop_process_text if process.restore_network else self.label("disconnect"))
        elif on_home:
            status = self.label("on_home")
        elif current is not None:
            status = f"{self.label('on_other')} {current}."
        else:
            status = self.status_off_text
        set_text(self.process_status, status)


def set_read_only(entry: QLineEdit, read_only: bool):
    if entry.isReadOnly() != read_only:
        entry.setReadOnly(read_only)
        # Re-polished so the stylesheet's QLineEdit:read-only look follows
        entry.style().unpolish(entry)
        entry.style().polish(entry)


def set_text(widget, text: str):
    if widget.text() != text:
        widget.setText(text)
