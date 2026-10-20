import math

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen, QRegion
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from ...app_core import Context
from ...app_core.context.style import PANEL_BORDER_WIDTH
from .. import MenuBar

# Rendered panel shadows (see surface_shadow), by everything that shapes
# one - panels of one size share theirs, and resizes don't redraw it
_SHADOWS: dict[tuple, QImage] = {}
_MAX_SHADOWS = 64


def surface_shadow(style, width: int, height: int) -> QImage | None:
    '''
    The theme's shadow (see Style.panel_shadow) for a panel-like surface
    width x height px, drawn inside the room Style.panel_margins leaves
    around it - its rounded shape, offset and blurred, with the surface's
    own area cut out so a see-through one isn't darkened by it (like CSS's
    box-shadow). Cached - see _SHADOWS. For panels, and anything dressed
    like one (e.g. the workspace select page's summary card).
    '''
    shadow = style.panel_shadow()
    if shadow is None or width <= 0 or height <= 0:
        return None
    radius = style.PANEL_RADIUS
    margins = style.panel_margins()
    key = (width, height, radius, margins, tuple(sorted(shadow.items())))
    if key in _SHADOWS:
        return _SHADOWS[key]
    left, top, right, bottom = margins
    body = QRectF(left, top, width - left - right, height - top - bottom)
    color = QColor(shadow["color"])
    color.setAlphaF(shadow["opacity"])
    blur = shadow["blur"]
    # Drawn at half size and blurred there - a soft shadow has no detail to lose
    scale = 0.5 if blur >= 4 else 1.0
    image = QImage(max(1, int(width * scale)), max(1, int(height * scale)), QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(scale, scale)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(color)
    painter.drawRoundedRect(body.translated(shadow["x"], shadow["y"]), radius, radius)
    painter.end()
    if blur >= 4:
        from ..visuals.background import pyramid_blur  # here - visuals import panels' package
        image = pyramid_blur(image, max(1, round(math.log2(blur * scale))))
        image = image.scaled(width, height, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(Qt.GlobalColor.black)
    painter.drawRoundedRect(body, radius, radius)
    painter.end()
    if len(_SHADOWS) >= _MAX_SHADOWS:
        _SHADOWS.clear()
    _SHADOWS[key] = image
    return image



def paint_panel(painter: QPainter, style, width: int, height: int, on_window: bool = False, shadowed: bool = True):
    '''
    Paints a panel-like surface width x height px by hand - the theme's
    shadow, its panel material in its rounded shape, and its outline (or
    raised bevel) - inside the room Style.panel_margins leaves. on_window
    first lays down the page's window material under it, for a surface
    nothing else is under (a popup window), so it looks as it would on a page.
    shadowed=False leaves the shadow, and the room for it, out - for a
    surface something else draws the shadow of (see DockArea.paintEvent).
    '''
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    shadow = surface_shadow(style, width, height) if shadowed else None
    if shadow is not None:
        painter.drawImage(0, 0, shadow)
    left, top, right, bottom = style.panel_margins() if shadowed else (0, 0, 0, 0)
    half = PANEL_BORDER_WIDTH / 2
    body = QRectF(left + half, top + half, width - left - right - 2 * half, height - top - bottom - 2 * half)
    radius = style.PANEL_RADIUS
    path = QPainterPath()
    path.addRoundedRect(body, radius, radius)
    if on_window:
        painter.fillPath(path, QColor(style.color("window", opaque=True)))
        painter.fillPath(path, style.brush("window", body))
    painter.fillPath(path, style.brush("panel", body))
    outline = style.material("panel_border")
    if style.setting("bevel"):
        # Raised, like the theme's panels (see Style.bevel)
        base = outline.name()
        for color, lines in ((style._shade(base, 0.85), ((body.topLeft(), body.topRight()), (body.topLeft(), body.bottomLeft()))),
                             (style._shade(base, -0.55), ((body.bottomLeft(), body.bottomRight()), (body.topRight(), body.bottomRight())))):
            painter.setPen(QPen(QColor(color), PANEL_BORDER_WIDTH))
            for start, end in lines:
                painter.drawLine(start, end)
    else:
        painter.setPen(QPen(outline, PANEL_BORDER_WIDTH))
        painter.drawPath(path)


class _DrawerLayout(QVBoxLayout):
    '''
    A panel's body layout - what its master.layout().addWidget(...) idiom
    reaches (see Panel.layout). Its margins are the panel's frame (see
    Panel.fit_frame), which body constructors can't clobber: e.g.
    Panes.__init__ sets master.layout()'s margins on whatever it's given.
    '''

    def __init__(self):
        super().__init__()
        super().setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

    def setContentsMargins(self, *args):
        pass  # Only the panel sets these - see frame

    def frame(self, left: int, top: int, right: int, bottom: int):
        super().setContentsMargins(left, top, right, bottom)


class Panel(QWidget):
    '''
    Initializes everything a panel should have: context, style, menu bar.
    A panel fills its master with no padding, and has a menu bar.
    This structure parallelizes all the gui elements that fill a pane and have a menu bar.

    A panel is a drawer (see themes' module docstring): its menu bar and a
    frame around its body - "panel_frame" px left, right and below - are
    all the panel material, one piece.

    It draws its own shadow, in room around it (see Style.panel_margins) -
    except docked (see set_docked), where the DockArea draws every panel's
    shadow under them all instead, so neighbors' shadows don't each widen
    the gap between them.
    '''
    KEY = "base_panel"
    # Settings keys (from _packages/_default.json) this panel reads or writes.
    # The workspace editor uses them to show which panels in a layout use a setting.
    SETTINGS: tuple[str, ...] = ()
    BORDER_WIDTH = PANEL_BORDER_WIDTH

    def __init__(self, master: QWidget, context: Context, menu_bar_label: str | None = None):
        super().__init__(master)
        self.context = context
        self.style = context.style
        # In a DockArea, which draws its shadow (see set_docked)
        self.docked = False

        self.style.set_material(self, "panel", rounded=True, outlined=True)
        # Room around it for the theme's shadow, if it has one (see Style.panel_shadow)
        self.setProperty("shadowed", True)
        master.layout().addWidget(self)

        # The menu bar/body otherwise fill this panel edge-to-edge, which
        # paints straight over the border - the same problem setMask below
        # works around for the menu bar's square corners covering this
        # panel's rounded ones, just for the border instead of the corners.
        # An inset contentsMargins on this widget's own layout would be the
        # obvious fix, but it isn't safe: e.g. Panes.__init__ unconditionally
        # calls master.layout().setContentsMargins(...) on whatever it's
        # given, which would silently clobber it back to 0 the moment a
        # panel's body is a nested Panes split (NetworkDiagram) - and there's
        # no guarantee some other future body constructor won't do the same.
        # Routing the master.layout().addWidget(...) idiom every body
        # constructor already uses (Scrollable/Panes/MenuBar/...) through a
        # separate, actually-installed inner layout instead - via the
        # layout() override below - keeps the border-inset margin on a
        # layout nothing outside this class ever touches.
        self.setLayout(QVBoxLayout())
        real_layout = super().layout()  # not self.layout() - that's overridden below, and self._content_layout doesn't exist yet
        real_layout.setSpacing(0)
        self._body_layout = None
        self.fit_shadow()
        self.style.signals.changed.connect(self.fit_shadow)

        self._content_area = QWidget()
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        real_layout.addWidget(self._content_area)

        if menu_bar_label is not None:
            self.menu_bar = MenuBar(self, context, menu_bar_label)

        # Everything added from here on is the body, in the drawer's frame
        # (see layout and fit_frame). Hidden (a minimized panel), it's
        # empty, and takes no room - frame and all.
        self._body_layout = _DrawerLayout()
        self._content_layout.addLayout(self._body_layout, 1)
        self.fit_frame()

        # A whole panel's body (whatever gets added below the menu bar via
        # master.layout().addWidget(body, 1) - Scrollable/Panes and the
        # handful of other direct bodies all pass that explicit stretch=1
        # now) claims 100% of any leftover space over this filler as long
        # as it's visible, since Qt's box layout gives leftover strictly by
        # relative stretch factor (1 beats this filler's default 0) - so
        # this stays squeezed to zero height and invisible in the normal
        # case. The one time it matters is a minimized panel, whose body is
        # hidden entirely: with no stretch=1 item left to compete with, this
        # is the sole remaining widget that can grow, so it - not the menu
        # bar - absorbs the leftover instead of Qt centering the lone
        # capped-height menu bar in it (its default behavior for a single
        # item that can't grow to fill the space it's offered).
        #
        # This replaces an earlier attempt that used QLayout.setAlignment on
        # the menu bar item to pin it to the top: that form makes Qt stop
        # stretching *every* item in the layout to fill its cell (using each
        # one's sizeHint instead) the moment *any* item has an explicit
        # alignment, which broke bodies whose sizeHint is naturally smaller
        # than their pane (e.g. NetworkDiagram's nested Panes splitter) -
        # both leaving a gap under the menu bar and shrinking the body away
        # from filling the pane at all, even fully maximized.
        filler = QWidget()
        filler.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self._content_layout.addWidget(filler)

    def layout(self):
        '''
        Overrides QWidget.layout() (not virtual on the C++ side, so this
        only affects Python-level callers - Qt's own internals keep using
        the real layout installed via setLayout() in __init__ regardless)
        to hand back the inner, border-padded content layout instead. Every
        body constructor (Scrollable, Panes, MenuBar, ...) adds itself via
        the master.layout().addWidget(...) idiom - routing that through
        here is what keeps their content inset from this panel's own
        border without needing any of them (or anything they in turn call,
        like Panes.__init__ resetting contentsMargins) to know a border
        exists at all. Once the menu bar's in, that's the body's layout,
        inside the drawer's frame (see fit_frame).
        '''
        return self._body_layout if self._body_layout is not None else self._content_layout

    def fit_frame(self):
        '''
        The drawer's frame around the body - the theme's "panel_frame" px
        left, right and below, and never so thin the body's square corners
        poke out of its rounded ones - or none with the body hidden
        (minimized), so the menu bar's room is the same above and below it.
        '''
        if self._body_layout is None:
            return
        layout = self._body_layout
        shown = any(not layout.itemAt(i).widget().isHidden() for i in range(layout.count()) if layout.itemAt(i).widget() is not None)
        # A corner's curve is this far in from the corner, along its diagonal - 1 - 1/sqrt(2) of its radius
        clear = math.ceil(self.style.PANEL_RADIUS * (1 - math.sqrt(0.5)))
        frame = max(self.style.setting("panel_frame"), clear) if shown else 0
        layout.frame(frame, 0, frame, frame)

    def showEvent(self, event):
        # Its body's been added since __init__'s fit_frame, which found none
        self.fit_frame()
        super().showEvent(event)

    def margins(self) -> tuple[int, int, int, int]:
        '''The room around it for its shadow (see Style.panel_margins) - none docked, where the DockArea draws it.'''
        return (0, 0, 0, 0) if self.docked else self.style.panel_margins()

    def set_docked(self, docked: bool):
        '''In a DockArea (or back out of one, as a peek's popup): the DockArea draws its shadow, under every panel's.'''
        if docked == self.docked:
            return
        self.docked = docked
        # The stylesheet's room for a shadow (see Style's "shadowed" rule) - matched only when polished
        self.setProperty("shadowed", not docked)
        qt_style = QWidget.style(self)
        qt_style.unpolish(self)
        qt_style.polish(self)
        self.fit_shadow()

    def body_rect(self) -> QRectF:
        '''Where the panel itself is drawn - inside the room for its shadow (see margins).'''
        left, top, right, bottom = self.margins()
        return QRectF(self.rect()).adjusted(left, top, -right, -bottom)

    def fit_shadow(self):
        '''After a theme change: room for the theme's shadow (or none), the border inset inside it, and the mask to match.'''
        left, top, right, bottom = self.margins()
        width = self.BORDER_WIDTH
        super().layout().setContentsMargins(left + width, top + width, right + width, bottom + width)
        self.fit_frame()
        self.update_mask()
        self.update()

    def shadow_image(self) -> QImage | None:
        '''The theme's shadow at this panel's size (see surface_shadow) - None docked (see set_docked).'''
        return None if self.docked else surface_shadow(self.style, self.width(), self.height())

    def paintEvent(self, event):
        # The stylesheet has already drawn the panel itself, inside its shadow's room (see fit_shadow)
        image = self.shadow_image()
        if image is not None:
            painter = QPainter(self)
            painter.drawImage(0, 0, image)
            painter.end()

    def update_mask(self):
        '''
        Clips the panel - menu bar, body and all - to its rounded shape
        (see resizeEvent), so whatever's under it shows past its corners.

        Not one drawing its own shadow: clipped, the bits of shadow just
        outside its corners would be cut away with them, leaving a square
        notch around each rounded corner. Its body never reaches its
        corners anyway (see fit_frame), and its menu bar has no
        background of its own.
        '''
        if self.style.panel_shadow() is not None and not self.docked:
            self.clearMask()
            return
        path = QPainterPath()
        path.addRoundedRect(self.body_rect(), self.style.PANEL_RADIUS, self.style.PANEL_RADIUS)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # border-radius alone only rounds *this* widget's own background -
        # it doesn't clip children, and the menu bar plus whatever body sits
        # below it are both opaque, square-cornered widgets that fill this
        # panel edge-to-edge with zero margin, completely covering its
        # corners. A mask clips the whole widget - menu bar, body, and all -
        # to a rounded-rect region instead, which is the only way the
        # rounding actually shows. Recomputed on every resize since the
        # mask is in this widget's own pixel coordinates.
        self.update_mask()