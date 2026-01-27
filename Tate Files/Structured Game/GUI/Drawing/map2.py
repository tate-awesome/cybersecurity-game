import math
import customtkinter
from customtkinter import CTkCanvas

SCALE = 1.0 # overall scale
OFFSET = [0.0, 0.0] # translation (tx, ty)
x_pan_start = 0
y_pan_start = 0

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

def transform_figure(F):
    """
    Transforms a flat list figure [x0,y0,x1,y1,...]
    using the global SCALE and OFFSET.


    Returns a new flat list.
    """
    global SCALE, OFFSET


    tx, ty = OFFSET
    s = SCALE


    out = []
    for i in range(0, len(F), 2):
        x, y = F[i], F[i+1]
        x_new = s * x + tx
        y_new = s * y + ty
        
        out.extend((x_new, y_new))


    return out

def triangle(canvas: CTkCanvas):
    triangle = [-100,0, 0,200, 100,0]
    angle = range_transform(triangle, 200, 200, 200, 200)


    new_triangle = transform_figure(angle)

    canvas.create_polygon(new_triangle, fill="orange")

def zoom_pan_canvas(parent, draw_callback, framerate_ms, draw_lock):
    canvas = CTkCanvas(parent)
    canvas.pack(fill="both", expand=True)

    
    # Redraw on resize
    def resize(event):
        draw_callback(canvas, draw_lock)
        print("config")
    parent.bind("<Configure>", resize)


    # Pan
    def start_pan(event):
        global x_pan_start, y_pan_start
        x_pan_start = event.x
        y_pan_start = event.y


    canvas.bind("<ButtonPress-1>", start_pan)


    def do_pan(event):
        global OFFSET, x_pan_start, y_pan_start


        dx = event.x - x_pan_start
        dy = event.y - y_pan_start


        # Update global offset
        OFFSET[0] += dx
        OFFSET[1] += dy


        x_pan_start = event.x
        y_pan_start = event.y


        draw_callback(canvas, draw_lock)


    canvas.bind("<B1-Motion>", do_pan)

    def apply_scale_about(C, k):
        """
        Updates the global SCALE and OFFSET to represent
        scaling about point C by factor k.
        Params:
        C: (cx, cy) -> scale center in world coords
        k: float -> scale factor
        """
        global SCALE, OFFSET


        cx, cy = C
        tx, ty = OFFSET


        # New collapsed parameters
        SCALE = k * SCALE
        OFFSET = [
        cx + k * (tx - cx),
        cy + k * (ty - cy),
        ]
    
    def reset_scale():
        global SCALE, OFFSET
        SCALE = 1.0
        OFFSET = [0, 0]

    # Zoom
    def zoom(event):
        global x_focus, y_focus, prev_zoom, x_translation, y_translation

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

        


        # Clamp scale
        # if not (0.2 <= new_scale <= 5.0):
        #     return

        x_focus = canvas.canvasx(event.x)
        y_focus = canvas.canvasy(event.y)
        apply_scale_about((x_focus,y_focus), factor)
        draw_callback(canvas, draw_lock)


        # canvas.scale("all", x_zoom, y_zoom, factor, factor)
    # Windows / Mac
    canvas.bind("<MouseWheel>", zoom)
    # Linux
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)


    def reset_view(event=None):
        reset_scale()
        draw_callback(canvas, draw_lock)

    canvas.bind("<Button-2>", reset_view)      # Windows/Linux
    canvas.bind("<Button-3>", reset_view)      # Mac sometimes uses Button-3

    def animation_loop(cx, cy):
        draw_callback(canvas, draw_lock)
        canvas.after(framerate_ms, lambda: animation_loop(cx, cy))
    animation_loop(0, 0)
