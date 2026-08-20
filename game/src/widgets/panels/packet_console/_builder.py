from customtkinter import *

from .filter_overlay import FilterOverlay
from .column_overlay import ColumnOverlay
from ....app_core import Context
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from ... import MenuBar
from ..panel import Panel
from customtkinter import CTkFrame
from ....network.buffer.meta_packet import MetaPacket

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "packet_console")

        self.buffer = context.net.buffer.packets
        #  self.create_filter_boxes(menu_frame)

        self.treeview, body_container = self.create_treeview(self)
        self.refresh_columns()
        self.treeview.bind("<<TreeviewSelect>>", self.on_select)


        filter_button = self.menu_bar.add_button("filters_overlay")
        self.filter_overlay = FilterOverlay(filter_button, context, self.apply_filters)
        self.filter_overlay.compile_filter()

        columns_button = self.menu_bar.add_button("columns_overlay")
        columns_overlay = ColumnOverlay(columns_button, context, self.refresh_columns)

        # jump_button = self.menu_bar.reversible_button(
        #     self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")
        pause_button = self.menu_bar.reversible_button(self.pause, self.unpause, "pause", "unpause")
        minimize_button = self.menu_bar.minimize_button(body_container, master)

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Reset print pointer on refresh
        self.buffer.reset_packet_cursor()

        # Start printing loop
        self.start_printing()
        

    def start_printing(self):
        self.run = True
        self.context.animation_manager.add_callback("packet_console", self.print_tick)
    
    def stop_printing(self):
        self.run = False
        self.context.animation_manager.remove_callback("packet_console")

    def print_tick(self):

        # Get new packets
        packets = self.buffer.get_new_packets(self.filter_overlay.function, max_return=1000)
        if not packets:
            return

        # Submit to treeview
        for packet in packets:
            self.submit_packet(self.treeview, packet)

        children = self.treeview.get_children()
        max_rows = 1000
        overflow_count = len(children) - max_rows
        
        if overflow_count > 0:
            # Delete the block slice of old items simultaneously
            for i in range(overflow_count):
                self.treeview.delete(children[i])
    
        # Auto scroll
        if self.jump_to_bottom:
            self.treeview.yview_moveto(1)
    
    def apply_filters(self):
        self.buffer.reset_packet_cursor()
        self.treeview.delete(*self.treeview.get_children())

    # Treeview
    def create_treeview(self, parent):

        # Styling options
        style = ttk.Style()
        style.theme_use('clam')
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe', 'border': '0'})
        ])
        style.configure("TFrame", borderwidth=0, relief="flat")
        tree_font = tkfont.Font(
            family="Consolas",
            size=self.style.get_font_size("treeview")
        )
        row_height = tree_font.metrics("linespace") * 2 + 6
        
        # 1. Treeview Body & Empty Rows Area
        style.configure(
            "Treeview",
            font=("Consolas", self.style.get_font_size("treeview"), "normal"),
            rowheight=row_height,
            background=self.style.color("field"),
            fieldbackground=self.style.color("field"),
            foreground=self.style.color("field_text"),
            borderwidth=0,
            relief="flat"
        )
        # Highlight colors when a cell/row is selected
        style.map(
            "Treeview",
            background=[("selected", self.style.color("accent"))],
            foreground=[("selected", self.style.color("field_text"))]
        )

        # 2. Table Headers Style
        style.configure(
            "Treeview.Heading",
            font=("Consolas", self.style.get_font_size("treeview"), "bold"),
            background=self.style.color("widget"),      # Contrasted panel color for headers
            foreground=self.style.color("field_text"),
            borderwidth=1,
            relief="flat"
        )
        style.map(
            "Treeview.Heading",
            background=[("active", self.style.color("accent"))],    # Accent color on hover
            foreground=[("active", self.style.color("field_text"))] # Text stays readable
        )

        # 3. Layout Container Frame Style
        style.configure(
            "TFrame",
            background=self.style.color("panel")  # Blends frame container with parent view
        )

        # 4. Scrollbar Track and Slider Elements
        style.configure(
            "TScrollbar",
            gripcount=0,
            background=self.style.color("scrollbar"),      # The slider handle color
            troughcolor=self.style.color("panel"),      # The tracking channel backdrop
            bordercolor=self.style.color("panel"),      # Outer slider thin border line
            arrowcolor=self.style.color("field_text"),  # Tiny arrow icons on cap ends
            lightcolor=self.style.color("panel"),       # Eliminates default 3D highlights
            darkcolor=self.style.color("panel"),
            borderwidth=0,
            thickness=self.style.get_scrollbar_size(),
            arrowsize=self.style.get_scrollbar_size()
        )
        style.map(
            "TScrollbar",
            background=[("active", self.style.color("scrollbar_hover"))] # Hover slider color shifts to accent
        )

        # Container for tree and scrollbars (Now safely targeted by TFrame styles)
        container = ttk.Frame(parent)
        container.pack(
            padx=self.style.pad_corrected(),  # Matches CustomTkinter's standard frame padding layout
            pady=self.style.pad_corrected(),
            fill="both",
            expand=True
        )

        # Columns
        all_columns = list(self.context.labels.get("packet_columns").keys())

        # Treeview
        tree = ttk.Treeview(
            container,
            columns=all_columns,
            show="headings"
        )

        # TODO tune scrolling on all platforms
        def custom_scroll_handler(event):
            # Determine if Shift key is actively held down
            # State 1 = Shift, 9 = Shift + NumLock, 17 = Shift + CapsLock, etc.
            is_shift = bool(event.state & 0x0001)
            
            # Select the target view method based on Shift state
            scroll_method = treeview.xview_scroll if is_shift else treeview.yview_scroll

            if sys.platform == "win32":
                # Windows sends multiples of 120. Normalize to standard steps.
                steps = -1 * int(event.delta / 120) * multiplier
                scroll_method(steps, "units")
                
            elif sys.platform == "darwin":
                # macOS tracks small acceleration changes.
                steps = -1 * event.delta * multiplier
                scroll_method(steps, "units")
                
            elif sys.platform == "linux":
                # Linux maps Shift + Scroll to separate discrete events (<Shift-Button-4/5>).
                # If those events fire, event.num tells us the direction.
                if event.num in (4, 6):    # Scroll Up / Scroll Left
                    scroll_method(-1 * multiplier, "units")
                elif event.num in (5, 7):  # Scroll Down / Scroll Right
                    scroll_method(1 * multiplier, "units")
                    
            # Block default system Tkinter behaviors from running
            return "break"

        # Configure columns
        for col in all_columns:

            stretch = (col == "Info")

            tree.heading(col, text=self.context.labels.get("packet_columns", col))

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
    
    def submit_packet(self, tree: ttk.Treeview, packet: MetaPacket):
        values = [packet.get_column_value(col) for col in self.columns]
        
        try:
            new_val = float(values[0])
        except (ValueError, TypeError):
            new_val = values[0]  # Fallback to string if non-numeric

        children = tree.get_children("")
        insert_index = "end"

        # Search from the bottom up (since packets usually arrive sequentially)
        for child in reversed(children):
            current_val_str = tree.set(child, self.columns[0])
            
            try:
                current_val = float(current_val_str)
            except (ValueError, TypeError):
                current_val = current_val_str

            # If the existing row is smaller than or equal to our new packet,
            # it means our packet belongs right AFTER this row.
            if current_val <= new_val:
                # Get the top-down index of this child and add 1 to place it below
                insert_index = tree.index(child) + 1
                break
        
        # If all items in the tree are larger than new_val, 
        # the loop finishes without breaking, insert_index stays "end" 
        # (or you could force it to 0 if it belongs at the very top).

        tree.insert("", insert_index, values=values, iid=str(packet.get("number")))

    def refresh_columns(self):

        active_columns = []

        for key in self.context.states.get("packet_columns"):

            if self.context.states.get("packet_columns", key) == "1" or self.context.states.get("packet_columns", key) == 1:
                active_columns.append(key)

        self.treeview["displaycolumns"] = active_columns

    # Selection
    def on_select(self, event=None):
        selection = self.treeview.selection()
        if not selection:
            return
        self.buffer.select(int(selection[0]))

    def select_child(self, index=-1):

        children = self.treeview.get_children("")
        if children:
            self.treeview.selection_set(children[-1])
            self.treeview.see(children[-1])

    # Buttons
    def pause(self):
        self.stop_printing()
        self.select_child()
        self.context.states.set("packet_console_state", "mode", value="paused")

    def unpause(self):
        self.start_printing()
        self.context.states.set("packet_console_state", "mode", value="live")

    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True