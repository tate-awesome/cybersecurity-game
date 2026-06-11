from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core.context import Context

class DefenderMap(Canvas):
      
      def __init__(self, master: CTkFrame, context: Context, defender_page):
            
        super().__init__(master, context, ((0, 0), (200, 200)))

        def frame_callback():
            self.delete("all")
            self.draw.grid_lines()
            if len(defender_page._positions) < 1:
                return
            self.draw.line(defender_page._positions, "red")
            if defender_page._last_bearing is None:
                return
            self.draw.boat(defender_page._positions[-1], defender_page._last_bearing, "white", "black")

        self.set_frame_callback(frame_callback)
        self.start_animation(defender_page.POLL_INTERVAL_MS)