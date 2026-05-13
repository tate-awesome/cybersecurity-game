from customtkinter import *

from ..style import Style
from .world_map import WorldMap
from .boat_focus import BoatFocus
from .values_table import ValuesTable
from .. import common

class Displays:
    def __init__(self, style, parent, context):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = self.context.net.data_buffer


        top, bottom = common.create_bifold(style, self.parent)

        self.top_grid(top)

        # toppish = common.create_stretchable(style, top)
        # toppish.configure(bg_color="red")



    def top_grid(self, parent: CTkFrame):

        #
        # MAIN GRID CONFIG
        #

        # Left column = fixed width
        parent.grid_columnconfigure(0, weight=0)

        # Right column = expandable
        parent.grid_columnconfigure(1, weight=1)

        # Top row expands vertically
        parent.grid_rowconfigure(0, weight=1)

        # Bottom row stays fixed height
        parent.grid_rowconfigure(1, weight=0)

        #
        # SCROLLABLE LEFT PANEL
        #

        LEFT_WIDTH = 320

        left_container = CTkFrame(parent, width=LEFT_WIDTH)
        left_container.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=self.style.cgap,
            pady=self.style.cgap
        )

        # Prevent container from shrinking to children
        left_container.grid_propagate(False)

        # Scrollable frame
        left_scroll = CTkScrollableFrame(
            left_container,
            width=LEFT_WIDTH
        )

        left_scroll.pack(fill="both", expand=True)

        # Widgets
        numbers_frame = ValuesTable(self.style, left_scroll, self.context)
        boat_focus = BoatFocus(self.style, left_scroll, self.context)

        for w in [numbers_frame, boat_focus]:
            w.frame.pack(
                side="top",
                fill="x",
                expand=False,
                pady=self.style.igap
            )

        def _on_mousewheel(event):
            left_scroll._parent_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        def _bind_mousewheel(event):
            left_scroll.bind_all("<MouseWheel>", _on_mousewheel)
            left_scroll.bind_all(
                "<Button-4>",
                lambda e: left_scroll._parent_canvas.yview_scroll(-1, "units")
            )
            left_scroll.bind_all(
                "<Button-5>",
                lambda e: left_scroll._parent_canvas.yview_scroll(1, "units")
            )

        def _unbind_mousewheel(event):
            left_scroll.unbind_all("<MouseWheel>")
            left_scroll.unbind_all("<Button-4>")
            left_scroll.unbind_all("<Button-5>")

        left_scroll.bind("<Enter>", _bind_mousewheel)
        left_scroll.bind("<Leave>", _unbind_mousewheel)

        #
        # RIGHT EXPANDABLE PANEL
        #


        world_map = WorldMap(self.style, parent, self.context, self.buffer)

        world_map.frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=self.style.cgap,
            pady=self.style.cgap
        )

        #
        # BOTTOM WIDGET
        #


        values_tracer = WorldMap(self.style, parent, self.context, self.buffer)

        values_tracer.frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=self.style.cgap,
            pady=self.style.cgap
        )