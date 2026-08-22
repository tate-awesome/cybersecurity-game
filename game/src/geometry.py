'''
Pure 2D point-list geometry functions shared by drawing/transformations.py,
widgets/canvases/core/transforms.py, and widgets/canvases/time_core/transforms.py.
No canvas/camera coupling - safe to use from any coordinate system.
'''

import math


def rotate(points: list[tuple[float, float]], angle: float, origin: tuple[float, float] | None = None) -> list[tuple[float, float]]:
    '''
    Rotates sprite in worldspace
    Angle: radians from 0
    '''
    # Mod angle
    angle = angle % (math.pi * 2)

    # Find origin from average point
    if origin is None:
        sum_x = sum(x for x, _ in points)
        sum_y = sum(y for _, y in points)
        origin = (sum_x / len(points), sum_y / len(points))

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


def scale(points: list[tuple[float, float]], mult: float, origin: tuple[float, float] | None = None) -> list[tuple[float, float]]:
    '''
    Scales sprite in worldspace
    Mult: multiplier for sprite coordinates
    '''

    # Find origin from average point
    if origin is None:
        sum_x = sum(x for x, _ in points)
        sum_y = sum(y for _, y in points)
        origin = (sum_x / len(points), sum_y / len(points))

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


def flatten(points: list[tuple[float, float]]) -> list[float]:
    out = []
    for x, y in points:
        out.extend((x, y))
    return out


def translate(points: list[tuple[float, float]], offset: tuple[float, float]) -> list[tuple[float, float]]:
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


def get_bearing(origin: tuple[float, float], target: tuple[float, float]) -> float:
    '''
    Gets an angle from two points
    '''
    x = target[0] - origin[0]
    y = target[1] - origin[1]
    return math.atan2(y, x)


def get_arc_points(center: tuple[float, float], radius: float, start_angle: float, end_angle: float, num_points: int = 20) -> list[tuple[float, float]]:
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


def apply_scale_about(scale: float, offset: tuple[float, float], focus: tuple[float, float], k: float) -> tuple[float, tuple[float, float]]:
    '''
    Computes the new (scale, offset) that result from zooming by factor k about
    a focus point (e.g. the mouse position), keeping that point fixed on screen.
    Shared by widgets/map.py's Map and widgets/canvases/core/camera.py's Camera.
    '''
    cx, cy = focus
    tx, ty = offset

    new_scale = k * scale
    new_offset = (
        cx + k * (tx - cx),
        cy + k * (ty - cy),
    )
    return new_scale, new_offset
