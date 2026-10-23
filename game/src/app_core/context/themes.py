'''
Theme files - assets/themes/<family>.json, and the user's own in
user_data/themes. A theme is a list of materials: what each kind of
widget is made of, in each mode -

    "materials": {"panel": {"dark": {"color": "#151a24", "opacity": 0.5},
                            "light": {"color": "#f1f5ff", "opacity": 0.6}},
                  "text": {"dark": {"color": "#e3eaf5"}, "light": {...}}, ...}

"color" is "#rrggbb"; "opacity" is 0-1 (1 = solid), for every material
but the text and line ones (see INK_MATERIALS), which are always solid.
Any material or mode left out gets MATERIALS' default.

Beside the materials: a "label" (its name), optionally a "note" (its
description - for copied themes, where it came from), "transparency"
(false for a theme that's always solid - see Style.allows_transparency),
each kind of button's corner radius in px ("button_radius" and
"menu_button_radius" - see BUTTON_KINDS), and for bundled themes a
"kind" ("original" or "copied") and which modes are "derived" rather
than copied (see Style.preset_name). A theme with only one mode lists it
in "modes" (e.g. ["dark"] - see theme_modes); left out, it has both.

Panels are made of three materials, from the top down (and any page
can use them the same way):
    "panel"  the drawer - a panel's menu bar and the frame around its
             contents, all one piece (see "panel_frame")
    "card"   the contents, just inside the drawer - what takes up most of
             it: cards, consoles, charts and canvases, tables and trees
    "field"  the deepest, and smaller - text boxes, the gaps between
             cards, every other row of a table or tree (see
             "alternate_row"), scrollbar troughs

Each kind of button has its own materials: its background, its
background on hover, its outline, its text and its text on hover. An
opacity of 0 leaves out a background or an outline - a ghost button, or
an outline with nothing inside it. A theme from before these existed
gets them from its other materials (see INHERITED), so it looks as it did.

A surface material can also have a "gradient" - {"angle": degrees (0 =
top to bottom, 90 = left to right), "stops": [[0-1, "#rrggbb", opacity],
...]} - drawn instead of its plain color (which hand-drawn widgets and
the editor's swatch still use). See read_gradient and Style.css.

More of what a theme looks like, all optional - left out, a theme looks
as it did before they existed (see STYLE_DEFAULTS):
    "background"       false turns the animated page background off in
                       this theme behind workspaces and settings - title
                       menu pages always keep it (if the user has it on)
    "background_blur"  px to blur the page background by (frosted glass),
                       on pages that blur it at all - instead of their own
    "panel_radius"     panels' corner radius in px
    "panel_frame"      px of the panel material around a panel's contents
                       (left, right and below - its menu bar is above)
    "panel_border_width" px - panels' outlines
    "panel_gap"        px between a page's panels (left out: the usual gap)
    "panel_shadow"     a shadow around each panel: {"x", "y", "blur" (px),
                       "dark": {"color", "opacity"}, "light": {...}} -
                       blur 0 is a hard shadow, x = y = 0 a glow
    "panel_light"      a second one, the same shape - in a light color, the
                       other way from the shadow, it's the lit edge of a
                       panel lit from one side
    "line_width"       px - the outlines of buttons, fields, tables and tabs
    "bevel"            true draws 3D outlines - raised buttons, panels and
                       headers, sunken fields (an old desktop's look)
    "button_shadow"    px - a hard shadow below and right of each button,
                       in its outline's color, that it presses into
    "button_lift"      px - how far buttons seem to stand off the surface:
                       a soft shadow below and right of each, and a lit
                       top and left edge (see Style.lift_button)
    "font_family"      the font for the interface's text (not consoles)
    "bold_buttons"     true makes buttons' text bold
    "scrollbar_radius" px - scrollbar handles' corners (left out: round ends)
    "scrollbar_inset"  px of track left around each scrollbar handle
    "scrollbar_outline" true outlines scrollbar handles like fields
    "card_outline"     true outlines cards like fields, so cards the same
                       color as what's around them still stand apart
    "noise_gradient"   a slowly drifting gradient laid out by a noise map,
                       over the window's color, behind the background
                       visual: {"dark": ["#rrggbb", ...], "light": [...]} -
                       the gradient's colors, 2 to 5
    "plasma"           the same, but laid out by a plasma - waves rippling
                       through each other - instead: {"dark": [...],
                       "light": [...]}, 2 to 7 colors (see paint_plasma)
    "abyss"            a deep-sea night in these colors, over the window's
                       color: soft glows drifting, specks twinkling, faint
                       diagram lines - {"dark": [...], "light": [...]}, 2
                       to 7 colors (see paint_abyss)
    "grain"            0-100 - a paper-like speckle over the page and its
                       surfaces (see Style.TEXTURE_MATERIALS), this strong
    "grain_stretch"    1-16 - how many times wider than tall each speck of
                       grain is: streaks, like wood's
    "scanlines"        0-100 - dark lines across the whole window, over
                       everything on it, like an old CRT's - this strong
                       (see Scanlines)
    "line_colors"      {"dark": ["#rrggbb", ...], "light": [...]} - plain
                       buttons and panels' outlines each take one of these
                       instead of the theme's one (see Style.line_color),
                       like the lines on a metro map - each panel's
                       buttons the same one as its outline

Older files had a "palette" of named colors per mode that materials
pointed into (or, older still, no materials - just the palette's modes at
the top level). read_theme still reads both, looking each material's
color up in the palette.

No Qt here, so scripts can read and write themes too.
'''
import copy
import math
import re

