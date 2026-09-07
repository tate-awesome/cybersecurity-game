import time
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from ...app_core import Context
from typing import Callable

class Overlay(QWidget):
    '''
    A popup panel anchored to a trigger button, toggled open/closed by
    clicking that button. Uses Qt.WindowType.Popup, which closes the
    window natively on an outside click - replacing the hand-rolled
    click-outside tracking (a ClickManager listener, climbing the widget's
    parent chain, a manual Escape binding) the customtkinter version needed
    since CTkFrame has no such built-in.
    '''

    def __init__(self, master: QWidget, context: Context, button: QPushButton, populate_func: "Callable[[Overlay], None]", anchor: str = "south"):
        super().__init__(master, Qt.WindowType.Popup)
        self.anchor = anchor
        self.context = context
        self.style = context.style
        self.button = button
        self.open_text = button.text()
        self.close_text = self.context.labels.get("menu_bar_buttons", "close_overlay")
        self.populate_func = populate_func
        self._last_hidden_at = 0.0

        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('panel')}; border: 2px solid {self.style.color('accent')};", self))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)

        button.clicked.connect(lambda checked=False: self._toggle())

    def _toggle(self):
        # Debounce: the same click that lands back on the trigger button
        # while this popup is open is also an "outside click" as far as
        # Qt's popup grab is concerned, so it auto-hides this widget before
        # the button's own clicked signal fires - without this guard that
        # click would immediately reopen what it was meant to close.
        if time.monotonic() - self._last_hidden_at < 0.15:
            return
        if self.isVisible():
            self.hide()
        else:
            self.click_open()

    def click_open(self):
        self._close_other_overlays()
        self.populate_func(self)
        self.button.setText(self.close_text)
        self.adjustSize()
        self.move(self.calculate_placement(self.anchor))
        self.show()

    def _close_other_overlays(self):
        '''
        Qt's popup-grab dismissal (see the class docstring) only reacts to
        real mouse events - it doesn't know about, or coordinate with,
        other independent Overlay instances. Clicking a different trigger
        button while another overlay is already open is a real click on a
        real widget, not an "outside click" as far as that overlay's own
        grab is concerned, so without this it would stay open alongside
        the new one. Every overlay is parented to context.root (see
        CheckboxOverlay/VariableOverlay/FilterOverlay), so that's searched
        rather than keeping a separate registry.
        '''
        for overlay in self.context.root.findChildren(Overlay):
            if overlay is not self and overlay.isVisible():
                overlay.hide()

    def click_close(self):
        self.hide()  # triggers hideEvent below, which does the actual cleanup

    def hideEvent(self, event):
        # Also runs when Qt closes this popup itself (outside click,
        # Escape) - not just when click_close() is called directly - so
        # this is the one place that resets the trigger button and clears
        # stale contents regardless of how the overlay got closed.
        self._last_hidden_at = time.monotonic()
        self.button.setText(self.open_text)
        self._clear_contents()
        super().hideEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def _clear_contents(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def calculate_placement(self, anchor: str) -> QPoint:
        screen_rect = self.button.screen().availableGeometry()
        btn_top_left = self.button.mapToGlobal(QPoint(0, 0))
        btn_w = self.button.width()
        btn_h = self.button.height()
        igap = self.style.igap

        frame_w = self.width()
        frame_h = self.height()

        btn_center_x = btn_top_left.x() + btn_w / 2
        btn_center_y = btn_top_left.y() + btn_h / 2

        # ---------------------------------------------------------
        # SOUTH: overlay below button
        # ---------------------------------------------------------
        if anchor == "south":
            x = btn_center_x - frame_w / 2
            ideal_y = btn_top_left.y() + btn_h + igap
            opposite_y = btn_top_left.y() - frame_h - igap

            x = min(x, screen_rect.right() - frame_w)
            x = max(screen_rect.left(), x)

            if ideal_y + frame_h <= screen_rect.bottom():
                y = ideal_y
            elif opposite_y >= screen_rect.top():
                y = opposite_y
            else:
                y = max(screen_rect.top(), screen_rect.bottom() - frame_h)

        # ---------------------------------------------------------
        # NORTH: overlay above button
        # ---------------------------------------------------------
        elif anchor == "north":
            x = btn_center_x - frame_w / 2
            ideal_y = btn_top_left.y() - frame_h - igap
            opposite_y = btn_top_left.y() + btn_h + igap

            x = min(x, screen_rect.right() - frame_w)
            x = max(screen_rect.left(), x)

            if ideal_y >= screen_rect.top():
                y = ideal_y
            elif opposite_y + frame_h <= screen_rect.bottom():
                y = opposite_y
            else:
                y = max(screen_rect.top(), min(ideal_y, screen_rect.bottom() - frame_h))

        # ---------------------------------------------------------
        # EAST: overlay to right of button
        # ---------------------------------------------------------
        elif anchor == "east":
            y = btn_center_y - frame_h / 2
            ideal_x = btn_top_left.x() + btn_w + igap
            opposite_x = btn_top_left.x() - frame_w - igap

            y = min(y, screen_rect.bottom() - frame_h)
            y = max(screen_rect.top(), y)

            if ideal_x + frame_w <= screen_rect.right():
                x = ideal_x
            elif opposite_x >= screen_rect.left():
                x = opposite_x
            else:
                x = max(screen_rect.left(), screen_rect.right() - frame_w)

        # ---------------------------------------------------------
        # WEST: overlay to left of button
        # ---------------------------------------------------------
        elif anchor == "west":
            y = btn_center_y - frame_h / 2
            ideal_x = btn_top_left.x() - frame_w - igap
            opposite_x = btn_top_left.x() + btn_w + igap

            y = min(y, screen_rect.bottom() - frame_h)
            y = max(screen_rect.top(), y)

            if ideal_x >= screen_rect.left():
                x = ideal_x
            elif opposite_x + frame_w <= screen_rect.right():
                x = opposite_x
            else:
                x = max(screen_rect.left(), min(ideal_x, screen_rect.right() - frame_w))

        else:
            raise ValueError(
                f"Invalid anchor '{anchor}'. "
                "Expected 'north', 'south', 'east', or 'west'."
            )

        return QPoint(int(x), int(y))
