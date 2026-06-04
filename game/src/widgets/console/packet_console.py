from customtkinter import *

from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from .filter_overlay import FilterOverlay
from .column_overlay import ColumnOverlay
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

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
        filter_overlay = FilterOverlay(self.context, self.style, filter_button, buffer, self.apply_filters)

        columns_button = self.create_menu_button(menu_frame, "Columns")
        columns_button = ColumnOverlay(self.context, self.style, columns_button, buffer, self.refresh_columns)

        self.treeview = self.create_treeview(parent)
        self.refresh_columns()

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
        container.pack(
            fill="both",
            expand=True,
            padx=self.style.gap,
            pady=self.style.gap
        )

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

        return tree
    
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