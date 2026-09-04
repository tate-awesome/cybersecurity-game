from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core import Context


class DefenderWorldMap(Canvas):
    '''
    Defender-page counterpart to WorldMap: draws the client boat's trail and
    heading from context.buffer.defender_map/defender_modbus (AP-polled
    telemetry) instead of context.buffer.submarine/modbus (sniffed
    MetaPackets) - a direct port of DefenderV0's old draw_defender_map
    closure as a reusable Canvas, so it can be selected as a modbus_model_panel
    model like WorldMap/House already are.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, ((0, 0), (200, 200)))
        self.map_buffer = context.buffer.defender_map
        self.modbus = context.buffer.defender_modbus

        def frame_callback():
            self.draw.grid_lines()

            positions = self.map_buffer.get_path("client_clean")
            if len(positions) < 1:
                return
            self.draw.line(positions, "red")

            bearing = self.modbus.get_single("theta", "client_clean")
            if bearing is None:
                return
            self.draw.boat(positions[-1], bearing, "white", "black")

        self.set_frame_callback(frame_callback)
        self.start_animation()
