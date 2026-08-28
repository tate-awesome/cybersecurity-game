from pathlib import Path
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .. import Context


class JsonBackedStore:
    '''
    Shared logic for InputManager and LocalizationManager: both load a default
    JSON file, merge a saved preference on top of it, and let the user select
    an additional JSON file at runtime to merge in. They differ only in which
    preference key they save under, which directory holds their default/
    selectable files, what to call the file-picker dialog, and what label to
    use in error messages.
    '''

    def __init__(self, context: "Context", preference_key: str, default_dir: Path,
                 select_dir: Path, dialog_title: str, error_label: str):
        self.context: "Context" = context
        self.preference_key = preference_key
        self.default_dir = default_dir
        self.select_dir = select_dir
        self.dialog_title = dialog_title
        self.error_label = error_label
        self.data: dict = self.get_preferred()

    def get_preferred(self) -> dict:
        '''
        Loads the default file, then merges the saved preference on top.
        '''
        default = self.get_default()
        if self.context.preferences.has(self.preference_key):
            self.context.json.deep_merge(default, self.context.preferences.get(self.preference_key))
        return default

    def get_default(self) -> dict:
        '''
        Loads the default JSON file.
        '''
        file_path = self.default_dir / "_default.json"
        return self.context.json.load(file_path)

    def reset(self):
        self.data = self.get_default()

    def select(self):
        '''
        Opens a dialog for the user to select a JSON file to merge in.
        '''
        file_path = self.context.paths.select_path(self.select_dir, self.dialog_title)
        if file_path is None:
            return
        self.context.json.merge_from_file(self.data, file_path)
        self.context.router.refresh()

    def get(self, *keys: str) -> Any:
        '''
        Returns the value at the given key sequence in the data dict.
        Raises a KeyError naming the full path if the path doesn't have a value.
        '''
        output = self.data
        for i, key in enumerate(keys):
            if not isinstance(output, dict) or key not in output:
                raise KeyError(f"{self.error_label}{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            output = output[key]
        return output

    def set(self, *keys: str, value: Any):
        '''
        Sets the given dict path to the given value.
        Raises a KeyError naming the full path if an intermediate key doesn't have a value.
        '''
        current = self.data

        for i, key in enumerate(keys[:-1]):
            if not isinstance(current, dict) or key not in current:
                raise KeyError(f"{self.error_label}{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            current = current[key]

        current[keys[-1]] = value
