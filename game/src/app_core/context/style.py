import copy
import json
import re
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QFontDatabase, QLinearGradient
from PySide6.QtWidgets import QApplication, QComboBox, QStyledItemDelegate, QWidget
import darkdetect

from .themes import (BUTTON_KINDS, COLOR_NAMES, DATA_MATERIALS, INK_MATERIALS, MATERIALS, STYLE_DEFAULTS, THEME_MODES, button_radius,
                     gradient_points, is_hex, read_theme, resolve_materials, style_setting, theme_file)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Hand-rolled replacement for qt-material's theme presets. Each theme is a
# list of materials - what each kind of widget is made of, in dark and light
# mode (see themes.py). Blue is built in so the app always has a theme, even
# without assets/ - it's themes.MATERIALS' defaults. Every other theme is a
# <family>.json in assets/themes (see Style._load_theme_files) - one there
# named "blue" replaces it. Every theme is drawn exactly as its file says.
PRESET_INFO: dict[str, dict] = {"blue": {"label": "Blue", "kind": "original"}}
# The default themes - the hand-picked families the theme selector offers
# everyone (most combinations of the theme editor's settings don't look
# good, so these are the ones that do). The first is the theme a fresh
# start, and Reset Theme, use. Imported themes (see IMPORTED_PREFIX) join
# them in the selector; every other preset is only in the theme editor.
CURATED_THEMES: list[str] = ["acrylic", "glassmorphism", "frutiger_aero", "cybercore", "neobrutalism", "webcore",
                             "flat", "kimbie_dark"]
# The user's own themes - <family>.json files in user_data/themes, the same
# shape as assets/themes' (imported, or made in the theme editor - see
# Style.new_theme) - are named "imported.<file name>", so one can never
# replace a bundled preset of the same name. Only these can be edited.
IMPORTED_PREFIX = "imported."

# How widgets are styled: each one names its material (see themes.MATERIALS)
# in a "material" property (see Style.set_material), and the app's one
# stylesheet (see Style._build_stylesheet) gives every material its color
# and opacity from the theme - so a theme change restyles every widget in
# place, without rebuilding the page. Besides the materials, "material"
# can be "none" (see-through, no border). Shape is its own property:
# "rounded" rounds the corners like a panel's, "outlined" adds a panel's
# border.
SPECIAL_MATERIALS = ("none",)
# A label's tone (see Style.set_tone) -> the theme's data color for it
TONES = {"muted": "muted_text", "good": "good", "warning": "warning", "bad": "bad"}
PANEL_BORDER_WIDTH = 2
# The color names (see themes.COLOR_NAMES) color() hands back see-through,
# at their material's opacity - so canvases and other hand-drawn widgets
# naming them follow the theme (e.g. a "field" chart background)
SEE_THROUGH_COLORS = ("panel", "widget", "field")
# The animated page background (see Page.add_background), each saved as a
# preference like the theme: which visual plays (a widgets.visuals.VISUALS
# key, "cycle", or NO_BACKGROUND), whether it moves, whether it's detailed
# in workspaces (the network's packets - title and lesson select pages
# always are; off by default since it's distracting behind panels), its
# frame rate, which visuals the background pickers leave out (chosen on
# the visuals demo page - "cycle" skips them too), and whether workspaces
# hold it still (on by default - it only shows through the gaps between
# panels, and every frame repaints the panels above) or leave it out
NO_BACKGROUND = "none"
DEFAULT_BACKGROUND_VISUAL = "network_mesh"
DEFAULT_BACKGROUND_ANIMATE = True
DEFAULT_BACKGROUND_DETAILED = False
DEFAULT_BACKGROUND_FPS = 30
DEFAULT_BACKGROUND_HIDDEN: tuple[str, ...] = ()
DEFAULT_BACKGROUND_WORKSPACE_FROZEN = True
DEFAULT_BACKGROUND_WORKSPACE_DISABLED = False
BACKGROUND_FPS_RANGE = (1, 120)

# Inverted buttons: text-colored labels on a background between panel and
# root, with a clear border - instead of accent_text on solid accent
DEFAULT_INVERT_BUTTONS = False



class StyleSignals(QObject):
    '''Style isn't a QObject - its signals live here (see Style.signals).'''
    # The theme or button style changed - everything is already
    # restyled; anything that shows those settings can catch up
    changed = Signal()
    # One of the user's themes was edited, saved or discarded (see Style.unsaved)
    edited = Signal()


# The symbols solo buttons show (see Style.icon) - name -> codepoint in
# ICON_FONT, a subset of Tabler Icons (MIT - see its license beside it) with
# just these. Names are Tabler's own; to add one, subset it into the font too.
ICON_FONT = "tabler-icons.ttf"
ICONS: dict[str, int] = {
    "menu-2": 0xec42,
    "arrow-left": 0xea19,
    "arrow-right": 0xea1f,
    "bookmark": 0xea3a,
    "bookmark-filled": 0xfa88,
    "settings": 0xeb20,
    "reload": 0xf3ae,
    "info-circle": 0xeac5,
    "minus": 0xeaf2,
    "square": 0xeb2c,
    "copy": 0xea7a,
    "power": 0xeb0d,
    "bug": 0xea48,
    "palette": 0xeb01,
    "adjustments-horizontal": 0xec38,
    # Marks in text (see _load_icon_font) - dropdowns, overflow, where a button goes
    "caret-down": 0xeb5d,
    "caret-up": 0xeb60,
    "chevrons-right": 0xea65,
    "x": 0xeb55,
    "external-link": 0xea99,
    "layers-subtract": 0xeaca,
    "folder": 0xeaad,
    "alert-triangle": 0xea06,
    "player-play": 0xed46,
    "chevron-right": 0xea61,
    "chevron-down": 0xea5f,
}


class _StyledComboItems(QObject):
    '''
    Gives every combobox the item painter that follows the stylesheet
    (QStyledItemDelegate) as it's first styled - its own one paints its
    open list's items in the combobox's colors instead, whatever the
    stylesheet says (see Style._build_stylesheet).
    '''

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Polish and isinstance(watched, QComboBox) and not watched.property("styled_items"):
            watched.setProperty("styled_items", True)
            watched.setItemDelegate(QStyledItemDelegate(watched))
        return False


