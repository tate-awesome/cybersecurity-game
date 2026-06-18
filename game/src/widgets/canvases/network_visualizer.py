from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core.context import Context


class NetworkVisualizer(Canvas):
    '''
    Canvas that displays elements from the world map: boat trails, boats, grid, ocean, etc.
    '''

    def __init__(self, master: CTkFrame, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((0,0),(600,400)))

        def frame_callback():

            sprites = context.states["world_map_sprites"]
            colors = context.states["world_map_colors"]
            
            self.delete("all")
            
            if int(sprites["ocean"]) == 1:
                self.draw.background(colors["ocean"])
            
            if int(sprites["grid_lines"]) == 1:
                self.draw.grid_lines(colors["grid_lines"], colors["grid_axes"])

            if int(sprites["path_in"]) == 1:
                positions = context.net.data_buffer.get_simple_path("in")
                self.draw.line(positions, colors["path_in"])
                positions = context.net.data_buffer.get_simple_path("other")
                self.draw.line(positions, colors["path_in"])

            if int(sprites["boat_in"]) == 1:
                bearing = context.net.data_buffer.get_bearing("in")
                position = context.net.data_buffer.get_position("in")
                self.draw.boat(position, bearing, colors["boat_in_fill"], colors["boat_in_outline"])
                bearing = context.net.data_buffer.get_bearing("other")
                position = context.net.data_buffer.get_position("other")
                self.draw.boat(position, bearing, colors["boat_in_fill"], colors["boat_in_outline"])

        
        self.set_frame_callback(frame_callback)
        self.start_animation()