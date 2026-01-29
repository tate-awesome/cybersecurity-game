'''
Handles drawing to the map. 
'''

from customtkinter import CTkCanvas
from customtkinter import CTkBaseClass
from threading import Lock

class Map:

    def resize(self, event):
        self.draw_callback(self.canvas, self.draw_lock)

    def start_pan(self, event):
        self.x_pan_start = event.x
        self.y_pan_start = event.y

    def do_pan(self, event):
        dx = event.x - self.x_pan_start
        dy = event.y - self.y_pan_start

        self.offset[0] += dx
        self.offset[1] += dy

        self.x_pan_start = event.x
        self.y_pan_start = event.y

        self.draw_callback(self.canvas, self.draw_lock)

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        cx, cy = C
        tx, ty = self.offset

        self.scale = k * self.scale
        self.offset = [
        cx + k * (tx - cx),
        cy + k * (ty - cy),
        ]

    # Zoom
    def zoom(self, event):
        # Determine zoom direction
        if event.delta > 0:
            factor = 1.1
        else:
            factor = 0.9
        if hasattr(event, "num"):
            if event.num == 4:
                factor = 1.1
            elif event.num == 5:
                factor = 0.9

        # Clamp scale?
        # if not (0.2 <= new_scale <= 5.0):
        #     return

        x_focus = self.canvas.canvasx(event.x)
        y_focus = self.canvas.canvasy(event.y)
        self.apply_scale_about((x_focus,y_focus), factor)
        self.draw_callback(self.canvas, self.draw_lock)

    def reset_scale(self):
        self.scale = 1.0
        self.offset = [0, 0]

    def reset_view(self, event=None):
        self.reset_scale()
        self.draw_callback(self.canvas, self.draw_lock)

    def __init__(self, parent: CTkBaseClass, draw_callback: function, framerate_ms: float, draw_lock: Lock, padding: float=20, margin: float=40):
        # zoom/pan persistent values
        self.scale = 1.0
        self.offset = [0.0, 0.0]
        self.x_pan_start = 0.0
        self.y_pan_start = 0.0

        # Padding for world plane
        self.padding = padding
        self.margin = margin

        # Assign variables
        self.parent = parent
        self.draw_callback = draw_callback
        self.framerate_ms = framerate_ms
        self.draw_lock = draw_lock

        # Create canvas
        self.canvas = CTkCanvas(parent)
        self.canvas.pack(fill="both", expand=True)

        # Bind events
        self.parent.bind("<Configure>", self.resize)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)
            # Windows / Mac
        self.canvas.bind("<MouseWheel>", self.zoom)
            # Linux
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        # canvas.scale("all", x_zoom, y_zoom, factor, factor)  # <--- only useful for already drawn canvases
        self.canvas.bind("<Button-2>", self.reset_view)      # Windows/Linux
        self.canvas.bind("<Button-3>", self.reset_view)      # Mac sometimes uses Button-3

        # Start animation loop
        def animation_loop():
            draw_callback(self.canvas, self.draw_lock)
            self.canvas.after(framerate_ms, lambda: animation_loop())
        animation_loop()


  