class Style:

    def __init__(self, context: "Context"):

        self.ui_scale = 100.0
        self.ui_scales = [25, 33, 50, 67, 75, 80, 90, 100, 110, 125, 133, 140, 150, 175, 200, 250, 300, 400, 500]

        self.root = context.root
        self.gap = (10, 10)
        self.gap2 = (20,20)
        self.nogap = (0, 0)
        self.gaptop = (10, 0)
        self.gapbot = (0, 10)
        self.igap = 10
        self.cgap = 2
        self.PANE_MIN_WIDTH = self.igap*10
        self.PANE_MIN_HEIGHT = self.igap*10
        self.PANE_BIG = self.igap*100
        self.fonts = {}
        # Font families already standing in for the icon font's glyphs (see _substitute_icons)
        self._icon_substitutes: set[str] = set()
        self.context = context
        # The icon font's family once loaded (see icon) - None if it couldn't be
        self.icon_family: str | None = self._load_icon_font(context.paths.fonts / ICON_FONT)
        self.signals = StyleSignals()
        # Widgets with colors in their own stylesheet, rebuilt on every theme
        # change (see live_style): id -> (widget, builder)
        self._live_sheets: dict[int, tuple[QWidget, Callable[[], str]]] = {}
        # Theme edits come many times a second during a slider drag or color
        # pick (see set_material_value) - restyling waits for a pause
        self._restyle_timer = QTimer()
        self._restyle_timer.setSingleShot(True)
        self._restyle_timer.setInterval(30)
        self._restyle_timer.timeout.connect(lambda: self.restyle(notify=False))
        # The user's themes with edits not yet saved to their files (see save_theme)
        self.unsaved: set[str] = set()

        # Surface settings (see materials) - load_preferred_surfaces()
        # replaces these defaults once preferences exist
        self.invert_buttons: bool = DEFAULT_INVERT_BUTTONS
        # Background settings - load_preferred_background() replaces these
        # defaults once preferences exist
        self.background_visual: str = DEFAULT_BACKGROUND_VISUAL
        self.background_animate: bool = DEFAULT_BACKGROUND_ANIMATE
        self.background_detailed: bool = DEFAULT_BACKGROUND_DETAILED
        self.background_fps: int = DEFAULT_BACKGROUND_FPS
        self.background_hidden: list[str] = list(DEFAULT_BACKGROUND_HIDDEN)
        self.background_workspace_frozen: bool = DEFAULT_BACKGROUND_WORKSPACE_FROZEN
        self.background_workspace_disabled: bool = DEFAULT_BACKGROUND_WORKSPACE_DISABLED

        # Preferences don't exist yet at this point in startup (see
        # ContextManager.start_session) - this is just a system-appropriate
        # bootstrap default; load_preferred_theme() overrides it once
        # preferences are available.
        # Each theme's materials (see themes.py)
        self.materials: dict[str, dict[str, dict[str, dict]]] = {name: resolve_materials(None) for name in PRESET_INFO}
        self.preset_info: dict[str, dict] = dict(PRESET_INFO)
        self._load_theme_files()
        # The current theme's materials' colors in the current mode, name -> "#rrggbb" (see _resolve_colors)
        self._colors: dict[str, str] = {}
        self.apply_theme(self.default_theme())

    def packing(self, type = "default"):
        options = {}

        if type == "default":
            options = {
                "fill": "both",
                "expand": True,
                "padx": self.gap,
                "pady": self.gap
            }

        if type == "panel":
            options = {
                "fill": "both",
                "expand": True,
                "padx": self.nogap,
                "pady": self.nogap
            }

        return options

    def get_scale_correction(self):
        # Qt applies its own DPI scaling to the widgets/fonts it lays out,
        # so no manual correction is needed here the way CTk's
        # ScalingTracker required. Revisit if a canvas-drawn panel (which
        # positions pixels by hand) needs its own correction once migrated.
        return 1.0

    def get_font(self, name="default"):
        if name not in self.fonts:
            if name == "default":
                font = QFont("Arial", self.get_font_size("default"))
            elif name == "title_btn":
                font = QFont()
                font.setPointSize(self.get_font_size("title_btn"))
            elif name == "mono":
                font = QFont("Consolas", self.get_font_size("small"))
            elif name == "treeview":
                font = QFont("Consolas", self.get_font_size("treeview"))
            elif name == "title":
                font = QFont("Arial", self.get_font_size("title"))
                font.setBold(True)
            elif name == "page_title":
                font = QFont("Arial", self.get_font_size("page_title"))
                font.setBold(True)
            elif name == "icon":
                font = QFont(self.icon_family or "Arial", self.get_font_size("icon"))
            elif name == "chart_title":
                font = QFont("Arial", self.get_font_size("chart_title"))
                font.setBold(True)
            elif name == "chart_numbers":
                font = QFont("Consolas", self.get_font_size("chart_numbers"))
            elif name == "chart_label":
                font = QFont("Arial", self.get_font_size("chart_label"))
            else:
                font = QFont()
                font.setPointSize(int(14.0*self.ui_scale/100.0))
            self.fonts[name] = font
        return self.fonts[name]

    @staticmethod
    def _load_icon_font(path: Path) -> str | None:
        '''
        Loads the icon font, and has it stand in for the text fonts' missing
        glyphs (QFont.insertSubstitution) - icons live in the private use
        area no text font covers, so an icon in a label's text ("Captures"
        and a dropdown caret, say) is drawn from the icon font, in the
        text's own color and size. Returns its family.
        '''
        font_id = QFontDatabase.addApplicationFont(str(path))
        families = QFontDatabase.applicationFontFamilies(font_id) if font_id >= 0 else []
        if not families:
            print(f"Couldn't load the icon font {path} - icons will show as blanks")
            return None
        # Every family text is drawn in - the fonts get_font names, and Qt's default
        for family in {"Arial", "Consolas", QApplication.font().family()}:
            QFont.insertSubstitution(family, families[0])
        return families[0]

    def _substitute_icons(self, family: str | None):
        '''A theme's own font (see themes.STYLE_DEFAULTS' "font_family") shows icons in text too - see _load_icon_font.'''
        if family and self.icon_family and family not in self._icon_substitutes:
            QFont.insertSubstitution(family, self.icon_family)
            self._icon_substitutes.add(family)

    def icon_css(self) -> str:
        '''
        The "icon" font as stylesheet declarations - for icon widgets with a
        stylesheet of their own, which (re)setting would otherwise reset
        their font to their parent's.
        '''
        return f"font-family: \"{self.icon_family or 'Arial'}\"; font-size: {self.get_font_size('icon')}pt;"

    @staticmethod
    def icon(name: str) -> str:
        '''One of ICONS as text, for a widget using the "icon" font (see get_font).'''
        return chr(ICONS[name])

    def get_font_size(self, name="default"):
        size = 16.0
        if name == "title_btn":
            size = 20.0
        elif name == "title":
            size = 72
        elif name == "page_title":
            size = 21.0
        elif name == "icon":
            size = 18.0
        elif name == "small":
            size = 15.0
        elif name == "chart_title":
            size = 13.0
        elif name == "chart_numbers":
            size = 10.0
        elif name == "chart_label":
            size = 10.0
        return int(size * self.ui_scale / 100.0)

    # The color names color() resolves (see themes.COLOR_NAMES) - also the
    # options the style editors offer (see important_buttons/settings_overlays)
    THEME_COLOR_NAMES = tuple(COLOR_NAMES) + DATA_MATERIALS

    def color(self, type: str, opaque: bool = False) -> str:
        '''
        A theme color for hand-drawn widgets and the few stylesheet rules
        that aren't backgrounds (text, borders): one of THEME_COLOR_NAMES or
        a material's name gives that material's color now, and anything
        else (e.g. "red" or a hex code) comes back as it is.

        "panel", "widget" and "field" come back at their material's opacity
        (see SEE_THROUGH_COLORS) - "#AARRGGBB" when see-through, which both
        stylesheets and QColor understand. opaque=True gives them solid.
        Backgrounds should name their material instead (see set_material).
        '''
        material = COLOR_NAMES.get(type, type)
        if material not in self._colors:
            return type
        if type in SEE_THROUGH_COLORS and not opaque:
            return self.material(material).name(QColor.NameFormat.HexArgb)
        return self._colors[material]

    def get_column_width(self, column_name):
        match column_name:
            case "time":
                return int(120*self.get_scale_correction())
            case "number":
                return int(70*self.get_scale_correction())
            case "length":
                return int(80*self.get_scale_correction())
            case "observer":
                return int(120*self.get_scale_correction())
            case "transaction_word":
                return int(100*self.get_scale_correction())
            case "transaction_ip":
                return int(450*self.get_scale_correction())
            case "transaction_mac":
                return int(450*self.get_scale_correction())
            case "layers":
                return int(250*self.get_scale_correction())
            case "protocol":
                return int(100*self.get_scale_correction())
            case "purpose":
                return int(200*self.get_scale_correction())
            case "summary":
                return int(600*self.get_scale_correction())
            case "modbus":
                return int(400*self.get_scale_correction())
        return 100

    def get_scrollbar_size(self):
        return 12 * self.get_scale_correction()

    def pad_corrected(self):
        return int(self.igap * self.get_scale_correction())

    def add_tooltip(self, widget, class_key: str, widget_key: str):
        widget.setToolTip(self.context.labels.get(f"{class_key}_{widget_key}"))

    def apply_theme(self, theme_name: str):
        '''
        Applies a theme ("<mode>_<family>") to every widget, in place (see
        restyle) - nothing needs rebuilding.
        '''
        mode, _, family = theme_name.partition("_")
        app = QApplication.instance()
        # First - the materials (see material) are the current theme's
        self.current_theme = theme_name
        self.mode = "Dark" if mode == "dark" else "Light"
        self._resolve_colors()
        # The native platform style (e.g. "windows11") largely ignores QSS
        # background-color/border-radius on QPushButton/QComboBox/QCheckBox -
        # Fusion is the style Qt's own docs recommend for full stylesheet
        # control, and what qt-material used under the hood for the same
        # reason. Only set it once: re-applying the same style on every theme
        # change (toggle_mode/set_theme trigger this repeatedly in one
        # session) leaves QScrollArea-based panels (Scrollable) with a stale,
        # unrepainted viewport background from the previous theme.
        if app.style().objectName().lower() != "fusion":
            app.setStyle("Fusion")
        self._substitute_icons(self.setting("font_family"))
        self.restyle()
        # The theme can turn the page background off, or blur it (see themes.STYLE_DEFAULTS)
        self.apply_background()

    # Styling widgets
    def set_material(self, widget: QWidget, material: str, rounded: bool = False, outlined: bool = False):
        '''
        Gives widget its background from the theme: one of
        themes.MATERIALS or SPECIAL_MATERIALS, optionally with a panel's
        rounded corners and border - styled by the app stylesheet, so it
        follows every theme change by itself. Can be changed any time.
        '''
        widget.setProperty("material", material)
        widget.setProperty("rounded", rounded)
        widget.setProperty("outlined", outlined)
        # A plain QWidget only paints a stylesheet background with this
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        if widget.testAttribute(Qt.WidgetAttribute.WA_WState_Polished):
            # Property selectors are only matched when a widget is polished.
            # QWidget.style, not widget.style - widgets that keep this Style
            # as their own .style (MenuBar, say) hide Qt's method
            qt_style = QWidget.style(widget)
            qt_style.unpolish(widget)
            qt_style.polish(widget)
            widget.update()

    def live_style(self, widget: QWidget, build: Callable[[], str]):
        '''
        Sets widget's own stylesheet to build(), and sets it again after
        every theme change - for the few rules that need colors (text,
        borders) beyond what set_material gives. build's rules need
        selectors: a bare declaration list would style every child too.
        '''
        key = id(widget)
        self._live_sheets[key] = (widget, build)
        widget.destroyed.connect(lambda *_: self._live_sheets.pop(key, None))
        widget.setStyleSheet(build())

    def css(self, material: str, shade: float = 0.0) -> str:
        '''
        A material's color for a stylesheet, as "rgba(r, g, b, a)" - or its
        gradient (see themes.read_gradient), as a "qlineargradient(...)",
        which stylesheets take anywhere a color goes. shade lightens it
        (> 0) or darkens it, keeping its opacity (see _shade).

        A gradient's stops keep their own opacities while surfaces can be
        see-through; solid (see material), every stop takes the
        material's opacity instead.
        '''
        color = self.material(material)
        entry = self.material_entry(material)
        gradient = entry.get("gradient")
        if gradient is None or material in INK_MATERIALS:
            if shade:
                alpha = color.alpha()
                color = QColor(self._shade(color.name(), shade))
                color.setAlpha(alpha)
            return self._css(color)
        solid = abs(color.alphaF() - entry["opacity"]) > 0.003
        stops = []
        for position, hex_color, opacity in gradient["stops"]:
            stop = QColor(self._shade(hex_color, shade) if shade else hex_color)
            stop.setAlphaF(color.alphaF() if solid else opacity)
            stops.append(f"stop:{position:g} {self._css(stop)}")
        x1, y1, x2, y2 = gradient_points(gradient["angle"])
        return f"qlineargradient(x1:{x1:.3f}, y1:{y1:.3f}, x2:{x2:.3f}, y2:{y2:.3f}, {', '.join(stops)})"

    def brush(self, material: str, rect: QRectF) -> QBrush:
        '''A material as a QBrush filling rect - its gradient across rect if it has one - for hand-painted backgrounds.'''
        color = self.material(material)
        entry = self.material_entry(material)
        gradient = entry.get("gradient")
        if gradient is None or material in INK_MATERIALS:
            return QBrush(color)
        solid = abs(color.alphaF() - entry["opacity"]) > 0.003
        x1, y1, x2, y2 = gradient_points(gradient["angle"])
        fill = QLinearGradient(QPointF(rect.left() + x1 * rect.width(), rect.top() + y1 * rect.height()),
                               QPointF(rect.left() + x2 * rect.width(), rect.top() + y2 * rect.height()))
        for position, hex_color, opacity in gradient["stops"]:
            stop = QColor(hex_color)
            stop.setAlphaF(color.alphaF() if solid else opacity)
            fill.setColorAt(position, stop)
        return QBrush(fill)

    @staticmethod
    def _css(color: QColor) -> str:
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"

    def restyle(self, notify: bool = True):
        '''
        Rebuilds the app stylesheet (Qt restyles every widget from it) and
        every live_style sheet, then lets everything else know (see
        StyleSignals.changed) - unless notify is False, for edits whose
        controls already show them (see set_material_value). After any
        change to the theme or button style.
        '''
        self._restyle_timer.stop()
        app = QApplication.instance()
        if not hasattr(self, "_combo_items"):
            self._combo_items = _StyledComboItems(app)
            app.installEventFilter(self._combo_items)
        app.setStyleSheet(self._build_stylesheet())
        # Links in text (workspace summaries, notes) - stylesheets can't color them
        palette = app.palette()
        link = QColor(self.link_color())
        for role in (palette.ColorRole.Link, palette.ColorRole.LinkVisited):
            palette.setColor(role, link)
        app.setPalette(palette)
        for key, (widget, build) in list(self._live_sheets.items()):
            try:
                widget.setStyleSheet(build())
            except RuntimeError:  # already deleted on the C++ side
                self._live_sheets.pop(key, None)
        if notify:
            self.signals.changed.emit()

    @staticmethod
    def _shade(hex_color: str, amount: float) -> str:
        '''
        Blends hex_color toward white (amount > 0) or black (amount < 0) by
        the given fraction - used to derive button/slider hover and pressed
        shades from a theme's single button color, instead of hand-authoring
        extra materials per theme per mode.
        '''
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        target = 255 if amount > 0 else 0
        amount = abs(amount)
        r, g, b = (int(v + (target - v) * amount) for v in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_card(self, material: str) -> str:
        '''What material looks like where it's used, inside a panel: over the card, over the drawer (see themes' module docstring) - "#rrggbb".'''
        color = QColor(self.color("panel", opaque=True))
        for layer in ("card", material):
            top = self.material(layer)
            a = top.alphaF()
            color = QColor.fromRgbF(top.redF() * a + color.redF() * (1 - a), top.greenF() * a + color.greenF() * (1 - a),
                                    top.blueF() * a + color.blueF() * (1 - a))
        return color.name()

    def readable_on(self, background: str) -> str:
        '''
        Text for a background "#rrggbb": the theme's own text colors, in
        order, until one reads on it (WCAG's 4.5:1) - else whichever of
        black or white reads best.
        '''
        for name in ("text", "menu_bar_text", "field_text", "accent_text"):
            if self._contrast(self.color(name), background) >= 4.5:
                return self.color(name)
        return max(("#000000", "#ffffff"), key=lambda color: self._contrast(color, background))

    @staticmethod
    def _contrast(hex_a: str, hex_b: str) -> float:
        '''The WCAG contrast ratio of two colors - 1 (the same) to 21 (black on white).'''
        def luminance(hex_color: str) -> float:
            channels = []
            for i in (1, 3, 5):
                v = int(hex_color[i:i + 2], 16) / 255
                channels.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
            return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
        high, low = sorted((luminance(hex_a), luminance(hex_b)), reverse=True)
        return (high + 0.05) / (low + 0.05)

    def link_color(self) -> str:
        '''
        Links' color: the accent - moved toward the text color, a step at a
        time, until it reads on a panel (WCAG's 4.5:1 for text).
        '''
        accent, text, panel = self.color("accent"), self.color("text"), self.color("panel", opaque=True)
        for step in range(11):
            color = self._mix(accent, text, step / 10)
            if self._contrast(color, panel) >= 4.5:
                return color
        return text

    def disabled_text(self) -> str:
        '''
        A disabled button's text (and outline): the text color faded toward
        what the buttons that get disabled sit on - a form's card - but only
        as far as it still reads on it (3:1 - dimmer than any enabled text,
        never lost in it). Not toward the panel: a theme's panel can be a
        loud color that tints it.
        '''
        text, card = self.color("text"), self.color("widget", opaque=True)
        for step in range(7, -1, -1):
            color = self._mix(text, card, step / 10)
            if self._contrast(color, card) >= 3:
                return color
        return text

    @staticmethod
    def _mix(hex_a: str, hex_b: str, amount: float) -> str:
        '''hex_a blended amount (0-1) of the way to hex_b.'''
        a, b = QColor(hex_a), QColor(hex_b)
        channels = (round(x + (y - x) * amount) for x, y in ((a.red(), b.red()), (a.green(), b.green()), (a.blue(), b.blue())))
        return "#" + "".join(f"{v:02x}" for v in channels)

    def _build_stylesheet(self) -> str:
        '''
        Hand-rolled replacement for qt-material's generated QSS: the native
        widgets this app uses (buttons, text boxes, checkboxes, combo boxes,
        tabs, trees, scrollbars, sliders, tooltips) and every material's
        rule (see set_material), all from the current theme's materials.
        '''
        # By the names the rules were written with (see themes.COLOR_NAMES), solid
        c = {name: self.color(name, opaque=True) for name in COLOR_NAMES}
        m = self.css
        scroll_w = int(self.get_scrollbar_size())

        def shaded(material: str, amount: float) -> str:
            '''A material lightened (amount > 0) or darkened, keeping its opacity.'''
            return self.css(material, amount)

        def at_opacity(color: str, material: str) -> str:
            '''A theme color (see color) or hex code at a material's opacity.'''
            qcolor = QColor(c.get(color, color))
            qcolor.setAlpha(self.material(material).alpha())
            return self._css(qcolor)

        if self.invert_buttons:
            # Text-colored, on a background between panel and root, with a
            # border drawn toward the text color so each button stays
            # clearly outlined against whatever it sits on
            button_bg = at_opacity(self._mix(c["panel"], c["root"], 0.5), "button")
            buttons = f'''
            QPushButton {{
                background-color: {button_bg};
                color: {c["text"]};
                border: 1px solid {self._mix(c["panel"], c["text"], 0.4)};
                border-radius: 4px;
                padding: 5px 11px;
            }}
            QPushButton:hover {{ background-color: {at_opacity("widget", "button")}; border-color: {c["accent"]}; }}
            QPushButton:pressed {{ background-color: {at_opacity("root", "button")}; border-color: {c["accent"]}; }}'''
        else:
            buttons = "".join(self._button_rules(kind, shaded) for kind in BUTTON_KINDS)
        # Disabled buttons of every kind look alike, whatever the theme: no
        # face of their own, just a dashed outline - still a button, plainly
        # not one to press - and text dimmed only as far as it still reads (see disabled_text)
        disabled = self.disabled_text()
        buttons += f'''
            QPushButton:disabled {{ background-color: transparent; color: {disabled};
                                    border-color: {disabled}; border-style: dashed; }}'''

        # The theme's outlines (see themes.STYLE_DEFAULTS): bevelled, or lines line_width thick
        bevel = self.setting("bevel")
        line = self.setting("line_width")
        outline = self.bevel(c["border"], raised=False) if bevel else f"{line}px solid {c['border']}"
        header_border = self.bevel(c["widget"]) if bevel else outline
        tab_shape = f"border: {self.bevel(c['widget'])}; border-bottom: none;" if bevel else ""
        panel_border = (self.bevel(self.color("panel_border")) if bevel
                        else f"{PANEL_BORDER_WIDTH}px solid {m('panel_border')}")
        # Scrollbars (see themes.STYLE_DEFAULTS): a handle inset in its track, pill-shaped unless the theme says
        inset = self.setting("scrollbar_inset")
        thickness = max(2, scroll_w - 2 * inset)
        radius = self.setting("scrollbar_radius")
        handle_radius = thickness // 2 if radius is None else min(radius, thickness // 2)
        if bevel:
            handle_border = self.bevel(c["scrollbar"])
        elif self.setting("scrollbar_outline"):
            handle_border = f"{line}px solid {c['border']}"
        else:
            handle_border = "none"
        left, top, right, bottom = self.panel_margins()
        font = self.setting("font_family")
        extras = []
        if font:
            # Not consoles, trees and tables - their monospace font is part of what they show
            extras.append(f'QPushButton, QLabel, QCheckBox, QRadioButton, QTabBar, QComboBox, QLineEdit, QHeaderView, QToolTip,'
                          f' QSpinBox {{ font-family: "{font}"; }}')
        # A label's tone (see set_tone) - after the rules above, so it wins over them
        extras_after = [f'QLabel[tone="{tone}"] {{ color: {self.color(name)}; }}' for tone, name in TONES.items()]
        # Column headers: text that reads on the header's own color, whatever the theme makes it
        header_text = self.readable_on(self.on_card("table_header"))
        extras_after.append(f'QLabel[material="table_header"] {{ color: {header_text}; }}')
        if self.setting("bold_buttons"):
            extras.append("QPushButton, QTabBar { font-weight: bold; }")
        if self.color("menu_bar_text") != c["text"]:
            # Text on a panel's drawer - its menu bar, and anything straight on
            # its frame - but not on what's inside it (see themes' module docstring)
            extras.append(f'*[material="panel"] QLabel, *[material="panel"] QCheckBox {{ color: {self.color("menu_bar_text")}; }}')
            inside = ", ".join(f'*[material="{name}"] QLabel, *[material="{name}"] QCheckBox'
                               for name in ("card", "field", "alternate_row", "table_header", "overlay", "overlay_card"))
            extras.append(f'{inside} {{ color: {c["text"]}; }}')

        return f'''
            QWidget {{ color: {c["text"]}; }}
            QMainWindow, QDialog {{ background-color: {m("window")}; }}
            QToolTip {{
                background-color: {m("tooltip")};
                color: {c["text"]};
                border: 1px solid {c["border"]};
            }}
            {buttons}
            QTabWidget::pane {{ border: {outline}; border-radius: {0 if bevel else 4}px; }}
            QTabBar::tab {{
                background-color: {m("tab")};
                color: {c["text"]};
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
                {tab_shape}
            }}
            QTabBar::tab:selected {{ background-color: {m("tab_selected")}; color: {c["accent_text"]}; }}
            QTabBar::tab:hover:!selected {{ background-color: {m("panel")}; }}
            QLineEdit, QComboBox, QPlainTextEdit, QTextEdit {{
                background-color: {m("field")};
                color: {c["field_text"]};
                border: {outline};
                border-radius: {0 if bevel else 4}px;
                padding: 4px;
            }}
            QPlainTextEdit, QTextEdit {{ background-color: {m("card")}; }}
            QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border-color: {c["accent"]}; }}
            QLineEdit:read-only {{ background-color: transparent; }}
            QComboBox QAbstractItemView {{
                background-color: {self.color("overlay")};
                border: none;
                outline: 0px;
                padding: 2px;
            }}
            QComboBox QAbstractItemView::item {{
                color: {self.readable_on(self.color("overlay"))};
                padding: 4px 8px;
                border: none;
            }}
            QComboBox QAbstractItemView::item:selected, QComboBox QAbstractItemView::item:hover {{
                background-color: {m("selection")};
                color: {c["accent_text"]};
            }}
            QComboBoxPrivateContainer {{
                background-color: {self.color("overlay")};
                border: {line}px solid {c["border"]};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: {outline};
                border-radius: {0 if bevel else 3}px;
                background-color: {m("field")};
            }}
            QCheckBox::indicator:checked {{
                background-color: {c["accent"]};
                border-color: {c["accent"]};
            }}
            QHeaderView {{ background-color: transparent; }}
            QHeaderView::section {{
                background-color: {m("table_header")};
                color: {header_text};
                border: {header_border};
                padding: 4px;
            }}
            QTreeWidget, QTreeView, QTableWidget, QTableView {{
                background-color: {m("card")};
                alternate-background-color: {m("alternate_row")};
                color: {c["text"]};
                border: {outline};
                gridline-color: {c["field"]};
            }}
            QTreeWidget::item:selected, QTreeView::item:selected, QTableWidget::item:selected, QTableView::item:selected {{
                background-color: {m("selection")};
                color: {c["accent_text"]};
            }}
            QSlider::groove:horizontal {{
                background: {m("field")};
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {c["accent"]};
                width: 14px;
                margin: -6px 0;
                border-radius: 7px;
            }}
            QScrollBar:vertical {{
                background: {m("field")};
                width: {scroll_w}px;
                margin: 0px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {m("scrollbar")};
                border: {handle_border};
                border-radius: {handle_radius}px;
                margin: {inset}px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {c["scrollbar_hover"]}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
            QScrollBar:horizontal {{
                background: {m("field")};
                height: {scroll_w}px;
                margin: 0px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background: {m("scrollbar")};
                border: {handle_border};
                border-radius: {handle_radius}px;
                margin: {inset}px;
                min-width: 24px;
            }}
            QScrollBar::handle:horizontal:hover {{ background: {c["scrollbar_hover"]}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
            QAbstractScrollArea::corner {{ background: {m("field")}; border: none; }}
            *[material="panel"] QAbstractScrollArea {{ border: none; border-radius: 0px; }}
            {self._material_rules()}
            *[material="overlay"] {{ border: 2px solid {c["accent"]}; }}
            *[material="none"] {{ background-color: transparent; border: none; }}
            *[rounded="true"] {{ border-radius: {self.PANEL_RADIUS}px; }}
            *[outlined="true"] {{ border: {panel_border}; }}
            *[shadowed="true"] {{ margin: {top}px {right}px {bottom}px {left}px; }}
            {" ".join(extras)}
            {" ".join(extras_after)}
        '''

    def _button_rules(self, kind: str, shaded: Callable[[str, float], str]) -> str:
        '''
        The stylesheet rules for one of themes.BUTTON_KINDS, from its
        materials. Plain buttons are every QPushButton; a menu button is
        one with the "button_kind" property "menu" (see mark_menu_button) -
        and checked, it looks hovered and marked (the selected workspace). Its outline
        is always there, if see-through, so a theme's choice of outline
        never changes a button's size.
        '''
        selector = "QPushButton" if kind == "button" else 'QPushButton[button_kind="menu"]'
        checked = f", {selector}:checked" if kind != "button" else ""
        line = self.setting("line_width")
        depth = self.setting("button_shadow")
        if self.setting("bevel"):
            # Raised, and sunken while pressed (see themes.STYLE_DEFAULTS)
            color = self.color(f"{kind}_border")
            border = f"border: {self.bevel(color)};"
            pressed = f"border: {self.bevel(color, raised=False)};"
        elif depth:
            # A hard shadow below and right, which pressing sinks into - the same size throughout
            border = (f"border: {line}px solid {self.css(f'{kind}_border')};"
                      f" border-right-width: {line + depth}px; border-bottom-width: {line + depth}px; margin: 0px;")
            pressed = f"border-right-width: {line}px; border-bottom-width: {line}px; margin: {depth}px 0px 0px {depth}px;"
        else:
            border = f"border: {line}px solid {self.css(f'{kind}_border')};"
            pressed = ""
        # A checked menu button (the selected workspace) stays pressed in - or,
        # where pressing looks like nothing, gets a bar in the accent color on
        # its left, its padding giving up the room so its text stays put
        bar = 3
        selected = pressed or (f"border-left: {line + bar}px solid {self.color('accent')};"
                               f" padding-left: {max(0, 11 - bar)}px;")
        selected_rule = (f"{selector}:checked {{ {selected} }}") if checked else ""
        return f'''
            {selector} {{
                background-color: {self.css(kind)};
                color: {self.color(f"{kind}_text")};
                {border}
                border-radius: {self.button_radius(kind)}px;
                padding: 5px 11px;
            }}
            {selector}:hover{checked} {{ background-color: {self.css(f"{kind}_hover")}; color: {self.color(f"{kind}_hover_text")}; }}
            {selector}:pressed {{ background-color: {shaded(f"{kind}_hover", -0.1)}; color: {self.color(f"{kind}_hover_text")}; {pressed} }}
            {selected_rule}'''

    def bevel(self, color: str, raised: bool = True) -> str:
        '''
        A 3D outline for a stylesheet's "border" (see themes.STYLE_DEFAULTS'
        "bevel"): lit top and left, shaded bottom and right - the other way
        round when sunken. Made from color, like an old desktop's chrome.
        '''
        light, dark = self._shade(color, 0.85), self._shade(color, -0.55)
        top, bottom = (light, dark) if raised else (dark, light)
        return f"2px solid; border-color: {top} {bottom} {bottom} {top}"

    def set_tone(self, label: QWidget, tone: str | None):
        '''
        Colors label's text by what it says (see TONES) - "muted", "good",
        "warning" or "bad" - from the theme, following every theme change.
        None goes back to the plain text color.
        '''
        if label.property("tone") == (tone or ""):
            return  # Callers often set it every frame - restyling is only for a change
        label.setProperty("tone", tone or "")
        if label.testAttribute(Qt.WidgetAttribute.WA_WState_Polished):
            qt_style = QWidget.style(label)
            qt_style.unpolish(label)
            qt_style.polish(label)

    @staticmethod
    def mark_menu_button(button: QWidget):
        '''Styles button as a menu button (see themes.BUTTON_KINDS) - the title menu's and the workspace list's.'''
        button.setProperty("button_kind", "menu")

    def _material_rules(self) -> str:
        '''Each material's background, for widgets set_material gave it.'''
        return "\n".join(f'*[material="{name}"] {{ background-color: {self.css(name)}; }}' for name in MATERIALS)

    # Materials
    def theme_materials(self) -> dict[str, dict[str, dict]]:
        '''The current theme's materials (see themes.py) - every one, for both modes.'''
        return self.materials.get(self.theme_family()) or resolve_materials(None)

    def material_entry(self, name: str) -> dict:
        '''One material in the current mode: {"color": "#rrggbb", "opacity": 0-1}.'''
        return self.theme_materials()[name][self.current_theme.partition("_")[0]]

    def material(self, name: str) -> QColor:
        '''
        What a material (see themes.MATERIALS) looks like right now: its
        color at its opacity - or solid, in a theme that doesn't allow
        transparency (see allows_transparency), or for text and lines (see
        themes.INK_MATERIALS).

        Buttons' see-through parts are part of their design, though, not
        just a look through to what's behind - solid, a button's (fully)
        transparent background or outline stays that way, and its hover
        keeps its own opacity over a transparent background (a ghost
        button's tint) - see button_opacity.
        '''
        entry = self.material_entry(name)
        color = QColor(entry["color"])
        if name in INK_MATERIALS:
            return color
        if self.allows_transparency():
            color.setAlphaF(entry["opacity"])
        else:
            opacity = self.button_opacity(name, entry["opacity"])
            # Solid - but a material left out (opacity 0, e.g. a scrollbar's
            # empty track) stays left out, rather than turning solid
            color.setAlphaF(opacity if opacity is not None else (0.0 if entry["opacity"] == 0 else 1.0))
        return color

    def button_opacity(self, name: str, opacity: float) -> float | None:
        '''A button material's opacity while surfaces are solid (see material) - None for any other material.'''
        kind = next((kind for kind in BUTTON_KINDS if name in (kind, f"{kind}_hover", f"{kind}_border")), None)
        if kind is None:
            return None
        if name == f"{kind}_border":
            return opacity
        if name == f"{kind}_hover" and self.material_entry(kind)["opacity"] == 0:
            return opacity
        return 0.0 if opacity == 0 else 1.0

    def button_radius(self, kind: str = "button") -> int:
        '''The current theme's corner radius for one of themes.BUTTON_KINDS, in px.'''
        return button_radius(self.preset_info.get(self.theme_family(), {}), kind)

    def set_button_radius(self, kind: str, radius: int):
        '''The current theme's corner radius for one of themes.BUTTON_KINDS.'''
        if not self.is_editable() or radius == self.button_radius(kind):
            return
        self.preset_info[self.theme_family()][f"{kind}_radius"] = int(radius)
        self._edited(self.theme_family())

    # The theme's other look settings (see themes.STYLE_DEFAULTS)
    def setting(self, key: str, family: str | None = None):
        '''One of themes.STYLE_DEFAULTS for a theme (the current one, by default).'''
        family = family or (self.theme_family() if hasattr(self, "current_theme") else "blue")
        return style_setting(self.preset_info.get(family, {}), key)

    def set_setting(self, key: str, value):
        '''Changes one of the current theme's look settings (see themes.STYLE_DEFAULTS) - restyled at once.'''
        if not self.is_editable() or value == self.setting(key):
            return
        self.preset_info[self.theme_family()][key] = value
        self._edited(self.theme_family(), notify=True)
        self.apply_background()

    @property
    def PANEL_RADIUS(self) -> int:
        '''Panels' corner radius in px, from the theme ("panel_radius").'''
        return self.setting("panel_radius")

    def panel_shadow(self) -> dict | None:
        '''The theme's shadow around panels in the current mode - {"x", "y", "blur", "color", "opacity"} - or None.'''
        shadow = self.setting("panel_shadow")
        if shadow is None:
            return None
        mode = self.current_theme.partition("_")[0]
        if shadow[mode]["opacity"] <= 0:
            return None
        return {"x": shadow["x"], "y": shadow["y"], "blur": shadow["blur"], **shadow[mode]}

    def panel_margins(self) -> tuple[int, int, int, int]:
        '''Room around each panel for its shadow (see panel_shadow) - left, top, right, bottom, in px.'''
        shadow = self.panel_shadow()
        if shadow is None:
            return 0, 0, 0, 0
        blur, x, y = shadow["blur"], shadow["x"], shadow["y"]
        return max(0, blur - x), max(0, blur - y), max(0, blur + x), max(0, blur + y)

    def background_shown(self, menu: bool = False, workspace: bool = False) -> bool:
        '''
        Whether a page shows its animated background - any visual but
        NO_BACKGROUND, unless the theme turns it off, or it's a workspace
        and "Disable Background in Workspaces" is on. Title menu pages (menu)
        always follow the preference: there the background is the page.
        '''
        if workspace and self.background_workspace_disabled:
            return False
        return self.background_visual != NO_BACKGROUND and (menu or self.setting("background"))

    def background_frozen(self, workspace: bool = False) -> bool:
        '''
        Whether the background holds still - frozen by the preference (or,
        in a workspace, the workspace one), or by there being no background to animate.
        '''
        return (not self.background_animate or self.background_visual == NO_BACKGROUND
                or (workspace and self.background_workspace_frozen))

    def _resolve_colors(self):
        mode = self.current_theme.partition("_")[0]
        self._colors = {name: modes[mode]["color"] for name, modes in self.theme_materials().items()}

    def allows_transparency(self, family: str | None = None) -> bool:
        '''Whether a theme (the current one, by default) lets surfaces be see-through at all ("transparency" - see themes.py).'''
        return self.preset_info.get(family or self.theme_family(), {}).get("transparency", True) is not False

    # Surfaces
    def load_preferred_surfaces(self):
        '''Reads the saved surface settings, keeping the default for anything missing or invalid.'''
        if isinstance(self.context.preferences.get("invert_buttons"), bool):
            self.invert_buttons = self.context.preferences.get("invert_buttons")
        self.restyle()

    def load_default_surfaces(self):
        '''Back to the default surface settings, without saving - like load_default_theme.'''
        self.invert_buttons = DEFAULT_INVERT_BUTTONS
        self.restyle()

    # Background
    BACKGROUND_PREFERENCES = {
        # attribute: (preference key, type)
        "background_visual": ("background_visual", str),
        "background_animate": ("background_animate", bool),
        "background_detailed": ("background_detailed", bool),
        "background_fps": ("background_fps", int),
        "background_hidden": ("background_hidden", list),
        "background_workspace_frozen": ("background_workspace_frozen", bool),
        "background_workspace_disabled": ("background_workspace_disabled", bool),
    }

    def load_preferred_background(self):
        '''Reads the saved background settings, keeping the default for anything missing or invalid.'''
        for attribute, (key, kind) in self.BACKGROUND_PREFERENCES.items():
            value = self.context.preferences.get(key)
            if kind is int and isinstance(value, (int, float)) and not isinstance(value, bool):
                value = int(value)
            if isinstance(value, kind) and not (kind is str and not value):
                setattr(self, attribute, value)
        self.background_fps = min(BACKGROUND_FPS_RANGE[1], max(BACKGROUND_FPS_RANGE[0], self.background_fps))
        self.background_hidden = [key for key in self.background_hidden if isinstance(key, str)]
        self.apply_background()

    def load_default_background(self):
        '''Back to the DEFAULT_BACKGROUND_* values, without saving - like load_default_theme.'''
        self.background_visual = DEFAULT_BACKGROUND_VISUAL
        self.background_animate = DEFAULT_BACKGROUND_ANIMATE
        self.background_detailed = DEFAULT_BACKGROUND_DETAILED
        self.background_fps = DEFAULT_BACKGROUND_FPS
        self.background_hidden = list(DEFAULT_BACKGROUND_HIDDEN)
        self.background_workspace_frozen = DEFAULT_BACKGROUND_WORKSPACE_FROZEN
        self.background_workspace_disabled = DEFAULT_BACKGROUND_WORKSPACE_DISABLED
        self.apply_background()

    def set_background(self, visual: str | None = None, animate: bool | None = None, detailed: bool | None = None,
                       fps: int | None = None, hidden: list[str] | None = None,
                       workspace_frozen: bool | None = None, workspace_disabled: bool | None = None):
        '''Changes background settings - applied to the page on screen at once, and saved.'''
        if visual is not None:
            self.background_visual = visual
        if animate is not None:
            self.background_animate = animate
        if detailed is not None:
            self.background_detailed = detailed
        if fps is not None:
            self.background_fps = min(BACKGROUND_FPS_RANGE[1], max(BACKGROUND_FPS_RANGE[0], int(fps)))
        if hidden is not None:
            self.background_hidden = list(hidden)
        if workspace_frozen is not None:
            self.background_workspace_frozen = workspace_frozen
        if workspace_disabled is not None:
            self.background_workspace_disabled = workspace_disabled
        self.apply_background()
        for attribute, (key, _kind) in self.BACKGROUND_PREFERENCES.items():
            self.context.preferences.set(key, getattr(self, attribute))

    def apply_background(self):
        '''
        Hands the current settings to every page background that follows
        them (see Page.add_background / VisualBackground.apply_preferences),
        so a change shows up without rebuilding the page.
        '''
        for widget in QApplication.allWidgets():
            apply = getattr(widget, "apply_preferences", None)
            if apply is not None and getattr(widget, "follows_preferences", False):
                apply()

    def set_invert_buttons(self, invert: bool):
        '''Switches inverted buttons (see DEFAULT_INVERT_BUTTONS) on or off - restyled in place, and saved.'''
        self.invert_buttons = invert
        self.restyle()
        self.save_surfaces()

    def reset_surfaces(self):
        '''Back to the defaults, saved.'''
        self.load_default_surfaces()
        self.save_surfaces()

    def save_surfaces(self):
        self.context.preferences.set("invert_buttons", self.invert_buttons)

    def _load_theme_files(self):
        '''
        Reads every assets/themes/<family>.json preset (see themes.py), then
        the user's own. Anything unreadable or without materials
        is skipped.
        '''
        for path in sorted(self.context.paths.themes.glob("*.json")):
            self._load_preset(path, path.stem)
        self.load_imported_themes()

    def _load_preset(self, path, family: str, kind: str | None = None) -> bool:
        '''Reads one theme file (see themes.py) in as family - False (and nothing added) if it's unreadable or incomplete.'''
        try:
            with open(path, encoding="utf-8") as file:
                theme = read_theme(json.load(file))
            if theme is None:
                print(f"Err: theme {path} has no materials - skipped.")
                return False
            self.materials[family] = theme["materials"]
            info = theme["info"]
            if kind is not None:
                info["kind"] = kind
            self.preset_info[family] = info
            return True
        except Exception as e:
            print(f"Err: [{e}] while loading theme {path}.")
            return False

    def load_imported_themes(self):
        '''
        (Re)reads user_data/themes (see IMPORTED_PREFIX) - so themes dropped
        in while the app is open show up the next time the selector opens,
        and deleted ones disappear. Themes with unsaved edits are kept as
        they are (see unsaved).
        '''
        for family in [name for name in self.materials if name.startswith(IMPORTED_PREFIX) and name not in self.unsaved]:
            del self.materials[family]
            del self.preset_info[family]
        for path in sorted(self.context.paths.user_themes.glob("*.json")):
            family = IMPORTED_PREFIX + path.stem
            if family in self.unsaved:
                continue
            if self._load_preset(path, family, "imported"):
                self.preset_info[family].setdefault("label", path.stem.replace("_", " ").title())

    # Editing themes - the user's own (see IMPORTED_PREFIX), and in developer
    # mode the built-in ones too. Edits show at once; save_theme writes them
    # to the theme's file.
    @staticmethod
    def is_user_theme(family: str) -> bool:
        return family.startswith(IMPORTED_PREFIX)

    def can_edit(self, family: str) -> bool:
        '''Whether a theme can be changed: the user's own always, built-in ones in developer mode.'''
        return self.is_user_theme(family) or self.context.preferences.is_developer()

    def is_editable(self) -> bool:
        '''Whether the current theme can be changed (see can_edit).'''
        return self.can_edit(self.theme_family())

    def theme_path(self, family: str) -> Path:
        '''Where a theme is saved: the user's own in user_data/themes, built-in ones in assets/themes.'''
        if self.is_user_theme(family):
            return self.context.paths.user_themes / f"{family[len(IMPORTED_PREFIX):]}.json"
        return self.context.paths.themes / f"{family}.json"

    def editor_themes(self) -> tuple[dict[str, str], dict[str, str]]:
        '''Every theme the theme editor offers, family -> shown name: (built-in ones, the user's own).'''
        self.load_imported_themes()
        names = self.preset_names()
        built_in = {family: name for family, name in names.items() if not self.is_user_theme(family)}
        own = {family: name for family, name in names.items() if self.is_user_theme(family)}
        return built_in, own

    @staticmethod
    def _file_stem(name: str) -> str:
        '''A file name for a theme called name - e.g. "Blue (soft light) copy" -> "blue_soft_light_copy".'''
        return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "theme"

    def new_theme(self, source: str) -> str:
        '''
        Copies a theme - its materials, description and transparency - into a new file of the user's own, named after it
        ("<name> copy"), and switches to it. Returns its family.
        '''
        folder = self.context.paths.user_themes
        self.context.paths.generate_path(folder)
        label = self.context.labels.get("theme_editor_copy_name").replace("{name}", self.preset_info[source].get("label", source))
        stem, number = self._file_stem(label), 1
        while (folder / f"{stem}.json").exists() or IMPORTED_PREFIX + stem in self.materials:
            number += 1
            stem = f"{self._file_stem(label)}_{number}"
        info = {"label": label if number == 1 else f"{label} {number}"}
        for key in ("note", "transparency", "button_radius", "menu_button_radius", *STYLE_DEFAULTS):
            if key in self.preset_info[source]:
                info[key] = self.preset_info[source][key]
        self._write_theme(folder / f"{stem}.json", {"info": info, "materials": copy.deepcopy(self.materials[source])})
        self.load_imported_themes()
        family = IMPORTED_PREFIX + stem
        self.set_family(family)
        return family

    def _edited(self, family: str, notify: bool = False):
        '''After any edit to family: it's unsaved, and shows - restyled shortly, or at once and announced with notify.'''
        self.unsaved.add(family)
        if family == self.theme_family():
            self._resolve_colors()
            if notify:
                self.restyle()
            else:
                self._restyle_timer.start()
        self.signals.edited.emit()

    def set_theme_info(self, label: str | None = None, note: str | None = None):
        '''The current theme's name and/or description.'''
        if not self.is_editable():
            return
        info = self.preset_info[self.theme_family()]
        changed = False
        if label is not None and label.strip() and label.strip() != info.get("label"):
            info["label"] = label.strip()
            changed = True
        if note is not None and note != info.get("note", ""):
            info["note"] = note
            changed = True
        if changed:
            self._edited(self.theme_family())

    def set_transparency(self, on: bool):
        '''Whether the current theme allows see-through surfaces at all (see allows_transparency).'''
        if not self.is_editable() or on == self.allows_transparency():
            return
        self.preset_info[self.theme_family()]["transparency"] = on
        self._edited(self.theme_family(), notify=True)

    def set_material_value(self, name: str, color: str | None = None, opacity: float | None = None):
        '''
        Changes one of the current theme's materials in the current mode -
        its color ("#rrggbb") and/or opacity (0-1, not for text and lines -
        see themes.INK_MATERIALS).
        '''
        if not self.is_editable():
            return
        family = self.theme_family()
        entry = self.materials[family][name][self.current_theme.partition("_")[0]]
        if color is not None and is_hex(color):
            entry["color"] = color.lower()
        if opacity is not None and name not in INK_MATERIALS:
            entry["opacity"] = min(1.0, max(0.0, float(opacity)))
        self._edited(family)

    def _theme_contents(self, family: str, kind: str | None = None) -> dict:
        info = dict(self.preset_info[family])
        if self.is_user_theme(family):
            # "kind" is "imported" for every theme read from user_data (see load_imported_themes) - not part of the file
            info.pop("kind", None)
        if kind is not None:
            info = {"label": info.pop("label", family), "kind": kind, **info}
        return {"info": info, "materials": self.materials[family]}

    def save_theme(self, family: str | None = None):
        '''Writes a theme (the current one, by default) to its file (see theme_path) - if it can be edited at all.'''
        family = family or self.theme_family()
        if not self.can_edit(family) or family not in self.materials:
            return
        if self._write_theme(self.theme_path(family), self._theme_contents(family)):
            self.unsaved.discard(family)
            self.signals.edited.emit()

    def discard_changes(self, family: str):
        '''Forgets a theme's unsaved edits, reading it back from its file.'''
        if family not in self.unsaved:
            return
        self.unsaved.discard(family)
        if self.is_user_theme(family):
            self.load_imported_themes()
        elif self.theme_path(family).is_file():
            self._load_preset(self.theme_path(family), family)
        else:  # built-in blue, which only has a file once it's been saved
            self.materials[family] = resolve_materials(None)
            self.preset_info[family] = dict(PRESET_INFO.get(family, {}))
        if family == self.theme_family():
            self.apply_theme(self.current_theme if family in self.materials else self.default_theme(self.current_theme.partition("_")[0]))
        self.signals.edited.emit()

    def built_in_path(self, family: str) -> Path:
        '''Where make_built_in puts one of the user's themes: assets/themes, named after it.'''
        return self.context.paths.themes / f"{self._file_stem(self.preset_info[family].get('label', family))}.json"

    def make_built_in(self, family: str) -> Path | None:
        '''
        Saves one of the user's themes as a built-in one, in assets/themes
        (see built_in_path) - for developers, to ship it. Its own file is
        saved too. Returns where it went, or None if it couldn't be written.
        '''
        if not self.is_user_theme(family):
            return None
        self.save_theme(family)
        path = self.built_in_path(family)
        if not self._write_theme(path, self._theme_contents(family, kind="original")):
            return None
        self._load_preset(path, path.stem)
        return path

    def _write_theme(self, path: Path, theme: dict) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(theme_file(theme), file, indent=4, ensure_ascii=False)
                file.write("\n")
            return True
        except OSError as e:
            print(f"Err: [{e}] while saving theme {path}.")
            return False

    def is_theme(self, theme_name) -> bool:
        if not isinstance(theme_name, str):
            return False
        mode, _, family = theme_name.partition("_")
        return mode in THEME_MODES and family in self.materials

    def theme_family(self) -> str:
        '''The current theme's family - its file's name (see IMPORTED_PREFIX for the user's own).'''
        return self.current_theme.partition("_")[2]

    def preset_name(self, family: str) -> str:
        '''A preset family's shown name - noting a derived side.'''
        info = self.preset_info[family]
        label = info.get("label", family)
        derived = [self.context.labels.get(f"settings_page_mode_{side}") for side in info.get("derived", [])]
        if derived:
            label += self.context.labels.get("theme_picker_derived").replace("{sides}", ", ".join(derived))
        return label

    def preset_names(self) -> dict[str, str]:
        '''Every preset family -> its shown name: originals first, then copied ones, then imported ones.'''
        return {name: self.preset_name(name) for kind in ("original", "copied", "imported")
                for name, info in self.preset_info.items() if info.get("kind", "original") == kind}

    def theme_choices(self) -> dict[str, str]:
        '''What the theme selector offers - the default themes (see CURATED_THEMES), then imported ones - family -> shown name.'''
        self.load_imported_themes()
        curated = [name for name in CURATED_THEMES if name in self.materials]
        imported = [name for name in self.materials if name.startswith(IMPORTED_PREFIX)]
        return {name: self.preset_name(name) for name in curated + imported}

    def default_theme(self, mode: str | None = None) -> str:
        '''The first default theme (or built-in blue, if assets/themes is missing it) - in mode, or the system's.'''
        if mode is None:
            mode = "dark" if darkdetect.isDark() else "light"
        family = next((name for name in CURATED_THEMES if name in self.materials), "blue")
        return f"{mode}_{family}"

    def load_preferred_theme(self):
        saved = self.context.preferences.get("theme")
        if self.is_theme(saved):
            self.apply_theme(saved)
        else:
            self.load_default_theme()

    def load_default_theme(self):
        self.apply_theme(self.default_theme())

    def reset_theme(self):
        '''
        Back to the first default theme, in the system's light or dark mode,
        and the default surface settings - saved, and restyled in place.
        '''
        self.reset_surfaces()
        self.set_theme(self.default_theme())

    def set_theme(self, theme_name: str):
        '''Applies a theme ("<mode>_<family>", e.g. "dark_teal") in place, and saves it.'''
        self.apply_theme(theme_name)
        self.context.preferences.set("theme", self.current_theme)

    def toggle_mode(self):
        '''
        Toggles between the light and dark variant of the current theme's
        color family (e.g. dark_teal <-> light_teal).
        '''
        current_mode, _, family = self.current_theme.partition("_")
        target_mode = "light" if current_mode == "dark" else "dark"
        self.set_theme(f"{target_mode}_{family}")

    def set_family(self, family: str):
        '''Switches to a theme family, keeping light or dark.'''
        self.set_theme(f"{self.current_theme.partition('_')[0]}_{family}")
