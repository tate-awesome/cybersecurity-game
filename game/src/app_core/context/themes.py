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
than copied (see Style.preset_name).

Each kind of button has its own materials: its background, its
background on hover, its outline, its text and its text on hover. An
opacity of 0 leaves out a background or an outline - a ghost button, or
an outline with nothing inside it. A theme from before these existed
gets them from its other materials (see INHERITED), so it looks as it did.

Older files had a "palette" of named colors per mode that materials
pointed into (or, older still, no materials - just the palette's modes at
the top level). read_theme still reads both, looking each material's
color up in the palette.

No Qt here, so scripts can read and write themes too.
'''
import copy
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
    },
    "light": {
        "root": "#d9e2f5", "panel": "#f1f5ff", "widget": "#e4ebfd",
        "field": "#ffffff", "field_text": "#1a2233", "text": "#1a2233",
        "accent": "#1e6fe0", "accent_text": "#ffffff", "border": "#d9e2f5",
        "scrollbar": "#d9e2f5", "scrollbar_hover": "#bfc7d8",
    },
}

# Every material - the kinds of widget a theme styles - with the palette
# color older files gave it, and its default opacity. Labels:
# "theme_materials_<name>" names one, "theme_materials_notes_<name>" says
# what uses it.
MATERIAL_SOURCES: dict[str, tuple[str, float]] = {
    # Surfaces - backgrounds, which can be see-through
    "window": ("root", 1.0),             # the window and page background
    "panel": ("panel", 0.5),             # panel bodies
    "panel_border": ("widget", 0.5),     # panel outlines
    "menu_bar": ("widget", 1.0),         # menu bars
    "card": ("widget", 0.5),             # forms and cards on panels
    "field": ("field", 0.5),             # text boxes, consoles, trees, canvases
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
    "alternate_row": ("widget", 0.5),    # every other row of tables and trees
    "selection": ("accent", 1.0),        # selected rows and items
    "scrollbar": ("scrollbar", 1.0),     # scrollbar handles
    "scrollbar_track": ("panel", 0.5),   # what scrollbar handles slide in
    "tooltip": ("panel", 1.0),           # tooltips
    "footer": ("widget", 1.0),           # the bar along the bottom of the window
    # Text and lines - always solid (see INK_MATERIALS)
    "text": ("text", 1.0),                        # all other text
    "field_text": ("field_text", 1.0),            # text in fields
    "accent_text": ("accent_text", 1.0),          # text on selections and the selected tab
    "button_text": ("accent_text", 1.0),          # text on buttons
    "button_hover_text": ("accent_text", 1.0),    # text on buttons under the mouse
    "menu_button_text": ("accent_text", 1.0),        # text on menu buttons
    "menu_button_hover_text": ("accent_text", 1.0),  # text on menu buttons under the mouse, and the selected workspace
    "accent": ("accent", 1.0),                    # highlights: focus outlines, checked boxes, slider handles, overlay outlines
    "border": ("border", 1.0),                    # outlines of fields, tables and tabs
    "scrollbar_hover": ("scrollbar_hover", 1.0),  # hovered scrollbar handles
}
INK_MATERIALS = ("text", "field_text", "accent_text", "accent", "border", "scrollbar_hover",
                 "button_text", "button_hover_text", "menu_button_text", "menu_button_hover_text")

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
