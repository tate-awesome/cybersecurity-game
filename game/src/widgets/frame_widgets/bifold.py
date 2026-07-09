from tkinter import PanedWindow
from customtkinter import CTkFrame
from ...app_core.context import Context


class Bifold(PanedWindow):

    def __init__(self, master, context: Context):
        self.context = context
        style = context.style

        # Get root color
        rc = style.color("root")

        # Create paned window
        super().__init__(master, orient="vertical", background=rc, sashwidth=style.igap, opaqueresize=0)
        self.pack(side="top", fill="both", expand=True, padx=style.nogap, pady=style.nogap)

        # Create panes with matching corners and preset widths
        master.update_idletasks()
        h = self.winfo_height() / context.style.get_scale_correction()
        self.top = CTkFrame(self, height=h//2, background_corner_colors=(rc, rc, rc, rc))
        self.bottom = CTkFrame(self, width=h//2, background_corner_colors=(rc, rc, rc, rc))

        # Add panes
        self.add(self.top, minsize=style.PANE_MIN)
        self.add(self.bottom, minsize=style.PANE_MIN)

        self.bind("<Configure>", self.on_pane_resize)

    def on_pane_resize(self, event=None):
        self.context.root.update_idletasks()