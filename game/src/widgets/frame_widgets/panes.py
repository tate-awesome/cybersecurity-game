from tkinter import PanedWindow
from customtkinter import CTkFrame
from ...app_core import Context

class Panes(PanedWindow):

    def __init__(self, master, context: Context, direction = "horizontal", child_count: int = 3, child_sizes: list[int] = [4, 3, 2], pad_around = True):
        '''
        Args:
            child_sizes: pane size is total size divided by child_size[i]. e.g. child_size = [3, 2, 1]
            means the first pane is 1/3 the size of the parent, the second pane is half the size of the parent,
            and the last pane takes the remaining space.
        '''
        if not direction in ["horizontal", "vertical"] or child_count < 2:
            raise ValueError(
                f"Invalid Panes args: direction={direction!r} (must be 'horizontal' or 'vertical'), "
                f"child_count={child_count!r} (must be >= 2)"
            )

        self.panels = []
        self.context = context
        style = context.style

        color = style.color("root")

        super().__init__(master, orient=direction, background=color, sashwidth=style.igap, opaqueresize=1)

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
        for i in range(child_count):
            size = s//child_sizes[i]
            pane = CTkFrame(self, height = size, width= size, background_corner_colors=(color, color, color, color))
            pane.default_size = size
            self.add(pane, minsize=min_size)
            self.panels.append(pane)

        self.bind("<Configure>", self.on_pane_resize)

    def on_pane_resize(self, event=None):
        self.context.root.update_idletasks()

    def pane(self, index: int):
        if hasattr(self, "panels"):
            return self.panels[index]