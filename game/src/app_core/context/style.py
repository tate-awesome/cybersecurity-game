import json
import re

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QApplication
import darkdetect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Hand-rolled replacement for qt-material's theme presets. Each family has a
# dark and light variant; every color key here is required (color() and
# Style._build_stylesheet both read them directly with no fallback), so a
# new family must define both variants with the full key set below.
# Blue is built in so the app always has a theme, even without assets/;
# every other family is a <family>.json in assets/themes with the same
# shape (see Style._load_theme_files).
PALETTES: dict[str, dict[str, dict[str, str]]] = {
    "blue": {
        # Dark mode: panel sits close to root (both near-black) so widget-
        # colored cards clearly pop above the recessed backdrop. Light mode
        # flips that - panel sits close to field (both near-white) so
        # widget-colored cards read as the slightly-toned layer between
        # them. Either way, widget is always the mode's biggest single step,
        # which is what actually keeps stacked forms from blending together.
        "dark": {
            "root": "#10141d", "panel": "#151a24", "widget": "#28303d",
            "field": "#353e4d", "field_text": "#e3eaf5", "text": "#e3eaf5",
            "accent": "#2979ff", "accent_text": "#ffffff", "border": "#2e3745",
            "scrollbar": "#2e3745", "scrollbar_hover": "#3e4755",
        },
        "light": {
            "root": "#d9e2f5", "panel": "#f1f5ff", "widget": "#e4ebfd",
            "field": "#ffffff", "field_text": "#1a2233", "text": "#1a2233",
            "accent": "#1e6fe0", "accent_text": "#ffffff", "border": "#d9e2f5",
            "scrollbar": "#d9e2f5", "scrollbar_hover": "#bfc7d8",
        },
    },
}
THEME_MODES = ("dark", "light")
THEME_KEYS = frozenset(PALETTES["blue"]["dark"])

# Fallback themes when no preference is saved yet, or when toggle_mode's
# target mode has no variant in the current color family.
DEFAULT_DARK_THEME = "dark_blue"
DEFAULT_LIGHT_THEME = "light_blue"

# Surfaces - the kinds of backgrounds whose opacity and backdrop blur the
# user can tune (the "Background" style dropdown), each saved as a
# preference like the theme:
#   panel  - the "panel" color: panel bodies and borders
#   bar    - menu bars
#   widget - the "widget" color: cards like forms
#   field  - the "field" color: text inputs, tree views, consoles, canvases
#   button  - buttons
#   overlay - dropdown overlays (popups), frosted over a snapshot of the
#             app behind them - see Overlay
# panel/widget/field are theme colors, so their opacity is built into what
# Style.color() returns for them (see COLOR_SURFACES). Menu bars,
# buttons and overlays don't have colors of their own, so they're tagged
# instead (see Style.surface).
SURFACE_KINDS = ("panel", "bar", "widget", "field", "button", "overlay")
COLOR_SURFACES = ("panel", "widget", "field")
# Whether surfaces can be see-through at all. Off, none of the surface
# machinery runs: every color is opaque and untagged, there's no backdrop
# blur or overlay snapshot, and scroll areas paint their own background -
# the app as it was before translucency.
DEFAULT_TRANSLUCENT_SURFACES = True
DEFAULT_SURFACE_OPACITY: dict[str, float] = {
    "panel": 0.5, "bar": 1.0, "widget": 0.5, "field": 0.5, "button": 0.75, "overlay": 1.0}  # 0-1
DEFAULT_SURFACE_BLUR: dict[str, float] = {kind: 0.0 for kind in SURFACE_KINDS}     # px
SURFACE_BLUR_MAX = 40.0
# The animated page background (see Page.add_background), each saved as a
# preference like the theme: whether it's drawn at all, which visual plays
# (a widgets.visuals.VISUALS key, or "cycle"), whether it moves, whether
# it's detailed in workspaces (the network's packets - title and lesson
# select pages always are; off by default since it's distracting behind
# panels), and its frame rate
DEFAULT_BACKGROUND_ENABLED = True
DEFAULT_BACKGROUND_VISUAL = "network_mesh"
DEFAULT_BACKGROUND_ANIMATE = True
DEFAULT_BACKGROUND_DETAILED = False
DEFAULT_BACKGROUND_FPS = 30
BACKGROUND_FPS_RANGE = (1, 120)

