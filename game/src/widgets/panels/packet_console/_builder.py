from .treeview import PacketTreeview
from ....app_core import Context
from ...frame_widgets.important_buttons import (ChooseShownPacketConsoleColumns, ClearAllCapturedBufferData,
                                                 FilterPacketConsole, PausePacketConsole)
from ...frame_widgets.important_buttons.packet_columns.columns_overlay import shown_columns
from ..panel import Panel
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from ....network.buffer.meta_packet import MetaPacket
from ....network.buffer.packet_filter import FilterError, compile_filter, parse

class Builder(Panel):
    KEY = "packet_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "packet_columns",
        "packet_columns_available",
        "packet_console",
        "packet_filter_available",
        "modbus_registers",
        "requested_packet_treeview_clear",
    )
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.packets
        #  self.create_filter_boxes(menu_frame)

        self.treeview = PacketTreeview(self, context)
        self.shown_columns = None  # the columns shown, in order, as of the last refresh_columns
        self.refresh_columns()
        self.treeview.bind_select(self.on_select)

        self.menu_bar.add_important(FilterPacketConsole)
        self.menu_bar.add_important(ChooseShownPacketConsoleColumns)
        self.menu_bar.add_important(PausePacketConsole)
        minimize_button = self.menu_bar.minimize_button(self.treeview.frame)
        self.menu_bar.add_important(ClearAllCapturedBufferData)

        # Printing Flags
        self.jump_to_bottom = True
        # This console's own place in the packet buffer: the last packet
        # number it has read - and, while paused, the newest packet when it
        # paused, which it reads no further than (see print_tick)
        self.cursor = 0
        self.frozen_at: int | None = None
        # The filter text as of the last tick, and the function it compiled to
        self.filter_text: str | None = None
        self.filter = lambda mpkt: True

        # Start printing loop
        self.context.animation_manager.add_callback(f"packet_panel_{id(self)}", self.print_tick)

    def print_tick(self):
        '''
        Called every frame: follows packet_columns and the filter, then adds
        the packets that arrived since the last tick and pass the filter.

        Paused (packet_console "mode" - see PausePacketConsole), it reads no
        further than the newest packet when it paused, but still follows
        the filter: a change re-reads every packet up to then through the
        new one. Unpaused, it catches up on what arrived meanwhile.
        '''
        self.refresh_columns()
        if self.context.states.get("requested_packet_treeview_clear") in (1, "1"):
            # The clear buttons empty the buffer too - so this starts over on an empty one
            self.context.states.set("requested_packet_treeview_clear", value=0)
            self.frozen_at = None
            self.restart()
        self.refresh_filter()

        if self.context.states.get("packet_console", "mode") == "paused":
            if self.frozen_at is None:
                self.frozen_at = self.buffer.latest_number()
                self.select_child()
        else:
            self.frozen_at = None

        packets, self.cursor = self.buffer.read(self.filter, after=self.cursor, up_to=self.frozen_at, max_return=1000)
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
        if self.jump_to_bottom and self.frozen_at is None:
            self.treeview.scroll_to_bottom()

    def refresh_filter(self):
        '''
        Compiles packet_console "filter" (see packet_filter) when it changed,
        and starts the rows over through it. A filter that can't be read
        (only possible typed into a config by hand - the overlay only saves
        ones that can) shows every packet.
        '''
        text = str(self.context.states.get("packet_console").get("filter") or "")
        if text == self.filter_text:
            return
        self.filter_text = text
        try:
            self.filter = compile_filter(parse(text), self.context)
        except FilterError as error:
            print(f"Packet filter {text!r} can't be read, so it's off: {error}")
            self.filter = lambda mpkt: True
        self.restart()

    def restart(self):
        '''Clears the rows, to read the buffer again from its start (up to where it paused, if paused).'''
        self.treeview.clear()
        self.cursor = 0
        if self.frozen_at is not None:
            # Keep the packet that was selected, if the new filter still shows it
            QTimer.singleShot(0, self, self.reselect)

    def reselect(self):
        if self.buffer.selected_number is not None:
            self.treeview.select(str(self.buffer.selected_number))

    # Treeview
    def submit_packet(self, packet: MetaPacket):
        values = [self.column_value(packet, col, self.context) for col in self.treeview.columns]
        self.treeview.submit(str(packet.get("number")), values)

    @staticmethod
    def column_value(packet: MetaPacket, column: str, context: Context):
        '''
        A packet's value for a column - its own field, but for the host
        columns, which name a device by its nickname from Configure Hosts
        (Preferences.network_hosts, by MAC) when it has one, else by its address.
        '''
        if column in ("src_host", "dst_host"):
            end = column[:3]
            nickname = context.preferences.host_field(packet.get(f"mac_{end}") or "", "nickname")
            return nickname or packet.get(end)
        return packet.get_column_value(column)

    def refresh_columns(self):
        '''
        Shows the columns in packet_columns' tray, in its order, but only
        those students are given (see shown_columns) - only acts when that changed.
        '''
        shown = shown_columns(self.context)
        if shown == self.shown_columns:
            return
        self.shown_columns = shown
        self.treeview.set_visible_columns(shown)

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