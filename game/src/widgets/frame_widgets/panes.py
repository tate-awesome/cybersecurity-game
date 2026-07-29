from tkinter import PanedWindow
from customtkinter import CTkFrame
from ...app_core.context import Context

class Panes(PanedWindow):

    def __init__(self, master, context: Context, direction = "horizontal", child_count: int = 3, child_sizes: list[int] = [4, 3, 2], pad_around = True):

        if not direction in ["horizontal", "vertical"] or child_count < 2:
            return

        self.context = context
        style = context.style

        color = style.color("root")

        super().__init__(master, orient=direction, background=color, sashwidth=style.igap, opaqueresize=0)

        if pad_around:
            self.pack(style.packing())
        else:
            self.pack(style.packing("panel"))
        
        master.update_idletasks()

        if direction == "horizontal":
            s = self.winfo_width() / context.style.get_scale_correction()
            min_size = style.PANE_MIN_WIDTH
        else:
            s = self.winfo_height() / context.style.get_scale_correction()
            min_size = style.PANE_MIN_HEIGHT

        self.panes = []       
        for i in range(child_count):
            size = s//child_sizes[i]
            pane = CTkFrame(self, height = size, width= size, background_corner_colors=(color, color, color, color))
            pane.default_size = size
            self.add(pane, minsize=min_size)
            self.panes.append(pane)

        self.bind("<Configure>", self.on_pane_resize)

    def on_pane_resize(self, event=None):
        self.context.root.update_idletasks()
    
    def panes(self):
        return self.panes

    def pane(self, index: int):
        return self.panes[index]