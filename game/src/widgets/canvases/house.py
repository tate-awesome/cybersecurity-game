from .core.canvas import Canvas
from ...app_core import Context
from customtkinter import CTkFrame

class House(Canvas):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, ((0, 0), (100, 100)))
        self.buffer = context.net.buffer.hvac
        self.set_frame_callback(self.frame_callback)
        self.start_animation()

    def frame_callback(self):
        print(self.buffer.get_heater("in"))
        print(self.buffer.get_heater("out"))
        print(self.buffer.get_temperature("in"))
        print(self.buffer.get_temperature("out"))
