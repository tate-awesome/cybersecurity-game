import time
from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from ...app_core import Context
from collections.abc import Callable

class Overlay(QWidget):
    '''
    A popup panel anchored to a trigger button, toggled open/closed by
    clicking that button. Uses Qt.WindowType.Popup, which closes the
    window natively on an outside click - replacing the hand-rolled
    click-outside tracking (a ClickManager listener, climbing the widget's
    parent chain, a manual Escape binding) the customtkinter version needed
    since CTkFrame has no such built-in.

    The trigger button keeps its own text with a triangle appended - ▾
    while closed, ▴ while open - so every overlay button reads as one at a
    glance, and shows which overlay is open. closed_text/open_text replace
    those whole texts instead (e.g. MenuBar's overflow button: » and ×).
    '''
    CLOSED_MARKER = "▾"
    OPEN_MARKER = "▴"

    def __init__(self, master: QWidget, context: Context, button: QPushButton, populate_func: "Callable[[Overlay], None]", anchor: str = "south",
                 closed_text: str | None = None, open_text: str | None = None):
        super().__init__(master, Qt.WindowType.Popup)
        self.anchor = anchor
        self.context = context
        self.style = context.style
        self.button = button
        self.closed_text = closed_text or f"{button.text()} {self.CLOSED_MARKER}"
        self.open_text = open_text or f"{button.text()} {self.OPEN_MARKER}"
        button.setText(self.closed_text)
        self.populate_func = populate_func
        self._last_hidden_at = 0.0
        self._parent_overlay: Overlay | None = None

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
        self.button.setText(self.open_text)
        self.adjustSize()
        # A click replayed from a menu bar overflow proxy (see
        # MenuBar._replay_click) lands on a button that's hidden while
        # squashed, so it has no real on-screen position - anchor to the
        # proxy that was actually clicked instead.
        target = getattr(self.button, "click_proxy", None) or self.button
        self.move(self.calculate_placement(self.anchor, target))
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
        self.button.setText(self.closed_text)
        self._clear_contents()
        # A closed overlay taking any overlays opened *from inside it* down
        # with it (rather than leaving them floating with no parent left)
        # mirrors a submenu closing when its parent menu does.
        for overlay in self.context.root.findChildren(Overlay):
            if overlay is not self and overlay._parent_overlay is self and overlay.isVisible():
                overlay.hide()
        self._parent_overlay = None
        super().hideEvent(event)

    def mousePressEvent(self, event):
        '''
        While popups are stacked, Qt sends every mouse press to the topmost
        one, and by default a press outside it closes only that one popup -
        so a single outside click would peel the stack back one layer at a
        time. Instead, close every overlay except the one under the mouse
        and its ancestors (all of them, if the press missed every overlay).
        '''
        if self.rect().contains(event.position().toPoint()):
            super().mousePressEvent(event)
            return
        global_pos = event.globalPosition().toPoint()
        under_mouse = QApplication.widgetAt(global_pos)
        target = under_mouse.window() if under_mouse is not None else None
        if not isinstance(target, Overlay) or not target.isVisible():
            target = None

        keep = target._lineage() if target is not None else set()
        for overlay in self.context.root.findChildren(Overlay):
            if overlay not in keep and overlay.isVisible():
                overlay.hide()

        if target is None:
            # No popups left open, so Qt replays this press onto whatever
            # main-window widget is under the mouse, same as for a lone popup
            return
        # Qt only replays a press once no popups are left at all - deliver
        # it to the surviving overlay's widget by hand, so a click that
        # lands on, say, a proxy button in the overflow overlay still
        # presses it rather than just closing the overlay above it. Qt
        # routes the matching release there itself (the now-topmost
        # popup's child under the mouse).
        receiver = target.childAt(target.mapFromGlobal(global_pos))
        if receiver is not None:
            forwarded = QMouseEvent(event.type(), QPointF(receiver.mapFromGlobal(global_pos)), event.globalPosition(),
                                    event.button(), event.buttons(), event.modifiers())
            QApplication.sendEvent(receiver, forwarded)

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

    def calculate_placement(self, anchor: str, target: QWidget) -> QPoint:
        '''Where to put this overlay so it sits on the given side of target.'''
        screen_rect = target.screen().availableGeometry()
        btn_top_left = target.mapToGlobal(QPoint(0, 0))
        btn_w = target.width()
        btn_h = target.height()
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
