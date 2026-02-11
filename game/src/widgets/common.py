from customtkinter import *
import tkinter as tk
# from tkinter import ttk


class Common:

    def __init__(self, ui_scale=100.0):
        self.scale = ui_scale

        self.fonts = {}
        self.GAP = 10
        self.PANE_MIN = self.GAP*4

    def get_font(self, name="default"):
        if name not in self.fonts:
            if name == "default":
                size = int(16.0*self.scale/100.0)
                self.fonts[name] = CTkFont(family="Arial", size=size)
            elif name == "subtitle":
                size=int(18.0*self.scale/100.0)
                self.fonts[name] = CTkFont(size=size)
            else:
                size = int(14.0*self.scale/100.0)
                self.fonts[name] = CTkFont(size=size)
        return self.fonts[name]

# DATA_FONT = CTkFont(family="Courier", size=16)
# HEADER_FONT = CTkFont(family="Arial", size=24)
# TITLE_FONT = CTkFont(family="Arial", size=max(32, root.winfo_height()//5), weight="bold")

    # Menu bar widgets
    def menu_bar(self, parent, title):
        med = self.get_font()
        menu_bar = CTkFrame(parent)
        menu_bar.pack(side="top", padx=self.GAP, pady=(self.GAP, 0), fill="x", anchor="n")
        game_label = CTkLabel(master = menu_bar, text=title, font=med)
        game_label.pack(fill=Y, side="left", padx=self.GAP)
        return menu_bar

    def menu_bar_button(self, parent, text, function=None):
        med = self.get_font()
        button = CTkButton(parent, text=text, command=function, font=med)
        button.pack(side="right", padx=self.GAP, pady=self.GAP)
        return button

    # Layout frames
    def trifold(self, parent):

        # Get root color
        root_color = parent.cget("fg_color")
        print(root_color)
        mode = get_appearance_mode()
        if mode == "Light":
            root_color = root_color[0]
        else:
            root_color = root_color[1]

        # Create paned window
        paned = tk.PanedWindow(parent, orient="horizontal", background=root_color, sashwidth=self.GAP)
        paned.pack(fill="both", expand=True, padx=self.GAP, pady=self.GAP)

        # Create panes with matching corners and preset widths
        parent.update_idletasks()
        w = paned.winfo_width()
        left = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))
        middle = CTkFrame(paned, width=w//2, background_corner_colors=(root_color, root_color, root_color, root_color))
        right = CTkFrame(paned, width=w//4, background_corner_colors=(root_color, root_color, root_color, root_color))

        # Add panes
        paned.add(left, minsize=self.PANE_MIN)
        paned.add(middle, minsize=self.PANE_MIN)
        paned.add(right, minsize=self.PANE_MIN)
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

    #       label1  label2  
    #       entry1  entry2  button
    # 
    # 
    def form_mult_offset(self, parent, text_1, text_2, button_text):
        frame = CTkFrame(parent)
        frame.pack(fill=X)
        
        label1 = CTkLabel(frame, text=text_1, font=self.get_font())
        label1.grid(row=0, column=0, sticky="w", pady=5, padx=10)

        entry1 = CTkEntry(frame, width=50)
        entry1.grid(row=1, column=0)

        label2 = CTkLabel(frame, text=text_2, font=self.get_font())
        label2.grid(row=0, column=2, sticky="w", pady=5, padx=10)

        entry2 = CTkEntry(frame, width=50)
        entry2.grid(row=1, column=2)

        button = CTkButton(frame, text=button_text, font=self.get_font())
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

    def form_arp_spoofing(self, parent):

        ip_frame = CTkFrame(parent)
        ip_frame.pack(side="top", fill="x", expand=False, padx=self.GAP, pady=(self.GAP, 0))
        ip_frame.columnconfigure(0, weight=0)
        ip_frame.columnconfigure(1, weight=1)
        ip_frame.columnconfigure(2, weight=0)

        ip_frame_header = CTkLabel(ip_frame, text="ARP Spoofing", font=self.get_font())
        ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(self.GAP,0))

        system_ip_label = CTkLabel(ip_frame, text="System IP:", font=self.get_font())
        system_ip_label.grid(row=1, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)
        system_ip_input = CTkEntry(ip_frame, font=self.get_font())
        system_ip_input.grid(row=1, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        controller_ip_label = CTkLabel(ip_frame, text="Controller IP:", font=self.get_font())
        controller_ip_label.grid(row=2, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)
        controller_ip_input = CTkEntry(ip_frame, font=self.get_font())
        controller_ip_input.grid(row=2, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        network_sniffing_btn = CTkButton(ip_frame, text="Start ARP Spoof", font=self.get_font(), command=None)
        network_sniffing_btn.grid(row=3, column=2, sticky="e", pady=self.GAP, padx=self.GAP)
        
    def form_nmap(self, parent):
        ip_frame = CTkFrame(parent)
        ip_frame.pack(side="top", fill="x", expand=False, padx=self.GAP, pady=(self.GAP, 0))
        ip_frame.columnconfigure(0, weight=0)
        ip_frame.columnconfigure(1, weight=1)
        ip_frame.columnconfigure(2, weight=0)

        ip_frame_header = CTkLabel(ip_frame, text="NMapping", font=self.get_font())
        ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(self.GAP,0))

        ip_label = CTkLabel(ip_frame, text="Your IP:", font=self.get_font())
        ip_label.grid(row=1, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)

        ip_input = CTkEntry(ip_frame, font=self.get_font())
        ip_input.grid(row=1, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        network_sniffing_btn = CTkButton(ip_frame, text="Map Network", font=self.get_font(), command=None)
        network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=self.GAP, padx=self.GAP)

        return

    def form_sniff(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=self.GAP, pady=(self.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)

        label = CTkLabel(frame, text="Traffic Sniffing", font=self.get_font())
        label.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(self.GAP,0))

        e_label = CTkLabel(frame, text="IP Address:", font=self.get_font())
        e_label.grid(row=1, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)

        entry = CTkEntry(frame, font=self.get_font())
        entry.grid(row=1, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        e_label2 = CTkLabel(frame, text="IP Address:", font=self.get_font())
        e_label2.grid(row=2, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)

        entry2 = CTkEntry(frame, font=self.get_font())
        entry2.grid(row=2, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        button = CTkButton(frame, text="Start sniffing", font=self.get_font(), command=None)
        button.grid(row=3, column=2, sticky="e", pady=self.GAP, padx=self.GAP)

        return

    def form_dos(self, parent):
        ip_frame = CTkFrame(parent)
        ip_frame.pack(side="top", fill="x", expand=False, padx=self.GAP, pady=(self.GAP, 0))
        ip_frame.columnconfigure(0, weight=0)
        ip_frame.columnconfigure(1, weight=1)
        ip_frame.columnconfigure(2, weight=0)

        ip_frame_header = CTkLabel(ip_frame, text="Denial of Service", font=self.get_font())
        ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(self.GAP,0))

        ip_label = CTkLabel(ip_frame, text="Packets per second:", font=self.get_font())
        ip_label.grid(row=1, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)

        ip_input = CTkEntry(ip_frame, font=self.get_font())
        ip_input.grid(row=1, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        network_sniffing_btn = CTkButton(ip_frame, text="Start DoS", font=self.get_font(), command=None)
        network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=self.GAP, padx=self.GAP)

        return

    def form_mitm(self, parent):
        ip_frame = CTkFrame(parent)
        ip_frame.pack(side="top", fill="x", expand=False, padx=self.GAP, pady=(self.GAP, 0))
        ip_frame.columnconfigure(0, weight=0)
        ip_frame.columnconfigure(1, weight=1)
        ip_frame.columnconfigure(2, weight=0)

        ip_frame_header = CTkLabel(ip_frame, text="Denial of Service", font=self.get_font())
        ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(self.GAP,0))

        ip_label = CTkLabel(ip_frame, text="Packets per second:", font=self.get_font())
        ip_label.grid(row=1, column=1, sticky="w", pady=(self.GAP,0), padx=self.GAP)

        ip_input = CTkEntry(ip_frame, font=self.get_font())
        ip_input.grid(row=1, column=2, sticky="e", pady=(self.GAP,0), padx=self.GAP)

        network_sniffing_btn = CTkButton(ip_frame, text="Start DoS", font=self.get_font(), command=None)
        network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=self.GAP, padx=self.GAP)

        return

    def map_frame(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill=BOTH, expand=TRUE, pady=(self.GAP, 0), padx=self.GAP)
        return frame       

    def open_popup(self, master, message):
        popup = self.ctk.CTkToplevel(master)
        popup.title("Help")
        popup.config(padx=10, pady=7)

        # Center to app
        width = 500
        height = 300
        root_x = master.winfo_rootx()
        root_y = master.winfo_rooty()
        win_x = root_x + master.winfo_width()/2 - width/2
        win_y = root_y + master.winfo_height()/2 - height/2

        popup.geometry(f"{width}x{height}+{int(win_x)}+{int(win_y)}")

        # Geometry

        # Add widgets to the popup
        frame = CTkFrame(popup)
        frame.pack(fill="both", side="top", padx=10, pady=7)

        label = CTkLabel(frame, text=message, font=self.MED_FONT)
        label.pack(pady=20, padx=10)

        close_button = CTkButton(frame, text="Dismiss", command=popup.destroy, font=self.MED_FONT)
        close_button.pack(pady=10, side="bottom")

        popup.grab_set()      # block interactions with main window
        popup.focus_force()   # force focus to the popup


    def buttons_wrapper(parent):
        wrapper = CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=2, column=1)
        return wrapper

    def button(self, parent, text, function):
        button = CTkButton(parent, text=text, width=280, height=50, command=function, font=self.LARGE_FONT)
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