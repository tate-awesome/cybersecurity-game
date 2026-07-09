from tkinter import PanedWindow
from customtkinter import CTkFrame
from ...app_core.context import Context


class Trifold(PanedWindow):

    def __init__(self, master, context: Context):
        self.context = context
        style = context.style

        # Get root color
        rc = style.color("root")

        # Create paned window
        super().__init__(master, orient="horizontal", background=rc, sashwidth=style.igap, opaqueresize=0)
        self.pack(fill="both", expand=True, padx=style.gap, pady=style.gap)

        # Create panes with matching corners and preset widths
        master.update_idletasks()
        w = self.winfo_width() / context.style.get_scale_correction()
        self.left = CTkFrame(self, width=w//4, background_corner_colors=(rc, rc, rc, rc))
        self.middle = CTkFrame(self, width=w//3, background_corner_colors=(rc, rc, rc, rc))
        self.right = CTkFrame(self, width=w//2, background_corner_colors=(rc, rc, rc, rc))

        # Add panes
        self.add(self.left, minsize=style.PANE_MIN)
        self.add(self.middle, minsize=style.PANE_MIN)
        self.add(self.right, minsize=style.PANE_MIN)

        self.bind("<Configure>", self.on_pane_resize)

    def on_pane_resize(self, event=None):
        self.context.root.update_idletasks()