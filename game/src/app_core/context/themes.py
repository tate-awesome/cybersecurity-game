'''
Theme files - assets/themes/<family>.json, and imported ones in
user_data/themes. Each theme has:

    "palette":   the theme's key colors, named, for each mode -
                 {"dark": {"root": "#10141d", ...}, "light": {...}}
                 with every one of PALETTE_KEYS
    "materials": what each kind of widget is made of, for each mode -
                 {"panel": {"dark": {"color": "panel", "opacity": 0.5},
                            "light": {"color": "panel", "opacity": 0.6}}, ...}
                 "color" is a palette key or a hex code; "opacity" is 0-1
                 (1 = solid). Any material or mode left out gets
                 MATERIALS' default, so a theme only lists what it changes.

plus a "label", a "kind" ("original" or "copied"), and optionally a source
"note" and which modes are "derived" rather than copied (see
Style.preset_name).

Older files had no materials and kept the palette's modes at the top level
({"dark": {...}, "light": {...}}) - read_theme still reads those.

No Qt here, so scripts can read and write themes too.
'''
import copy

THEME_MODES = ("dark", "light")

# The palette's key colors - what materials, canvases ("model_colors",
# "strip_chart_colors") and stylesheet details like text and borders name
PALETTE_KEYS = (
    "root",             # behind everything - the window
    "panel",            # panels
    "widget",           # cards and bars on panels
    "field",            # text boxes, consoles, tables, canvases
    "field_text",       # text in fields
    "text",             # all other text
    "accent",           # buttons, selections, highlights
    "accent_text",      # text on the accent
    "border",           # outlines of fields, tables and tabs
    "scrollbar",        # scrollbar handles
    "scrollbar_hover",  # hovered scrollbar handles
)


def _both(color: str, opacity: float) -> dict[str, dict]:
    return {mode: {"color": color, "opacity": opacity} for mode in THEME_MODES}


# Every material - the kinds of widget a theme styles - with its default.
# Labels: "theme_materials_<name>" names one, "theme_materials_notes_<name>"
# says what uses it.
MATERIALS: dict[str, dict[str, dict]] = {
    "window": _both("root", 1.0),           # the window and page background
    "panel": _both("panel", 0.5),           # panel bodies
    "panel_border": _both("widget", 0.5),   # panel outlines
    "menu_bar": _both("widget", 1.0),       # menu bars
    "card": _both("widget", 0.5),           # forms and cards on panels
    "field": _both("field", 0.5),           # text boxes, consoles, trees, canvases
    "button": _both("accent", 0.75),        # buttons
    "overlay": _both("panel", 1.0),         # dropdown overlays
    "overlay_card": _both("widget", 1.0),   # cards inside dropdown overlays
    "tab": _both("widget", 0.5),            # tabs
    "tab_selected": _both("accent", 1.0),   # the selected tab
    "table_header": _both("widget", 0.5),   # table and tree headers
    "alternate_row": _both("widget", 0.5),  # every other row of tables and trees
    "selection": _both("accent", 1.0),      # selected rows and items
    "scrollbar": _both("scrollbar", 1.0),   # scrollbar handles
    "scrollbar_track": _both("panel", 0.5), # what scrollbar handles slide in
    "tooltip": _both("panel", 1.0),         # tooltips
    "footer": _both("widget", 1.0),         # the bar along the bottom of the window
}


def is_color(value) -> bool:
    '''A palette key or a "#rrggbb" hex code.'''
    if not isinstance(value, str):
        return False
    if value in PALETTE_KEYS:
        return True
    return len(value) == 7 and value.startswith("#") and all(c in "0123456789abcdefABCDEF" for c in value[1:])


def resolve_materials(overrides) -> dict[str, dict[str, dict]]:
    '''MATERIALS' defaults with a theme's own materials on top - anything invalid is skipped.'''
    materials = copy.deepcopy(MATERIALS)
    if not isinstance(overrides, dict):
        return materials
    for name, modes in overrides.items():
        if name not in materials or not isinstance(modes, dict):
            continue
        for mode in THEME_MODES:
            entry = modes.get(mode)
            if not isinstance(entry, dict):
                continue
            if is_color(entry.get("color")):
                materials[name][mode]["color"] = entry["color"]
            opacity = entry.get("opacity")
            if isinstance(opacity, (int, float)) and not isinstance(opacity, bool):
                materials[name][mode]["opacity"] = min(1.0, max(0.0, float(opacity)))
    return materials


def read_theme(data) -> dict | None:
    '''
    A theme file's contents as {"info": {...}, "palette": {...},
    "materials": {...}} - every mode, palette key and material filled in -
    or None if its palette is missing or incomplete. Reads the old format
    too (see the module docstring).
    '''
    if not isinstance(data, dict):
        return None
    palette = data.get("palette")
    if palette is None and all(mode in data for mode in THEME_MODES):
        palette = {mode: data[mode] for mode in THEME_MODES}
    if not isinstance(palette, dict):
        return None
    for mode in THEME_MODES:
        colors = palette.get(mode)
        if not isinstance(colors, dict) or not all(isinstance(colors.get(key), str) for key in PALETTE_KEYS):
            return None
    return {
        "info": {key: value for key, value in data.items() if key not in ("palette", "materials", *THEME_MODES)},
        "palette": {mode: {key: palette[mode][key] for key in PALETTE_KEYS} for mode in THEME_MODES},
        "materials": resolve_materials(data.get("materials")),
    }


def theme_file(theme: dict) -> dict:
    '''A read_theme result back as a theme file's contents: its info, then the palette, then every material.'''
    return {**theme["info"], "palette": theme["palette"], "materials": theme["materials"]}
