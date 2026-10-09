import colorsys

# Builds a full palette (the same 11 keys as style.PALETTES) from an accent
# color and a "hierarchy" - how far apart the surface layers sit. Hierarchies
# live in assets/themes/generator/hierarchies.json, each a set of HSL
# lightness steps for both modes:
#   dark:  dr = root's lightness, then d1/d2/d3 = the step up to panel,
#          widget and field; ds = how much of the accent's hue the surfaces carry
#   light: lr = root's lightness, then l1/l2 = the step down to panel and
#          widget, l3 = widget to border (field is always white); ls = saturation
#   inset (optional): how far below root an inset field sits - see inset()
# tint scales ds/ls - how much the accent bleeds into the surfaces (0 = gray,
# 1 = as the hierarchy has it)
# Plain colorsys, no Qt, so it can be checked without the app running.

DEFAULT_INSET = 0.045
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


def contrast(a: str, b: str) -> float:
    '''WCAG contrast ratio between two "#rrggbb" colors (1 to 21).'''
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def generate(accent: str, hierarchy: dict[str, float], mode: str, inset: float | None = None,
             tint: float = 1.0) -> dict[str, str]:
    '''The palette for one mode ("dark"/"light") of accent + hierarchy, with an inset field (dark only) if inset is given.'''
    h, accent_l, accent_s = _hls(accent)
    if mode == "dark":
        s = min(1.0, hierarchy["ds"] * tint)
        root = hierarchy["dr"]
        steps = [root, root + hierarchy["d1"]]
        steps += [steps[1] + hierarchy["d2"], steps[1] + hierarchy["d2"] + hierarchy["d3"]]
        border = steps[2] + 0.4 * hierarchy["d3"]
        hover = border + 0.05
        if inset is not None:
            steps[3] = root - inset
        text = _hex(h, 0.92, 0.4)
    else:
        s = min(1.0, hierarchy["ls"] * tint)
        steps = [hierarchy["lr"], hierarchy["lr"] - hierarchy["l1"]]
        steps += [steps[1] - hierarchy["l2"], 1.0]
        border = steps[2] - hierarchy["l3"]
        hover = border - 0.06
        text = _hex(h, 0.14, 0.3)
    colors = {key: _hex(h, l, s) for key, l in zip(("root", "panel", "widget", "field"), steps)}

    lightness = accent_l
    if mode == "dark":
        while contrast(accent, colors["panel"]) < DARK_ACCENT_CONTRAST and lightness < 1.0:
            lightness += 0.01
            accent = _hex(h, lightness, accent_s)
    else:
        while contrast(accent, "#ffffff") < LIGHT_ACCENT_CONTRAST and lightness > 0.0:
            lightness -= 0.01
            accent = _hex(h, lightness, accent_s)
    accent_text = ACCENT_TEXT_DARK if contrast(accent, ACCENT_TEXT_DARK) >= contrast(accent, "#ffffff") else "#ffffff"

    border_color = _hex(h, border, s)
    colors.update(field_text=text, text=text, accent=accent, accent_text=accent_text,
                  border=border_color, scrollbar=border_color, scrollbar_hover=_hex(h, hover, s))
    return colors


def inset(colors: dict[str, str], amount: float = DEFAULT_INSET) -> dict[str, str]:
    '''A copy of a (dark) palette whose field sits below root instead of above it - recessed inputs.'''
    h, l, s = _hls(colors["root"])
    return {**colors, "field": _hex(h, l - amount, s)}
