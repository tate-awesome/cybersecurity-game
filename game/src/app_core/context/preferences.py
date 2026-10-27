from typing import TYPE_CHECKING, TypedDict
from .performance import (DEFAULT_ANTIALIASING, DEFAULT_PAGE_TRANSITIONS, DEFAULT_SMOOTH_SCROLLING, DEFAULT_PERFORMANCE_LOG,
                          DEFAULT_PERFORMANCE_OVERLAY, DEFAULT_UI_FPS)
from .style import (DEFAULT_BACKGROUND_ANIMATE, DEFAULT_BACKGROUND_DETAILED, DEFAULT_BACKGROUND_FPS,
                    DEFAULT_BACKGROUND_HIDDEN, DEFAULT_BACKGROUND_VISUAL, DEFAULT_BACKGROUND_WORKSPACE_DISABLED,
                    DEFAULT_BACKGROUND_WORKSPACE_FROZEN,
                    NO_BACKGROUND)
if TYPE_CHECKING:
    from .. import Context

# Developer mode: whether pages get the debug menu bar group (see
# MenuBar.add_config_buttons). 1 or 0 in preferences.json.
DEFAULT_IS_DEVELOPER = 1

# Privileged network helper: whether network capture runs in a separate
# elevated process (see network/helper). Off keeps everything in-process.
# Toggled on the settings page's Performance tab.
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
    "background_enabled",  # the background's on/off switch - now its "none" visual (see style.NO_BACKGROUND)
)

class PreferencesData(TypedDict, total=False):
    '''
    Documents the shape preferences.json is expected to have after a fresh
    clear() (see below) - loaded from user-editable JSON on disk, so this
    doesn't guarantee the shape at runtime (see Preferences.has()'s guard).
    '''
    theme: str
    is_developer: int
    invert_buttons: bool
    background_visual: str
    background_animate: bool
    background_detailed: bool
    background_fps: int
    background_hidden: list[str]
    background_workspace_frozen: bool
    background_workspace_disabled: bool
    ui_fps: int
    antialiasing: bool
    page_transitions: bool
    smooth_scrolling: bool
    performance_overlay: bool
    performance_log: bool
    network_helper: bool
    labels_file: str
    page: str
    workspace_description: str
    fullscreen: bool
    keybinds: dict[str, str]
    fade_in: bool
    fade_out: bool
    debug_labels: bool
    wifi_home: str
    wifi_device: str

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
        # A background switched off carries over as no background
        if self.data.get("background_enabled") is False:
            self.data["background_visual"] = NO_BACKGROUND
        # Settings the app no longer has - dropped, so the file only holds live ones
        retired = [key for key in RETIRED_KEYS if key in self.data]
        for key in retired:
            del self.data[key]
        if retired:
            self.save()
        # Nicknames were briefly kept here with hiding, as "network_hosts" - just the nicknames stay
        if "network_hosts" in self.data:
            self.adopt_nicknames(self.data.pop("network_hosts"))
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

    # Host nicknames
    def host_nicknames(self) -> dict:
        '''
        Every host's (device's) nickname, by lower-case MAC -
        {"b8:27:eb:44:10:9a": "PLC"} - kept across workspaces and sessions,
        since a device is the same device in every lesson. Whether the
        network graph hides a host is each workspace's own (its
        "network_hosts" setting). Change one with set_host_nickname, which saves.
        '''
        names = self.data.get("host_nicknames")
        if not isinstance(names, dict):
            names = self.data["host_nicknames"] = {}
        return names

    def host_nickname(self, mac: str) -> str:
        return str(self.host_nicknames().get(str(mac).lower()) or "")

    def set_host_nickname(self, mac: str, name: str, save: bool = True):
        '''Gives a host a nickname - or, empty, takes it away.'''
        names = self.host_nicknames()
        mac, name = str(mac).lower(), str(name)
        if name:
            names[mac] = name
        else:
            names.pop(mac, None)
        if save:
            self.save()

    def adopt_nicknames(self, entries) -> bool:
        '''
        Takes in the nicknames from {mac: {"nickname": ...}} entries - a
        workspace's "network_hosts" setting from before nicknames moved
        here. A nickname here already wins. Entries not keyed by a MAC
        (older "macs"/"ips" groupings, "-") are skipped. Returns whether
        any were taken in (it saves if so).
        '''
        if not isinstance(entries, dict):
            return False
        names, changed = self.host_nicknames(), False
        for mac, entry in entries.items():
            mac = str(mac).lower()
            if mac.count(":") != 5 or not isinstance(entry, dict) or not entry.get("nickname"):
                continue
            if not names.get(mac):
                names[mac] = str(entry["nickname"])
                changed = True
        if changed:
            self.save()
        return changed

    def clear(self):
        self.data.clear()
        self.data = {
            "theme": "",            # autosaved in Style
            "is_developer": DEFAULT_IS_DEVELOPER,  # set by hand in the file - 1 adds the debug tools to menu bars
            "invert_buttons": False,  # toggled on the Appearance tab (see Style.set_invert_buttons)
            # Set in quick settings and on the settings page (see Style.set_background)
            "background_visual": DEFAULT_BACKGROUND_VISUAL,
            "background_animate": DEFAULT_BACKGROUND_ANIMATE,
            "background_detailed": DEFAULT_BACKGROUND_DETAILED,
            "background_fps": DEFAULT_BACKGROUND_FPS,
            "background_hidden": list(DEFAULT_BACKGROUND_HIDDEN),  # chosen on the visuals demo page
            "background_workspace_frozen": DEFAULT_BACKGROUND_WORKSPACE_FROZEN,  # on the Graphics tab
            "background_workspace_disabled": DEFAULT_BACKGROUND_WORKSPACE_DISABLED,  # on the Graphics tab
            # Set on the settings page's Performance tab (see Performance.set)
            "ui_fps": DEFAULT_UI_FPS,
            "antialiasing": DEFAULT_ANTIALIASING,
            "page_transitions": DEFAULT_PAGE_TRANSITIONS,
            "smooth_scrolling": DEFAULT_SMOOTH_SCROLLING,
            "performance_overlay": DEFAULT_PERFORMANCE_OVERLAY,  # also F3 (see KeyBinds)
            "performance_log": DEFAULT_PERFORMANCE_LOG,
            "network_helper": DEFAULT_NETWORK_HELPER,  # toggled on the Performance tab (see PrivilegedHelper)
            "labels_file": "",      # autosaved in LocalizationManager
            "page": "",             # manual saved in menu bar/router
            # The workspace whose description was read last - the select page opens on it,
            # or on the first in its list with none (see WorkspaceSelectPage)
            "workspace_description": "",
            "fullscreen": DEFAULT_FULLSCREEN,  # autosaved in KeyBinds
            "fade_in": DEFAULT_FADE_IN,    # toggled on the General tab (see App)
            "fade_out": DEFAULT_FADE_OUT,  # toggled on the General tab (see Router.quit)
            "keybinds": {},         # set on the settings page (see KeyBinds.rebind) - empty means keybinds.DEFAULT_KEYBINDS
            "debug_labels": False,  # toggled by ToggleDebugLabels (see LocalizationManager.is_debug)
            "host_nicknames": {},   # host nicknames, by MAC (see host_nicknames)
            # Set from the Wi-Fi form's entries (see WifiForm) - app-wide, since
            # there's only the one Wi-Fi radio whichever page switches it
            "wifi_home": "",
            "wifi_device": "",
        }
        self.save()

    def save_page(self):
        self.set("page", self.context.router.current_page)
