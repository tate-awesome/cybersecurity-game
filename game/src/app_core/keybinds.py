from customtkinter import CTk
from .context import Context

class KeyBinds:

    def __init__(self, root: CTk, context: Context, refresh: callable, quit: callable):
        self.root = root
        self.context = context
        self.refresh = refresh

        # Page zoom control
        root.bind("<Control-plus>", self.zoom_in)            # Ctrl +
        root.bind("<Control-minus>", self.zoom_out)          # Ctrl -
        root.bind("<Control-0>", self.zoom_default)          # Ctrl 0
        root.bind("<Control-equal>", self.zoom_in)   # (linux) Ctrl = also works as Ctrl +

        # Key events
        # self.context.root.bind("<Key>", self.print_key)

        # Fullscreen control
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.exit_fullscreen)

        # On close
        root.protocol("WM_DELETE_WINDOW", quit)


    def toggle_fullscreen(self, event=None):
        is_fullscreen = not bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", is_fullscreen)


    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)


    def zoom_in(self, event=None):
        next_index = self.context.ui_scales.index(int(self.context.ui_scale)) + 1
        if next_index >= len(self.context.ui_scales):
            return
        self.context.ui_scale = float(self.context.ui_scales[next_index])
        self.refresh()


    def zoom_out(self, event=None):
        next_index = self.context.ui_scales.index(int(self.context.ui_scale)) - 1
        if next_index < 0:
            return
        self.context.ui_scale = float(self.context.ui_scales[next_index])
        self.refresh()


    def zoom_default(self, event=None):
        self.context.ui_scale = 100.0
        self.refresh()

    
    def print_key(e):
        print(e.keysym, e.state)