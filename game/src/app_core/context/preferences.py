from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from .. import Context

class PreferencesData(TypedDict, total=False):
    '''
    Documents the shape preferences.json is expected to have after a fresh
    clear() (see below) - loaded from user-editable JSON on disk, so this
    doesn't guarantee the shape at runtime (see Preferences.has()'s guard).
    '''
    mode: str
    theme: str
    labels: dict
    page: str
    panes: dict
    settings: dict
    fullscreen: str

class Preferences:
    def __init__(self, context: "Context"):
        '''
        Manages app-wide user settings across sessions.
        Themes, accessibility, app behavior, localization
        Created before the root in App().
        '''
        self.context: "Context" = context
        # PreferencesData documents the expected shape, but self.data itself
        # stays a plain dict - it needs generic dict operations (.clear(), being
        # passed to Json.save_to_file()) a TypedDict doesn't support, and it's
        # loaded from user-editable JSON so the shape isn't actually guaranteed.
        self.data: dict = {}
        self.load()

    def load(self):
        data = {}
        path = self.context.paths.user_data / "preferences.json"
        self.context.json.merge_from_file(data, path)
        
        for key, value in data.items():
            self.data[key] = value

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

    def set(self, key: str, value):
        self.data[key] = value
        self.save()

    def clear(self):
        self.data.clear()
        self.data = {
            "mode": "",
            "theme": "",
            "labels": {},
            "page": "",
            "fullscreen": ""
        }
        self.save()

    def save_settings(self):
        self.set("settings", self.context.states.get())

    def save_preferences(self):
        self.set("labels", self.context.labels.get())
        self.set("mode", self.context.style.mode())
        self.set("theme", self.context.style.current_theme)

    def save_page(self):
        self.set("page", self.context.router.current_page)
