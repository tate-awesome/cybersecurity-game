from .treeview import PacketTreeview
from ....app_core import Context
from ...frame_widgets.important_buttons import (ChooseShownPacketConsoleColumns, ClearAllCapturedBufferData,
                                                 FilterPacketConsole, PausePacketConsole)
from ...frame_widgets.important_buttons.filter_packet_console.filter_overlay import compile_packet_filter
from ..panel import Panel
from PySide6.QtWidgets import QWidget
from ....network.buffer.meta_packet import MetaPacket

class Builder(Panel):
    KEY = "packet_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "packet_columns",
        "packet_console",
        "packet_filter_categories",
        "packet_filter_checkboxes",
        "packet_filter_entries",
        "requested_packet_treeview_clear",
    )
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.packets
        #  self.create_filter_boxes(menu_frame)

        self.treeview = PacketTreeview(self, context)
        self.shown_columns = None  # packet_columns as of the last refresh_columns
        self.refresh_columns()
        self.treeview.bind_select(self.on_select)

        self.menu_bar.add_important(FilterPacketConsole)
        self.menu_bar.add_important(ChooseShownPacketConsoleColumns)
        self.menu_bar.add_important(PausePacketConsole)
        minimize_button = self.menu_bar.minimize_button(self.treeview.frame, master)
        self.menu_bar.add_important(ClearAllCapturedBufferData)

        # Printing Flags
        self.jump_to_bottom = True
        self.paused = False  # whether print_tick last saw packet_console "mode" as "paused"

        # Reset print pointer on refresh
        self.buffer.reset_packet_cursor()

        # Start printing loop
        self.context.animation_manager.add_callback(f"packet_panel_{id(self)}", self.print_tick)

    def print_tick(self):
        '''
        Called every frame: follows packet_columns, then - unless packet_console
        "mode" is "paused" (see PausePacketConsole) - adds packets that arrived
        since the last tick and pass the current filter (see FilterPacketConsole).
        '''
        self.refresh_columns()

        if self.context.states.get("packet_console", "mode") == "paused":
            if not self.paused:
                self.paused = True
                self.select_child()
            return
        self.paused = False

        # Get new packets
        packets = self.buffer.get_new_packets(compile_packet_filter(self.context), max_return=1000)
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

    # Treeview
    def submit_packet(self, packet: MetaPacket):
        values = [packet.get_column_value(col) for col in self.treeview.columns]
        self.treeview.submit(str(packet.get("number")), values)

    def refresh_columns(self):
        '''Shows the columns ticked in packet_columns - only acts when that changed.'''
        shown = dict(self.context.states.get("packet_columns"))
        if shown == self.shown_columns:
            return
        self.shown_columns = shown

        active_columns = []

        for key in shown:

            if self.context.states.get("packet_columns", key) == "1" or self.context.states.get("packet_columns", key) == 1:
                active_columns.append(key)

        self.treeview.set_visible_columns(active_columns)

    # Selection
    def on_select(self, event=None):
        selection = self.treeview.selection()
        if not selection:
            return
        self.buffer.select(int(selection[0]))

    def select_child(self, index=-1):
        self.treeview.select_last()

    # Scrolling
    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True