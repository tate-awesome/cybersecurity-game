from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core.context import Context


class WorldMap(Canvas):
    '''
    Canvas that displays elements from the world map: boat trails, boats, grid, ocean, etc.
    '''

    def __init__(self, master: CTkFrame, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((0,0),(200,200)))

        def frame_callback():
            positions = context.net.data_buffer.get_simple_path("other")
            bearing = context.net.data_buffer.get_bearing("other")
            self.delete("all")
            self.draw.ocean()
            self.draw.grid_lines()
            if len(positions) < 1: return
            self.draw.line(positions, "yellow")
            if bearing is None: return
            last_position = positions[-1]
            self.draw.boat(last_position, bearing, "yellow", "yellow")

        
        self.set_frame_callback(frame_callback)
        self.start_animation()