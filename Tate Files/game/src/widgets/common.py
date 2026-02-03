from customtkinter import *
import tkinter as tk
# from tkinter import ttk

class Common:

    # Styling globals
    fonts = {}
    def get_font(name="default"):
        if name not in Common.fonts:
            if name == "default":
                Common.fonts[name] = CTkFont(family="Arial", size=16)
            elif name == "subtitle":
                Common.fonts[name] = CTkFont(size=18)
            else:
                Common.fonts[name] = CTkFont(size=14)
        return Common.fonts[name]

    # if MED_FONT is None:
    #     MED_FONT = ctk.CTkFont(family="Arial", size=16)
    # if LARGE_FONT is None:
    #     LARGE_FONT = ctk.CTkFont(family="Arial", size=24)
    # if MONO_FONT is None:
    #     MONO_FONT = ctk.CTkFont(family="Courier", size=14)
    #     return Common.fonts[name]

    GAP = 10
    PANE_MIN = GAP*4

    # Menu bar widgets
    def menu_bar(parent, title):
        med = Common.get_font()
        menu_bar = CTkFrame(parent)
        menu_bar.pack(side="top", padx=Common.GAP, pady=(Common.GAP, 0), fill="x", anchor="n")
        game_label = CTkLabel(master = menu_bar, text=title, font=med)
        game_label.pack(side="left", padx=Common.GAP, pady=(Common.GAP, 0))
        return menu_bar

    def menu_bar_button(parent, text, function):
        med = Common.get_font()
        button = CTkButton(parent, text=text, command=function, font=med)
        button.pack(side="right", padx=Common.GAP, pady=Common.GAP)

    # Layout frames
    def trifold(parent):

        # Get root color
        root_color = parent.cget("fg_color")
        mode = get_appearance_mode()
        if mode == "Light":
            root_color = root_color[0]
        else:
            root_color = root_color[1]

        # Create paned window
        paned = tk.PanedWindow(parent, orient="horizontal", background=root_color, sashwidth=Common.GAP)
        paned.pack(fill="both", expand=True, padx=Common.GAP, pady=Common.GAP)

        # Create panes with matching corners and preset widths
        parent.update_idletasks()
        w = paned.winfo_width()
        left = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))
        middle = CTkFrame(paned, width=w//2, background_corner_colors=(root_color, root_color, root_color, root_color))
        right = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))

        # Add panes
        paned.add(left, minsize=Common.PANE_MIN)
        paned.add(middle, minsize=Common.PANE_MIN)
        paned.add(right, minsize=Common.PANE_MIN)
        return left, middle, right




# DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")
   




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
    button.pack(side="top", pady=Common.PANE_MIN, padx=Common.PANE_MIN, fill="x")
    return button

def big_textarea(parent):
    textarea = CTkTextbox(parent, font=MONO_FONT)
    textarea.pack(side="top", pady=Common.PANE_MIN, padx=Common.PANE_MIN, fill=BOTH, expand=TRUE)
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
        