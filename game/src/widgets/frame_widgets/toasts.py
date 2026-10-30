'''
Status toasts: every status the network actions put (see
network/buffer/notice.py) pops up at the top right, under the menu bar's
bell - a plain status as written, an error as written with a link to its
fix, a report as its one-line summary with a link to the report itself.

Each toast fades in rising into place below the ones already up, stays a
while (longer for errors and reports - hovering holds it), then shrinks
into the bell, which pops as it swallows it. At most MAX_SHOWN are up at
once: one more pushes the oldest straight into the bell. Everything stays
in the bell's dropdown afterwards, and the bell counts the errors and
reports since it was last opened.

Dragging a toast moves the whole stack: let go, and it settles in the
nearest of ANCHORS - a top or bottom corner, or the middle of either edge -
remembered for that workspace (PAGE_ANCHORS_PREFERENCE), until Quick
Settings' Save Toast Position as Default makes it every workspace's
(ANCHOR_PREFERENCE - see Toasts.save_anchor_as_default). Wherever it is, toasts
still shrink into the bell - which moves over beside Quick Settings while
the stack is on the right (see MenuBar.place_bell).

Toasts belongs to the session (see ContextManager.start_session) - the
toasts are children of the main window, not of a page, so they ride over
page changes - and each page's menu bar binds its own bell (see StatusBell).
'''
import math
import time
from collections import deque

from PySide6.QtCore import QEasingCurve, QElapsedTimer, QObject, QPoint, QPointF, QRect, QRectF, Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsOpacityEffect, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from ... import STARTED
from ...app_core import Context
from ...network.buffer.meta_status import MetaStatus
from .important_buttons._base_button import ImportantButton, MODAL_MARK
from .overlay import Overlay

# The wall-clock instant this session's clock started, so a status's wall-clock
# time (see StatusBuffer.put) converts to the same session time the footer
# shows (perf_counter since STARTED) - see session_stamp.
_SESSION_START_WALL = time.time() - time.perf_counter() + STARTED


def session_stamp(status_time: float) -> str:
    '''A status's time as session time, H:MM:SS - the same clock as the footer's.'''
    elapsed = max(0, int(status_time - _SESSION_START_WALL))
    hours, rest = divmod(elapsed, 3600)
    minutes, seconds = divmod(rest, 60)
    return f"{hours}:{minutes:02}:{seconds:02}"

# How wide a toast's card is, px - the shadow's room comes on top
TOAST_WIDTH = 380
# At most this many up at once - one more sends the oldest into the bell at once
MAX_SHOWN = 4
# How long each kind stays up, ms - hovering holds it
LIFETIME_MS = {"status": 3000, "error": 8000, "report": 8000}
# How many statuses the bell's dropdown keeps
HISTORY_SIZE = 300
# How often the status buffer is read, ms
POLL_MS = 100
# Coming in: fading in while rising this far into place
ENTER_MS = 260
RISE_PX = 18
# Sliding up into the room an eaten toast left
MOVE_MS = 220
# Shrinking into the bell, then the bell's pop - growing by POP_SCALE and back
EAT_MS = 340
POP_MS = 240
POP_SCALE = 0.35
# The bell's dropdown scrolls past this much of the window's height
DROPDOWN_HEIGHT = 0.6
# Where the stack can sit - (vertical, horizontal) - and where it starts:
# at the top right, under the bell beside Quick Settings. Dragged somewhere (see Toast.mouseReleaseEvent),
# it's saved for that page in preferences' PAGE_ANCHORS_PREFERENCE
# ({page key: anchor}) - and ANCHOR_PREFERENCE is every other page's
ANCHORS = {
    "top_left": ("top", "left"), "top_center": ("top", "center"), "top_right": ("top", "right"),
    "bottom_left": ("bottom", "left"), "bottom_center": ("bottom", "center"), "bottom_right": ("bottom", "right"),
}
DEFAULT_ANCHOR = "top_right"
ANCHOR_PREFERENCE = "status_toasts_anchor"
PAGE_ANCHORS_PREFERENCE = "status_toasts_page_anchors"


def kind_color(context: Context, kind: str) -> QColor:
    '''What marks a kind - its header, its outline and its link: errors bad, reports the accent, statuses muted.'''
    style = context.style
    if kind == "error":
        return QColor(style.color("bad"))
    if kind == "report":
        return QColor(style.material("accent"))
    return QColor(style.color("muted_text"))


