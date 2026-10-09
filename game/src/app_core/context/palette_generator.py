import colorsys

# Builds a full palette (the same 11 keys as style.PALETTES) from an accent
# color and a "hierarchy" - how far apart the surface layers sit. Hierarchies
# live in assets/themes/generator/hierarchies.json, each with a block per mode.
# Lightness is CIE L* (0 black - 100 white): perceptual, so a step of the same
# size looks the same in both modes, at any height, and for every accent hue.
#   dark:  root = root's L*, then panel/widget/field = the step up to each
#   light: root = root's L*, then panel/widget = the step down to each
#          (field is always white)
#   tint:  saturation the surfaces take from the accent's hue (0 = gray)
#   inset (optional): how far below the darkest layer an inset field sits - see inset()
# The rest are the user's adjustments (see Style.theme_adjust):
#   tint   - scales the hierarchy's tint (0 = gray, 1 = as the hierarchy has it)
#   steps  - scales every step (0 = flat, 1 = as the hierarchy has it)
#   height - moves root, and everything stacked on it, by this much L*
# Borders aren't part of a hierarchy - see borders().
# Plain colorsys, no Qt, so it can be checked without the app running.

# How far below the darkest layer an inset field sits, for themes without their own amount (L*)
DEFAULT_INSET = 3.7
# How far a border sits beyond the surfaces it separates, at border strength
# 1 (L*): lighter than the lightest in dark mode, darker than the darkest in
# light mode. Light mode needs more - a thin dark line between bright areas
# gets washed out by the light the eye scatters into it
BORDER_CONTRAST = {"dark": 6.0, "light": 12.0}
# How much further a hovered scrollbar handle goes (L*)
SCROLLBAR_HOVER_STEP = 6.0
# Dark accents are lightened until they stand out this much from the panel;
# light accents are darkened until they stand out this much from white
DARK_ACCENT_CONTRAST = 4.5
LIGHT_ACCENT_CONTRAST = 3.4
ACCENT_TEXT_DARK = "#0d1417"


def _hls(hex_color: str) -> tuple[float, float, float]:
    return colorsys.rgb_to_hls(*(int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)))


def _hex(h: float, l: float, s: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h, min(1.0, max(0.0, l)), s)
    return "#%02x%02x%02x" % tuple(round(c * 255) for c in (r, g, b))


def _luminance(hex_color: str) -> float:
    channels = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def lightness(hex_color: str) -> float:
    '''A color's CIE L* - perceived lightness, 0 (black) to 100 (white).'''
    y = _luminance(hex_color)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def _at_lightness(h: float, s: float, target: float) -> str:
    '''The color of this HSL hue and saturation whose L* is closest to target.'''
    target = min(100.0, max(0.0, target))
    low, high = 0.0, 1.0
    for _ in range(24):  # lightness() only grows with HSL lightness, so bisect
        middle = (low + high) / 2
        if lightness(_hex(h, middle, s)) < target:
            low = middle
        else:
            high = middle
    return _hex(h, (low + high) / 2, s)


def contrast(a: str, b: str) -> float:
    '''WCAG contrast ratio between two "#rrggbb" colors (1 to 21).'''
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def generate(accent: str, hierarchy: dict, mode: str, inset: float | None = None, tint: float = 1.0,
             steps: float = 1.0, height: float = 0.0, border: float = 1.0) -> dict[str, str]:
    '''
    The palette for one mode ("dark"/"light") of accent + hierarchy, with
    an inset field (see inset()) if inset (L*) is given, and borders at the
    given strength (see borders).
    '''
    h, accent_l, accent_s = _hls(accent)
    layers = hierarchy[mode]
    s = min(1.0, layers["tint"] * tint)
    root = layers["root"] + height
    if mode == "dark":
        panel = root + layers["panel"] * steps
        widget = panel + layers["widget"] * steps
        field = widget + layers["field"] * steps
        text = _hex(h, 0.92, 0.4)
    else:
        panel = root - layers["panel"] * steps
        widget = panel - layers["widget"] * steps
        field = 100.0
        text = _hex(h, 0.14, 0.3)
    if inset is not None:
        field = min(root, panel, widget) - inset
    colors = {key: _at_lightness(h, s, value) for key, value in
              (("root", root), ("panel", panel), ("widget", widget), ("field", field))}

    shade = accent_l
    if mode == "dark":
        while contrast(accent, colors["panel"]) < DARK_ACCENT_CONTRAST and shade < 1.0:
            shade += 0.01
            accent = _hex(h, shade, accent_s)
    else:
        while contrast(accent, "#ffffff") < LIGHT_ACCENT_CONTRAST and shade > 0.0:
            shade -= 0.01
            accent = _hex(h, shade, accent_s)
    accent_text = ACCENT_TEXT_DARK if contrast(accent, ACCENT_TEXT_DARK) >= contrast(accent, "#ffffff") else "#ffffff"

    colors.update(field_text=text, text=text, accent=accent, accent_text=accent_text, border=_hex(h, 0.5, s))
    return borders(colors, mode, border, scrollbars=True)


def borders(colors: dict[str, str], mode: str, strength: float = 1.0, scrollbars: bool = False) -> dict[str, str]:
    '''
    A copy of a palette whose border sits BORDER_CONTRAST * strength beyond
    the surfaces it separates (panel, widget, field) - keeping the border's
    own hue and saturation, so a theme's borders stay its own color. With
    scrollbars, the scrollbar handle matches the border, and goes further
    still when hovered.
    '''
    surfaces = [lightness(colors[key]) for key in ("panel", "widget", "field")]
    direction = 1 if mode == "dark" else -1
    target = (max(surfaces) if mode == "dark" else min(surfaces)) + direction * BORDER_CONTRAST[mode] * strength
    h, _, s = _hls(colors["border"])
    result = {**colors, "border": _at_lightness(h, s, target)}
    if scrollbars:
        result["scrollbar"] = result["border"]
        result["scrollbar_hover"] = _at_lightness(h, s, target + direction * SCROLLBAR_HOVER_STEP)
    return result


def inset(colors: dict[str, str], amount: float = DEFAULT_INSET) -> dict[str, str]:
    '''
    A copy of a palette whose field sits amount L* below its darkest layer
    (root, panel or widget) - recessed inputs, cut into whatever they're on.
    In dark mode that's below the page; in light mode, a gray well below the
    cards instead of white.
    '''
    darkest = min(("root", "panel", "widget"), key=lambda key: lightness(colors[key]))
    h, _, s = _hls(colors[darkest])
    return {**colors, "field": _at_lightness(h, s, lightness(colors[darkest]) - amount)}
