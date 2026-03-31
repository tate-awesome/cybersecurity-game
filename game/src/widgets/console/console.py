from ...app_core.context import Context
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from .packet_console import PacketConsole
from .status_console import StatusConsole
from .filter_overlay import FilterOverlay
from customtkinter import *
from tkinter import ttk
import tkinter as tk

class Console:
    '''
    Wireshark-like treeview output for different hacks
    '''

    def __init__(self, style, parent, context: Context, buffer: DataBuffer):
        self.context = context
        self.style = style
        self.frame = parent
        self.buffer = buffer
        self.filter_func = lambda mpkt: True

        parent.configure(fg_color=style.color("root"))

        menu_frame = self.create_menu_frame(self.frame)
        refresh_button = self.create_menu_button(menu_frame, "Refresh")
        filter_button = self.create_menu_button(menu_frame, "Filters")
        filter_overlay = FilterOverlay(self.context, self.style, filter_button)
        
        top, bottom = self.create_paned_window(self.frame)
        packet_console = PacketConsole(style, top, context, buffer)
        status_console = StatusConsole(style, bottom, context, buffer)

    # Menu
    def create_menu_frame(self, parent):
        menu_frame = CTkFrame(parent)
        menu_frame.pack(side="top", fill="x")
        return menu_frame
    
    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="left", padx=self.style.gap, pady=self.style.gap)
        return button
    
    # PanedWindow
    def create_paned_window(self, parent: CTkFrame):

        # Console bifold
        rc = self.style.color("root")

        # Create paned window
        paned = tk.PanedWindow(parent, orient="vertical", background=rc, sashwidth=self.style.igap)
        paned.pack(side="top", fill="both", expand=True, pady=self.style.gaptop)

        # Create panes with matching corners and preset widths
        h = paned.winfo_height()
        top = CTkFrame(paned, height=400, background_corner_colors=(rc, rc, rc, rc))
        bottom = CTkFrame(paned, height=400, background_corner_colors=(rc, rc, rc, rc))

        # Add panes
        paned.add(top, minsize=self.style.PANE_MIN)
        paned.add(bottom, minsize=self.style.PANE_MIN)
        return top, bottom

    def menu_dropdown(self, frame, options: list[str], function):
        med = self.style.get_font()
        dropdown = CTkOptionMenu(
            frame,
            values=options,
            command=function,
            font=med,
            dropdown_font=med
        )
        dropdown.pack(side="left", padx=self.style.gap, pady=self.style.gap, fill="y")
        dropdown.set("None")
        return dropdown
    
    
    

    # ------------------------------------



    def show_stream(self, source: str):
        print(source)

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

    def build_frame(self, parent):
        frame = CTkFrame(parent)
        frame.pack(fill="both", expand=True)
        return frame

    def build_tab(self, hack: str):

        if hack in self.tabs:
            return  # already exists

        tab = self.tabview.add(hack)

        textbox = CTkTextbox(
            tab,
            wrap="none",
            state="disabled"
        )
        textbox.pack(fill="both", expand=True)

        self.tabs[hack] = textbox

        # Load previous console history if exists
        for entry in self.context.consoles[hack]:
            if isinstance(entry, str):
                self._append_text(hack, entry)
            else:
                self._append_packet(hack, entry)

    def submit_line(self, hack: str, line: str):

        if hack not in self.tabs:
            self.build_tab(hack)

        self.context.consoles[hack].append(line)
        self._append_text(hack, line)

    def submit_packet(self, hack: str, mpkt: MetaPacket):

        if hack not in self.tabs:
            self.build_tab(hack)

        self.context.consoles[hack].append(mpkt)
        self._append_packet(hack, mpkt)

    def _append_text(self, hack, line):
        textbox = self.tabs[hack]
        textbox.configure(state="normal")
        textbox.insert("end", line + "\n")
        textbox.see("end")
        textbox.configure(state="disabled")

    def _append_packet(self, hack, mpkt: MetaPacket):
        textbox = self.tabs[hack]

        formatted = (
            f"[{mpkt.number}] "
            f"{mpkt.direction.upper()} "
            f"{mpkt.pkt.summary()} "
            f"{mpkt.variable}={mpkt.value}"
        )

        textbox.configure(state="normal")
        textbox.insert("end", formatted + "\n")
        textbox.see("end")
        textbox.configure(state="disabled")