from customtkinter import *
import tkinter as tk
from .style import Style
# from tkinter import ttk

def menu_bar(style: Style, parent, title):
    med = style.get_font()
    menu_bar = CTkFrame(parent)
    menu_bar.pack(side="top", padx=style.GAP, pady=(style.GAP, 0), fill="x", anchor="n")
    game_label = CTkLabel(master = menu_bar, text=title, font=med)
    game_label.pack(fill=Y, side="left", padx=style.GAP)
    return menu_bar

def menu_bar_button(style: Style, parent, text, function=None):
    med = style.get_font()
    button = CTkButton(parent, text=text, command=function, font=med)
    button.pack(side="right", padx=style.GAP, pady=style.GAP)
    return button

# Layout frames
def trifold(style: Style, parent):

    # Get root color
    root_color = parent.cget("fg_color")
    mode = get_appearance_mode()
    if mode == "Light":
        root_color = root_color[0]
    else:
        root_color = root_color[1]

    # Create paned window
    paned = tk.PanedWindow(parent, orient="horizontal", background=root_color, sashwidth=style.GAP)
    paned.pack(fill="both", expand=True, padx=style.GAP, pady=style.GAP)

    # Create panes with matching corners and preset widths
    parent.update_idletasks()
    w = paned.winfo_width()
    left = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))
    middle = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))
    right = CTkFrame(paned, width=w//2, background_corner_colors=(root_color, root_color, root_color, root_color))

    # Add panes
    paned.add(left, minsize=style.PANE_MIN)
    paned.add(middle, minsize=style.PANE_MIN)
    paned.add(right, minsize=style.PANE_MIN)
    return left, middle, right

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