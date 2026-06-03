from customtkinter import CTkFont, get_appearance_mode, ThemeManager, ScalingTracker

class Style:

    def __init__(self, context):
        self.root = context.root
        self.context = context
        self.scale = context.ui_scale
        self.gap = (10, 10)
        self.gap2 = (20,20)
        self.nogap = (0, 0)
        self.gaptop = (10, 0)
        self.gapbot = (0, 10)
        self.igap = 10
        self.cgap = 2
        self.PANE_MIN = self.igap*4
        self.fonts = {}

        # DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")

    def get_scale_correction(self):
        return ScalingTracker.get_widget_scaling(self.context.root)

    def get_font(self, name="default"):
        if name not in self.fonts:
            if name == "default":
                self.fonts[name] = CTkFont(family="Arial", size=self.get_font_size("default"))
            elif name == "title_btn":
                self.fonts[name] = CTkFont(size=self.get_font_size("title"))
            elif name == "mono":
                self.fonts[name] = CTkFont(family="Consolas", size=self.get_font_size("default"))
            elif name == "treeview":
                self.fonts[name] = CTkFont(family="Consolas", size=self.get_font_size("treeview"))
            else:
                size = int(14.0*self.scale/100.0)
                self.fonts[name] = CTkFont(size=size)
        return self.fonts[name]

    def get_font_size(self, name="default"):
        size = 16.0
        if name == "treeview":
            tk_scale = float(self.context.root.tk.call("tk", "scaling"))
            # print(tk_scale)
            size = size * self.get_scale_correction() / tk_scale
            # TODO TK vs CTK font scaling on different platforms
        elif name == "title":
            size = 20.0
        return int(size * self.scale / 100.0)

    def color(self, type: str) -> str:
        '''
        Returns a theme color:
        "root": root color,
        "panel": fg_color,
        "widget": top_fg_color
        '''
        root_color = self.root.cget("fg_color")
        mode = get_appearance_mode()
        colors = {}
        if mode == "Light":
            colors["root"] = root_color[0]
            colors["panel"] = ThemeManager.theme["CTkFrame"]["fg_color"][0]
            colors["widget"] = ThemeManager.theme["CTkFrame"]["top_fg_color"][0]
            colors["accent"] = ThemeManager.theme["CTkButton"]["fg_color"][0]
        else:
            colors["root"] = root_color[1]
            colors["panel"] = ThemeManager.theme["CTkFrame"]["fg_color"][1]
            colors["widget"] = ThemeManager.theme["CTkFrame"]["top_fg_color"][1]
            colors["accent"] = ThemeManager.theme["CTkButton"]["fg_color"][1]
        return colors[type]

    def get_column_width(self, column_name):
        match column_name:
            case "time":
                return int(120*self.get_scale_correction())
            case "number":
                return int(70*self.get_scale_correction())
            case "length":
                return int(80*self.get_scale_correction())
            case "hack_info":
                return int(120*self.get_scale_correction())
            case "transaction":
                return int(500*self.get_scale_correction())
            case "layers":
                return int(250*self.get_scale_correction())
            case "purpose":
                return int(200*self.get_scale_correction())
            case "summary":
                return int(600*self.get_scale_correction())
            case "modbus":
                return int(400*self.get_scale_correction())
        return 100