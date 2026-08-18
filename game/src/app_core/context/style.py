from customtkinter import CTkFont, get_appearance_mode, ThemeManager, ScalingTracker, set_appearance_mode
from CTkToolTip import CTkToolTip

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

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
        self.PANE_MIN_WIDTH = self.igap*50
        self.PANE_MIN_HEIGHT = self.igap*10
        self.PANE_BIG = self.igap*100
        self.fonts = {}

        self.current_theme = "blue"
        self.context = context        

        # DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")

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
        return ScalingTracker.get_widget_scaling(self.root)

    def get_font(self, name="default"):
        if name not in self.fonts:
            if name == "default":
                self.fonts[name] = CTkFont(family="Arial", size=self.get_font_size("default"))
            elif name == "title_btn":
                self.fonts[name] = CTkFont(size=self.get_font_size("title_btn"))
            elif name == "mono":
                self.fonts[name] = CTkFont(family="Consolas", size=self.get_font_size("small"))
            elif name == "treeview":
                self.fonts[name] = CTkFont(family="Consolas", size=self.get_font_size("treeview"))
            elif name == "title":
                self.fonts[name] = CTkFont(family="Arial", size=self.get_font_size("title"), weight="bold")
            else:
                size = int(14.0*self.ui_scale/100.0)
                self.fonts[name] = CTkFont(size=size)
        return self.fonts[name]

    def get_font_size(self, name="default"):
        size = 16.0
        if name == "treeview":
            tk_scale = float(self.root.tk.call("tk", "scaling"))
            # print(tk_scale)
            size = size * self.get_scale_correction() / tk_scale
            # TODO TK vs CTK font scaling on different platforms
        elif name == "title_btn":
            size = 20.0
        elif name == "title":
            size = 72
        elif name == "small":
            size = 15.0
        return int(size * self.ui_scale / 100.0)

    def color(self, type: str) -> str:
        '''
        Returns a theme color:
        "root": root_color,
        "panel": fg_color,
        "widget": top_fg_color,
        "accent": button fg_color,
        "field": CTkTextBox fg_color
        "field_text": CTkTextBox text_color
        "scrollbar": CTkScrollbar button_color
        "scrollbar_hover": CTkScrollbar button_hover_color
        '''
        mode = get_appearance_mode()
        colors = {}
        if mode == "Light":
            i = 0
        else:
            i = 1
        colors["root"] = self.root.cget("fg_color")
        colors["panel"] = ThemeManager.theme["CTkFrame"]["fg_color"]
        colors["widget"] = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        colors["accent"] = ThemeManager.theme["CTkButton"]["fg_color"]
        colors["field"] = ThemeManager.theme["CTkTextbox"]["fg_color"]
        colors["field_text"] = ThemeManager.theme["CTkTextbox"]["text_color"]
        colors["scrollbar"] = ThemeManager.theme["CTkScrollbar"]["button_color"]
        colors["scrollbar_hover"] = ThemeManager.theme["CTkScrollbar"]["button_hover_color"]
        if not type in colors:
            return "purple"
        return colors[type][i]

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
        CTkToolTip(widget,
                   self.context.labels.get(class_key, widget_key),
                   follow=False,
                   font=self.get_font(),
                   x_offset=self.igap, y_offset=self.igap, border_width=2,
                   border_color=self.color("accent"))

    def mode(self):
        return get_appearance_mode()

    def load_preferred_theme(self):
        if self.context.preferences.has("theme"):
            file_path = self.context.preferences.data["theme"]
            try:
                ThemeManager.load_theme(file_path)
            except:
                pass
        else:
            ThemeManager.load_theme("blue")

    def load_default_theme(self):
        ThemeManager.load_theme("blue")

    def load_preferred_mode(self):
        if self.context.preferences.has("mode"):
            mode = self.context.preferences.data["mode"]
            set_appearance_mode(mode)
        else:
            set_appearance_mode("Light")

    def load_default_mode(self):
        set_appearance_mode("Light")

    def toggle_mode(self):
        '''
        Toggles the appearance mode (light/dark mode)
        '''
        mode = get_appearance_mode()
        if mode  == "Dark":
            mode = "Light"
        else:
            mode = "Dark"
        set_appearance_mode(mode)
        # set_appearance_mode refreshes all CTk elements automatically, but we have some TK elements and custom colors.
        self.context.router.refresh()

    def select_theme(self):
        '''
        Opens a dialog for the user to select a CTk theme.
        '''
        themes_dir = self.context.paths.themes
        file_path = self.context.paths.select_path(themes_dir, "Select a Theme File")
        ThemeManager.load_theme(file_path)
        self.current_theme = file_path
        self.context.router.refresh()