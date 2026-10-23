from PySide6.QtWidgets import QVBoxLayout, QWidget
from ...app_core import Context

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .figure_theme import follow_theme


class HVACChart(QWidget):
    '''
    A rolling room-temperature graph with a dashed comparison line and the
    heater's OFF/ON history underneath, shared by the polled
    (DefenderHVACChart) and sniffed (SniffedHVACChart) HVAC models so both
    look the same. Subclasses say where the three histories come from
    (histories()) and what the dashed line is (SECOND_LINE_LABEL). Not a
    Canvas subclass (it isn't a coordinate-space drawing canvas), but
    matches the same start_animation/stop_animation contract
    modbus_model_panel expects when it swaps models out.
    '''

    MAX_POINTS = 300
    SECOND_LINE_LABEL = ""

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master)
        context.style.set_material(self, "card")
        # Stretch 1: see Scrollable.__init__ for why (same Panel-body/
        # trailing-filler interaction, harmless when master isn't a Panel).
        master.layout().addWidget(self, 1)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(
            context.style.igap, context.style.igap, context.style.igap, context.style.igap
        )
        self.context = context

        # Colored by the theme - see follow_theme, below
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Temperature Trajectory Over Time", fontsize=11)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°F)")
        ax.margins(0, 0.2)

        (self._room_line,) = ax.plot([], [], linewidth=1.8, label="Room Temp")
        (self._second_line,) = ax.plot([], [], linewidth=1.8, linestyle="--", label=self.SECOND_LINE_LABEL)

        # Heater state is a 0/1 history, not a temperature - its own axis
        # (sharing the same x/time axis via twinx) keeps it from squashing
        # flat against the bottom of the temperature range.
        heater_ax = ax.twinx()
        heater_ax.set_ylabel("Heater")
        heater_ax.set_ylim(-0.1, 1.1)
        heater_ax.set_yticks([0, 1])
        heater_ax.set_yticklabels(["OFF", "ON"])
        (self._heater_line,) = heater_ax.step([], [], where="post", linewidth=1.2, alpha=0.7, label="Heater")

        lines = [self._room_line, self._second_line, self._heater_line]
        legend = ax.legend(lines, [line.get_label() for line in lines], loc="upper left", fontsize=8)
        fig.tight_layout()

        self._fig = fig
        self._ax = ax
        self._heater_ax = heater_ax
        # FigureCanvasQTAgg is itself a QWidget, unlike Tk's FigureCanvasTkAgg
        # (which needed .get_tk_widget() to get at the actual Tk widget) -
        # it goes straight into the layout.
        self._figure_canvas = FigureCanvasQTAgg(fig)
        self.layout().addWidget(self._figure_canvas)
        follow_theme(context.style, self._figure_canvas, [ax, heater_ax],
                     {self._room_line: "chart_1", self._second_line: "chart_2", self._heater_line: "hot"}, legend)
        self._figure_canvas.draw()

    def histories(self) -> tuple[list, list, list]:
        '''The room, dashed-line and heater histories, each a list of (time, value).'''
        raise NotImplementedError

    def start_animation(self):
        self.context.animation_manager.add_callback(f"{type(self).__name__}_{id(self)}", self.redraw)

    def stop_animation(self):
        self.context.animation_manager.remove_callback(f"{type(self).__name__}_{id(self)}")

    def redraw(self):
        room_history, second_history, heater_history = (
            history[-self.MAX_POINTS:] for history in self.histories()
        )

        if not room_history and not second_history and not heater_history:
            return
        t0 = (room_history or second_history or heater_history)[0][0]

        room_times, room_values = zip(*room_history) if room_history else ((), ())
        second_times, second_values = zip(*second_history) if second_history else ((), ())
        heater_times, heater_values = zip(*heater_history) if heater_history else ((), ())

        self._room_line.set_data([t - t0 for t in room_times], room_values)
        self._second_line.set_data([t - t0 for t in second_times], second_values)
        self._heater_line.set_data([t - t0 for t in heater_times], heater_values)
        self._ax.relim()
        self._ax.autoscale_view()
        # heater_ax shares the x-axis with _ax (twinx) so it already tracks
        # the same time range - only relim/autoscale the primary axis, or
        # this would fight the fixed OFF/ON y-range set at construction.

        y_min, y_max = self._ax.get_ylim()
        center = (y_min + y_max) / 2
        min_range = 150.0
        if (y_max - y_min) < min_range:
            half_range = min_range / 2
            self._ax.set_ylim(center - half_range, center + half_range)

        self._figure_canvas.draw_idle()
