from customtkinter import CTkFont, get_appearance_mode, ThemeManager

class Style:

    def __init__(self, context):
        self.root = context.root
        self.scale = context.ui_scale
        self.gap = (10, 10)
        self.nogap = (0, 0)
        self.gaptop = (10, 0)
        self.igap = 10
        self.cgap = 2
        self.PANE_MIN = self.igap*4
        self.fonts = {}
        # DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")


    def get_font(self, name="default"):
        if name not in self.fonts:
            if name == "default":
                size = int(16.0*self.scale/100.0)
                self.fonts[name] = CTkFont(family="Arial", size=size)
            elif name == "title_btn":
                size=int(20.0*self.scale/100.0)
                self.fonts[name] = CTkFont(size=size)
            else:
                size = int(14.0*self.scale/100.0)
                self.fonts[name] = CTkFont(size=size)
        return self.fonts[name]

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
        else:
            colors["root"] = root_color[1]
            colors["panel"] = ThemeManager.theme["CTkFrame"]["fg_color"][1]
            colors["widget"] = ThemeManager.theme["CTkFrame"]["top_fg_color"][1]
        return colors[type]