import tkinter as tk
from tkinter import ttk
from customtkinter import *
import customtkinter as ctk

# MED_FONT = CTkFont(family="Arial", size=16)
PANE_GAPS = 10
PANE_MIN = PANE_GAPS*4
MED_FONT = None
LARGE_FONT = None
MONO_FONT = None

def set_fonts():
    global MED_FONT
    global LARGE_FONT
    global MONO_FONT
    if MED_FONT is None:
        MED_FONT = ctk.CTkFont(family="Arial", size=16)
    if LARGE_FONT is None:
        LARGE_FONT = ctk.CTkFont(family="Arial", size=24)
    if MONO_FONT is None:
        MONO_FONT = ctk.CTkFont(family="Courier", size=14)

# DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")
   
# Menu bar widgets
def menu_bar(parent, title):
    menu_bar = CTkFrame(parent)
    menu_bar.pack(side="top", padx=PANE_GAPS/2, pady=PANE_GAPS/2, fill="x", anchor="n")
    game_label = CTkLabel(master = menu_bar, text=title, font=MED_FONT)
    game_label.pack(side="left", padx=20, pady=10)
    return menu_bar

def menu_bar_button(parent, text, function):
    button = CTkButton(parent, text=text, command=function, font=MED_FONT)
    button.pack(side="right", padx=10, pady=10)

