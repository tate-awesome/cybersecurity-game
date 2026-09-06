from PySide6.QtGui import QFont
import darkdetect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Approximate stand-in for customtkinter's "blue" theme, keyed the same way
# Style.color() was already called everywhere - light mode value first, dark
# mode value second - so callers didn't need to change. Not wired up to any
# theme-file loading yet (see load_preferred_theme/select_theme below).
PALETTE = {
    "root":            ("#F2F2F2", "#242424"),
    "panel":           ("#EBEBEB", "#2B2B2B"),
    "widget":          ("#FFFFFF", "#333333"),
    "accent":          ("#3B8ED0", "#1F6AA5"),
    "field":           ("#F9F9FA", "#343638"),
    "field_text":      ("#000000", "#FFFFFF"),
    "scrollbar":       ("#C0C0C0", "#4A4A4A"),
    "scrollbar_hover": ("#A0A0A0", "#5A5A5A"),
}

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
        self.mode = "Dark" if darkdetect.isDark() else "Light"
        self.current_theme = "blue"
        self.context = context

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
        Returns the input string OR a theme color:
        "root": window background
        "panel": panel background
        "widget": nested/inner widget background
        "accent": button/highlight color
        "field": text field background
        "field_text": text field text color
        "scrollbar": scrollbar handle color
        "scrollbar_hover": scrollbar handle hover color
        '''
        i = 0 if self.mode == "Light" else 1
        if type not in PALETTE:
            return type
        return PALETTE[type][i]

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

    def load_preferred_theme(self):
        # TODO: customtkinter's JSON theme-file loading (ThemeManager) has
        # no Qt equivalent yet; only the preference itself carries over.
        if self.context.preferences.has("theme"):
            self.current_theme = self.context.preferences.data["theme"]
        else:
            self.current_theme = "blue"

    def load_default_theme(self):
        self.current_theme = "blue"

    def load_preferred_mode(self):
        if self.context.preferences.has("mode"):
            self.mode = self.context.preferences.data["mode"]

    def load_default_mode(self):
        self.mode = "Light"

    def toggle_mode(self):
        '''
        Toggles the appearance mode (light/dark mode)
        '''
        self.mode = "Light" if self.mode == "Dark" else "Dark"
        self.context.preferences.set("mode", self.mode)
        self.context.router.refresh()

    def select_theme(self):
        '''
        Opens a dialog for the user to select a theme file.
        TODO: no theme file format is loaded yet - only the selected path
        is recorded, pending a Qt-native theme/palette system.
        '''
        themes_dir = self.context.paths.themes
        file_path = self.context.paths.select_path(themes_dir, "Select a Theme File")
        if file_path is None:
            return
        self.current_theme = file_path
        self.context.preferences.set("theme", self.current_theme)
        self.context.router.refresh()