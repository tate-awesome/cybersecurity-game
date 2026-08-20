import math

from customtkinter import CTkCanvas
import math

'''
Helper functions for camera, sprites, and drawings. Very useful math with highly granular control
'''

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

def right_align(points: list[tuple[float, float]], time_bounds: tuple[float, float], canvas: CTkCanvas) -> list[tuple[float, float]]:
    '''
    Aligns the right edge of the points to the right edge of the canvas
    '''
    if not points:
        return []

    # Find the rightmost x-coordinate (time) in the points
    max_x = time_bounds[1]

    # Get the width of the canvas
    canvas_width = canvas.winfo_width()

    # Calculate the offset needed to align the right edge of the points with the right edge of the canvas
    offset_x = canvas_width - max_x

    # Apply the offset to all points
    aligned_points = [(x + offset_x, y) for x, y in points]

    return aligned_points

def padded_vertical_fit(points: list[tuple[float, float]], data_bounds: tuple[float, float], canvas: CTkCanvas, padding: float):
    '''
    Converts coordinates from the incoming dataset to a padded area inside the canvas. Preserves aspect ratio and centers the figure in the canvas.
    Returns: list(tuple)
    '''
    if not points:
        return []

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # 1. Get max and min of the incoming points    
    min_y = data_bounds[0]
    max_y = data_bounds[1]

    # 2. Get the padded bounds of the canvas
    padded_bl = (padding, padding)
    padded_tr = (w - padding, h - padding)

    return affine(points, (0, min_y), (w, max_y), padded_bl, padded_tr)

def zoom_and_pan(points: list[tuple[float, float]], vertical_scale: float, time_scale: float, time_offset: float):
    '''
    Transforms a figure using the scale and offset
    '''

    ox, oy = time_offset, 0.0
    sx, sy = time_scale, vertical_scale

    out = []
    for x, y in points:
        x_new = sx * x + ox
        y_new = sy * y + oy
        
        out.append((x_new, y_new))

    return out

def zoom_and_pan_reverse(points: list[tuple[float, float]], vertical_scale: float, time_scale: float, time_offset: float):
    ox, oy = time_offset, 0.0
    sx, sy = time_scale, vertical_scale

    out = []
    for x, y in points:
        x_new = (x - ox)/sx
        y_new = (y - oy)/sy

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

def get_bearing(origin: tuple[float, float], target: tuple[float, float]):
    '''
    Gets an angle from two points
    '''
    x = target[0] - origin[0]
    y = target[1] - origin[1]
    return math.atan2(y, x)

def get_arc_points(center: tuple[float, float], radius: float, start_angle: float, end_angle: float, num_points: int=20):
    '''
    Gets points along an arc defined by the parameters
    '''
    cx, cy = center
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        angle = start_angle + t * (end_angle - start_angle)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

def padded_fit_vertical_snap_right(points: list[tuple[float, float]],
                                   canvas: CTkCanvas,
                                   padding: float):
    '''
    Converts coordinates from the incoming plane to a plane padded vertically
    inside the canvas. Horizontal scaling is ignored, but the right edge of
    the input is snapped to the right edge of the canvas.

    Returns: list(tuple)
    '''

    if not points:
        return []

    w = canvas.winfo_width()
    h = canvas.winfo_height()
    p = padding

    # Compute bounds of incoming points
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    in_h = max_y - min_y
    if in_h == 0:
        scale_y = 1
    else:
        scale_y = (h - 2 * p) / abs(in_h)

    # Height after scaling
    fit_h = abs(in_h) * scale_y

    # Vertically center within the padded region
    offset_y = p + (h - 2 * p - fit_h) / 2

    transformed = []

    for x, y in points:
        # No horizontal scaling. Right edge snaps to canvas padding.
        new_x = x + (w - p - max_x)

        # Scale vertically about the minimum y.
        new_y = h - (offset_y + (y - min_y) * scale_y)

        transformed.append((new_x, new_y))

    return transformed