THEME_MODES = ("dark", "light")

# Built-in blue, which every material's default comes from (see MATERIALS),
# as the palette older theme files named their colors from (see read_theme)
FALLBACK_PALETTE = {
    "dark": {
        "root": "#10141d", "panel": "#151a24", "widget": "#28303d",
        "field": "#353e4d", "field_text": "#e3eaf5", "text": "#e3eaf5",
        "accent": "#2979ff", "accent_text": "#ffffff", "border": "#2e3745",
        "scrollbar": "#2e3745", "scrollbar_hover": "#3e4755",
        "muted_text": "#8b95a7", "good": "#4ade80", "warning": "#fbbf24", "bad": "#f87171",
        "incoming": "#60a5fa", "outgoing": "#fb923c", "hot": "#f87171", "cold": "#60a5fa",
        "chart_1": "#60a5fa", "chart_2": "#fb923c", "chart_3": "#4ade80", "chart_4": "#f472b6",
        "chart_5": "#facc15", "chart_6": "#a78bfa", "chart_7": "#2dd4bf", "chart_8": "#f87171",
    },
    "light": {
        "root": "#d9e2f5", "panel": "#f1f5ff", "widget": "#e4ebfd",
        "field": "#ffffff", "field_text": "#1a2233", "text": "#1a2233",
        "accent": "#1e6fe0", "accent_text": "#ffffff", "border": "#d9e2f5",
        "scrollbar": "#d9e2f5", "scrollbar_hover": "#bfc7d8",
        "muted_text": "#5b6577", "good": "#15803d", "warning": "#b45309", "bad": "#b91c1c",
        "incoming": "#1d4ed8", "outgoing": "#c2410c", "hot": "#b91c1c", "cold": "#1d4ed8",
        "chart_1": "#1d4ed8", "chart_2": "#c2410c", "chart_3": "#15803d", "chart_4": "#be185d",
        "chart_5": "#a16207", "chart_6": "#6d28d9", "chart_7": "#0f766e", "chart_8": "#b91c1c",
    },
}

