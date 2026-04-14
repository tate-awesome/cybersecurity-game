from ...app_core.context import Context
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from .packet_console import PacketConsole
from .status_console import StatusConsole
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
        
        top, bottom = self.create_paned_window(self.frame)
        packet_console = PacketConsole(style, top, context, buffer)
        status_console = StatusConsole(style, bottom, context, buffer)
    
    # PanedWindow
    def create_paned_window(self, parent: CTkFrame):

        # Console bifold
        rc = self.style.color("root")

        # Create paned window
        paned = tk.PanedWindow(parent, orient="vertical", background=rc, sashwidth=self.style.igap)
        paned.pack(side="top", fill="both", expand=True)

        # Create panes with matching corners and preset widths
        self.context.root.update_idletasks()
        h = paned.winfo_height()
        top = CTkFrame(paned, height=h//2, background_corner_colors=(rc, rc, rc, rc))
        bottom = CTkFrame(paned, height=h//2, background_corner_colors=(rc, rc, rc, rc))

        # Add panes
        paned.add(top, minsize=110)
        paned.add(bottom, minsize=110)
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