# Inverted buttons: text-colored labels on a background between panel and
# root, with a clear border - instead of accent_text on solid accent
DEFAULT_INVERT_BUTTONS = False

# A tagged surface color in a stylesheet (see Style.surface):
# "rgba(r, g, b, a) /*s:<kind>:#rrggbb*/". The comment marks it so
# restyle_surfaces can find and rewrite it, without rebuilding the page.
SURFACE_PATTERN = re.compile(r"rgba\(\d+, \d+, \d+, \d+\) /\*s:(\w+):(#[0-9a-fA-F]{6})\*/")
# One "property: value" declaration, and a hex color inside a value - for
# rewriting color()'s panel/widget/field colors (see restyle_surfaces)
DECLARATION_PATTERN = re.compile(r"([\w-]+)(\s*:\s*)([^;{}]*)")
HEX_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})\b")
# Text color properties are never surfaces, even when a text color happens
# to match one (e.g. light themes' white accent_text and field)
TEXT_PROPERTIES = ("color", "selection-color")
COMMENT_PATTERN = re.compile(r"(/\*.*?\*/)", re.S)
# The shared rules (see _build_stylesheet) are wrapped in these markers
# inside every stylesheet that carries a copy (see themed), so
# restyle_surfaces can swap the whole block for a freshly built one
BASE_PATTERN = re.compile(r"/\*qss:(opaque|surfaces)\*/.*?/\*qss:end\*/", re.S)

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
        self.PANEL_RADIUS = self.igap
        self.fonts = {}
        self.context = context

        # Surface settings (see SURFACE_KINDS) - load_preferred_surfaces()
        # replaces these defaults once preferences exist
        self.translucent_surfaces: bool = DEFAULT_TRANSLUCENT_SURFACES
        self.surface_opacity: dict[str, float] = dict(DEFAULT_SURFACE_OPACITY)
        self.surface_blur: dict[str, float] = dict(DEFAULT_SURFACE_BLUR)
        self.invert_buttons: bool = DEFAULT_INVERT_BUTTONS
        # Background settings - load_preferred_background() replaces these
        # defaults once preferences exist
        self.background_enabled: bool = DEFAULT_BACKGROUND_ENABLED
        self.background_visual: str = DEFAULT_BACKGROUND_VISUAL
        self.background_animate: bool = DEFAULT_BACKGROUND_ANIMATE
        self.background_detailed: bool = DEFAULT_BACKGROUND_DETAILED
        self.background_fps: int = DEFAULT_BACKGROUND_FPS
        # Slider drags change these many times a second - restyling and
        # saving are each coalesced onto a short timer
        self._restyle_timer = QTimer()
        self._restyle_timer.setSingleShot(True)
        self._restyle_timer.setInterval(30)
        self._restyle_timer.timeout.connect(self.restyle_surfaces)
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(400)
        self._save_timer.timeout.connect(self.save_surfaces)
        from .backdrop import Backdrop
        self.backdrop = Backdrop(self)

        # Preferences don't exist yet at this point in startup (see
        # ContextManager.start_session) - this is just a system-appropriate
        # bootstrap default; load_preferred_theme() overrides it once
        # preferences are available.
        self.palettes = {**PALETTES, **self._load_theme_files()}
        self._theme_colors: dict[str, str] = {}
        self.apply_theme(DEFAULT_DARK_THEME if darkdetect.isDark() else DEFAULT_LIGHT_THEME)

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

    def get_font_size(self, name="default"):
        size = 16.0
        if name == "title_btn":
            size = 20.0
        elif name == "title":
            size = 72
        elif name == "small":
            size = 15.0
        elif name == "chart_title":
            size = 13.0
        elif name == "chart_numbers":
            size = 10.0
        elif name == "chart_label":
            size = 10.0
        return int(size * self.ui_scale / 100.0)

    # The color names color() resolves from the active palette - also the
    # options the style editors offer (see important_buttons/settings_overlays)
    THEME_COLOR_NAMES = (
        "root",             # window background
        "panel",            # panel background
        "widget",           # nested/inner widget background
        "accent",           # button/highlight color
        "field",            # text field background
        "field_text",       # text field text color
        "text",             # general text color
        "scrollbar",        # scrollbar handle color
        "scrollbar_hover",  # scrollbar handle hover color
    )

    def color(self, type: str, opaque: bool = False) -> str:
        '''
        Returns a color from the active hand-rolled palette (see
        palettes/apply_theme) for one of THEME_COLOR_NAMES, or the input
        string itself (e.g. "red" or a hex code) for anything else.

        "panel", "widget" and "field" come back at their surface opacity
        (see COLOR_SURFACES) - as "#AARRGGBB" when see-through, which both
        stylesheets and QColor understand - so everything drawn in them
        follows the "Background" style settings. opaque=True skips that,
        for anything that must stay solid.
        '''
        if type not in self.THEME_COLOR_NAMES:
            return type
        hex_color = self._theme_colors[type]
        if opaque or type not in COLOR_SURFACES:
            return hex_color
        opacity = self.opacity(type)
        if opacity >= 1.0:
            return hex_color
        return f"#{round(255 * opacity):02x}{hex_color.lstrip('#')}"

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
        Applies a hand-rolled palette globally (its QSS stylesheet covers
        every native Qt widget - see _build_stylesheet) and refreshes the
        color() values this app's own hand-styled widgets pull from. Those
        are set once, inline, at construction time (see Panel/BaseForm/
        MenuBar etc.), so - unlike native widgets - they only pick up a new
        theme on their next rebuild; callers changing the theme after
        startup (toggle_mode, set_theme) follow this with
        context.router.refresh().
        '''
        mode, _, family = theme_name.partition("_")
        app = QApplication.instance()
        self._theme_colors = self.palettes[family][mode]
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
        self._widget_qss = self._build_stylesheet(self._theme_colors)
        self._opaque_qss = self._build_stylesheet(self._theme_colors, opaque=True)
        app.setStyleSheet(self._widget_qss)
        self.current_theme = theme_name
        self.mode = "Dark" if mode == "dark" else "Light"

    def themed(self, extra: str = "", widget=None, opaque: bool = False) -> str:
        '''
        Returns the shared widget-styling stylesheet (QPushButton, QLineEdit,
        QCheckBox, etc. - see _build_stylesheet) plus an optional extra rule,
        for use in a widget's own setStyleSheet() call. Qt's style sheet
        cascade stops climbing the ancestor chain at the first widget with
        its own local stylesheet - so every container that sets one of its
        own (Panel, BaseForm, Page, Panes, MenuBar, Scrollable, overlays,
        etc.) must carry its own copy of the shared rules, or native widgets
        nested inside it silently fall back to unstyled defaults instead of
        the stylesheet set on the QApplication in apply_theme.

        If `extra` is already a full rule with its own selector(s) (e.g. a
        "QSplitter::handle { ... }" override), it's appended as-is. If it's
        a bare declaration list instead (e.g. "background-color: X;" - the
        common case for a container's own background), `widget` is required:
        Qt's QSS parser only allows a selector-less declaration list when
        it's the ENTIRE stylesheet, so mixed in after other "Selector {...}"
        blocks it's invalid and gets silently dropped - leaving the widget's
        background unset and falling back to Qt's default palette instead of
        the intended color, which is what made panels/forms look like stray
        dark-gray boxes regardless of the active theme. Assigning `widget` a
        unique object name and scoping the declaration under a matching ID
        selector keeps it valid.

        opaque=True uses a copy of the shared rules with every surface fully
        opaque - for anything that must stay solid whatever the "Background"
        settings say.
        '''
        base = self._opaque_qss if opaque else self._widget_qss
        if not extra:
            return base
        if "{" in extra:
            return base + "\n" + extra
        assert widget is not None, "themed() needs `widget` to scope a bare declaration list"
        name = f"_themed_{id(widget)}"
        widget.setObjectName(name)
        # A widget whose own background is a surface is marked with its
        # kind, so the backdrop blur knows to paint under it (see Backdrop)
        kind = self.surface_kind_of(extra)
        if kind is not None:
            widget.setProperty("surface", kind)
        return base + f"\n#{name} {{ {extra} }}"

    @staticmethod
    def _shade(hex_color: str, amount: float) -> str:
        '''
        Blends hex_color toward white (amount > 0) or black (amount < 0) by
        the given fraction - used to derive button/slider hover and pressed
        shades from a palette's single accent color, instead of hand-authoring
        extra keys per palette per mode.
        '''
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        target = 255 if amount > 0 else 0
        amount = abs(amount)
        r, g, b = (int(v + (target - v) * amount) for v in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _mix(hex_a: str, hex_b: str, amount: float) -> str:
        '''hex_a blended amount (0-1) of the way to hex_b.'''
        a, b = QColor(hex_a), QColor(hex_b)
        channels = (round(x + (y - x) * amount) for x, y in ((a.red(), b.red()), (a.green(), b.green()), (a.blue(), b.blue())))
        return "#" + "".join(f"{v:02x}" for v in channels)

    def _build_stylesheet(self, c: dict[str, str], opaque: bool = False) -> str:
        '''
        Hand-rolled replacement for qt-material's generated QSS - covers the
        native widgets this app actually uses (buttons, line edits,
        checkboxes, combo boxes, tree views, scrollbars, sliders, tooltips)
        with the current palette's colors. Widgets that already set their
        own background inline (Panel, BaseForm, etc. via style.color()) are
        left alone here; this only fills in what those don't cover.
        '''
        accent_hover = self._shade(c["accent"], 0.15)
        accent_pressed = self._shade(c["accent"], -0.15)
        scroll_w = int(self.get_scrollbar_size())

        def s(kind: str, color: str) -> str:
            return color if opaque else self.surface(kind, color)

        # Popup-only rules (tooltips, combo box lists) stay opaque - see color()
        raw = c
        if not opaque:
            c = {**c, **{name: self.color(name) for name in COLOR_SURFACES}}

        if self.invert_buttons:
            # Text-colored, on a background between panel and root, with a
            # border drawn toward the text color so each button stays
            # clearly outlined against whatever it sits on
            button_bg = self._mix(raw["panel"], raw["root"], 0.5)
            buttons = f'''
            QPushButton {{
                background-color: {s("button", button_bg)};
                color: {raw["text"]};
                border: 1px solid {self._mix(raw["panel"], raw["text"], 0.4)};
                border-radius: 4px;
                padding: 5px 11px;
            }}
            QPushButton:hover {{ background-color: {s("button", raw["widget"])}; border-color: {raw["accent"]}; }}
            QPushButton:pressed {{ background-color: {s("button", raw["root"])}; border-color: {raw["accent"]}; }}
            QPushButton:disabled {{ background-color: {s("button", button_bg)}; color: {raw["border"]}; border-color: {raw["border"]}; }}'''
        else:
            buttons = f'''
            QPushButton {{
                background-color: {s("button", raw["accent"])};
                color: {raw["accent_text"]};
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: {s("button", accent_hover)}; }}
            QPushButton:pressed {{ background-color: {s("button", accent_pressed)}; }}
            QPushButton:disabled {{ background-color: {s("button", raw["widget"])}; color: {raw["border"]}; }}'''

        return f"/*qss:{'opaque' if opaque else 'surfaces'}*/" + f'''
            QWidget {{ color: {c["text"]}; }}
            QMainWindow, QDialog {{ background-color: {c["root"]}; }}
            QToolTip {{
                background-color: {raw["panel"]};
                color: {c["text"]};
                border: 1px solid {c["border"]};
            }}
            {buttons}
            QTabWidget::pane {{ border: 1px solid {c["border"]}; border-radius: 4px; }}
            QTabBar::tab {{
                background-color: {c["widget"]};
                color: {c["text"]};
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{ background-color: {c["accent"]}; color: {c["accent_text"]}; }}
            QTabBar::tab:hover:!selected {{ background-color: {c["panel"]}; }}
            QLineEdit, QComboBox, QPlainTextEdit, QTextEdit {{
                background-color: {c["field"]};
                color: {c["field_text"]};
                border: 1px solid {c["border"]};
                border-radius: 4px;
                padding: 4px;
            }}
            QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border: 1px solid {c["accent"]}; }}
            QComboBox QAbstractItemView {{
                background-color: {raw["field"]};
                color: {c["field_text"]};
                selection-background-color: {c["accent"]};
                selection-color: {c["accent_text"]};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {c["border"]};
                border-radius: 3px;
                background-color: {c["field"]};
            }}
            QCheckBox::indicator:checked {{
                background-color: {c["accent"]};
                border: 1px solid {c["accent"]};
            }}
            QHeaderView::section {{
                background-color: {c["widget"]};
                color: {c["text"]};
                border: 1px solid {c["border"]};
                padding: 4px;
            }}
            QTreeWidget, QTreeView {{
                background-color: {c["field"]};
                alternate-background-color: {c["widget"]};
                color: {c["text"]};
                border: 1px solid {c["border"]};
            }}
            QTreeWidget::item:selected, QTreeView::item:selected {{
                background-color: {c["accent"]};
                color: {c["accent_text"]};
            }}
            QSlider::groove:horizontal {{
                background: {c["field"]};
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
                background: {c["panel"]};
                width: {scroll_w}px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {c["scrollbar"]};
                border-radius: {scroll_w // 2}px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {c["scrollbar_hover"]}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar:horizontal {{
                background: {c["panel"]};
                height: {scroll_w}px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {c["scrollbar"]};
                border-radius: {scroll_w // 2}px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{ background: {c["scrollbar_hover"]}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
        ''' + "/*qss:end*/"

    # Surfaces
    def surface(self, kind: str, color: str) -> str:
        '''
        A stylesheet color for a background of one of SURFACE_KINDS:
        `color` (a theme color name or hex code - see color()) at that
        kind's opacity, tagged so restyle_surfaces can update it live.
        For surfaces without a theme color of their own (menu bars,
        buttons) - panel/widget/field get theirs from color().
        '''
        qcolor = QColor(self.color(color))
        if not self.translucent_surfaces:
            return qcolor.name()  # just the color - no translucency, nothing tagged
        alpha = round(255 * self.opacity(kind))
        return f"rgba({qcolor.red()}, {qcolor.green()}, {qcolor.blue()}, {alpha}) /*s:{kind}:{qcolor.name()}*/"

    def opacity(self, kind: str) -> float:
        '''How solid a surface of this kind draws right now - always 1 with translucent_surfaces off.'''
        return self.surface_opacity.get(kind, 1.0) if self.translucent_surfaces else 1.0

    def set_translucent_surfaces(self, on: bool):
        '''
        Switches surface translucency on or off (see DEFAULT_TRANSLUCENT_SURFACES),
        saves it, and rebuilds the page - it changes how every stylesheet is
        built, not just its colors, so it can't be restyled in place.
        '''
        self.translucent_surfaces = on
        self._rebuild_stylesheets()
        self.backdrop.sync()
        self.save_surfaces()
        self.context.router.refresh()

    def surface_kind_of(self, declarations: str) -> str | None:
        '''
        Which surface kind a widget's own declarations (e.g. "background-
        color: ...; border: ...") paint its background in, if any.
        '''
        tagged = SURFACE_PATTERN.search(declarations)
        if tagged:
            return tagged.group(1)
        surfaces = self._surface_colors()
        for match in DECLARATION_PATTERN.finditer(declarations):
            if match.group(1) in ("background", "background-color"):
                hex_match = HEX_PATTERN.search(match.group(3))
                if hex_match:
                    return surfaces.get(hex_match.group(0)[-6:].lower())
        return None

    def _surface_colors(self) -> dict[str, str]:
        '''rrggbb (no #, lowercase) -> name, for the current theme's panel/widget/field.'''
        return {self._theme_colors[name].lstrip("#").lower(): name for name in COLOR_SURFACES}

    def load_preferred_surfaces(self):
        '''Reads the saved surface settings, keeping the default for anything missing or invalid.'''
        for key, values, low, high in (("surface_opacity", self.surface_opacity, 0.0, 1.0),
                                       ("surface_blur", self.surface_blur, 0.0, SURFACE_BLUR_MAX)):
            saved = self.context.preferences.get(key)
            if not isinstance(saved, dict):
                continue
            for kind in SURFACE_KINDS:
                value = saved.get(kind)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    values[kind] = min(high, max(low, float(value)))
        if isinstance(self.context.preferences.get("invert_buttons"), bool):
            self.invert_buttons = self.context.preferences.get("invert_buttons")
        if isinstance(self.context.preferences.get("translucent_surfaces"), bool):
            self.translucent_surfaces = self.context.preferences.get("translucent_surfaces")
        self._rebuild_stylesheets()
        self.backdrop.sync()

    def load_default_surfaces(self):
        '''Back to DEFAULT_SURFACE_OPACITY/BLUR, without saving - like load_default_theme.'''
        self.translucent_surfaces = DEFAULT_TRANSLUCENT_SURFACES
        self.surface_opacity = dict(DEFAULT_SURFACE_OPACITY)
        self.surface_blur = dict(DEFAULT_SURFACE_BLUR)
        self.invert_buttons = DEFAULT_INVERT_BUTTONS
        self.restyle_surfaces()
        self.backdrop.sync()

    def set_surface(self, kind: str, opacity: float | None = None, blur: float | None = None):
        '''
        Changes one surface kind's opacity (0-1) and/or blur (px). Takes
        effect right away on the current page - no rebuild - and is saved
        to preferences shortly after the last change.
        '''
        if opacity is not None:
            self.surface_opacity[kind] = min(1.0, max(0.0, opacity))
            self._restyle_timer.start()
        if blur is not None:
            self.surface_blur[kind] = min(SURFACE_BLUR_MAX, max(0.0, blur))
        self.backdrop.sync()
        self._save_timer.start()

    # Background
    BACKGROUND_PREFERENCES = {
        # attribute: (preference key, type)
        "background_enabled": ("background_enabled", bool),
        "background_visual": ("background_visual", str),
        "background_animate": ("background_animate", bool),
        "background_detailed": ("background_detailed", bool),
        "background_fps": ("background_fps", int),
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
        self.apply_background()

    def load_default_background(self):
        '''Back to the DEFAULT_BACKGROUND_* values, without saving - like load_default_theme.'''
        self.background_enabled = DEFAULT_BACKGROUND_ENABLED
        self.background_visual = DEFAULT_BACKGROUND_VISUAL
        self.background_animate = DEFAULT_BACKGROUND_ANIMATE
        self.background_detailed = DEFAULT_BACKGROUND_DETAILED
        self.background_fps = DEFAULT_BACKGROUND_FPS
        self.apply_background()

    def set_background(self, enabled: bool | None = None, visual: str | None = None, animate: bool | None = None,
                       detailed: bool | None = None, fps: int | None = None):
        '''Changes background settings - applied to the page on screen at once, and saved.'''
        if enabled is not None:
            self.background_enabled = enabled
        if visual is not None:
            self.background_visual = visual
        if animate is not None:
            self.background_animate = animate
        if detailed is not None:
            self.background_detailed = detailed
        if fps is not None:
            self.background_fps = min(BACKGROUND_FPS_RANGE[1], max(BACKGROUND_FPS_RANGE[0], int(fps)))
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
        '''Switches inverted buttons (see DEFAULT_INVERT_BUTTONS) on or off - live, and saved.'''
        self.invert_buttons = invert
        self.restyle_surfaces()
        self.backdrop.sync()
        self.save_surfaces()

    def reset_surfaces(self):
        '''Back to the defaults, saved - the "Background" dropdown's reset button.'''
        self.load_default_surfaces()
        self.save_surfaces()

    def save_surfaces(self):
        self._save_timer.stop()
        self.context.preferences.set("surface_opacity", dict(self.surface_opacity))
        self.context.preferences.set("surface_blur", dict(self.surface_blur))
        self.context.preferences.set("invert_buttons", self.invert_buttons)
        self.context.preferences.set("translucent_surfaces", self.translucent_surfaces)

    def _rebuild_stylesheets(self):
        self._widget_qss = self._build_stylesheet(self._theme_colors)
        self._opaque_qss = self._build_stylesheet(self._theme_colors, opaque=True)
        QApplication.instance().setStyleSheet(self._widget_qss)

    def restyle_surfaces(self):
        '''
        Rewrites every surface color in the app's and every widget's
        stylesheet to its kind's current opacity - both tagged ones (see
        surface()) and color()'s panel/widget/field colors, recognized by
        their RGB in any non-text property - so opacity changes show up
        instantly instead of on the next page rebuild.
        '''
        self._restyle_timer.stop()
        self._rebuild_stylesheets()

        surfaces = self._surface_colors()
        bases = {"surfaces": self._widget_qss, "opaque": self._opaque_qss}

        def replace_tagged(match: re.Match) -> str:
            return self.surface(match.group(1), match.group(2))

        def replace_hex(match: re.Match) -> str:
            name = surfaces.get(match.group(0)[-6:].lower())
            return self.color(name) if name else match.group(0)

        def replace_declaration(match: re.Match) -> str:
            name, separator, value = match.groups()
            if name in TEXT_PROPERTIES:
                return match.group(0)
            # Never inside a comment - a surface tag's own hex has to stay
            # exactly as surface() wrote it, or it stops being found
            parts = COMMENT_PATTERN.split(value)
            return name + separator + "".join(part if i % 2 else HEX_PATTERN.sub(replace_hex, part) for i, part in enumerate(parts))

        def rewrite(text: str) -> str:
            return DECLARATION_PATTERN.sub(replace_declaration, SURFACE_PATTERN.sub(replace_tagged, text))

        for widget in QApplication.allWidgets():
            sheet = widget.styleSheet()
            if not sheet:
                continue
            # The shared block is swapped whole (that's how structural
            # changes like inverted buttons get in); the widget's own rules
            # around it get their surface colors rewritten
            pieces, position = [], 0
            for match in BASE_PATTERN.finditer(sheet):
                outside = sheet[position:match.start()]
                pieces.append(rewrite(outside))
                pieces.append(bases[match.group(1)])
                position = match.end()
            pieces.append(rewrite(sheet[position:]))
            updated = "".join(pieces)
            if updated != sheet:
                widget.setStyleSheet(updated)

    def _load_theme_files(self) -> dict[str, dict[str, dict[str, str]]]:
        '''
        Reads every assets/themes/<family>.json (see PALETTES), skipping
        any file that's unreadable or missing a variant or color key.
        '''
        palettes = {}
        for path in sorted(self.context.paths.themes.glob("*.json")):
            if path.stem in PALETTES:
                continue  # built-in families can't be overridden
            try:
                with open(path, encoding="utf-8") as file:
                    variants = json.load(file)
                if all(THEME_KEYS <= set(variants[mode]) for mode in THEME_MODES):
                    palettes[path.stem] = {mode: variants[mode] for mode in THEME_MODES}
                else:
                    print(f"Err: theme {path} is missing color keys - skipped.")
            except Exception as e:
                print(f"Err: [{e}] while loading theme {path}.")
        return palettes

    def _list_themes(self) -> list[str]:
        return [f"{mode}_{family}" for family in self.palettes for mode in THEME_MODES]

    def load_preferred_theme(self):
        saved = self.context.preferences.data.get("theme")
        if self.context.preferences.has("theme") and saved in self._list_themes():
            self.apply_theme(saved)
        else:
            self.load_default_theme()

    def load_default_theme(self):
        self.apply_theme(DEFAULT_DARK_THEME if darkdetect.isDark() else DEFAULT_LIGHT_THEME)

    def theme_families(self) -> list[str]:
        return list(self.palettes)

    def set_theme(self, theme_name: str):
        '''Applies a theme ("<mode>_<family>", e.g. "dark_teal"), saves it, and rebuilds the page in it.'''
        self.apply_theme(theme_name)
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()

    def toggle_mode(self):
        '''
        Toggles between the light and dark variant of the current theme's
        color family (e.g. dark_teal <-> light_teal).
        '''
        current_mode, _, family = self.current_theme.partition("_")
        target_mode = "light" if current_mode == "dark" else "dark"
        self.set_theme(f"{target_mode}_{family}")
