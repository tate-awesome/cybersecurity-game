import math
import customtkinter
from customtkinter import CTkCanvas

current_zoom = 1.0
x_zoom = 0
y_zoom = 0

def range_transform(points: list, x_in_range, y_in_range, x_out_range, y_out_range):
    '''
    Converts the incoming list from one range to another. Converts from map bottom-left origin to canvas top-left origin.
    Useful for converting 0-200 position coordinates to canvas coordinates
    Returns: list (x1, y1, x2, y2...)
    '''
    tracks = []
    for i in range(0, len(points)):
        if i%2 == 0:
            # X: 0-input_x -> 0-output_x
            x_out = points[i] * x_out_range / x_in_range
            tracks.append(x_out) # 0-100 becomes 0-canvas_size
        if i%2 == 1:
            y_out = points[i] * y_out_range / y_in_range
            tracks.append(y_out_range - y_out) # 0-100 becomes canvas-0
        i += 1
    return tracks

def draw_bbox_ocean(canvas: CTkCanvas, color):
    '''
    Draws the ocean bigger than the canvas with some regard for zoom.
    Provides a bounding box for comfortable panning.
    '''
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    s = min(w, h)
    m = 0.5 * s
    z = current_zoom
    canvas.create_rectangle(-m*z, -m*z, (w+m)*z, (h+m)*z, fill=color)

def draw_bbox_cage(canvas: CTkCanvas, color):
    '''
    Draws the 0-200 range for the boat as a dashed box
    '''
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    p = 50
    z = current_zoom
    x = -x_zoom/2
    y = -y_zoom/2
    canvas.create_rectangle((p-x)*z, (p-y)*z, (w-p-x)*z, (h-p-y)*z, fill="", outline=color)

def draw_mouse(canvas: CTkCanvas):
    x = x_zoom
    y = y_zoom
    s = 5
    canvas.create_oval(x-s, y-s, x+s, y+s, fill="red")

def draw_reference_dots(positions: list, color):
    '''
    Draws 
    '''

def zoom_pan_canvas(parent, draw_callback, framerate_ms):
    global current_zoom
    canvas = CTkCanvas(parent)
    canvas.pack(fill="both", expand=True)

    
    # Redraw on resize
    def resize(event):
        draw_callback(canvas)
        print("config")
    parent.bind("<Configure>", resize)


    # Pan 
    def start_pan(event):
        canvas.scan_mark(event.x, event.y)
    canvas.bind("<ButtonPress-1>", start_pan)
    def do_pan(event):
        canvas.scan_dragto(event.x, event.y, gain=1)
    canvas.bind("<B1-Motion>", do_pan)


    # Zoom
    def zoom(event):
        global current_zoom, x_zoom, y_zoom

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

        new_scale = current_zoom * factor

        # Clamp scale
        # if not (0.2 <= new_scale <= 5.0):
        #     return
        current_zoom = new_scale

        # Zoom around mouse
        x_zoom = canvas.canvasx(event.x)
        y_zoom = canvas.canvasy(event.y)

        # canvas.scale("all", x_zoom, y_zoom, factor, factor)
    # Windows / Mac
    canvas.bind("<MouseWheel>", zoom)
    # Linux
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)


    def reset_view(event=None):
        global current_zoom

        scale_factor = 1 / current_zoom
        current_zoom = 1.0
        canvas.scale("all", 0, 0, scale_factor, scale_factor)

        canvas.configure(scrollregion=canvas.bbox("all"))

        # Center view
        bbox = canvas.bbox("all")
        if bbox:
            x0, y0, x1, y1 = bbox
            canvas.xview_moveto((x0 + x1 - canvas.winfo_width()) / (x1 - x0))
            canvas.yview_moveto((y0 + y1 - canvas.winfo_height()) / (y1 - y0))

    canvas.bind("<Button-2>", reset_view)      # Windows/Linux
    canvas.bind("<Button-3>", reset_view)      # Mac sometimes uses Button-3

    def animation_loop(cx, cy):
        draw_callback(canvas)
        canvas.after(framerate_ms, lambda: animation_loop(cx, cy))
    animation_loop(0, 0)
