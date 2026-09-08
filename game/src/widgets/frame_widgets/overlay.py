import time
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
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
        self._parent_overlay: "Overlay | None" = None

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
        # QApplication.activePopupWidget() is Qt's own live answer to
        # "which popup is the user currently inside" - the same question
        # the CTk version's global click listener answered by hand (it had
        # no widget-parent relationship between Toplevels to lean on
        # either). Whatever popup is still active right now, right before
        # this one grabs, is genuinely the context this click happened in:
        # true even when the click arrived indirectly (see menu_bar.py's
        # overflow overlay, which triggers a real button's own click()
        # from a proxy sitting in *its* popup - activePopupWidget() still
        # correctly reports that popup, unlike either button's fixed
        # widget-parent chain, which the proxy indirection breaks).
        active_popup = QApplication.activePopupWidget()
        self._parent_overlay = active_popup if isinstance(active_popup, Overlay) and active_popup is not self else None

        self._close_unrelated_overlays()
        self.populate_func(self)
        self.button.setText(self.close_text)
        self.adjustSize()
        self.move(self.calculate_placement(self.anchor))
        self.show()

    def _lineage(self) -> set["Overlay"]:
        '''
        This overlay plus every ancestor recorded in _parent_overlay at
        open time, closest first - the set of overlays a close sweep
        should leave alone.
        '''
        lineage = set()
        node = self
        while node is not None and node not in lineage:
            lineage.add(node)
            node = node._parent_overlay
        return lineage

    def _close_unrelated_overlays(self):
        '''
        Qt's popup-grab dismissal (see the class docstring) only reacts to
        real mouse events outside every open popup - it doesn't know that
        two Overlay instances opened from unrelated trigger buttons should
        also close each other. Closes every other currently open overlay
        except this one and its lineage of ancestor overlays (see
        click_open/_parent_overlay), so opening an overlay from a button
        that lives inside an already-open one (a nested picker, or a proxy
        button in the menu bar's own overflow popup) doesn't blow away
        that parent - only truly unrelated overlays get closed, matching
        the CTk version's lineage-aware global click listener. Every
        overlay is parented to context.root (see CheckboxOverlay/
        VariableOverlay/FilterOverlay), so that's searched rather than
        keeping a separate registry.
        '''
        lineage = self._lineage()
        for overlay in self.context.root.findChildren(Overlay):
            if overlay not in lineage and overlay.isVisible():
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
        # A closed overlay taking any overlays opened *from inside it* down
        # with it (rather than leaving them floating with no parent left)
        # mirrors a submenu closing when its parent menu does.
        for overlay in self.context.root.findChildren(Overlay):
            if overlay is not self and overlay._parent_overlay is self and overlay.isVisible():
                overlay.hide()
        self._parent_overlay = None
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
