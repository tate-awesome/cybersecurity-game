from PySide6.QtWidgets import QGridLayout, QPlainTextEdit
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
        # StripChart places itself via master.grid_layout (see time_core's
        # StripChartBase) - right_frame only has the plain QVBoxLayout Panes
        # gives every pane, so a real grid goes inside it. Also lets
        # selected_text share the exact same cell as rate_chart (both added
        # at (0, 0)) the way the old grid_remove()/grid() swap needed.
        right_frame.grid_layout = QGridLayout()
        right_frame.layout().addLayout(right_frame.grid_layout)
        right_frame.grid_layout.setColumnStretch(0, 1)
        right_frame.grid_layout.setRowStretch(0, 1)

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

        self.selected_text = QPlainTextEdit()
        self.selected_text.setFont(self.style.get_font("mono"))
        self.selected_text.setReadOnly(True)
        self.selected_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        right_frame.grid_layout.addWidget(self.selected_text, 0, 0)
        self.selected_text.hide()

        self.menu_bar.minimize_button(panes, master)

        self.current_mode = "live"
        self.current_selected_number = None
        self.context.animation_manager.add_callback("network_diagram_panel", self.tick)

    def tick(self):
        mode = self.context.states.get("packet_console_state", "mode")

        if mode != self.current_mode:
            self.current_mode = mode
            if mode == "paused":
                self.rate_chart.hide()
                self.selected_text.show()
            else:
                self.selected_text.hide()
                self.rate_chart.show()

        if mode != "paused":
            return

        mpkt = self.buffer.get_selected()
        number = mpkt.get("number") if mpkt is not None else None

        if number == self.current_selected_number:
            return
        self.current_selected_number = number

        if mpkt is not None:
            self.selected_text.setPlainText(mpkt.get("pkt").show(dump=True))
        else:
            self.selected_text.clear()
