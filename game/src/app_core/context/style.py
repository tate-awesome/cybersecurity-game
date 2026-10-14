import json
import re

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QApplication
import darkdetect

from . import palette_generator
from .themes import MATERIALS, PALETTE_KEYS, THEME_MODES, read_theme, resolve_materials

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Hand-rolled replacement for qt-material's theme presets. Each family has a
# dark and light palette with every one of themes.PALETTE_KEYS, and a
# material list (see themes.py) - defaults, for the built-in one.
# Blue is built in so the app always has a theme, even without assets/;
# every other preset family is a <family>.json in assets/themes (see
# themes.py and Style._load_theme_files) - one there named "blue"
# replaces it. Beyond the presets, any accent can be paired with any
# hierarchy (assets/themes/generator - see palette_generator): a family
# named "<accent>.<hierarchy>", e.g. "cyan.whisper".
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
PRESET_INFO: dict[str, dict] = {"blue": {"label": "Blue", "kind": "original"}}
# What the accent/hierarchy pickers start from while a preset is in use
DEFAULT_ACCENT = "azure"
DEFAULT_HIERARCHY = "baseline"
# Whether fields sit below the darkest layer - recessed inputs (see palette_generator.inset)
DEFAULT_THEME_INSET = False
# How much the accent bleeds into accent + hierarchy themes' surfaces - a
# multiple of the hierarchy's own tint (see palette_generator.generate)
DEFAULT_THEME_TINT = 1.0
THEME_TINT_MAX = 3.0
# Per-mode adjustments (see palette_generator.generate/borders):
#   steps  - multiplies accent + hierarchy themes' layer steps
#   height - moves their root (and everything on it) up or down, in L*
#   border - multiplies how far borders sit from the surfaces around them -
#            for every theme, special ones too, since borders are about
#            being able to see where things end
DEFAULT_THEME_ADJUST: dict[str, dict[str, float]] = {mode: {"steps": 1.0, "height": 0.0, "border": 1.0} for mode in ("dark", "light")}
THEME_ADJUST_RANGE: dict[str, tuple[float, float]] = {"steps": (0.0, 3.0), "height": (-20.0, 20.0), "border": (0.0, 3.0)}

# The default themes - the hand-picked families the theme selector offers
# everyone (most combinations of the theme editor's settings don't look
# good, so these are the ones that do). The first is the theme a fresh
# start, and Reset Theme, use. Imported themes (see IMPORTED_PREFIX) join
# them in the selector; every other preset is only in the theme editor.
CURATED_THEMES: list[str] = ["blue_v2_light"]
# Imported themes - <family>.json files in user_data/themes, the same shape
# as assets/themes' - are named "imported.<file name>", so one can never
# replace a bundled preset of the same name
IMPORTED_PREFIX = "imported."

# Surfaces - the kinds of backgrounds that can be see-through, each at its
# material's opacity in the theme (see SURFACE_MATERIALS and themes.py):
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
# The material each surface kind takes its opacity from
SURFACE_MATERIALS = {"panel": "panel", "bar": "menu_bar", "widget": "card", "field": "field",
                     "button": "button", "overlay": "overlay"}