# Every material - the kinds of widget a theme styles - with the palette
# color older files gave it, and its default opacity. Labels:
# "theme_materials_<name>" names one, "theme_materials_notes_<name>" says
# what uses it.
MATERIAL_SOURCES: dict[str, tuple[str, float]] = {
    # Surfaces - backgrounds, which can be see-through
    "window": ("root", 1.0),             # the window and page background
    "panel": ("panel", 0.5),             # panels' drawer: their menu bar and the frame around their contents
    "panel_border": ("widget", 0.5),     # panel outlines
    "card": ("widget", 0.5),             # what's in the drawer: cards, consoles, charts, rows
    "field": ("field", 0.5),             # the deepest: text boxes, gaps between cards, scrollbar troughs
    "button": ("accent", 0.75),          # buttons
    "button_hover": ("accent", 0.75),    # buttons under the mouse
    "button_border": ("accent", 0.0),    # buttons' outlines
    "menu_button": ("accent", 0.75),         # menu buttons - the title menu's and the workspace list's
    "menu_button_hover": ("accent", 0.75),   # menu buttons under the mouse, and the selected workspace
    "menu_button_border": ("accent", 0.0),   # menu buttons' outlines
    "overlay": ("panel", 1.0),           # dropdown overlays
    "overlay_card": ("widget", 1.0),     # cards inside dropdown overlays
    "tab": ("widget", 0.5),              # tabs
    "tab_selected": ("accent", 1.0),     # the selected tab
    "table_header": ("widget", 0.5),     # table and tree headers
    "alternate_row": ("widget", 0.5),    # every other row of tables and trees - like "field"
    "selection": ("accent", 1.0),        # selected items, and cells of tables
    "row_selection": ("accent", 1.0),    # selected rows of trees - the packet console's
    "scrollbar": ("scrollbar", 1.0),     # scrollbar handles
    "tooltip": ("panel", 1.0),           # tooltips
    "footer": ("widget", 1.0),           # the bar along the bottom of the window
    # Text and lines - always solid (see INK_MATERIALS)
    "text": ("text", 1.0),                        # all other text
    "field_text": ("field_text", 1.0),            # text in fields
    "accent_text": ("accent_text", 1.0),          # text on selections and the selected tab
    "menu_bar_text": ("text", 1.0),               # titles and labels on panels' menu bars
    "button_text": ("accent_text", 1.0),          # text on buttons
    "button_hover_text": ("accent_text", 1.0),    # text on buttons under the mouse
    "menu_button_text": ("accent_text", 1.0),        # text on menu buttons
    "menu_button_hover_text": ("accent_text", 1.0),  # text on menu buttons under the mouse, and the selected workspace
    "accent": ("accent", 1.0),                    # highlights: focus outlines, checked boxes, slider handles, overlay outlines
    "border": ("border", 1.0),                    # outlines of fields, tables and tabs
    "scrollbar_hover": ("scrollbar_hover", 1.0),  # hovered scrollbar handles
    # Data colors - also always solid (see DATA_MATERIALS)
    "muted_text": ("muted_text", 1.0),  # quieter text: column headers, hints, things that are off
    "good": ("good", 1.0),              # status that's fine: on, connected, running
    "warning": ("warning", 1.0),        # status worth a look: off, waiting
    "bad": ("bad", 1.0),                # status that's wrong: errors, disconnected
    "incoming": ("incoming", 1.0),      # what comes in: received paths and boats, the other hosts
    "outgoing": ("outgoing", 1.0),      # what goes out: sent paths and boats, this host
    "hot": ("hot", 1.0),                # heat: hotness, heaters
    "cold": ("cold", 1.0),              # cold: coldness
    **{f"chart_{i}": (f"chart_{i}", 1.0) for i in range(1, 9)},  # strip chart lines, in order
}
# The colors data is drawn in - text states, models and charts - kept
# apart on canvases and the card they sit on, in every theme and mode.
# Charts cycle through chart_1-8, so their lines stay apart from each other too.
CHART_COLORS = tuple(f"chart_{i}" for i in range(1, 9))
DATA_MATERIALS = ("muted_text", "good", "warning", "bad", "incoming", "outgoing", "hot", "cold") + CHART_COLORS
INK_MATERIALS = ("text", "field_text", "menu_bar_text", "accent_text", "accent", "border", "scrollbar_hover",
                 "button_text", "button_hover_text", "menu_button_text", "menu_button_hover_text") + DATA_MATERIALS