# Trifold paned window
def trifold(parent):

    # Get root color
    rc = parent.cget("fg_color")
    mode = ctk.get_appearance_mode()
    if mode == "Light":
        rc = rc[0]
    else:
        rc = rc[1]

    # Create paned window
    paned = tk.PanedWindow(parent, orient="horizontal", background=rc, sashwidth=PANE_GAPS)
    paned.pack(fill="both", expand=True, padx=PANE_GAPS, pady=(0, PANE_GAPS))

    # Create panes with matching corners and preset widths
    parent.update_idletasks()
    w = paned.winfo_width()
    left = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))
    middle = CTkFrame(paned, width=w//2, background_corner_colors=(rc, rc, rc, rc))
    right = CTkFrame(paned, width=w//4, background_corner_colors=(rc, rc, rc, rc))

    # Add panes
    paned.add(left, minsize=PANE_MIN)
    paned.add(middle, minsize=PANE_MIN)
    paned.add(right, minsize=PANE_MIN)
    return left, middle, right

class form:
    #       label1  label2  
    #       entry1  entry2  button
    # 
    # 
    def double_entry(parent, text_1, text_2, button_text):
        frame = CTkFrame(parent)
        frame.pack(fill=X)
        
        label1 = CTkLabel(frame, text=text_1, font=MED_FONT)
        label1.grid(row=0, column=0, sticky="w", pady=5, padx=10)

        entry1 = CTkEntry(frame, width=50)
        entry1.grid(row=1, column=0)

        label2 = CTkLabel(frame, text=text_2, font=MED_FONT)
        label2.grid(row=0, column=2, sticky="w", pady=5, padx=10)

        entry2 = CTkEntry(frame, width=50)
        entry2.grid(row=1, column=2)

        button = CTkButton(frame, text=button_text, font=MED_FONT)
        button.grid(row=1, column=4)
        def con():
            print("button")
        button.configure(command=con)

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=0)

        return entry1, entry2, button


class tab:
    def container(parent):
        tabs = ctk.CTkTabview(parent, corner_radius=0, border_width=0)
        tabs.pack(fill="both", expand=True, padx=0, pady=0)
        tabs._segmented_button._canvas.configure(highlightthickness=0)
        tabs._segmented_button.grid(sticky="w", padx=4, pady=(2, 0))

        # Visual Studio style colors
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            bg = "#1E1E1E"
            active = "#252526"
            text = "#FFFFFF"
            inactive_text = "#AAAAAA"
        else:
            bg = "#F3F3F3"
            active = "#E7E7E7"
            text = "#000000"
            inactive_text = "#555555"

        # Configure tabview appearance
        tabs.configure(fg_color=bg, segmented_button_fg_color=bg)
        tabs._segmented_button.configure(
            fg_color=bg,
            selected_color=active,
            selected_hover_color=active,
            unselected_color=bg,
            unselected_hover_color=active,
            text_color=text,
            text_color_disabled=inactive_text,
            corner_radius=0,
        )
        return tabs
    
class tree:
    def root(parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=len(col)*8, anchor="w")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def branch():
        return
        

# Nmap button
def big_button(parent, text, function=None):
    button = CTkButton(parent, text=text, command=function, font=LARGE_FONT)
    # nmap_start_button.grid(row=1, column=1, ipadx=20, ipady=10)
    button.pack(side="top", pady=PANE_MIN, padx=PANE_MIN, fill="x")
    return button

def big_textarea(parent):
    textarea = CTkTextbox(parent, font=MONO_FONT)
    textarea.pack(side="top", pady=PANE_MIN, padx=PANE_MIN, fill=BOTH, expand=TRUE)
    return textarea

def append_text(box, text):
    box.insert(END, text+"\n")
    box.see(END)



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
    
    def zoom_pan_canvas(parent, draw_callback, framerate_ms):
        global current_scale
        current_scale = 1.0
        canvas = CTkCanvas(parent)
        canvas.pack(fill=BOTH, expand=True)


        # for i in range(20):
        #     canvas.create_oval(50+i*40, 50+i*20, 120+i*40, 120+i*20, fill="cyan")
        
        def resize(event):
            # Resize on window changes
            # w = parent.winfo_width()
            # h = parent.winfo_height()
            # canvas.config(width = w, height = h)
            draw_callback(canvas, 100, 100)
            print("config")
        parent.bind("<Configure>", resize)

        def start_pan(event):
            canvas.scan_mark(event.x, event.y)
        canvas.bind("<ButtonPress-1>", start_pan)

        def do_pan(event):
            canvas.scan_dragto(event.x, event.y, gain=1)
        canvas.bind("<B1-Motion>", do_pan)

        def zoom(event):
            global current_scale

            # Determine zoom direction
            if event.delta > 0:
                factor = 1.1
            else:
                factor = 0.9

            # Linux support
            if hasattr(event, "num"):
                if event.num == 4:
                    factor = 1.1
                elif event.num == 5:
                    factor = 0.9
            new_scale = current_scale * factor

            # Clamp scale
            # if not (0.2 <= new_scale <= 5.0):
            #     return
            current_scale = new_scale

            # Zoom around mouse
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)

            canvas.scale("all", x, y, factor, factor)
            canvas.configure(scrollregion=canvas.bbox("all"))
        # Windows / Mac
        canvas.bind("<MouseWheel>", zoom)
        # Linux
        canvas.bind("<Button-4>", zoom)
        canvas.bind("<Button-5>", zoom)

        def reset_view(event=None):
            global current_scale

            scale_factor = 1 / current_scale
            current_scale = 1.0
            canvas.scale("all", 0, 0, scale_factor, scale_factor)

            canvas.configure(scrollregion=canvas.bbox("all"))

            # Center view
            bbox = canvas.bbox("all")
            if bbox:
                x0, y0, x1, y1 = bbox
                canvas.xview_moveto((x0 + x1 - canvas.winfo_width()) / (x1 - x0))
                canvas.yview_moveto((y0 + y1 - canvas.winfo_height()) / (y1 - y0))

        canvas.bind("<Button-2>", reset_view)      # Windows/Linux
        canvas.bind("<Button-3>", reset_view)      # Mac sometimes uses Button-3

        def animation_loop(cx, cy):
            cx, cy = draw_callback(canvas, cx, cy)
            canvas.after(framerate_ms, lambda: animation_loop(cx, cy))
        animation_loop(0, 0)


class main_menu:
    def buttons_wrapper(parent):
        wrapper = CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=2, column=1)
        return wrapper

    def button(parent, text, function):
        button = CTkButton(parent, text=text, width=280, height=50, command=function, font=LARGE_FONT)
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
        