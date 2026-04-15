from customtkinter import *

from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from .filter_overlay import FilterOverlay
from .column_overlay import ColumnOverlay
import tkinter as tk
from tkinter import ttk

class PacketConsole:
    def __init__(self, style, parent, context, buffer: DataBuffer):
        self.context = context
        self.style = style
        self.buffer = buffer

        menu_frame = self.create_menu_bar(parent)
        #  self.create_filter_boxes(menu_frame)

        jump_button = self.create_menu_button(menu_frame, "Unlock Scrolling")
        self.configure_reversible_button(jump_button, self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")

        filter_button = self.create_menu_button(menu_frame, "Filters")
        filter_overlay = FilterOverlay(self.context, self.style, filter_button, buffer, self.refresh)

        columns_button = self.create_menu_button(menu_frame, "Columns")
        columns_button = ColumnOverlay(self.context, self.style, columns_button, buffer, self.refresh)

        self.columns = []
        self.treeview = self.create_treeview(parent)

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Start printing loop
        self.start_printing()
        

    def start_printing(self):
        print("start")
        self.run = True
        self.print_tick()
    
    def stop_printing(self):
        print("stop")
        self.run = False
        if self.after_id:
            self.text_box.after_cancel(self.after_id)
            self.after_id = None

    def print_tick(self):
        flag = True
        while flag:
            # Filter
            packet = self.buffer.pop_packet(self.context.inputs["packet_filter_function"]["function"])
            if packet is None:
                flag = False
                continue
            # Submit packet to treeview
            self.submit_packet(self.treeview, packet)
            # Limit rows
            max_rows = 1000
            children = self.treeview.get_children()
            if len(children) > max_rows:
                self.treeview.delete(children[0])
        # Auto scroll
        if self.jump_to_bottom:
            self.treeview.yview_moveto(1)
        if self.run:
            self.after_id = self.treeview.after(100, self.print_tick)

    # Treeview
    def create_treeview(self, parent):
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)
        active_columns = []
        for key in self.context.inputs["column_selections"]:
            if self.context.inputs["column_selections"][key]["state"] == "1":
                active_columns.append(key)
        tree = ttk.Treeview(parent, columns=active_columns, show="headings")
        tree.pack(fill="both", expand=True, padx=self.style.gap, pady=self.style.gap)
        for col in active_columns:
            tree.heading(col, text=col)
            tree.column(col, width=len(col)*8, anchor="w")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.columns = active_columns
        return tree
    
    def submit_packet(self, tree, packet):
        values = []

        for col in self.columns:
            value = self.context.inputs["column_selections"][col]["function"](packet)
            values.append(value)

        tree.insert("", "end", values=values)

    def refresh(self):
        ...

    # Buttons
    def pause(self):
        self.stop_printing()

    def unpause(self):
        self.start_printing()
    
    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True

    # Menu Bar

    def create_menu_bar(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", pady=self.style.gaptop, padx=self.style.gap)

        header = CTkLabel(frame, text="Packet Stream", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    def configure_reversible_button(self, the_button: CTkButton, start_func: callable, stop_func: callable, inactive_name: str, active_name: str):
        def stop():
            stop_func()
            the_button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            the_button.configure(command=stop, text=active_name)
        the_button.configure(command=start, text=inactive_name)