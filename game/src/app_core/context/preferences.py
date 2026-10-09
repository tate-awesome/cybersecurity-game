from typing import TYPE_CHECKING, TypedDict
from .style import (DEFAULT_BACKGROUND_ANIMATE, DEFAULT_BACKGROUND_DETAILED, DEFAULT_BACKGROUND_ENABLED,
                    DEFAULT_BACKGROUND_FPS, DEFAULT_BACKGROUND_VISUAL, DEFAULT_TRANSLUCENT_SURFACES)
if TYPE_CHECKING:
    from .. import Context

# Developer mode: whether pages get the debug menu bar group (see
# MenuBar.add_config_buttons). 1 or 0 in preferences.json.
DEFAULT_IS_DEVELOPER = 1

class PreferencesData(TypedDict, total=False):
    '''
    Documents the shape preferences.json is expected to have after a fresh
    clear() (see below) - loaded from user-editable JSON on disk, so this
    doesn't guarantee the shape at runtime (see Preferences.has()'s guard).
    '''
    theme: str
    theme_inset: bool
    theme_tint: float
    is_developer: int
    translucent_surfaces: bool
    surface_opacity: dict[str, float]
    surface_blur: dict[str, float]
    invert_buttons: bool
    background_enabled: bool
    background_visual: str
    background_animate: bool
    background_detailed: bool
    background_fps: int
    labels_file: str
    page: str
    fullscreen: str
    debug_labels: bool

class Preferences:
    def __init__(self, context: "Context"):
        '''
        Manages app-wide user settings across sessions.
        Themes, accessibility, app behavior, localization
        Created before the root in App().
        '''
        self.context: Context = context
        self.data: dict = {}
        self.load()

    def load(self):
        data = {}
        path = self.context.paths.user_data / "preferences.json"
        self.context.json.merge_from_file(data, path)
        
        for key, value in data.items():
            self.data[key] = value
        # Written out if missing, so it's there to find and flip in the file
        if "is_developer" not in self.data:
            self.data["is_developer"] = DEFAULT_IS_DEVELOPER
            self.save()

    def save(self):
        path = self.context.paths.user_data / "preferences.json"
        self.context.json.save_to_file(self.data, path)

    def has(self, key: str) -> bool:
        value = self.data.get(key)
        # Sized types (dict/list/str/...) count as "present" only if non-empty; a
        # hand-edited preferences.json could put any JSON type here, so anything
        # else (bool/int/float) just needs to not be missing entirely.
        if isinstance(value, (str, dict, list, tuple, set)):
            return len(value) > 0
        return value is not None

    def get(self, key: str):
        return self.data.get(key)

    def is_developer(self) -> bool:
        '''Developer mode (preferences.json "is_developer": 1/0) - adds the debug tools to every page's menu bar.'''
        return self.data.get("is_developer", DEFAULT_IS_DEVELOPER) in (1, "1", True)

    def set(self, key: str, value):
        self.data[key] = value
        self.save()

    def clear(self):
        self.data.clear()
        self.data = {
            "theme": "",            # autosaved in Style
            "theme_inset": False,   # toggled on the settings page (see Style.set_inset)
            "theme_tint": 1.0,      # set on the settings page (see Style.set_tint)
            "is_developer": DEFAULT_IS_DEVELOPER,  # set by hand in the file - 1 adds the debug tools to menu bars
            "translucent_surfaces": DEFAULT_TRANSLUCENT_SURFACES,  # toggled on the settings page (see Style.set_translucent_surfaces)
            "surface_opacity": {},  # autosaved in Style.set_surface - empty means style.DEFAULT_SURFACE_OPACITY
            "surface_blur": {},     # autosaved in Style.set_surface - empty means style.DEFAULT_SURFACE_BLUR
            "invert_buttons": False,  # toggled in the Background dropdown (see Style.set_invert_buttons)
            # Set in the Background dropdown (see Style.set_background)
            "background_enabled": DEFAULT_BACKGROUND_ENABLED,
            "background_visual": DEFAULT_BACKGROUND_VISUAL,
            "background_animate": DEFAULT_BACKGROUND_ANIMATE,
            "background_detailed": DEFAULT_BACKGROUND_DETAILED,
            "background_fps": DEFAULT_BACKGROUND_FPS,
            "labels_file": "",      # autosaved in LocalizationManager
            "page": "",             # manual saved in menu bar/router
            "fullscreen": "",       # autosaved in KeyBinds
            "debug_labels": False   # toggled by ToggleDebugLabels (see LocalizationManager.is_debug)
        }
        self.save()

    def save_page(self):
        self.set("page", self.context.router.current_page)
