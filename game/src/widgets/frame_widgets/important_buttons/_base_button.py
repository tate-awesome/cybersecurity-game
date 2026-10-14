import os, subprocess, webbrowser

from PySide6.QtWidgets import QPushButton
from ....app_core import Context
from ....app_core.context.style import Style

# Marks are icons in the text (see Style._load_icon_font).
# Marks everything only developers see (developer mode - preferences.json
# "is_developer"): a bug, like the Debug dropdown's
DEVELOPER_MARK = Style.icon("bug")
# After a button's label, where clicking it takes you (see ImportantButton.OPENS):
# another page in the app, a popup window (a message, a confirmation, a file
# picker), or somewhere outside the app (the browser, a folder)
PAGE_MARK = Style.icon("arrow-right")
POPUP_MARK = Style.icon("layers-subtract")
POPOUT_MARK = Style.icon("external-link")
OPENS_MARKS = {"page": PAGE_MARK, "popup": POPUP_MARK, "outside": POPOUT_MARK}


def developer_text(text: str) -> str:
    '''text with the developer-only mark in front (once).'''
    return text if text.startswith(DEVELOPER_MARK) else f"{DEVELOPER_MARK} {text}"


def open_in_browser(url: str):
    '''Opens url in the user's browser - as the user, not root, when the app runs under sudo.'''
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        # Open browser as not sudo
        subprocess.Popen(["sudo", "-u", sudo_user, "xdg-open", url])
    else:
        # Fallback when not running under sudo
        webbrowser.open(url)


class ImportantButton(QPushButton):
    '''
    A button that can be placed anywhere - a MenuBar (add_important), a
    TitleMenu (add_important), or any plain layout - and reads and behaves
    the same in all of them. The one place a button's label, tooltip, and
    click behavior are tied together.

    Subclasses set LABEL/TOOLTIP (labels keys - TOOLTIP None means no
    tooltip) and override on_click. Placement only decides position and
    font, never what the button says or does.
    '''
    LABEL = "menu_bar_buttons__default"
    TOOLTIP: str | None = None
    # Where clicking it takes you - "page", "popup" or "outside", shown with
    # that one of OPENS_MARKS after the label (see opens) - or None
    OPENS: str | None = None

    def __init__(self, context: Context, label_key: str | None = None):
        super().__init__(context.labels.get(label_key or self.LABEL))
        self.developer_only = False
        # (inactive, active) icon names while shown as a symbol - see show_icon
        self.icons: tuple[str, str] | None = None
        self.context = context
        self.setFont(context.style.get_font())
        if self.TOOLTIP is not None:
            self.setToolTip(context.labels.get(self.TOOLTIP))
        if self.opens():
            self.setText(self.text())  # (the constructor's text skips setText - see below)
        # clicked emits a "checked" bool that on_click doesn't take
        self.clicked.connect(lambda checked=False: self.on_click())

    @classmethod
    def is_available(cls, context: Context) -> bool:
        '''Whether this button makes sense right now - placements skip it if not.'''
        return True

    def mark_developer_only(self):
        '''
        Shows the developer-only mark (DEVELOPER_MARK) in front of this
        button's text from now on - kept through any later setText, e.g. a
        ToggleButton's label swap or an overlay's dropdown marker.
        '''
        # The mark comes from a fallback font with a taller line than the UI
        # font's, which would make this button taller than its neighbors -
        # so it keeps the height it has without the mark (the glyph itself fits)
        height = self.sizeHint().height()
        self.developer_only = True
        self.setText(self.text())
        self.setFixedHeight(height)

    def show_icon(self, icon: str, active_icon: str | None = None):
        '''
        Shows one of style.ICONS in place of the label (which becomes the
        tooltip, if there isn't one) - for a ToggleButton, active_icon while
        it's active.
        '''
        if not self.toolTip():
            self.setToolTip(self.text())
        self.icons = (icon, active_icon or icon)
        self.setFont(self.context.style.get_font("icon"))
        self.show_state()

    def show_state(self):
        '''Puts the button's current look in place - its icon, if it has one (see show_icon).'''
        if self.icons is not None:
            self.setText(self.context.style.icon(self.icons[0]))

    def opens(self) -> str | None:
        '''Where clicking it takes you right now (see OPENS) - by default, always the same.'''
        return self.OPENS

    def setText(self, text: str):
        if getattr(self, "icons", None) is None:  # a bare icon (see show_icon) gets no marks
            mark = OPENS_MARKS.get(self.opens())
            if mark is not None and not text.endswith(mark):
                text = f"{text} {mark}"
            if getattr(self, "developer_only", False):
                text = developer_text(text)
        super().setText(text)

    def on_click(self):
        pass


class PanelButton(ImportantButton):
    '''
    A button that only works on one panel (PANEL - its KEY in widgets.PANELS)
    - unavailable on pages whose panes don't include it. On pages that
    build their panels in code (no "layout_shape" config), it's left available.
    '''
    PANEL = ""

    @classmethod
    def is_available(cls, context: Context) -> bool:
        panels = context.pages.page_panel_keys(context.router.current_page)
        return panels is None or cls.PANEL in panels


class ToggleButton(ImportantButton):
    '''
    A two-state button: each click calls start() or stop() and swaps its
    label between LABEL (inactive) and ACTIVE_LABEL (active). The state only
    flips once start/stop returns, so one that raises leaves it unchanged.

    Subclasses whose state lives somewhere else (e.g. context.states)
    override is_active to read it - the label is re-synced to it every
    frame, so it follows changes made by other widgets too.
    '''
    ACTIVE_LABEL = "menu_bar_buttons__default"

    def __init__(self, context: Context):
        super().__init__(context)
        self.active = False
        # Syncs the label to whatever state start/stop already represent,
        # without invoking either
        self.active = self.is_active()
        self.show_state()

        name = f"toggle_button_{id(self)}"
        manager = context.animation_manager
        manager.add_callback(name, self.sync_state)
        # Buttons can be destroyed long before the page is (e.g. inside an
        # overlay, rebuilt on every open) - a callback left behind would
        # call into a deleted widget every frame
        self.destroyed.connect(lambda *_: manager.remove_callback(name))

    def is_active(self) -> bool:
        '''The real state this button shows - by default, just its own clicks.'''
        return self.active

    def sync_state(self):
        active = self.is_active()
        if active != self.active:
            self.active = active
            self.show_state()

    def on_click(self):
        if self.active:
            self.stop()
        else:
            self.start()
        self.active = not self.active
        self.show_state()

    def show_state(self):
        if self.icons is not None:
            self.setText(self.context.style.icon(self.icons[1] if self.active else self.icons[0]))
        else:
            self.setText(self.context.labels.get(self.ACTIVE_LABEL if self.active else self.LABEL))

    def start(self):
        pass

    def stop(self):
        pass