# The kinds of button a theme styles separately - each "<kind>" material is
# its background, with "<kind>_hover", "<kind>_border", "<kind>_text" and
# "<kind>_hover_text", and "<kind>_radius" its corners (see the module
# docstring). Menu buttons are the title menu's and the workspace list's.
BUTTON_KINDS = ("button", "menu_button")
DEFAULT_BUTTON_RADIUS = 4
MAX_BUTTON_RADIUS = 24

# Materials a theme may leave out, made instead from another of its own
# materials - (that material, how far toward white (+) or black (-), and
# an opacity, or None to keep that material's) - so a theme from before
# they existed looks as it did: buttons lighten on hover, keep their text
# on hover, have no outline, and menu buttons look like other buttons.
# In order - each can come from one made before it.
INHERITED: dict[str, tuple[str, float, float | None]] = {
    "menu_bar_text": ("text", 0.0, None),
    "row_selection": ("selection", 0.0, None),
    "button_hover": ("button", 0.15, None),
    "button_border": ("button", 0.0, 0.0),
    "button_text": ("accent_text", 0.0, None),
    "button_hover_text": ("button_text", 0.0, None),
    "menu_button": ("button", 0.0, None),
    "menu_button_hover": ("button_hover", 0.0, None),
    "menu_button_border": ("button_border", 0.0, None),
    "menu_button_text": ("button_text", 0.0, None),
    "menu_button_hover_text": ("button_hover_text", 0.0, None),
}
MATERIALS: dict[str, dict[str, dict]] = {
    name: {mode: {"color": FALLBACK_PALETTE[mode][source], "opacity": opacity} for mode in THEME_MODES}
    for name, (source, opacity) in MATERIAL_SOURCES.items()
}

# The color names page settings and hand-drawn widgets use (e.g.
# "model_colors": {"ocean": "field"} - see Style.color), and the material
# each one is now
COLOR_NAMES: dict[str, str] = {
    "root": "window", "panel": "panel", "widget": "card", "field": "field", "field_text": "field_text",
    "text": "text", "accent": "accent", "accent_text": "accent_text", "border": "border",
    "scrollbar": "scrollbar", "scrollbar_hover": "scrollbar_hover",
}

# The look settings beside the materials (see the module docstring), and
# what a theme without one gets
STYLE_DEFAULTS: dict = {
    "background": True,
    "background_blur": None,
    "panel_radius": 10,
    "panel_frame": 6,
    "panel_border_width": 2,
    "panel_gap": None,
    "panel_shadow": None,
    "panel_light": None,
    "line_width": 1,
    "bevel": False,
    "button_shadow": 0,
    "button_lift": 0,
    "font_family": None,
    "bold_buttons": False,
    "scrollbar_radius": None,
    "scrollbar_inset": 0,
    "scrollbar_outline": False,
    "card_outline": False,
    "noise_gradient": None,
    "plasma": None,
    "abyss": None,
    "grain": 0,
    "grain_stretch": 1,
    "scanlines": 0,
    "line_colors": None,
}
MAX_PANEL_RADIUS = 24
MAX_PANEL_FRAME = 16
MAX_BACKGROUND_BLUR = 64

HEX_PATTERN = re.compile(r"#[0-9a-fA-F]{6}")


def is_hex(value) -> bool:
    return isinstance(value, str) and HEX_PATTERN.fullmatch(value) is not None


def _old_palette(data: dict) -> dict | None:
    '''An older file's palette (see the module docstring) - each mode's named colors - or None.'''
    palette = data.get("palette")
    if palette is None and all(isinstance(data.get(mode), dict) for mode in THEME_MODES):
        palette = {mode: data[mode] for mode in THEME_MODES}
    if not isinstance(palette, dict) or not all(isinstance(palette.get(mode), dict) for mode in THEME_MODES):
        return None
    return palette


