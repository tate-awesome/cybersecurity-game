from customtkinter import *
import tkinter as tk
from .style import Style
from . import popup
# from tkinter import ttk

# Layout frames
def trifold(style: Style, parent):

    # Get root color
    rc = style.color("root")

    # Create paned window
    paned = tk.PanedWindow(parent, orient="horizontal", background=rc, sashwidth=style.igap)
    paned.pack(fill="both", expand=True, padx=style.gap, pady=style.gap)

    # Create panes with matching corners and preset widths
    parent.update_idletasks()
    w = paned.winfo_width()
    left = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))
    middle = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))
    right = CTkFrame(paned, width=w//2, background_corner_colors=(rc, rc, rc, rc))

    # Add panes
    paned.add(left, minsize=style.PANE_MIN)
    paned.add(middle, minsize=style.PANE_MIN)
    paned.add(right, minsize=style.PANE_MIN)
    return left, middle, right

def scrollable(style: Style, parent):
    frame = CTkScrollableFrame(parent, fg_color=style.color("panel"))
    frame.pack(side="top", fill="both", expand="y", padx=style.gap, pady=style.gap)
    bind_scroll(frame)
    return frame

def bind_scroll(sf: CTkScrollableFrame):
    canvas = sf._parent_canvas

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

    sf.bind("<Enter>", _bind_to_mousewheel)
    sf.bind("<Leave>", _unbind_from_mousewheel)

def configure_reversible_button(the_button: CTkButton, start_func: callable, stop_func: callable, func_name: str):
    def stop():
        the_button.configure(text=f"Stopping {func_name}...")
        stop_func()
        the_button.configure(command=start, text=f"Start {func_name}")

    def start():
        the_button.configure(text=f"Starting {func_name}...")
        start_func()
        the_button.configure(command=stop, text=f"Stop {func_name}")
    the_button.configure(command=start, text=f"Start {func_name}")

def clear(parent):
    for widget in parent.winfo_children():
        widget.destroy()