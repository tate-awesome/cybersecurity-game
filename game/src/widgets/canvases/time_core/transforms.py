import math

'''
Helper functions for camera, sprites, and drawings. Very useful math with highly granular control
'''

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

def nice_ticks(min_v: float, max_v: float, target_count: int = 5) -> tuple[list[float], float]:
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
