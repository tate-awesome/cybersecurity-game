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
    WifiBaseClass.is_running), so the button points at where it switches to:
    "-> Device" when home, "-> Home" when on the device. Switching either way
    needs both networks (there'd be no getting back otherwise), so until
    they're both entered the button shows the shared caution "Input" and a
    click posts which one is missing to the wifi log instead of switching.
    Once both are saved, the entry for whichever network you're on is
    read-only - a fact, not a choice - and both are while switching.
    '''
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="wifi", flat=True)
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
            entry.editingFinished.connect(lambda entry=entry: self.save_entries(entry))
        # Before the process row's first poll, so a device network the app
        # started on is already recognised (see is_running's detection)
        self.apply_entries()

        self.add_process_row(self.connect_device, self.disconnect_to_home, self.process.is_running)
        # Return in Device Name connects to it; in Home Network it only saves
        # (editingFinished) - it'd be odd for setting home to leave home.
        for entry in self.entries:
            entry.returnPressed.disconnect()
        self.device_entry.returnPressed.connect(self.submit_device)

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
        self.process.set_match_name(self.device_entry.text().strip() or None)

    def save_entries(self, edited: QLineEdit | None = None):
        '''
        Saves both entries to preferences and hands them to the process.
        The home network can't match the Device Name (it'd count as the
        device, and "home" would go nowhere). A saved home the Device Name
        was just edited to match keeps its place and the new name is
        cleared; otherwise home goes - it was either just typed, or only the
        startup guess (see default_home), which starting on the device's AP
        makes wrong.
        '''
        home = self.home_entry.text().strip()
        device = self.device_entry.text().strip()
        if home and Wifi._matches(home, device or None):
            if edited is self.device_entry and self.preferences.get("wifi_home") == home:
                self.context.buffer.put("wifi", f"'{device}' {self.label('device_is_home')}")
                self.device_entry.setText("")
                device = ""
            else:
                self.context.buffer.put("wifi", f"'{home}' {self.label('home_is_device')}")
                self.home_entry.setText("")
                home = ""
        for entry, text in ((self.home_entry, home), (self.device_entry, device)):
            if entry.text() != text:
                entry.setText(text)  # trimmed
        for key, value in (("wifi_home", home), ("wifi_device", device)):
            if self.preferences.get(key) != value:
                self.preferences.set(key, value)
        self.apply_entries()

    def connect_device(self):
        '''Start = connect to the device, or post what's missing if it can't.'''
        self.save_entries()
        missing = self.missing(self.process.is_connected)
        if missing is not None:
            self.context.buffer.put("wifi", self.label(missing))
            return
        self.process.start(self.device_entry.text())

    def refresh_input_warning(self):
        # Wifi sets its own button text each poll (see refresh_process_button),
        # including the shared "Input" caution, so skip the base's pass.
        pass

    def disconnect_to_home(self):
        '''Stop = go back home, or post that home is missing if it can't.'''
        if not self.process.home_network:
            self.context.buffer.put("wifi", self.label("needs_home"))
            return
        self.process.stop()

    def submit_device(self):
        '''
        Return in Device Name: connect to it, if that's what the button
        offers once the new name is in - not if the name turned out to match
        the network already on (now detected as the device, the button
        would mean "go home" instead).
        '''
        self.save_entries(self.device_entry)
        self.refresh_process_button()
        if not self.process.is_connected:
            self.process_button.click()

    def missing(self, on_device: bool) -> str | None:
        '''The label key naming what's missing before the button can switch, or None.'''
        home = self.process.home_network
        device = self.process.match_name
        if on_device:
            return None if home else "needs_home"
        if not home and not device:
            return "needs_both"
        if not device:
            return "needs_device"
        if not home:
            return "needs_home"
        return None

    def refresh_process_button(self):
        '''
        On top of the base's dot reconcile, every poll: the button's
        destination text, which entry is locked, and the brief lockout while
        a switch is in flight. Reads the entries as last applied (see
        apply_entries), so an edit counts once it's finished. A click that
        can't switch posts why (see connect_device / disconnect_to_home).
        '''
        super().refresh_process_button()
        process = self.process
        switching = process._connecting
        on_device = process.is_connected
        current = process.current_ssid
        on_home = not on_device and Wifi._equal_ci(current, process.home_network)

        # Locking reads as "you're here - switch to the other one" only once
        # there is another one, saved - until then both stay open to fix
        paired = bool(self.preferences.get("wifi_home") and self.preferences.get("wifi_device"))
        set_read_only(self.device_entry, switching or (paired and on_device))
        set_read_only(self.home_entry, switching or (paired and on_home))
        set_enabled(self.process_button, not switching)

        if switching:
            return  # leave the optimistic text set by the click
        if not self.entries_filled():
            # Same caution as every other card when an entry is empty.
            text = self.input_needed_text
        else:
            # The arrow points at where a click would take you.
            text = f"{self.style.icon('arrow-right')}  {'Home' if on_device else 'Device'}"
        set_text(self.process_button, text)


def set_read_only(entry: QLineEdit, read_only: bool):
    if entry.isReadOnly() != read_only:
        entry.setReadOnly(read_only)
        # Re-polished so the stylesheet's QLineEdit:read-only look follows
        entry.style().unpolish(entry)
        entry.style().polish(entry)


def set_enabled(widget: QWidget, enabled: bool):
    if widget.isEnabled() != enabled:
        widget.setEnabled(enabled)


def set_text(widget, text: str):
    if widget.text() != text:
        widget.setText(text)