# Whether surfaces can be see-through at all. Off, none of the surface
# machinery runs: every color is opaque and untagged, there's no overlay
# snapshot, and scroll areas paint their own background - the app as it
# was before translucency.
DEFAULT_TRANSLUCENT_SURFACES = True
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
        self.invert_buttons: bool = DEFAULT_INVERT_BUTTONS
        # Background settings - load_preferred_background() replaces these
        # defaults once preferences exist
        self.background_enabled: bool = DEFAULT_BACKGROUND_ENABLED
        self.background_visual: str = DEFAULT_BACKGROUND_VISUAL
        self.background_animate: bool = DEFAULT_BACKGROUND_ANIMATE
        self.background_detailed: bool = DEFAULT_BACKGROUND_DETAILED
        self.background_fps: int = DEFAULT_BACKGROUND_FPS

        # Preferences don't exist yet at this point in startup (see
        # ContextManager.start_session) - this is just a system-appropriate
        # bootstrap default; load_preferred_theme() overrides it once
        # preferences are available.
        self.palettes: dict[str, dict[str, dict[str, str]]] = dict(PALETTES)
        # Each preset's materials (see themes.py) - accent + hierarchy themes use the defaults
        self.materials: dict[str, dict[str, dict[str, dict]]] = {name: resolve_materials(None) for name in PALETTES}
        self.preset_info: dict[str, dict] = dict(PRESET_INFO)
        self.accents: dict[str, str] = {}
        self.hierarchies: dict[str, dict[str, float]] = {}
        self._load_theme_files()
        self.theme_inset: bool = DEFAULT_THEME_INSET
        self.theme_tint: float = DEFAULT_THEME_TINT
        self.theme_adjust: dict[str, dict[str, float]] = {mode: dict(values) for mode, values in DEFAULT_THEME_ADJUST.items()}
        # The last accent + hierarchy used, kept while a preset is shown
        self.theme_accent: str = DEFAULT_ACCENT
        self.theme_hierarchy: str = DEFAULT_HIERARCHY
        self._theme_colors: dict[str, str] = {}
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
        # First - the materials (see material) are the current theme's
        self.current_theme = theme_name
        self.mode = "Dark" if mode == "dark" else "Light"
        self._theme_colors = self._palette(family, mode)
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
        # A widget whose own background is a surface is marked with its kind
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
        '''How solid a surface of this kind draws right now - its material's opacity, or 1 with translucent_surfaces off.'''
        if not self.translucent_surfaces or kind not in SURFACE_MATERIALS:
            return 1.0
        return self.material_entry(SURFACE_MATERIALS[kind])["opacity"]

    # Materials
    def theme_materials(self) -> dict[str, dict[str, dict]]:
        '''The current theme's materials (see themes.py) - every one, for both modes.'''
        return self.materials.get(self.theme_family()) or resolve_materials(None)

    def material_entry(self, name: str) -> dict:
        '''One material in the current mode: {"color": <palette key or hex>, "opacity": 0-1}.'''
        return self.theme_materials()[name][self.current_theme.partition("_")[0]]

    def material(self, name: str) -> QColor:
        '''
        What a material (see themes.MATERIALS) looks like right now: its
        color, resolved from the palette if it names one, at its opacity -
        or solid, with translucent_surfaces off.
        '''
        entry = self.material_entry(name)
        color = QColor(self._theme_colors.get(entry["color"], entry["color"]))
        if self.translucent_surfaces:
            color.setAlphaF(entry["opacity"])
        return color

    def set_translucent_surfaces(self, on: bool):
        '''
        Switches surface translucency on or off (see DEFAULT_TRANSLUCENT_SURFACES),
        saves it, and rebuilds the page - it changes how every stylesheet is
        built, not just its colors, so it can't be restyled in place.
        '''
        self.translucent_surfaces = on
        self._rebuild_stylesheets()
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
        if isinstance(self.context.preferences.get("invert_buttons"), bool):
            self.invert_buttons = self.context.preferences.get("invert_buttons")
        if isinstance(self.context.preferences.get("translucent_surfaces"), bool):
            self.translucent_surfaces = self.context.preferences.get("translucent_surfaces")
        self._rebuild_stylesheets()

    def load_default_surfaces(self):
        '''Back to the default surface settings, without saving - like load_default_theme.'''
        self.translucent_surfaces = DEFAULT_TRANSLUCENT_SURFACES
        self.invert_buttons = DEFAULT_INVERT_BUTTONS
        self.restyle_surfaces()

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
        self.save_surfaces()

    def reset_surfaces(self):
        '''Back to the defaults, saved - the "Background" dropdown's reset button.'''
        self.load_default_surfaces()
        self.save_surfaces()

    def save_surfaces(self):
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

    def _load_theme_files(self):
        '''
        Reads every assets/themes/<family>.json preset (see themes.py) -
        plus the generator's accents and hierarchies. Anything unreadable
        or with an incomplete palette is skipped.
        '''
        for path in sorted(self.context.paths.themes.glob("*.json")):
            self._load_preset(path, path.stem)
        generator = self.context.paths.themes / "generator"
        try:
            with open(generator / "accents.json", encoding="utf-8") as file:
                self.accents = json.load(file)
            with open(generator / "hierarchies.json", encoding="utf-8") as file:
                self.hierarchies = json.load(file)
        except Exception as e:
            print(f"Err: [{e}] while loading the theme generator - only presets are available.")
            self.accents, self.hierarchies = {}, {}
        self.load_imported_themes()

    def _load_preset(self, path, family: str, kind: str | None = None) -> bool:
        '''Reads one theme file (see themes.py) in as family - False (and nothing added) if it's unreadable or incomplete.'''
        try:
            with open(path, encoding="utf-8") as file:
                theme = read_theme(json.load(file))
            if theme is None:
                print(f"Err: theme {path} has an incomplete palette - skipped.")
                return False
            self.palettes[family] = theme["palette"]
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
        and deleted ones disappear.
        '''
        for family in [name for name in self.palettes if name.startswith(IMPORTED_PREFIX)]:
            del self.palettes[family]
            del self.materials[family]
            del self.preset_info[family]
        for path in sorted(self.context.paths.user_themes.glob("*.json")):
            family = IMPORTED_PREFIX + path.stem
            if self._load_preset(path, family, "imported"):
                self.preset_info[family].setdefault("label", path.stem.replace("_", " ").title())

    def _palette(self, family: str, mode: str) -> dict[str, str]:
        '''One mode of a preset or "<accent>.<hierarchy>" family, inset if theme_inset is on.'''
        inset = self.theme_inset
        adjust = self.theme_adjust[mode]
        if family in self.palettes:
            colors = self.palettes[family][mode]
            if inset:
                colors = palette_generator.inset(colors)
            return palette_generator.borders(colors, mode, adjust["border"])
        accent, _, hierarchy = family.partition(".")
        profile = self.hierarchies[hierarchy]
        self.theme_accent, self.theme_hierarchy = accent, hierarchy
        return palette_generator.generate(self.accents[accent], profile, mode,
                                          profile.get("inset", palette_generator.DEFAULT_INSET) if inset else None,
                                          self.theme_tint, adjust["steps"], adjust["height"], adjust["border"])

    def is_theme(self, theme_name) -> bool:
        if not isinstance(theme_name, str):
            return False
        mode, _, family = theme_name.partition("_")
        accent, _, hierarchy = family.partition(".")
        return mode in THEME_MODES and (family in self.palettes or (accent in self.accents and hierarchy in self.hierarchies))

    def theme_family(self) -> str:
        '''The current preset's name, or "<accent>.<hierarchy>".'''
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
        curated = [name for name in CURATED_THEMES if name in self.palettes]
        imported = [name for name in self.palettes if name.startswith(IMPORTED_PREFIX)]
        return {name: self.preset_name(name) for name in curated + imported}

    def default_theme(self, mode: str | None = None) -> str:
        '''The first default theme (or built-in blue, if assets/themes is missing it) - in mode, or the system's.'''
        if mode is None:
            mode = "dark" if darkdetect.isDark() else "light"
        family = next((name for name in CURATED_THEMES if name in self.palettes), "blue")
        return f"{mode}_{family}"

    def is_preset(self) -> bool:
        return self.theme_family() in self.palettes

    def load_preferred_theme(self):
        self.theme_inset = self.context.preferences.get("theme_inset") is True
        tint = self.context.preferences.get("theme_tint")
        if isinstance(tint, (int, float)) and not isinstance(tint, bool):
            self.theme_tint = min(THEME_TINT_MAX, max(0.0, float(tint)))
        saved_adjust = self.context.preferences.get("theme_adjust")
        for mode, values in self.theme_adjust.items():
            saved_values = saved_adjust.get(mode) if isinstance(saved_adjust, dict) else None
            for key, (low, high) in THEME_ADJUST_RANGE.items():
                value = saved_values.get(key) if isinstance(saved_values, dict) else None
                values[key] = min(high, max(low, float(value))) if isinstance(value, (int, float)) and not isinstance(value, bool) \
                    else DEFAULT_THEME_ADJUST[mode][key]
        saved = self.context.preferences.get("theme")
        if self.is_theme(saved):
            self.apply_theme(saved)
        else:
            self.load_default_theme()

    def load_default_theme(self):
        self.theme_inset = DEFAULT_THEME_INSET
        self.theme_tint = DEFAULT_THEME_TINT
        self.theme_adjust = {mode: dict(values) for mode, values in DEFAULT_THEME_ADJUST.items()}
        self.apply_theme(self.default_theme())

    def reset_theme(self):
        '''
        Everything the theme editor changes back to its default - the first
        default theme (keeping light or dark), its fine-tuning and the
        surfaces - saved, and the page rebuilt in it.
        '''
        self.theme_inset = DEFAULT_THEME_INSET
        self.theme_tint = DEFAULT_THEME_TINT
        self.theme_adjust = {mode: dict(values) for mode, values in DEFAULT_THEME_ADJUST.items()}
        self.context.preferences.set("theme_inset", self.theme_inset)
        self.context.preferences.set("theme_tint", self.theme_tint)
        self.context.preferences.set("theme_adjust", {mode: dict(values) for mode, values in self.theme_adjust.items()})
        self.reset_surfaces()
        self.set_theme(self.default_theme(self.current_theme.partition("_")[0]))

    def set_theme(self, theme_name: str):
        '''Applies a theme ("<mode>_<family>", e.g. "dark_teal" or "light_cyan.whisper"), saves it, and rebuilds the page in it.'''
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

    def set_family(self, family: str):
        '''Switches to a preset or "<accent>.<hierarchy>" family, keeping light or dark.'''
        self.set_theme(f"{self.current_theme.partition('_')[0]}_{family}")

    def set_accent(self, accent: str):
        self.set_family(f"{accent}.{self.theme_hierarchy}")

    def set_hierarchy(self, hierarchy: str):
        '''Pairs the current accent with this hierarchy - turning inset fields on if it has its own (e.g. "inset", "slots").'''
        if "inset" in self.hierarchies.get(hierarchy, {}):
            self.theme_inset = True
            self.context.preferences.set("theme_inset", True)
        self.set_family(f"{self.theme_accent}.{hierarchy}")

    def set_tint(self, tint: float):
        '''How much the accent bleeds into the surfaces (see DEFAULT_THEME_TINT) - saved, and the page rebuilt in it.'''
        self.theme_tint = min(THEME_TINT_MAX, max(0.0, tint))
        self.context.preferences.set("theme_tint", self.theme_tint)
        self.set_theme(self.current_theme)

    def set_adjust(self, mode: str, key: str, value: float):
        '''One of a mode's adjustments (see DEFAULT_THEME_ADJUST) - saved, and the page rebuilt in it.'''
        low, high = THEME_ADJUST_RANGE[key]
        self.theme_adjust[mode][key] = min(high, max(low, value))
        self.context.preferences.set("theme_adjust", {mode: dict(values) for mode, values in self.theme_adjust.items()})
        self.set_theme(self.current_theme)

    def set_inset(self, on: bool):
        '''Inset fields (see DEFAULT_THEME_INSET) on or off - saved, and the page rebuilt in it.'''
        self.theme_inset = on
        self.context.preferences.set("theme_inset", on)
        self.set_theme(self.current_theme)
