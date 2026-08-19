from customtkinter import CTkFrame, CTkTextbox
from ....app_core import Context
from ...canvases.network_diagram import NetworkDiagramCanvas
from ...canvases.strip_chart import StripChart
from ..panel import Panel

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "network_panel")

        self.buffer = context.net.buffer.packets

        body = CTkFrame(self, fg_color=self.style.color("panel"))
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left_frame = CTkFrame(body, fg_color=self.style.color("panel"))
        left_frame.grid(row=0, column=0, sticky="nsew")

        right_frame = CTkFrame(body, fg_color=self.style.color("panel"))
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.diagram = NetworkDiagramCanvas(left_frame, context)

        # Wrap the strip chart since it packs itself internally, but the right
        # frame needs to grid/grid_remove it alongside the paused textbox.
        self.chart_wrapper = CTkFrame(right_frame, fg_color=self.style.color("panel"))
        self.rate_chart = StripChart(self.chart_wrapper, context, self.buffer.get_rate_history, "Packets/sec")
        self.rate_chart.start_animation()
        self.chart_wrapper.grid(row=0, column=0, sticky="nsew")

        self.selected_text = CTkTextbox(right_frame, wrap="none", font=self.style.get_font("mono"), state="disabled")
        self.selected_text.grid(row=0, column=0, sticky="nsew")
        self.selected_text.grid_remove()

        self.menu_bar.minimize_button(body, master)

        self.current_mode = "live"
        self.current_selected_number = None
        self.context.animation_manager.add_callback("network_diagram_panel", self.tick)

    def tick(self):
        mode = self.context.states.get("packet_console_state", "mode")

        if mode != self.current_mode:
            self.current_mode = mode
            if mode == "paused":
                self.chart_wrapper.grid_remove()
                self.selected_text.grid()
            else:
                self.selected_text.grid_remove()
                self.chart_wrapper.grid()

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
