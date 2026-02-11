from customtkinter import CTkFont

class Style:

    def __init__(self, ui_scale: float=100.0):
        self.scale = ui_scale
        self.GAP = 10
        self.PANE_MIN = self.GAP*4
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