def open_notice(context: Context, status: MetaStatus):
    '''Shows a report, or an error's fix, in a modal (see MarkdownModal).'''
    from ..modal import MarkdownModal  # here - modal imports the panels, which import this package
    notice = status.notice
    if notice is None:
        return
    if notice.kind == "report":
        MarkdownModal(context, notice.title or status.hack, f"**{_escape(status.status)}**\n\n{notice.markdown or ''}").show()
        return
    path = context.paths.fixes / f"{notice.fix}.md"
    try:
        fix = path.read_text(encoding="utf-8")
    except OSError:
        fix = f"# {context.labels.get('status_toasts_fix_title')}\n\n{context.labels.get('status_toasts_fix_missing')}"
    # Its own heading becomes the modal's title - the error itself heads the body
    first, _, rest = fix.partition("\n")
    title = first[2:].strip() if first.startswith("# ") else context.labels.get("status_toasts_fix_title")
    body = rest if first.startswith("# ") else fix
    MarkdownModal(context, title, f"**{_escape(status.status)}**\n\n{body.lstrip()}").show()


def _escape(text: str) -> str:
    from ...network.buffer.notice import Report
    return Report.escape(text)


class NoticeContent(QWidget):
    '''
    What a toast (and a row of the bell's dropdown) shows of a status: a
    small header - its kind, source and session time (see session_stamp) - in its
    kind's color, its text word for word, and for an error or report, a
    chip that opens the fix or the report. opened runs after the chip's click.
    selectable lets its text be selected, to copy a URL or a command - not
    on a toast, where a press starts a drag (see Toast).
    '''

    def __init__(self, context: Context, status: MetaStatus, opened=None, selectable: bool = False):
        super().__init__()
        self.context = context
        self.status = status
        style = context.style
        labels = context.labels
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(style.cgap * 2)

        parts = [labels.get(f"status_toasts_kind_{status.kind}").upper(), status.hack, session_stamp(status.time)]
        header = QLabel("  ·  ".join(parts))
        header.setTextFormat(Qt.TextFormat.PlainText)
        font = QFont(style.get_font("small"))
        font.setBold(True)
        font.setPointSizeF(font.pointSizeF() * 0.8)
        header.setFont(font)
        style.live_style(header, lambda: f"QLabel {{ color: {kind_color(context, status.kind).name()}; }}")
        column.addWidget(header)

        message = QLabel(status.status)
        message.setTextFormat(Qt.TextFormat.PlainText)
        message.setWordWrap(True)
        message.setFont(style.get_font())
        if selectable:
            message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        style.live_style(message, lambda: f"QLabel {{ color: {style.color('text')}; background: transparent; }}")
        column.addWidget(message)

        if status.notice is not None:
            key = "status_toasts_view_report" if status.kind == "report" else "status_toasts_view_fix"
            chip = QPushButton(f"{labels.get(key)} {MODAL_MARK}")
            chip.setFont(style.get_font("small"))
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            name = f"_notice_chip_{id(chip)}"
            chip.setObjectName(name)

            def sheet() -> str:
                color = kind_color(context, status.kind)
                tint, hover = QColor(color), QColor(color)
                tint.setAlpha(40)
                hover.setAlpha(70)
                return (f"QPushButton#{name} {{ background: {tint.name(QColor.NameFormat.HexArgb)}; color: {color.name()};"
                        f" border: none; border-radius: 6px; padding: {style.cgap * 2}px {style.igap}px; font-weight: bold; }}"
                        f" QPushButton#{name}:hover {{ background: {hover.name(QColor.NameFormat.HexArgb)}; }}")
            style.live_style(chip, sheet)

            def clicked(checked=False):
                open_notice(context, status)
                if opened is not None:
                    opened()
            chip.clicked.connect(clicked)
            column.addSpacing(style.cgap * 2)
            column.addWidget(chip, 0, Qt.AlignmentFlag.AlignLeft)


