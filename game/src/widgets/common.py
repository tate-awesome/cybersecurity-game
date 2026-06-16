from customtkinter import *
import tkinter as tk
from . import popup
from ..app_core.context import Context
# from tkinter import ttk

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

def scroll_deadspace(parent, context: Context):
    style = context.style
    parent.update_idletasks()
    h = parent.winfo_height() * 0.8
    frame = CTkFrame(parent, fg_color=style.color("panel"), height=h)
    frame.pack(side="top", fill="x", expand=False, padx=style.nogap, pady=style.nogap)


def create_bifold(parent: CTkFrame, context: Context):
    style = context.style

    # bifold
    rc = style.color("root")

    # Create paned window
    paned = tk.PanedWindow(parent, orient="vertical", background=rc, sashwidth=style.igap)
    paned.pack(side="top", fill="both", expand=True)

    # Create panes with matching corners and preset widths
    parent.update_idletasks()
    h = paned.winfo_height()
    top = CTkFrame(paned, height=h//2, background_corner_colors=(rc, rc, rc, rc))
    bottom = CTkFrame(paned, height=h//2, background_corner_colors=(rc, rc, rc, rc))

    # Add panes
    paned.add(top, minsize=110)
    paned.add(bottom, minsize=110)
    return top, bottom

def create_stretchable(parent, context: Context, side="top"):
    style = context.style
    frame = CTkFrame(parent)
    frame.pack(side=side, fill="both", expand=True)
    return frame