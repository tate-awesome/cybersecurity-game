from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QInputDialog
import darkdetect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Hand-rolled replacement for qt-material's theme presets. Each family has a
# dark and light variant; every color key here is required (color() and
# Style._build_stylesheet both read them directly with no fallback), so a
# new family must define both variants with the full key set below.
PALETTES: dict[str, dict[str, dict[str, str]]] = {
    "teal": {
        # Dark mode: panel sits close to root (both near-black) so widget-
        # colored cards clearly pop above the recessed backdrop. Light mode
        # flips that - panel sits close to field (both near-white) so
        # widget-colored cards read as the slightly-toned layer between
        # them. Either way, widget is always the mode's biggest single step,
        # which is what actually keeps stacked forms from blending together.
        "dark": {
            "root": "#12181a", "panel": "#171e21", "widget": "#2a343a",
            "field": "#37424a", "field_text": "#e0f2f1", "text": "#e0f2f1",
            "accent": "#00bcd4", "accent_text": "#062024", "border": "#303b42",
            "scrollbar": "#303b42", "scrollbar_hover": "#404b52",
        },
        "light": {
            "root": "#dbe9e8", "panel": "#f3fcf8", "widget": "#e6f2f0",
            "field": "#ffffff", "field_text": "#263238", "text": "#263238",
            "accent": "#00acc1", "accent_text": "#ffffff", "border": "#dbe9e8",
            "scrollbar": "#dbe9e8", "scrollbar_hover": "#c1cdcc",
        },
    },
    "blue": {
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
    "purple": {
        "dark": {
            "root": "#16121f", "panel": "#1b1826", "widget": "#2e2e3f",
            "field": "#3b3c4f", "field_text": "#ede6f5", "text": "#ede6f5",
            "accent": "#9c5fff", "accent_text": "#ffffff", "border": "#343547",
            "scrollbar": "#343547", "scrollbar_hover": "#444557",
        },
        "light": {
            "root": "#e6daf3", "panel": "#feedff", "widget": "#f1e3fb",
            "field": "#ffffff", "field_text": "#2a2233", "text": "#2a2233",
            "accent": "#8a3ffc", "accent_text": "#ffffff", "border": "#e6daf3",
            "scrollbar": "#e6daf3", "scrollbar_hover": "#cac0d6",
        },
    },
    "amber": {
        "dark": {
            "root": "#1c160f", "panel": "#211c16", "widget": "#34322f",
            "field": "#41403f", "field_text": "#f5e9d8", "text": "#f5e9d8",
            "accent": "#ffb300", "accent_text": "#241d16", "border": "#3a3937",
            "scrollbar": "#3a3937", "scrollbar_hover": "#4a4947",
        },
        "light": {
            "root": "#f2e4c9", "panel": "#fff7d9", "widget": "#fdedd1",
            "field": "#ffffff", "field_text": "#33291a", "text": "#33291a",
            "accent": "#f59f00", "accent_text": "#241d16", "border": "#f2e4c9",
            "scrollbar": "#f2e4c9", "scrollbar_hover": "#d5c9b1",
        },
    },
    "red": {
        "dark": {
            "root": "#1c1013", "panel": "#21161a", "widget": "#342c33",
            "field": "#413a43", "field_text": "#f5dde0", "text": "#f5dde0",
            "accent": "#ff5252", "accent_text": "#ffffff", "border": "#3a333b",
            "scrollbar": "#3a333b", "scrollbar_hover": "#4a434b",
        },
        "light": {
            "root": "#f2d8db", "panel": "#ffebeb", "widget": "#fde1e3",
            "field": "#ffffff", "field_text": "#331a1d", "text": "#331a1d",
            "accent": "#e53935", "accent_text": "#ffffff", "border": "#f2d8db",
            "scrollbar": "#f2d8db", "scrollbar_hover": "#d5bec1",
        },
    },
}

# Fallback themes when no preference is saved yet, or when toggle_mode's
# target mode has no variant in the current color family.
DEFAULT_DARK_THEME = "dark_teal"
DEFAULT_LIGHT_THEME = "light_teal"

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
        self.context = context

        # Preferences don't exist yet at this point in startup (see
        # ContextManager.start_session) - this is just a system-appropriate
        # bootstrap default; load_preferred_theme() overrides it once
        # preferences are available.
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

    def color(self, type: str) -> str:
        '''
        Returns the input string OR a color from the active hand-rolled
        palette (see PALETTES/apply_theme):
        "root": window background
        "panel": panel background
        "widget": nested/inner widget background
        "accent": button/highlight color
        "field": text field background
        "field_text": text field text color
        "scrollbar": scrollbar handle color
        "scrollbar_hover": scrollbar handle hover color
        '''
        colors = {
            "root": self._theme_colors["root"],
            "panel": self._theme_colors["panel"],
            "widget": self._theme_colors["widget"],
            "accent": self._theme_colors["accent"],
            "field": self._theme_colors["field"],
            "field_text": self._theme_colors["field_text"],
            "scrollbar": self._theme_colors["scrollbar"],
            "scrollbar_hover": self._theme_colors["scrollbar_hover"],
        }
        return colors.get(type, type)

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
        widget.setToolTip(self.context.labels.get(class_key, widget_key))

    def apply_theme(self, theme_name: str):
        '''
        Applies a hand-rolled palette globally (its QSS stylesheet covers
        every native Qt widget - see _build_stylesheet) and refreshes the
        color() values this app's own hand-styled widgets pull from. Those
        are set once, inline, at construction time (see Panel/BaseForm/
        MenuBar etc.), so - unlike native widgets - they only pick up a new
        theme on their next rebuild; callers changing the theme after
        startup (toggle_mode, select_theme) follow this with
        context.router.refresh().
        '''
        mode, _, family = theme_name.partition("_")
        app = QApplication.instance()
        self._theme_colors = PALETTES[family][mode]
        # The native platform style (e.g. "windows11") largely ignores QSS
        # background-color/border-radius on QPushButton/QComboBox/QCheckBox -
        # Fusion is the style Qt's own docs recommend for full stylesheet
        # control, and what qt-material used under the hood for the same
        # reason. Only set it once: re-applying the same style on every theme
        # change (toggle_mode/select_theme trigger this repeatedly in one
        # session) leaves QScrollArea-based panels (Scrollable) with a stale,
        # unrepainted viewport background from the previous theme.
        if app.style().objectName().lower() != "fusion":
            app.setStyle("Fusion")
        self._widget_qss = self._build_stylesheet(self._theme_colors)
        app.setStyleSheet(self._widget_qss)
        self.current_theme = theme_name
        self.mode = "Dark" if mode == "dark" else "Light"

    def themed(self, extra: str = "", widget=None) -> str:
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
        '''
        if not extra:
            return self._widget_qss
        if "{" in extra:
            return self._widget_qss + "\n" + extra
        assert widget is not None, "themed() needs `widget` to scope a bare declaration list"
        name = f"_themed_{id(widget)}"
        widget.setObjectName(name)
        return self._widget_qss + f"\n#{name} {{ {extra} }}"

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

    def _build_stylesheet(self, c: dict[str, str]) -> str:
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

        return f'''
            QWidget {{ color: {c["text"]}; }}
            QMainWindow, QDialog {{ background-color: {c["root"]}; }}
            QToolTip {{
                background-color: {c["panel"]};
                color: {c["text"]};
                border: 1px solid {c["border"]};
            }}
            QPushButton {{
                background-color: {c["accent"]};
                color: {c["accent_text"]};
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: {accent_hover}; }}
            QPushButton:pressed {{ background-color: {accent_pressed}; }}
            QPushButton:disabled {{ background-color: {c["widget"]}; color: {c["border"]}; }}
            QLineEdit, QComboBox, QPlainTextEdit, QTextEdit {{
                background-color: {c["field"]};
                color: {c["field_text"]};
                border: 1px solid {c["border"]};
                border-radius: 4px;
                padding: 4px;
            }}
            QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border: 1px solid {c["accent"]}; }}
            QComboBox QAbstractItemView {{
                background-color: {c["field"]};
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
        '''

    def _list_themes(self) -> list[str]:
        return [f"{mode}_{family}" for family in PALETTES for mode in ("dark", "light")]

    def load_preferred_theme(self):
        saved = self.context.preferences.data.get("theme")
        if self.context.preferences.has("theme") and saved in self._list_themes():
            self.apply_theme(saved)
        else:
            self.load_default_theme()

    def load_default_theme(self):
        self.apply_theme(DEFAULT_DARK_THEME if darkdetect.isDark() else DEFAULT_LIGHT_THEME)

    def toggle_mode(self):
        '''
        Toggles between the light and dark variant of the current theme's
        color family (e.g. dark_teal <-> light_teal).
        '''
        current_mode, _, family = self.current_theme.partition("_")
        target_mode = "light" if current_mode == "dark" else "dark"
        self.apply_theme(f"{target_mode}_{family}")
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()

    def select_theme(self):
        '''
        Opens a dialog for the user to pick a color family only - light vs.
        dark is controlled solely by toggle_mode (the "Toggle Theme" button)
        and stays whatever it currently is; picking a color here keeps the
        current mode and just swaps the family (e.g. dark_teal -> dark_blue).
        '''
        families = list(PALETTES.keys())
        labels = [family.title() for family in families]
        current_mode, _, current_family = self.current_theme.partition("_")
        current_index = families.index(current_family) if current_family in families else 0

        label, ok = QInputDialog.getItem(
            self.root, "Select a Theme", "Color:", labels, current_index, editable=False
        )
        if not ok:
            return

        self.apply_theme(f"{current_mode}_{families[labels.index(label)]}")
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()
