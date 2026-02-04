'''
Module for coordinate transforms used in drawing
'''

from customtkinter import CTkCanvas
import math

def rotate(points: list[tuple[float, float]], angle: float, origin: tuple | None=None):
    '''
    Rotates sprite in worldspace
    Angle: radians from 0
    '''
    # Mod angle
    angle = angle % (math.pi * 2)

    # Find origin from average point
    if origin is None:
        origin = [0, 0]
        for x, y in points:
            origin[0] += x
            origin[1] += y
        origin[0] = origin[0] / (len(points))
        origin[1] = origin[1] / (len(points))

    # Create new vertices
    vertices = []
    for sx, sy in points:
        # Center object for rotation
        sprite_x = sx - origin[0]
        sprite_y = sy - origin[1]

        # Trig rotations
        rx = sprite_x * math.cos(angle) - sprite_y * math.sin(angle)
        ry = sprite_x * math.sin(angle) + sprite_y * math.cos(angle)

        # Move sprite back to its origin
        sprite_x = rx + origin[0]
        sprite_y = ry + origin[1]

        vertices.append((sprite_x, sprite_y))

    return vertices

def scale(points: list[tuple[float, float]], mult: float, origin: tuple | None=None):
    '''
    Scales sprite in worldspace
    Mult: multiplier for sprite coordinates
    '''

    # Find origin from average point
    if origin is None:
        origin = [0, 0]
        for x, y in points:
            origin[0] += x
            origin[1] += y
        origin[0] = origin[0] / (len(points))
        origin[1] = origin[1] / (len(points))

    # Create new vertices
    vertices = []
    for sx, sy in points:
        # Center object for scaling
        sprite_x = sx - origin[0]
        sprite_y = sy - origin[1]

        # Scale
        mx = sprite_x * mult
        my = sprite_y * mult

        # Move sprite back to its origin
        sprite_x = mx + origin[0]
        sprite_y = my + origin[1]

        vertices.append((sprite_x, sprite_y))

    return vertices

def affine(points: list[tuple[float, float]], in_bl: tuple[float, float],
                                                in_tr: tuple[float, float],
                                                out_bl: tuple[float, float],
                                                out_tr: tuple[float, float]) -> list[tuple[float, float]]:
    '''
    Converts coordinates from one range to another, matching top right and bottom left of the ranges.
    '''
    
    in_xmin, in_ymin = in_bl
    in_xmax, in_ymax = in_tr
    out_xmin, out_ymin = out_bl
    out_xmax, out_ymax = out_tr

    in_w = in_xmax - in_xmin
    in_h = in_ymax - in_ymin
    out_w = out_xmax - out_xmin
    out_h = out_ymax - out_ymin

    sx = out_w / in_w if in_w != 0 else 1.0
    sy = out_h / in_h if in_h != 0 else 1.0

    out = []
    for x, y in points:
        nx = (x - in_xmin) * sx + out_xmin
        ny = (y - in_ymin) * sy + out_ymin
        out.append((nx, ny))

    return out

def canvas_fit(points: list[tuple[float, float]], in_bl: tuple[float, float],
                                                    in_tr: tuple[float, float],
                                                    canvas: CTkCanvas):
    '''
    Converts coordinates from the incoming plane to the canvas plane.
    Returns: list(tuple)
    '''
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    canvas_bl = (0, h)
    canvas_tr = (w, 0)
    return affine(points, in_bl, in_tr, canvas_bl, canvas_tr)

def padded_fit(points: list[tuple[float, float]], in_bl: tuple[float, float],
                                                    in_tr: tuple[float, float],
                                                    canvas: CTkCanvas,
                                                    padding: float):
    '''
    Converts coordinates from the incoming plane to a plane padded inside the canvas.
    Returns: list(tuple)
    '''
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    p = padding
    canvas_bl = (p, h-p)
    canvas_tr = (w-p, p)
    return affine(points, in_bl, in_tr, canvas_bl, canvas_tr)

def padded_fit_uniform(points: list[tuple[float, float]], in_bl: tuple[float, float],
                                                    in_tr: tuple[float, float],
                                                    canvas: CTkCanvas,
                                                    padding: float):
    '''
    Converts coordinates from the incoming plane to a plane padded inside the canvas.
    Returns: list(tuple)
    '''
    w = canvas.winfo_width()
    h = canvas.winfo_height()

     # 1. Available canvas area (the padded "box" you want to fit inside)
    p = padding
    target_w = w - 2*p
    target_h = h - 2*p

    # 2. Input dimensions
    in_w = in_tr[0] - in_bl[0]
    in_h = in_tr[1] - in_bl[1]

    # 3. Calculate uniform scale (preserving aspect ratio)
    # Using abs() ensures it works even if coordinates are inverted (e.g. y-up vs y-down)
    scale = min(abs(target_w / in_w), abs(target_h / in_h))

    # 4. New dimensions for the fitted rectangle
    fit_w = in_w * scale
    fit_h = in_h * scale

    # 5. Calculate offsets to center the fitted rectangle in the canvas
    # We center it within the area [p, w-p] and [p, h-p]
    offset_x = p + (target_w - abs(fit_w)) / 2
    offset_y = p + (target_h - abs(fit_h)) / 2

    # 6. Define the new target coordinates (fitted_bl and fitted_tr)
    # Adjust for Tkinter's coordinate system (y=0 at top, y=h at bottom)
    fitted_bl = (offset_x, h - offset_y)
    fitted_tr = (offset_x + abs(fit_w), offset_y)

    return affine(points, in_bl, in_tr, fitted_bl, fitted_tr)

def zoom_and_pan(points: list[tuple[float, float]], scale: float, offset: tuple[float, float]):
    '''
    Transforms a figure using the scale and offset
    '''

    tx, ty = offset
    s = scale

    out = []
    for x, y in points:
        x_new = s * x + tx
        y_new = s * y + ty
        
        out.append((x_new, y_new))

    return out

def flatten(points: list[tuple[float, float]]):
    out = []
    for x, y in points:
        out.extend((x, y))
    return out

def translate(points: list[tuple[float, float]], offset: tuple[float, float]):
    '''
    Translates a figure by an offset
    '''
    tx, ty = offset

    out = []
    for x, y in points:
        x_new = x + tx
        y_new = y + ty
        
        out.append((x_new, y_new))

    return out