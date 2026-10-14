from typing import TYPE_CHECKING, TypedDict
from .performance import (DEFAULT_ANTIALIASING, DEFAULT_PAGE_TRANSITIONS, DEFAULT_PERFORMANCE_LOG,
                          DEFAULT_PERFORMANCE_OVERLAY, DEFAULT_UI_FPS)
from .style import (DEFAULT_BACKGROUND_ANIMATE, DEFAULT_BACKGROUND_DETAILED, DEFAULT_BACKGROUND_ENABLED,
                    DEFAULT_BACKGROUND_FPS, DEFAULT_BACKGROUND_VISUAL, DEFAULT_TRANSLUCENT_SURFACES)
if TYPE_CHECKING:
    from .. import Context

# Developer mode: whether pages get the debug menu bar group (see
# MenuBar.add_config_buttons). 1 or 0 in preferences.json.
DEFAULT_IS_DEVELOPER = 1

# Privileged network helper: whether network capture runs in a separate
# elevated process (see network/helper). Off keeps everything in-process,
# exactly as before. Toggled on the settings page's Performance tab.
DEFAULT_NETWORK_HELPER = False

# Fullscreen: whether the window starts fullscreen. Saved whenever it's
# switched (the keybind or the settings page's checkbox, see KeyBinds).
DEFAULT_FULLSCREEN = True

# Fading the window in on startup and out on quit (see FadeIn/FadeOut in
# app_core.transitions). Toggled on the settings page's General tab.
DEFAULT_FADE_IN = True
DEFAULT_FADE_OUT = False

# Preferences from older versions, removed from preferences.json on load
RETIRED_KEYS = (
    "surface_blur",  # surfaces' frosted-glass blur, removed
    "surface_opacity",  # surfaces' opacity, now each theme's materials (see themes.py)
    "theme_inset", "theme_tint", "theme_adjust",  # palette tweaks on top of themes - each is drawn as authored now
)

class PreferencesData(TypedDict, total=False):
    '''
    Documents the shape preferences.json is expected to have after a fresh
    clear() (see below) - loaded from user-editable JSON on disk, so this
    doesn't guarantee the shape at runtime (see Preferences.has()'s guard).
    '''
    theme: str
    is_developer: int
    translucent_surfaces: bool
    invert_buttons: bool
    background_enabled: bool
    background_visual: str
    background_animate: bool
    background_detailed: bool
    background_fps: int
    ui_fps: int
    antialiasing: bool
    page_transitions: bool
    performance_overlay: bool
    performance_log: bool
    network_helper: bool
    labels_file: str
    page: str
    fullscreen: bool
    keybinds: dict[str, str]
    fade_in: bool
    fade_out: bool
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
        # Settings the app no longer has - dropped, so the file only holds live ones
        retired = [key for key in RETIRED_KEYS if key in self.data]
        for key in retired:
            del self.data[key]
        if retired:
            self.save()
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

    def is_fullscreen(self) -> bool:
        '''Whether the window starts fullscreen (preferences.json "fullscreen") - see DEFAULT_FULLSCREEN.'''
        value = self.data.get("fullscreen")
        if isinstance(value, str):  # older files saved it as "True"/"False" ("" for unset)
            value = {"True": True, "False": False}.get(value)
        return DEFAULT_FULLSCREEN if value is None else bool(value)

    def is_fade_in(self) -> bool:
        '''Whether the window fades in on startup (preferences.json "fade_in").'''
        value = self.data.get("fade_in")
        return value if isinstance(value, bool) else DEFAULT_FADE_IN

    def is_fade_out(self) -> bool:
        '''Whether the window fades out on quit (preferences.json "fade_out").'''
        value = self.data.get("fade_out")
        return value if isinstance(value, bool) else DEFAULT_FADE_OUT

    def set(self, key: str, value):
        self.data[key] = value
        self.save()

    def clear(self):
        self.data.clear()
        self.data = {
            "theme": "",            # autosaved in Style
            "is_developer": DEFAULT_IS_DEVELOPER,  # set by hand in the file - 1 adds the debug tools to menu bars
            "translucent_surfaces": DEFAULT_TRANSLUCENT_SURFACES,  # toggled on the settings page (see Style.set_translucent_surfaces)
            "invert_buttons": False,  # toggled in the Background dropdown (see Style.set_invert_buttons)
            # Set in the Background dropdown (see Style.set_background)
            "background_enabled": DEFAULT_BACKGROUND_ENABLED,
            "background_visual": DEFAULT_BACKGROUND_VISUAL,
            "background_animate": DEFAULT_BACKGROUND_ANIMATE,
            "background_detailed": DEFAULT_BACKGROUND_DETAILED,
            "background_fps": DEFAULT_BACKGROUND_FPS,
            # Set on the settings page's Performance tab (see Performance.set)
            "ui_fps": DEFAULT_UI_FPS,
            "antialiasing": DEFAULT_ANTIALIASING,
            "page_transitions": DEFAULT_PAGE_TRANSITIONS,
            "performance_overlay": DEFAULT_PERFORMANCE_OVERLAY,  # also F3 (see KeyBinds)
            "performance_log": DEFAULT_PERFORMANCE_LOG,
            "network_helper": DEFAULT_NETWORK_HELPER,  # toggled on the Performance tab (see PrivilegedHelper)
            "labels_file": "",      # autosaved in LocalizationManager
            "page": "",             # manual saved in menu bar/router
            "fullscreen": DEFAULT_FULLSCREEN,  # autosaved in KeyBinds
            "fade_in": DEFAULT_FADE_IN,    # toggled on the General tab (see App)
            "fade_out": DEFAULT_FADE_OUT,  # toggled on the General tab (see Router.quit)
            "keybinds": {},         # set on the settings page (see KeyBinds.rebind) - empty means keybinds.DEFAULT_KEYBINDS
            "debug_labels": False   # toggled by ToggleDebugLabels (see LocalizationManager.is_debug)
        }
        self.save()

    def save_page(self):
        self.set("page", self.context.router.current_page)