def shade(hex_color: str, amount: float) -> str:
    '''hex_color blended toward white (amount > 0) or black (amount < 0) by that fraction.'''
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    target = 255 if amount > 0 else 0
    r, g, b = (int(v + (target - v) * abs(amount)) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def read_gradient(value) -> dict | None:
    '''A material's "gradient" (see the module docstring) cleaned up - None if it isn't one, or has under two stops.'''
    if not isinstance(value, dict) or not isinstance(value.get("stops"), list):
        return None
    stops = []
    for stop in value["stops"]:
        if (isinstance(stop, (list, tuple)) and len(stop) == 3 and isinstance(stop[0], (int, float))
                and is_hex(stop[1]) and isinstance(stop[2], (int, float))):
            stops.append([min(1.0, max(0.0, float(stop[0]))), stop[1].lower(), min(1.0, max(0.0, float(stop[2])))])
    if len(stops) < 2:
        return None
    angle = value.get("angle", 0)
    return {"angle": float(angle) if isinstance(angle, (int, float)) else 0.0, "stops": sorted(stops, key=lambda stop: stop[0])}


def gradient_points(angle: float) -> tuple[float, float, float, float]:
    '''Where a gradient at angle (see the module docstring) starts and ends, in its widget's 0-1 box: x1, y1, x2, y2.'''
    radians = math.radians(angle)
    dx, dy = math.sin(radians) / 2, math.cos(radians) / 2
    return 0.5 - dx, 0.5 - dy, 0.5 + dx, 0.5 + dy


def style_setting(info: dict, key: str):
    '''One of STYLE_DEFAULTS from a theme's info (see read_theme) - its default if missing or the wrong type.'''
    default = STYLE_DEFAULTS[key]
    value = info.get(key, default)
    if key in ("background", "bevel", "bold_buttons", "scrollbar_outline", "card_outline"):
        return value if isinstance(value, bool) else default
    if key == "font_family":
        return value if isinstance(value, str) and value.strip() else None
    if key in ("noise_gradient", "plasma", "abyss"):
        if not isinstance(value, dict):
            return None
        most = 5 if key == "noise_gradient" else 7
        colors = {mode: [c.lower() for c in value.get(mode, []) if is_hex(c)][:most] for mode in THEME_MODES}
        return colors if all(len(c) >= 2 for c in colors.values()) else None
    if key == "line_colors":
        if not isinstance(value, dict):
            return None
        colors = {mode: [c.lower() for c in value.get(mode, []) if is_hex(c)][:8] for mode in THEME_MODES}
        return colors if all(colors.values()) else None
    if key in ("panel_shadow", "panel_light"):
        if not isinstance(value, dict):
            return None
        numbers = {name: value.get(name, 0) for name in ("x", "y", "blur")}
        if not all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in numbers.values()):
            return None
        shadow = {name: int(min(48, max(-48, n))) for name, n in numbers.items()}
        shadow["blur"] = max(0, shadow["blur"])
        for mode in THEME_MODES:
            entry = value.get(mode) if isinstance(value.get(mode), dict) else {}
            opacity = entry.get("opacity", 0.4)
            shadow[mode] = {"color": entry["color"].lower() if is_hex(entry.get("color")) else "#000000",
                            "opacity": min(1.0, max(0.0, float(opacity))) if isinstance(opacity, (int, float)) else 0.4}
        return shadow
    if value is None or not isinstance(value, (int, float)) or isinstance(value, bool):
        return default
    limits = {"background_blur": (0, MAX_BACKGROUND_BLUR), "panel_radius": (0, MAX_PANEL_RADIUS),
              "panel_frame": (0, MAX_PANEL_FRAME),
              "line_width": (1, 4), "button_shadow": (0, 8), "scrollbar_radius": (0, 12), "scrollbar_inset": (0, 4), "grain": (0, 100),
              "grain_stretch": (1, 16), "scanlines": (0, 100), "button_lift": (0, 12),
              "panel_border_width": (1, 8), "panel_gap": (0, 48)}[key]
    return int(min(limits[1], max(limits[0], value)))


