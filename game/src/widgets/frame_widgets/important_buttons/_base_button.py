from PySide6.QtWidgets import QPushButton
from ....app_core import Context


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

    def __init__(self, context: Context, label_key: str | None = None):
        super().__init__(context.labels.get(label_key or self.LABEL))
        self.context = context
        self.setFont(context.style.get_font())
        if self.TOOLTIP is not None:
            self.setToolTip(context.labels.get(self.TOOLTIP))
        # clicked emits a "checked" bool that on_click doesn't take
        self.clicked.connect(lambda checked=False: self.on_click())

    @classmethod
    def is_available(cls, context: Context) -> bool:
        '''Whether this button makes sense right now - placements skip it if not.'''
        return True

    def on_click(self):
        pass


class ToggleButton(ImportantButton):
    '''
    A two-state button: each click calls start() or stop() and swaps its
    label between LABEL (inactive) and ACTIVE_LABEL (active). The state only
    flips once start/stop returns, so one that raises leaves it unchanged.
    '''
    ACTIVE_LABEL = "menu_bar_buttons__default"

    def __init__(self, context: Context):
        super().__init__(context)
        # Syncs the label to whatever state start/stop already represent,
        # without invoking either
        self.active = self.starts_active()
        self.show_state()

    def starts_active(self) -> bool:
        return False

    def on_click(self):
        if self.active:
            self.stop()
        else:
            self.start()
        self.active = not self.active
        self.show_state()

    def show_state(self):
        self.setText(self.context.labels.get(self.ACTIVE_LABEL if self.active else self.LABEL))

    def start(self):
        pass

    def stop(self):
        pass
