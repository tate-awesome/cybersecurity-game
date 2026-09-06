from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QInputDialog
import darkdetect
import qt_material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Fallback themes when no preference is saved yet, or when toggle_mode's
# target mode has no variant in the current color family (e.g. light_orange
# has no dark_orange - see qt_material.list_themes()).
DEFAULT_DARK_THEME = "dark_teal.xml"
DEFAULT_LIGHT_THEME = "light_teal.xml"

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
        Returns the input string OR a color from the active qt-material
        theme (see apply_theme) - qt-material only exposes 7 named roles,
        so several of these keys share one:
        "root": window background
        "panel": panel background
        "widget": nested/inner widget background
        "accent": button/highlight color (the theme's primary color)
        "field": text field background
        "field_text": text field text color
        "scrollbar": scrollbar handle color
        "scrollbar_hover": scrollbar handle hover color
        '''
        colors = {
            "root": self._root_color,
            "panel": self._panel_color,
            "widget": self._theme_colors["secondaryLightColor"],
            "accent": self._theme_colors["primaryColor"],
            "field": self._theme_colors["secondaryLightColor"],
            "field_text": self._theme_colors["secondaryTextColor"],
            "scrollbar": self._theme_colors["secondaryLightColor"],
            "scrollbar_hover": self._theme_colors["primaryLightColor"],
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
        # Native Qt tooltip - simpler than CTkToolTip (no custom border/
        # offset styling), which is an acceptable loss for now.
        widget.setToolTip(self.context.labels.get(class_key, widget_key))

    def apply_theme(self, theme_name: str):
        '''
        Applies a qt-material theme globally (its QSS stylesheet covers
        every native Qt widget automatically) and refreshes the color()
        values this app's own hand-styled widgets pull from. Those are set
        once, inline, at construction time (see Panel/BaseForm/MenuBar
        etc.), so - unlike native widgets - they only pick up a new theme
        on their next rebuild; callers changing the theme after startup
        (toggle_mode, select_theme) follow this with context.router.refresh().
        '''
        app = QApplication.instance()
        qt_material.apply_stylesheet(app, theme=theme_name)
        self.current_theme = theme_name
        self._theme_colors = qt_material.get_theme(theme_name)
        self.mode = "Dark" if theme_name.startswith("dark_") else "Light"

        # qt-material's secondaryColor/secondaryDarkColor aren't consistently
        # ordered by actual lightness across its dark_*/light_* theme families
        # (dark families: secondaryColor is the darkest of the two; light
        # families: secondaryDarkColor is) - so root (outermost, should read
        # as most "recessed") and panel (should read as "raised" above it)
        # are assigned by comparing their actual luminance rather than
        # assuming either name means what it says relative to the other.
        secondary = self._theme_colors["secondaryColor"]
        secondary_dark = self._theme_colors["secondaryDarkColor"]
        if self._luminance(secondary) <= self._luminance(secondary_dark):
            self._root_color, self._panel_color = secondary, secondary_dark
        else:
            self._root_color, self._panel_color = secondary_dark, secondary

    def _luminance(self, hex_color: str) -> int:
        hex_color = hex_color.lstrip("#")
        return sum(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def load_preferred_theme(self):
        saved = self.context.preferences.data.get("theme")
        if self.context.preferences.has("theme") and saved in qt_material.list_themes():
            self.apply_theme(saved)
        else:
            self.load_default_theme()

    def load_default_theme(self):
        self.apply_theme(DEFAULT_DARK_THEME if darkdetect.isDark() else DEFAULT_LIGHT_THEME)

    def toggle_mode(self):
        '''
        Toggles between the light and dark variant of the current theme's
        color family (e.g. dark_teal.xml <-> light_teal.xml). Falls back to
        the default theme for the target mode if this family has no variant
        for it (e.g. light_orange has no dark_orange).
        '''
        current_mode, _, family = self.current_theme.partition("_")
        target_mode = "light" if current_mode == "dark" else "dark"
        target_theme = f"{target_mode}_{family}"
        if target_theme not in qt_material.list_themes():
            target_theme = DEFAULT_DARK_THEME if target_mode == "dark" else DEFAULT_LIGHT_THEME

        self.apply_theme(target_theme)
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()

    def select_theme(self):
        '''
        Opens a dialog for the user to pick one of qt-material's built-in
        themes by name - replacing customtkinter's arbitrary theme-file
        picker, since qt-material ships named presets rather than files to
        browse to.
        '''
        themes = qt_material.list_themes()
        labels = [self._theme_display_name(t) for t in themes]
        current_index = themes.index(self.current_theme) if self.current_theme in themes else 0

        label, ok = QInputDialog.getItem(
            self.root, "Select a Theme", "Theme:", labels, current_index, editable=False
        )
        if not ok:
            return

        self.apply_theme(themes[labels.index(label)])
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()

    def _theme_display_name(self, theme_file: str) -> str:
        return theme_file.removesuffix(".xml").replace("_", " ").title()