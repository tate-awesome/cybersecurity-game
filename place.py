import tkinter as tk
from tkinter import ttk
from customtkinter import *
import customtkinter as ctk

# MED_FONT = CTkFont(family="Arial", size=16)
PANE_GAPS = 10
PANE_MIN = PANE_GAPS*4
# MED_FONT = CTkFont(family="Arial", size=16)
# DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")
   
# Menu bar widgets
def menu_bar(parent, title):
    menu_bar = CTkFrame(parent)
    menu_bar.pack(side="top", padx=PANE_GAPS/2, pady=PANE_GAPS/2, fill="x", anchor="n")
    game_label = CTkLabel(master = menu_bar, text=title, font=CTkFont(family="Arial", size=16))
    game_label.pack(side="left", padx=20, pady=10)
    return menu_bar

def menu_bar_button(parent, text, function):
    button = CTkButton(parent, text=text, command=function, font=CTkFont(family="Arial", size=16))
    button.pack(side="right", padx=10, pady=10)

# Trifold paned window
def trifold(parent):

    # Get root color
    rc = parent.cget("fg_color")
    mode = ctk.get_appearance_mode()
    print(rc)
    if mode == "Light":
        rc = rc[0]
    else:
        rc = rc[1]

    # Create paned window
    paned = tk.PanedWindow(parent, orient="horizontal", background=rc, sashwidth=PANE_GAPS)
    paned.pack(fill="both", expand=True, padx=PANE_GAPS, pady=(0, PANE_GAPS))

    # Create panes with matching corners and preset widths
    w = parent.winfo_screenwidth()*3/4
    left = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))
    middle = CTkFrame(paned, width=w//2, background_corner_colors=(rc, rc, rc, rc))
    right = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))

    # Add panes
    paned.add(left, minsize=PANE_MIN)
    paned.add(middle, minsize=PANE_MIN)
    paned.add(right, minsize=PANE_MIN)
    return left, middle, right

class virtual_map:
    def canvas(parent, draw_function, framerate_ms):
        square_size = min(parent.winfo_height(), parent.winfo_width())
        canvas = CTkCanvas(parent)
        canvas.pack()
        canvas.config(width=square_size, height=square_size)
        def resize(event):
            # Keep square and redraw on resize
            square_size = min(parent.winfo_height(), parent.winfo_width())
            canvas.config(width=square_size, height=square_size)
            draw_function(canvas)
        parent.bind("<Configure>", resize)
        
        def animation_loop():
            draw_function(canvas)
            canvas.after(framerate_ms, animation_loop)
        animation_loop()
        return canvas

class main_menu:
    def buttons_wrapper(parent):
        wrapper = CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=2, column=1)
        return wrapper

    def button(parent, text, function):
        button = CTkButton(parent, text=text, width=280, height=50, command=function, font=CTkFont(family="Arial", size=24))
        button.pack(pady=10)
        return button

    def title(parent, text, root):
        # Place title
        title_font = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")
        title_label = CTkLabel(
                parent,
                text="Cybersecurity Game",
                font=title_font
            )
        title_label.grid(row=1, column=1, ipady=20)

        # Make title respond to window sizes
        def resize(event):
            # scale font size with window width
            new_size = max(32, event.height // 20)
            title_label.configure(font=("Arial", new_size))
        parent.bind("<Configure>", resize)

        # Center title
        for i in [0, 3]:
            parent.grid_rowconfigure(i, weight=1)
            parent.grid_columnconfigure(i, weight=1)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_columnconfigure(1, weight=0)

        return title_label

    def wrapper(parent):
        main_menu_frame = CTkFrame(parent)
        main_menu_frame.pack(fill="both", expand=True)
        return main_menu_frame
        