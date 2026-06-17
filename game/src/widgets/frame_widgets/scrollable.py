from ...app_core.context import Context
from customtkinter import CTkFrame, CTkScrollableFrame

class Scrollable(CTkScrollableFrame):
    '''
    Vertically scrollable CTk frame with mousewheel support
    Inherits CTkScrollableFrame.
    '''

    def __init__(self, master: CTkFrame, context: Context, height: int = -1, fill = "both", expand=True):
        self.context = context
        self.master = master
        style = context.style

        super().__init__(master, fg_color=style.color("panel"))
        
        if not height == -1:
            self.configure(height=height)

        self.pack(side="top", fill=fill, expand=expand, padx=style.cgap, pady=style.cgap)
        self.bind_scroll()


    def bind_scroll(self):
        canvas = self._parent_canvas

        def _on_mousewheel(event):
            canvas.yview_scroll(-int(event.delta / 480), "units")

        def _bind_to_mousewheel(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        def _unbind_from_mousewheel(_):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_to_mousewheel)
        canvas.bind("<Leave>", _unbind_from_mousewheel)

    def add_deadspace(self, height: float | int = 0.8):
        style = self.context.style
        self.update_idletasks()
        if isinstance(height, float):
            h = self.winfo_height() * height
        elif isinstance(height, int):
            h = height
        else:
            h = self.winfo_height() * 0.8
        
        frame = CTkFrame(self, fg_color=style.color("panel"), height=h)
        frame.pack(side="top", fill="x", expand=False, padx=style.nogap, pady=style.nogap)
        return frame