class ToastCard(QWidget):
    '''
    One status (see NoticeContent) on a card shaped like a popup window's
    (see paint_panel), outlined in its kind's color - with room around it
    for the card's shadow. A Toast, and each row of the bell's dropdown, so
    they look the same.
    '''

    def __init__(self, context: Context, status: MetaStatus, opened=None, selectable: bool = False, parent: QWidget | None = None):
        super().__init__(parent)
        self.context = context
        self.status = status
        style = context.style
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        left, top, right, bottom = self.shadow_room()
        pad = style.igap + style.igap // 2
        column = QVBoxLayout(self)
        column.setContentsMargins(left + pad, top + style.igap, right + pad, bottom + style.igap)
        column.addWidget(NoticeContent(context, status, opened=opened, selectable=selectable))
        width = TOAST_WIDTH + left + right
        self.setFixedSize(width, column.totalHeightForWidth(width))
        style.signals.changed.connect(self.update)

    def shadow_room(self) -> tuple[int, int, int, int]:
        style = self.context.style
        return style.shadow_margins(style.popup_shadows())

    def card(self) -> QRect:
        '''The card itself, inside the shadow's room.'''
        left, top, right, bottom = self.shadow_room()
        return self.rect().adjusted(left, top, -right, -bottom)

    def paintEvent(self, event):
        from ..panels.panel import paint_panel  # here - panels import this package
        style = self.context.style
        # A plain status keeps the panels' own outline - a theme's floating one is its accent, a report's color
        outline = kind_color(self.context, self.status.kind) if self.status.kind != "status" else None
        painter = QPainter(self)
        paint_panel(painter, style, self.width(), self.height(), on_window=True, outline=outline, shadows=style.popup_shadows())
        painter.end()


class Toast(ToastCard):
    '''
    A ToastCard over the main window, placed by Toasts - it fades in rising
    into place (see enter), slides up as the ones above it go (see
    move_to), and asks Toasts to eat it when its time is up (see
    LIFETIME_MS) - hovering holds it. Dragged, it takes the whole stack
    somewhere else (see Toasts.drop).
    '''

    def __init__(self, toasts: "Toasts", status: MetaStatus):
        super().__init__(toasts.context, status, opened=lambda: toasts.eat(self), parent=toasts.context.root)
        self.toasts = toasts

        self.opacity = QGraphicsOpacityEffect(self)
        self.opacity.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity)
        self._motion: QVariantAnimation | None = None

        # Time left, held while the mouse is over it
        self.remaining = LIFETIME_MS[status.kind]
        self.clock = QElapsedTimer()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: toasts.eat(self))
        # Where a press landed (its own coordinates), and whether it's become a drag
        self._pressed: QPoint | None = None
        self.dragging = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def start_clock(self):
        self.clock.restart()
        self.timer.start(max(0, self.remaining))

    def enterEvent(self, event):
        if self.timer.isActive():
            self.remaining -= self.clock.elapsed()
            self.timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.toasts.is_shown(self) and not self.dragging:
            self.start_clock()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._pressed is None:
            return super().mouseMoveEvent(event)
        at = event.position().toPoint()
        if not self.dragging and (at - self._pressed).manhattanLength() >= QApplication.startDragDistance():
            self.dragging = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            if self._motion is not None:
                self._motion.stop()
            self.opacity.setOpacity(1.0)
            self.raise_()
        if self.dragging:
            self.move(self.mapTo(self.context.root, at) - self._pressed)

    def mouseReleaseEvent(self, event):
        dragged = self.dragging
        self._pressed = None
        self.dragging = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        if dragged:
            self.toasts.drop(self.mapTo(self.context.root, self.card().center()))
        super().mouseReleaseEvent(event)

    def enter(self, at: QPoint):
        '''Shows it at its place, fading in as it rises the last RISE_PX into it.'''
        self.move(at)
        self.show()
        self.raise_()
        self.start_clock()
        if not self.context.performance.page_transitions:
            return
        start = QPoint(at.x(), at.y() + RISE_PX)
        self.move(start)
        self.opacity.setOpacity(0.0)
        self._animate(ENTER_MS, QEasingCurve.Type.OutCubic,
                      lambda t: (self.move(start + (at - start) * t), self.opacity.setOpacity(t)))

    def move_to(self, at: QPoint):
        '''Slides to a new place - up into room left by one that went.'''
        if at == self.pos():
            return
        if not self.context.performance.page_transitions:
            self.move(at)
            return
        start = self.pos()
        opacity = self.opacity.opacity()
        self._animate(MOVE_MS, QEasingCurve.Type.OutCubic,
                      lambda t: (self.move(start + (at - start) * t), self.opacity.setOpacity(opacity + (1 - opacity) * t)))

    def _animate(self, duration: int, curve: QEasingCurve.Type, step):
        if self._motion is not None:
            self._motion.stop()
        motion = QVariantAnimation(self)
        motion.setStartValue(0.0)
        motion.setEndValue(1.0)
        motion.setDuration(duration)
        motion.setEasingCurve(curve)
        motion.valueChanged.connect(lambda value: step(float(value)))
        self._motion = motion
        motion.start()


