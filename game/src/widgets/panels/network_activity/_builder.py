from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget
from ....app_core import Context
from ...canvases.strip_chart import StripChart
from ..panel import Panel
from ...frame_widgets.text_area import TextArea
from ...frame_widgets.important_buttons import PausePacketConsole, ToggleStripChartAutoFit

class Builder(Panel):
    '''
    A packets-per-second strip chart - replaced, while paused, by a full
    dump of the packet selected in the packet console.
    '''
    KEY = "activity_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    # packet_console's "mode" pauses it along with the packet console; its rate chart is a strip chart
    SETTINGS = (
        "packet_console",
        "strip_chart_colors",
        "strip_chart_auto_fit",
        "strip_chart_auto_fit_max_seconds",
    )
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.packets

        # StripChart places itself via master.grid_layout (see time_core's
        # StripChartBase), so the body gets a real grid. Also lets
        # selected_text share the exact same cell as rate_chart (both added
        # at (0, 0)), shown in its place while paused.
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body.grid_layout = QGridLayout()
        body_layout.addLayout(body.grid_layout)
        body.grid_layout.setColumnStretch(0, 1)
        body.grid_layout.setRowStretch(0, 1)
        self.layout().addWidget(body, 1)

        def title():
            return self.context.labels.get("network_graph_stripchart_title")
        def units():
            return ""  # the title says it's packets - a units label would sit right on it
        def factor():
            return 1.0
        self.rate_chart = StripChart(body, context, (0, 0), title, units, factor,
                                      lambda: {"": list(self.buffer.get_window_type_pps())},
                                      min_max=2)
        self.rate_chart.start_animation()

        self.selected_text = TextArea()
        self.selected_text.setFont(self.style.get_font("mono"))
        self.selected_text.setReadOnly(True)
        self.selected_text.setLineWrapMode(TextArea.LineWrapMode.NoWrap)
        body.grid_layout.addWidget(self.selected_text, 0, 0)
        self.selected_text.hide()

        self.menu_bar.add_important(ToggleStripChartAutoFit)
        self.menu_bar.add_important(PausePacketConsole)
        self.menu_bar.minimize_button(body)

        self.current_mode = "live"
        self.current_selected_number = None
        self.context.animation_manager.add_callback(f"activity_panel_{id(self)}", self.tick)

    def tick(self):
        mode = self.context.states.get("packet_console", "mode")

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
