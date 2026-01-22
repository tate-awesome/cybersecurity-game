import customtkinter as ctk
import tkinter as tk

current_scale = 1.0

def zoom_pan_canvas(parent, draw_callback, framerate_ms):
    global current_scale
    current_scale = 1.0

    canvas = tk.Canvas(parent, bg="black")
    canvas.pack(fill="both", expand=True)

    # --- Pan ---
    def start_pan(event):
        canvas.scan_mark(event.x, event.y)
    def do_pan(event):
        canvas.scan_dragto(event.x, event.y, gain=1)
    canvas.bind("<ButtonPress-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)

    # --- Zoom ---
    def zoom(event):
        global current_scale
        factor = 1.0

        if event.delta > 0:
                factor = 1.1
        else:
            factor = 0.9

        # Linux support
        if hasattr(event, "num"):
            if event.num == 4:
                factor = 1.1
            elif event.num == 5:
                factor = 0.9
            

        current_scale *= factor

        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        canvas.scale("all", x, y, factor, factor)
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)

    # --- Reset view ---
    def reset_view(event=None):
        global current_scale
        factor = 1 / current_scale
        current_scale = 1.0
        canvas.scale("all", 0, 0, factor, factor)
        canvas.configure(scrollregion=canvas.bbox("all"))
        # optional: center
        bbox = canvas.bbox("all")
        if bbox:
            x0, y0, x1, y1 = bbox
            canvas.xview_moveto((x0 + x1 - canvas.winfo_width()) / (x1 - x0))
            canvas.yview_moveto((y0 + y1 - canvas.winfo_height()) / (y1 - y0))

    canvas.bind("<Button-2>", reset_view)
    canvas.bind("<Button-3>", reset_view)

    # --- Animation loop ---
    # cx, cy are world coordinates
    def animation_loop(cx, cy):
        canvas.delete("all")
        # Transform world -> screen coordinates
        sx0, sy0 = 0 * current_scale, 0 * current_scale
        sx1, sy1 = cx * current_scale, cy * current_scale

        canvas.create_rectangle(sx0, sy0, sx1, sy1, fill="red", outline="white")

        # Update scroll region so panning works infinitely
        margin = 5000  # extra space around content
        canvas.configure(scrollregion=(-margin, -margin, sx1 + margin, sy1 + margin))

        # Move cx/cy around for demo (like your original callback)
        w = 400
        h = 300
        if cx == 0 and cy == 0:
            cx += 10
        elif cx == 0 and cy == h:
            cy -= 10
        elif cx == w and cy == h:
            cx -= 10
        elif cx == w and cy == 0:
            cy += 10
        elif cx == 0:
            cy -= 10
        elif cx == w:
            cy += 10
        elif cy == 0:
            cx += 10
        elif cy == h:
            cx -= 10

        canvas.after(framerate_ms, lambda: animation_loop(cx, cy))

    animation_loop(0, 0)

root = ctk.CTk()
sw = int(root.winfo_screenwidth()*3/4)
sh = int(root.winfo_screenheight()*3/4)
root.geometry(f"{sw}x{sh}")

zoom_pan_canvas(root, None, 20)

root.mainloop()