class _Swallowed(QWidget):
    '''
    A toast on its way into the bell: a snapshot of it, shrinking toward
    the bell's middle and fading as it goes, faster and faster - then gone,
    and the bell pops (see StatusBell.pop).
    '''

    def __init__(self, root: QWidget, picture: QPixmap, start: QRect, end: QPointF, done):
        super().__init__(root)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.picture = picture
        self.start = QRectF(start)
        self.end = end
        self.progress = 0.0
        self.setGeometry(root.rect())
        self.show()
        self.raise_()
        motion = QVariantAnimation(self)
        motion.setStartValue(0.0)
        motion.setEndValue(1.0)
        motion.setDuration(EAT_MS)
        motion.setEasingCurve(QEasingCurve.Type.InCubic)
        motion.valueChanged.connect(self._step)

        def finished():
            done()
            self.deleteLater()
        motion.finished.connect(finished)
        motion.start()

    def _step(self, value):
        self.progress = float(value)
        self.update()

    def paintEvent(self, event):
        t = self.progress
        scale = max(0.02, 1.0 - t)
        middle = self.start.center() + (self.end - self.start.center()) * t
        size = self.start.size() * scale
        target = QRectF(middle.x() - size.width() / 2, middle.y() - size.height() / 2, size.width(), size.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(1.0 - 0.7 * t)
        painter.drawPixmap(target, self.picture, QRectF(self.picture.rect()))
        painter.end()


class Toasts(QObject):
    '''
    Reads new statuses off the status buffer (see StatusBuffer.statuses_after),
    shows each as a Toast, keeps them for the bell's dropdown, and counts
    the errors and reports not yet seen there.
    '''

    def __init__(self, context: Context):
        super().__init__(context.root)
        self.context = context
        # The last status number read - this keeps its own place in the buffer
        self.last = 0
        self.history: deque[MetaStatus] = deque(maxlen=HISTORY_SIZE)
        # Errors and reports since the bell's dropdown was last opened
        self.unseen = 0
        # Oldest first - top to bottom
        self.shown: list[Toast] = []
        self.bell: "StatusBell | None" = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(POLL_MS)

    def bind_bell(self, bell: "StatusBell"):
        '''A new page's menu bar's bell - the one toasts gather under, and shrink into, from now on.'''
        self.bell = bell
        bell.destroyed.connect(lambda *_: self._bell_gone(bell))
        # The new page was laid over the toasts - back on top of it, and under its bell
        for toast in self.shown:
            toast.raise_()
        QTimer.singleShot(0, self.place)

    def _bell_gone(self, bell):
        if self.bell is bell:
            self.bell = None

    def live_bell(self) -> "StatusBell | None":
        try:
            if self.bell is not None and self.bell.isVisible():
                return self.bell
        except RuntimeError:
            self.bell = None  # deleted with its page
        return None

    def poll(self):
        new = self.context.buffer.status.statuses_after(self.last)
        if not new:
            return
        self.last = new[-1].number
        for status in new:
            self.history.append(status)
            if status.kind != "status":
                self.unseen += 1
        bell = self.live_bell()
        if bell is not None:
            bell.update()
        # A burst bigger than fits only toasts its last few - the rest are in the dropdown
        for status in new[-MAX_SHOWN:]:
            self.show_toast(status)

    def show_toast(self, status: MetaStatus):
        # Full up - the oldest goes into the bell now, making room
        while len(self.shown) >= MAX_SHOWN:
            self.eat(self.shown[0])
        toast = Toast(self, status)
        self.shown.append(toast)
        self.place(entering=toast)

    def is_shown(self, toast: Toast) -> bool:
        return toast in self.shown

    def anchor(self) -> str:
        '''Where the stack sits on this page: where it was dragged to here, or else the default.'''
        pages = self.context.preferences.get(PAGE_ANCHORS_PREFERENCE)
        anchor = pages.get(self.context.router.current_page) if isinstance(pages, dict) else None
        return anchor if anchor in ANCHORS else self.default_anchor()

    def default_anchor(self) -> str:
        anchor = self.context.preferences.get(ANCHOR_PREFERENCE)
        return anchor if anchor in ANCHORS else DEFAULT_ANCHOR

    def set_anchor(self, anchor: str):
        '''Keeps the stack at anchor on this page from now on - forgotten for it if that's the default anyway.'''
        preferences = self.context.preferences
        pages = preferences.get(PAGE_ANCHORS_PREFERENCE)
        pages = dict(pages) if isinstance(pages, dict) else {}
        if anchor == self.default_anchor():
            pages.pop(self.context.router.current_page, None)
        else:
            pages[self.context.router.current_page] = anchor
        preferences.set(PAGE_ANCHORS_PREFERENCE, pages)

    def save_anchor_as_default(self):
        '''
        Makes this page's anchor every page's - those dragged somewhere of
        their own, too: they all go where this one is (see SaveToastPositionAsDefault).
        '''
        preferences = self.context.preferences
        preferences.set(ANCHOR_PREFERENCE, self.anchor())
        preferences.set(PAGE_ANCHORS_PREFERENCE, {})

    def bell_on_right(self) -> bool:
        '''Whether the bell belongs beside Quick Settings - with the stack on the right (see MenuBar.place_bell).'''
        return ANCHORS[self.anchor()][1] == "right"

    def bounds(self) -> QRect:
        '''
        Where toasts can go: the window, inset by igap - below the menu
        bar (just under the bell) and above the footer.
        '''
        root, style = self.context.root, self.context.style
        bell = self.live_bell()
        if bell is not None:
            top = bell.mapTo(root, QPoint(0, bell.height())).y()
        else:
            from .window_chrome import window_bar_height
            top = window_bar_height(self.context)
        bottom = root.height()
        from .footer import Footer
        for footer in root.findChildren(Footer):
            if footer.isVisible():
                bottom = min(bottom, footer.mapTo(root, QPoint(0, 0)).y())
        gap = style.igap
        return QRect(gap, top + gap, max(0, root.width() - 2 * gap), max(0, bottom - top - 2 * gap))

    def place(self, entering: Toast | None = None):
        '''
        Stacks the toasts at the anchor (see ANCHORS), oldest on top - the
        entering one fades in at the bottom. At a bottom anchor the
        stack's bottom sits on the edge, so it grows upward.
        '''
        vertical, horizontal = ANCHORS[self.anchor()]
        bounds, gap = self.bounds(), self.context.style.igap
        cards = [toast.height() - toast.shadow_room()[1] - toast.shadow_room()[3] for toast in self.shown]
        y = bounds.top() if vertical == "top" else bounds.bottom() - sum(cards) - gap * max(0, len(cards) - 1)
        for toast, height in zip(self.shown, cards):
            left, top, right, _ = toast.shadow_room()
            width = toast.width() - left - right
            x = {"left": bounds.left(), "center": bounds.center().x() - width // 2, "right": bounds.right() - width}[horizontal]
            at = QPoint(x - left, y - top)
            if toast.dragging:
                pass  # following the mouse - it settles once dropped
            elif toast is entering:
                toast.enter(at)
            else:
                toast.move_to(at)
            y += height + gap

    def drop(self, at: QPoint):
        '''A toast was dragged and let go with its middle at at - the stack moves to the nearest anchor.'''
        bounds = self.bounds()
        vertical = "top" if at.y() < bounds.center().y() else "bottom"
        third = bounds.width() / 3
        horizontal = "left" if at.x() < bounds.left() + third else "right" if at.x() > bounds.right() - third else "center"
        anchor = next(key for key, value in ANCHORS.items() if value == (vertical, horizontal))
        was_right = self.bell_on_right()
        if anchor != self.anchor():
            self.set_anchor(anchor)
        bell = self.live_bell()
        if bell is not None and self.bell_on_right() != was_right and bell.menu_bar is not None:
            bell.menu_bar.place_bell()
        # After the bar's relaid out - the bell's place sets the stack's top
        QTimer.singleShot(0, self.place)
        for toast in self.shown:
            if not toast.underMouse():
                toast.start_clock()

    def eat(self, toast: Toast):
        '''Takes a toast down - shrinking it into the bell, which pops - and slides the rest up.'''
        if toast not in self.shown:
            return
        self.shown.remove(toast)
        toast.timer.stop()
        bell = self.live_bell()
        if bell is not None and self.context.performance.page_transitions and toast.isVisible():
            card = toast.card()
            picture = toast.grab(card)
            start = QRect(toast.mapTo(self.context.root, card.topLeft()), card.size())
            middle = QPointF(bell.mapTo(self.context.root, bell.rect().center()))
            _Swallowed(self.context.root, picture, start, middle, lambda: self._swallowed(bell))
        toast.hide()
        toast.deleteLater()
        self.place()

    def _swallowed(self, bell: "StatusBell"):
        try:
            bell.pop()
        except RuntimeError:
            pass  # its page went while the toast was on its way

    def mark_seen(self):
        self.unseen = 0
        bell = self.live_bell()
        if bell is not None:
            bell.update()


class StatusBell(ImportantButton):
    '''
    The menu bar's bell - after refresh, or beside Quick Settings while the
    stack is on the right (see MenuBar.place_bell): what toasts gather under and shrink
    into (see Toasts), with the count of errors and reports since it was last
    opened on it. Opens a dropdown of every status so far, newest first,
    each just as its toast looked (see ToastCard) - which clears the count.
    '''
    LABEL = "menu_bar_buttons_status_button"
    TOOLTIP = "menu_bar_tooltips_status_button"
    ICON = "bell"

    def __init__(self, context: Context):
        super().__init__(context)
        self.scale = 1.0
        self._pop: QVariantAnimation | None = None
        # The page menu bar it's on - set by it, which moves it (see MenuBar.place_bell)
        self.menu_bar = None
        self.dropdown = Overlay(context.root, context, self, self.fill, trigger_texts=False)
        context.style.signals.changed.connect(self.update)
        context.toasts.bind_bell(self)

    def on_click(self):
        self.context.toasts.mark_seen()
        self.dropdown.click_open()

    def pop(self):
        '''Grows by POP_SCALE and back - having just swallowed a toast.'''
        if self._pop is not None:
            self._pop.stop()
        pop = QVariantAnimation(self)
        pop.setStartValue(0.0)
        pop.setEndValue(1.0)
        pop.setDuration(POP_MS)
        pop.valueChanged.connect(self._pop_step)
        pop.finished.connect(lambda: self._pop_step(1.0))
        self._pop = pop
        pop.start()

    def _pop_step(self, value):
        self.scale = 1.0 + POP_SCALE * math.sin(math.pi * float(value))
        self.update()

    def paintEvent(self, event):
        '''Its bell drawn by hand, so it can pop (see scale) - and the count on its shoulder.'''
        style = self.context.style
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        middle = QRectF(self.rect()).center()
        painter.save()
        painter.translate(middle)
        painter.scale(self.scale, self.scale)
        painter.translate(-middle)
        painter.setFont(self.font())
        painter.setPen(QColor(style.color("accent" if self.underMouse() else "text")))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, style.icon("bell"))
        painter.restore()

        count = self.context.toasts.unseen
        if count:
            text = str(count) if count < 100 else "99+"
            font = QFont(style.get_font("small"))
            font.setBold(True)
            # Sized by the bell, centered on its top right shoulder - kept inside the button
            glyph = self.fontMetrics().height()
            font.setPixelSize(max(9, int(glyph * 0.5)))
            painter.setFont(font)
            metrics = painter.fontMetrics()
            height = metrics.height()
            width = max(height, metrics.horizontalAdvance(text) + height // 2)
            badge = QRectF(0, 0, width, height)
            badge.moveCenter(QPointF(middle.x() + glyph * 0.35, middle.y() - glyph * 0.3))
            badge.moveTop(max(0.0, badge.top()))
            badge.moveRight(min(badge.right(), self.width() - 1.0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(style.color("bad")))
            painter.drawRoundedRect(badge, height / 2, height / 2)
            painter.setPen(QColor("white"))
            painter.drawText(badge, Qt.AlignmentFlag.AlignCenter, text)
        painter.end()

    def fill(self, overlay: Overlay):
        '''The dropdown: every status kept (see HISTORY_SIZE), newest first, each on the card its toast had.'''
        context, style = self.context, self.context.style
        history = list(self.context.toasts.history)
        if not history:
            empty = QLabel(context.labels.get("status_toasts_empty"))
            empty.setFont(style.get_font())
            overlay.layout().addWidget(empty)
            return
        column = QWidget()
        rows = QVBoxLayout(column)
        rows.setContentsMargins(0, 0, 0, 0)
        cards = [ToastCard(context, status, opened=overlay.close_chain, selectable=True) for status in reversed(history)]
        # As far apart as the toasts' cards (see Toasts.place) - their shadows' room overlapping
        left, top, right, bottom = cards[0].shadow_room()
        rows.setSpacing(max(0, style.igap - top - bottom))
        for card in cards:
            rows.addWidget(card)
        column.setFixedWidth(cards[0].width())
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
        scroll.setWidget(column)
        height = min(column.sizeHint().height(), int(context.root.height() * DROPDOWN_HEIGHT))
        scroll.setFixedSize(column.width() + scroll.verticalScrollBar().sizeHint().width(), height)
        overlay.layout().addWidget(scroll)