def zoom_and_pan_horizontal(points: list[tuple[float, float]], scale: float, offset: tuple[float, float]):
    '''
    Transforms a figure using the scale and offset - horizontal only
    '''

    tx, ty = offset
    s = scale

    out = []
    for x, y in points:
        if tx > 0:
            tx = 0
        x_new = s * x + tx

        out.append((x_new, y))

    return out

# --------------------------------------------------------------------------------------------------------------------------
#                                                       AXIS TICKS
# --------------------------------------------------------------------------------------------------------------------------

def nice_number(value: float, round_: bool) -> float:
    '''
    Rounds value to a "nice" number: a power of ten multiplied by 1, 2, or 5.
    round_=True snaps to the nearest nice number, round_=False rounds up.
    '''
    if value <= 0:
        return 0.0

    exponent = math.floor(math.log10(value))
    fraction = value / (10 ** exponent)

    if round_:
        if fraction < 1.5:
            nice_fraction = 1
        elif fraction < 3:
            nice_fraction = 2
        elif fraction < 7:
            nice_fraction = 5
        else:
            nice_fraction = 10
    else:
        if fraction <= 1:
            nice_fraction = 1
        elif fraction <= 2:
            nice_fraction = 2
        elif fraction <= 5:
            nice_fraction = 5
        else:
            nice_fraction = 10

    return nice_fraction * (10 ** exponent)

def nice_ticks(min_v: float, max_v: float, target_count: int = 5):
    '''
    Picks whole-number/nice-fraction tick values (step size 1, 2, or 5 x10^n) that
    cover [min_v, max_v]. Returns (ticks, step).
    '''
    if min_v > max_v:
        min_v, max_v = max_v, min_v

    span = max_v - min_v
    if span <= 0:
        # Degenerate range (e.g. a flat signal) - open up a small window around it
        half = (abs(min_v) * 0.05) or 0.5
        min_v -= half
        max_v += half
        span = max_v - min_v

    raw_step = span / max(target_count - 1, 1)
    step = nice_number(raw_step, True)

    nice_min = math.floor(min_v / step) * step
    nice_max = math.ceil(max_v / step) * step

    count = int(round((nice_max - nice_min) / step)) + 1
    ticks = [nice_min + i * step for i in range(count)]
    return ticks, step

def decimals_for_step(step: float) -> int:
    '''
    Minimum number of decimal places needed to tell values spaced `step` apart.
    '''
    step = abs(step)
    if step <= 0:
        return 0
    for decimals in range(0, 8):
        if abs(round(step, decimals) - step) < 1e-9 * max(1.0, step):
            return decimals
    return 8

def format_tick(value: float, decimals: int) -> str:
    '''
    Formats a tick value with a fixed number of decimals, avoiding "-0".
    '''
    value = round(value, decimals)
    if value == 0:
        value = 0.0
    return f"{value:.{decimals}f}"

def format_max_decimals(value: float, max_decimals: int) -> str:
    '''
    Formats value with up to max_decimals decimal places, dropping trailing
    zeros (and the decimal point itself if nothing is left after them).
    '''
    value = round(value, max_decimals)
    if value == 0:
        value = 0.0
    text = f"{value:.{max_decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text

def choose_time_step(pixels_per_unit: float, min_label_spacing_px: float, candidates: list[float]) -> float:
    '''
    Picks the smallest candidate step whose on-screen spacing is at least
    min_label_spacing_px, so labels are rarely crowded together. Falls back to
    doubling the largest candidate if even it is too small on screen.
    '''
    if pixels_per_unit <= 0 or not candidates:
        return candidates[-1] if candidates else 1.0

    for step in candidates:
        if step * pixels_per_unit >= min_label_spacing_px:
            return step

    step = candidates[-1]
    while step * pixels_per_unit < min_label_spacing_px:
        step *= 2
    return step