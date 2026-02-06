from ...app_core.context import Context
from ...drawing.viewport import ViewPort
from ...drawing import sprites
from ...widgets.map import Map

from threading import Lock
from customtkinter import CTkCanvas


class BoatMotion:
    def __init__(self, context: Context):
        self.context = context


        # Make initial boat path
        self.positions = sprites.random_spline_path(20, 100)
        def random_visible_color():
            import random
            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                # Calculate brightness (perceived luminance)
                brightness = 0.299*r + 0.587*g + 0.114*b

                # White is ~255; reject colors that are too bright
                if brightness < 200:
                    return f"#{r:02x}{g:02x}{b:02x}"
        self.color = random_visible_color()

        

        map = Map(self.context.root, self.frame_callback, 100, 20)

    def frame_callback(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        import time
        from ...drawing import transformations as t

        path_duration = 30.0
        path_index = int(((time.time() % path_duration) / path_duration) * (len(self.positions)-2))
        bearing = t.get_bearing(self.positions[path_index], self.positions[path_index+1])
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.grid_lines()
            draw.line(self.positions, self.color)
            last_position = self.positions[path_index]
            draw.boat(last_position, bearing)