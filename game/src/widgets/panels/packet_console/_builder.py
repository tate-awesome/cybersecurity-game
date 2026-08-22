from .filter_overlay import FilterOverlay
from .treeview import PacketTreeview
from ....app_core import Context
from ... import MenuBar, CheckboxOverlay
from ..panel import Panel
from customtkinter import CTkFrame
from ....network.buffer.meta_packet import MetaPacket

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "packet_console")

        self.buffer = context.net.buffer.packets
        #  self.create_filter_boxes(menu_frame)

        self.treeview = PacketTreeview(self, context)
        self.refresh_columns()
        self.treeview.bind_select(self.on_select)


        filter_button = self.menu_bar.add_button("filters_overlay")
        self.filter_overlay = FilterOverlay(filter_button, context, self.apply_filters)
        self.filter_overlay.compile_filter()

        columns_button = self.menu_bar.add_button("columns_overlay")
        columns_overlay = CheckboxOverlay(columns_button, context, self.refresh_columns, "packet_columns", "Show Columns")

        # jump_button = self.menu_bar.reversible_button(
        #     self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")
        pause_button = self.menu_bar.reversible_button(self.pause, self.unpause, "pause", "unpause")
        minimize_button = self.menu_bar.minimize_button(self.treeview.frame, master)

        def reset_capture():
            self.context.net.buffer.reset()
            self.clear_tree()

        reset_button = self.menu_bar.add_button("clear_packets_button", reset_capture)

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
            self.submit_packet(packet)

        max_rows = 1000
        overflow_count = self.treeview.count() - max_rows

        if overflow_count > 0:
            self.treeview.trim_oldest(overflow_count)

        # Auto scroll
        if self.jump_to_bottom:
            self.treeview.scroll_to_bottom()

    def apply_filters(self):
        self.buffer.reset_packet_cursor()
        self.treeview.clear()

    # Treeview
    def submit_packet(self, packet: MetaPacket):
        values = [packet.get_column_value(col) for col in self.treeview.columns]
        self.treeview.submit(str(packet.get("number")), values)

    def refresh_columns(self):

        active_columns = []

        for key in self.context.states.get("packet_columns"):

            if self.context.states.get("packet_columns", key) == "1" or self.context.states.get("packet_columns", key) == 1:
                active_columns.append(key)

        self.treeview.set_visible_columns(active_columns)

    def clear_tree(self):
        self.treeview.clear()

    # Selection
    def on_select(self, event=None):
        selection = self.treeview.selection()
        if not selection:
            return
        self.buffer.select(int(selection[0]))

    def select_child(self, index=-1):
        self.treeview.select_last()

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