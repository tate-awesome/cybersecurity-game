from .core.canvas import Canvas
from PySide6.QtWidgets import QWidget
from ...app_core import Context


class WorldMap(Canvas):
    '''
    Canvas that displays elements from the world map: boat trails, boats, grid, ocean, etc.
    '''

    def __init__(self, master: QWidget, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((0,0),(200,200)))
        self.buffer = context.buffer.submarine

        def frame_callback():
            def color(key):
                return self.context.style.color(self.context.states.get("model_colors", key))
            def sprite(key):
                return context.states.get("model_sprites", key)
            def sprite_enabled(key):
                # A malformed/non-numeric sprite config value would otherwise
                # raise on every frame, permanently freezing this canvas.
                try:
                    return int(sprite(key)) == 1
                except (TypeError, ValueError):
                    return False

            if sprite_enabled("ocean"):
                self.draw.background(color("ocean"))

            if sprite_enabled("grid_lines"):
                self.draw.grid_lines(color("grid_lines"), color("grid_axes"), color("grid_numbers"),
                                     color("ocean"), sprite_enabled("grid_numbers"))

            if sprite_enabled("path_in"):
                positions = self.buffer.get_simple_path("in")
                self.draw.line(positions, color("path_in"))
                positions = self.buffer.get_simple_path("out")
                self.draw.line(positions, color("path_out"))

            if sprite_enabled("boat_in"):
                bearing = self.buffer.get_bearing("in")
                position = self.buffer.get_position("in")
                self.draw.boat(position, bearing, color("boat_in_fill"), color("boat_in_outline"))
                bearing = self.buffer.get_bearing("out")
                position = self.buffer.get_position("out")
                self.draw.boat(position, bearing, color("boat_out_fill"), color("boat_out_outline"))

            # Drawn last so the crosshairs sit on top: a legend row per boat whose
            # label (its name) or position (its coordinates) is switched on
            rows = []
            for direction in ("in", "out"):
                show_label = sprite_enabled(f"boat_{direction}_label")
                show_position = sprite_enabled(f"boat_{direction}_position")
                position = self.buffer.get_position(direction)
                if position is None or not (show_label or show_position):
                    continue
                rows.append((context.labels.get(f"map_legend_{direction}") if show_label else "",
                             color(f"boat_{direction}_fill"),
                             self.draw.coordinates(position) if show_position else ""))
            self.draw.map_crosshairs(self.hover_pos, rows, color("grid_numbers"), color("ocean"))

        
        self.set_frame_callback(frame_callback)
        self.start_animation()