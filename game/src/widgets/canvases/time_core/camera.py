from customtkinter import CTkCanvas
from ....app_core.context import Context
from . import transforms as t

class Camera:

    def __init__(self, canvas: CTkCanvas, context: Context, time_scale: list[float], time_offset: list[float]):
        '''
        Tracks axis scaling and transforms. Uses a shared time_sync_ptr to synchronize time scaling and offset across multiple canvases.
        '''
        self.canvas = canvas

        self.time_scale = time_scale
        self.time_offset = time_offset
        self.vertical_scale = 1.0

        self.time_scale[0] = 1.0
        self.time_offset[0] = 0.0
        self.vertical_scale = 1.0

        self.vertical_offset = 0.0
        self.padding = 0
        self.update_padding() #Set padding based of canvas size

        # Starting position for each mouse pan event - panning moves the time offset and vertical scale
        self.pan_start = [0.0, 0.0]

        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.click_callback)
        self.canvas.bind("<B1-Motion>", self.do_pan)
            # Windows / Mac
        self.canvas.bind("<Shift-MouseWheel>", self.zoom)
            # Linux
        self.canvas.bind("<Shift-Button-4>", self.zoom)
        self.canvas.bind("<Shift-Button-5>", self.zoom)
        # canvas.scale("all", x_zoom, y_zoom, factor, factor)  # <--- only useful for already drawn canvases
        self.canvas.bind("<Button-2>", self.reset_camera)      # Windows/Linux
        self.canvas.bind("<Button-3>", self.reset_camera)      # Mac sometimes uses Button-3

    def update_padding(self):
        base = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.padding = max(base * 0.025, 10)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       TRANSFORMERS
# --------------------------------------------------------------------------------------------------------------------------

    def data_to_strip_chart(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        right_aligned = t.right_align(points_in, self.canvas)
        chart_fit = t.padded_vertical_fit(right_aligned, self.canvas, self.padding)
        panned = t.zoom_and_pan(chart_fit, self.vertical_scale, self.time_scale[0], self.time_offset[0])
        return panned
    
    def strip_chart_to_data(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        # time_unscaled = t.unzoom_and_unpan_horizontal(points_in, self.scale, self.offset)
        # data_fit = t.unpadded_fit_vertical_snap_right(time_unscaled, self.canvas, self.padding)
        # return data_fit
        return points_in

# --------------------------------------------------------------------------------------------------------------------------
#                                                       EVENT CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------

    def click_callback(self, event=None):
        print(f"Raw: {event.x}, {event.y}")
        raw_points = [(event.x, event.y)]
        world_points = self.strip_chart_to_data(raw_points)
        x = world_points[0][0]
        y = world_points[0][1]
        print(f"World: {x}, {y}")
        self.pan_start = [event.x, event.y]

    def do_pan(self, event=None):
        # Calculate movement
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        self.time_offset[0] += dx
        # self.vertical_scale += dy

        self.pan_start = [event.x, event.y]

        # Redraw for each mouse position
        if self.canvas.frame_callback is not None:
            self.canvas.frame_callback()

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        cx, cy = C
        tx, ty = self.time_offset[0], 0.0

        self.time_scale[0] = k * self.time_scale[0]
        # self.vertical_scale = k * self.vertical_scale
        self.time_offset[0] = cx + k * (tx - cx)

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

        # Redraw for each zoom scroll
        if self.canvas.frame_callback is not None:
            self.canvas.frame_callback()

    def reset_camera(self, event=None):
        self.time_scale[0] = 1.0
        self.time_offset[0] = 0.0
        self.vertical_scale = 1.0
        # Redraw on reset scale
        if self.canvas.frame_callback:
            self.canvas.frame_callback()  