def resolve_materials(given, palette: dict | None = None) -> dict[str, dict[str, dict]]:
    '''
    Every material in both modes: given's colors and opacities, with
    MATERIALS' defaults for anything missing or invalid - or, for
    INHERITED ones, made from the theme's own materials. palette is an
    older file's (see read_theme) - a color naming one of its colors is
    looked up there, and a material it has no entry for gets its color
    from the palette color older files gave it (see MATERIAL_SOURCES).
    '''
    materials = copy.deepcopy(MATERIALS)
    given = given if isinstance(given, dict) else {}
    # (name, mode) of the INHERITED materials given has no color for
    missing: set[tuple[str, str]] = set()
    for name, (source, _) in MATERIAL_SOURCES.items():
        modes = given.get(name) if isinstance(given.get(name), dict) else {}
        for mode in THEME_MODES:
            entry = modes.get(mode) if isinstance(modes.get(mode), dict) else {}
            colors = palette[mode] if palette else {}
            color = entry.get("color")
            if is_hex(color):
                materials[name][mode]["color"] = color.lower()
            elif isinstance(color, str) and is_hex(colors.get(color)):
                materials[name][mode]["color"] = colors[color].lower()
            elif name in INHERITED:
                missing.add((name, mode))
            elif is_hex(colors.get(source)):
                materials[name][mode]["color"] = colors[source].lower()
            opacity = entry.get("opacity")
            gradient = read_gradient(entry.get("gradient")) if name not in INK_MATERIALS else None
            if gradient is not None:
                materials[name][mode]["gradient"] = gradient
            if name not in INK_MATERIALS and isinstance(opacity, (int, float)) and not isinstance(opacity, bool):
                materials[name][mode]["opacity"] = min(1.0, max(0.0, float(opacity)))
            elif (name, mode) in missing:
                missing.add((name, mode, "opacity"))
    for name, (source, amount, opacity) in INHERITED.items():
        for mode in THEME_MODES:
            if (name, mode) not in missing:
                continue
            origin = materials[source][mode]
            materials[name][mode]["color"] = shade(origin["color"], amount) if amount else origin["color"]
            if (name, mode, "opacity") in missing and name not in INK_MATERIALS:
                materials[name][mode]["opacity"] = origin["opacity"] if opacity is None else opacity
    return materials


def button_radius(info: dict, kind: str) -> int:
    '''A theme's corner radius for one of BUTTON_KINDS, from its info (see read_theme) - DEFAULT_BUTTON_RADIUS if it has none.'''
    radius = info.get(f"{kind}_radius")
    if isinstance(radius, (int, float)) and not isinstance(radius, bool):
        return int(min(MAX_BUTTON_RADIUS, max(0, radius)))
    return DEFAULT_BUTTON_RADIUS


def theme_modes(info: dict) -> tuple[str, ...]:
    '''Which of THEME_MODES a theme has, from its info (see read_theme) - its "modes", or both if it names none.'''
    modes = info.get("modes")
    given = tuple(mode for mode in THEME_MODES if mode in modes) if isinstance(modes, list) else ()
    return given or THEME_MODES


def read_theme(data) -> dict | None:
    '''
    A theme file's contents as {"info": {...}, "materials": {...}} - every
    material in both modes filled in - or None if it has no materials (or
    older palette) to read. Reads older files too (see the module
    docstring).
    '''
    if not isinstance(data, dict):
        return None
    palette = _old_palette(data)
    if not isinstance(data.get("materials"), dict) and palette is None:
        return None
    return {
        "info": {key: value for key, value in data.items() if key not in ("palette", "materials", *THEME_MODES)},
        "materials": resolve_materials(data.get("materials"), palette),
    }


def theme_file(theme: dict) -> dict:
    '''A read_theme result back as a theme file's contents: its info, then every material (text and lines without an opacity).'''
    materials = {name: {mode: ({"color": entry["color"]} if name in INK_MATERIALS else dict(entry)) for mode, entry in modes.items()}
                 for name, modes in theme["materials"].items()}
    return {**theme["info"], "materials": materials}
