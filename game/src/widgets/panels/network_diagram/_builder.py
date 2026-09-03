from customtkinter import CTkTextbox
from ....app_core import Context
from ...canvases.network_diagram import NetworkDiagramCanvas
from ...canvases.strip_chart import StripChart
from ... import Panes
from ..panel import Panel

class Builder(Panel):
    KEY = "network_graph_panel"
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.packets

        panes = Panes(self, context, "horizontal", 2, [2, 2], False)

        left_frame = panes.pane(0)
        right_frame = panes.pane(1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.diagram = NetworkDiagramCanvas(left_frame, context)

        def title():
            return self.context.labels.get("network_graph", "stripchart_title")
        def units():
            return self.context.labels.get("network_graph", "stripchart_units")
        def factor():
            return 1.0
        self.rate_chart = StripChart(right_frame, context, (0, 0), title, units, factor,
                                      lambda: {"": list(self.buffer.get_window_type_pps())})
        self.rate_chart.start_animation()

        self.selected_text = CTkTextbox(right_frame, wrap="none", font=self.style.get_font("mono"), state="disabled")
        self.selected_text.grid(row=0, column=0, sticky="nsew")
        self.selected_text.grid_remove()

        self.menu_bar.minimize_button(panes, master)

        self.current_mode = "live"
        self.current_selected_number = None
        self.context.animation_manager.add_callback("network_diagram_panel", self.tick)

    def tick(self):
        mode = self.context.states.get("packet_console_state", "mode")

        if mode != self.current_mode:
            self.current_mode = mode
            if mode == "paused":
                self.rate_chart.grid_remove()
                self.selected_text.grid()
            else:
                self.selected_text.grid_remove()
                self.rate_chart.grid()

        if mode != "paused":
            return

        mpkt = self.buffer.get_selected()
        number = mpkt.get("number") if mpkt is not None else None

        if number == self.current_selected_number:
            return
        self.current_selected_number = number

        self.selected_text.configure(state="normal")
        self.selected_text.delete("1.0", "end")
        if mpkt is not None:
            self.selected_text.insert("1.0", mpkt.get("pkt").show(dump=True))
        self.selected_text.configure(state="disabled")
