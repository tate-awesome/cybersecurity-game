from customtkinter import CTkFrame
from ...app_core import Context

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Hardcoded dark-theme colors matching AP_ESP32.ino's config page palette -
# ported as-is from the old HVACView._build_graph, see its comment: not
# pulled from Style on purpose, matplotlib needs a single concrete color
# string and CTk colors can be light/dark-mode tuples.
_FIG_BG      = "#16213e"
_AXES_BG     = "#0a0a1a"
_GRID        = "#0f3460"
_TEXT        = "#e0e0e0"
_ROOM_LINE   = "#4caf50"
_TARGET_LINE = "#e94560"


class DefenderHVACChart(CTkFrame):
    '''
    Defender-page counterpart to House: a rolling room-vs-target temperature
    graph read from context.buffer.defender_modbus, ported from the old
    HVACView._build_graph/refresh's matplotlib figure so it can be selected
    as a modbus_model_panel model like WorldMap/House already are. Not a
    Canvas subclass (it isn't a coordinate-space drawing canvas), but
    matches the same start_animation/stop_animation contract modbus_model_panel
    expects when it swaps models out.
    '''

    MAX_POINTS = 300

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, fg_color=context.style.color("widget"))
        self.pack(side="top", fill="both", expand=True, pady=context.style.gap, padx=context.style.gap)
        self.context = context
        self.modbus = context.buffer.defender_modbus

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(_FIG_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(_AXES_BG)
        ax.set_title("Temperature Trajectory Over Time", color=_TEXT, fontsize=11)
        ax.set_xlabel("Time (s)", color=_TEXT)
        ax.set_ylabel("Temperature (°F)", color=_TEXT)
        ax.tick_params(colors=_TEXT)
        ax.grid(True, color=_GRID, linewidth=0.6)
        ax.margins(0, 0.2)
        for spine in ax.spines.values():
            spine.set_color(_GRID)

        (self._room_line,) = ax.plot([], [], color=_ROOM_LINE, linewidth=1.8, label="Room Temp")
        (self._target_line,) = ax.plot([], [], color=_TARGET_LINE, linewidth=1.8, linestyle="--", label="Target Setpoint")
        legend = ax.legend(loc="upper left", facecolor=_FIG_BG, edgecolor=_GRID, fontsize=8)
        for text in legend.get_texts():
            text.set_color(_TEXT)
        fig.tight_layout()

        self._fig = fig
        self._ax = ax
        self._figure_canvas = FigureCanvasTkAgg(fig, master=self)
        self._figure_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._figure_canvas.draw()

        self.start_animation()

    def start_animation(self):
        self.context.animation_manager.add_callback(f"DefenderHVACChart_{id(self)}", self.redraw)

    def stop_animation(self):
        self.context.animation_manager.remove_callback(f"DefenderHVACChart_{id(self)}")

    def redraw(self):
        room_history = self.modbus.get_history("temperature", "client_clean")[-self.MAX_POINTS:]
        target_history = self.modbus.get_history("temperature", "target")[-self.MAX_POINTS:]

        if not room_history and not target_history:
            return
        t0 = (room_history or target_history)[0][0]

        room_times, room_values = zip(*room_history) if room_history else ((), ())
        target_times, target_values = zip(*target_history) if target_history else ((), ())

        self._room_line.set_data([t - t0 for t in room_times], room_values)
        self._target_line.set_data([t - t0 for t in target_times], target_values)
        self._ax.relim()
        self._ax.autoscale_view()

        y_min, y_max = self._ax.get_ylim()
        center = (y_min + y_max) / 2
        min_range = 150.0
        if (y_max - y_min) < min_range:
            half_range = min_range / 2
            self._ax.set_ylim(center - half_range, center + half_range)

        self._figure_canvas.draw_idle()
