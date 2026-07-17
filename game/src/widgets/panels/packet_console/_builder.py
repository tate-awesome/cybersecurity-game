from customtkinter import *

from ....network.meta_packet import MetaPacket
from ....network.data_buffer import DataBuffer
from .filter_overlay import FilterOverlay
from .column_overlay import ColumnOverlay
from ....app_core.context import Context
from typing import cast
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from ... import MenuBar
from ..panel import Panel
from customtkinter import CTkFrame

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "Packet Console")

        self.buffer = cast(DataBuffer, context.net.data_buffer)
        #  self.create_filter_boxes(menu_frame)

        self.treeview, body_container = self.create_treeview(self)
        self.refresh_columns()

        minimize_button = self.menu_bar.minimize_button(body_container, master)

        jump_button = self.menu_bar.reversible_button(
            self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")

        filter_button = self.menu_bar.add_button("Filters")
        filter_overlay = FilterOverlay(filter_button, context, self.apply_filters)

        columns_button = self.menu_bar.add_button("Columns")
        columns_overlay = ColumnOverlay(columns_button, context, self.refresh_columns)

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Reset print pointer on refresh
        self.buffer.reset_packet_cursor()

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
        # self.buffer.reset_packet_cursor()
        # self.treeview.delete(*self.treeview.get_children())
        if isinstance(self.context.states["packet_filter_function"]["function"], str):
            self.context.states["packet_filter_function"]["function"] = eval(self.context.states["packet_filter_function"]["function"])
        packets = self.buffer.get_new_packets(self.context.states["packet_filter_function"]["function"])
        if len(packets) == 0:
            # Don't print
            ...
        else:
            # Do print
            for packet in packets:
                self.submit_packet(self.treeview, packet)
            max_rows = 1000
            while len(self.treeview.get_children()) > max_rows:
                    self.treeview.delete(self.treeview.get_children()[0])
        
            # Auto scroll
            if self.jump_to_bottom:
                self.treeview.yview_moveto(1)
        if self.run:
            self.after_id = self.treeview.after(100, self.print_tick)
    
    def apply_filters(self):
        self.buffer.reset_packet_cursor()
        self.treeview.delete(*self.treeview.get_children())

    # Treeview
    def create_treeview(self, parent):

        # Styling options
        style = ttk.Style()
        tree_font = tkfont.Font(
            family="Consolas",
            size=self.style.get_font_size("treeview")
        )
        row_height = tree_font.metrics("linespace") * 2 + 6
        style.configure(
            "Treeview",
            font=("Consolas", self.style.get_font_size("treeview"), "normal"),
            rowheight=row_height
        )
        style.configure(
            "Treeview.Heading",
            font=("Consolas", self.style.get_font_size("treeview"), "bold")
        )

        # Container for tree and scrollbars
        container = ttk.Frame(parent)
        container.pack(**self.style.packing())

        # Columns
        all_columns = list(self.context.labels["packet_columns"].keys())

        # Treeview
        tree = ttk.Treeview(
            container,
            columns=all_columns,
            show="headings"
        )

        # Configure columns
        for col in all_columns:

            stretch = (col == "Info")

            tree.heading(col, text=self.context.labels["packet_columns"][col])

            tree.column(
                col,
                width=self.style.get_column_width(col),
                minwidth=50,
                stretch=stretch,
                anchor="w"
            )

        # Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=tree.yview
        )

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(
            container,
            orient="horizontal",
            command=tree.xview
        )

        # Connect scrollbars
        tree.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Layout
        tree.grid(row=0, column=0, sticky="nsew")

        y_scrollbar.grid(row=0, column=1, sticky="ns")

        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Make tree expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.columns = all_columns

        return tree, container
    
    def submit_packet(self, tree, packet):
        values = []

        for col in self.columns:
            value = packet.get_column_value(col)
            values.append(value)

        tree.insert("", "end", values=values)

    def refresh_columns(self):

        active_columns = []

        for key in self.context.states["packet_columns"]:

            if self.context.states["packet_columns"][key] == "1" or self.context.states["packet_columns"][key] == 1:
                active_columns.append(key)

        self.treeview["displaycolumns"] = active_columns

    # Buttons
    def pause(self):
        self.stop_printing()

    def unpause(self):
        self.start_printing()
    
    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True