from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core import Context


class WorldMap(Canvas):
    '''
    Canvas that displays elements from the world map: boat trails, boats, grid, ocean, etc.
    '''

    def __init__(self, master: CTkFrame, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((0,0),(200,200)))
        self.buffer = context.net.buffer.submarine

        def frame_callback():
            def color(key):
                return self.context.style.color(self.context.states.get("world_map_colors", key))
            def sprite(key):
                return context.states.get("world_map_sprites", key)
            
            self.delete("all")
            
            if int(sprite("ocean")) == 1:
                self.draw.background(color("ocean"))
            
            if int(sprite("grid_lines")) == 1:
                self.draw.grid_lines(color("grid_lines"), color("grid_axes"), color("grid_numbers"))

            if int(sprite("path_in")) == 1:
                positions = self.buffer.get_simple_path("in")
                self.draw.line(positions, color("path_in"))
                positions = self.buffer.get_simple_path("out")
                self.draw.line(positions, color("path_out"))

            if int(sprite("boat_in")) == 1:
                bearing = self.buffer.get_bearing("in")
                position = self.buffer.get_position("in")
                self.draw.boat(position, bearing, color("boat_in_fill"), color("boat_in_outline"))
                bearing = self.buffer.get_bearing("out")
                position = self.buffer.get_position("out")
                self.draw.boat(position, bearing, color("boat_out_fill"), color("boat_out_outline"))

        
        self.set_frame_callback(frame_callback)
        self.start_animation()