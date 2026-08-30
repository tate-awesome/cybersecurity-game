
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .. import Context


class LocalizationManager:
    def __init__(self, context: "Context"):
        self.context: "Context" = context
        self.default_path = self.context.paths.labels / "_default.json"
        self.data: dict = self.get_preferred()

    # Startup
    def get_preferred(self) -> dict:
        '''
        Loads the default file, then merges the saved preference on top.
        '''
        labels = self.get_default()
        if self.context.preferences.has("labels_file"):
            self.context.json.merge_from_file(labels, self.context.preferences.get("labels_file"))
        return labels

    def get_default(self) -> dict:
        '''
        Loads the default JSON file.
        '''
        return self.context.json.load(self.default_path)

    # Reset
    def reset(self):
        self.data = self.get_default()

    # Select
    def select(self):
        '''
        Opens a dialog for the user to select a JSON file to merge in.
        '''
        file_path = self.context.paths.select_path(self.context.paths.labels, "Select a Localization File")
        if file_path is None:
            return
        self.load(file_path)
        self.context.router.refresh()

    def load(self, file_path: str):
        '''
        Merges the given JSON file on top of the current data, and saves
        the file path to preferences
        '''
        self.context.json.merge_from_file(self.data, file_path)
        self.context.preferences.set("labels_file", file_path)
        print("set file path")
        print(file_path)

    # Control (readonly)
    def get(self, *keys: str) -> Any:
        '''
        Returns the value at the given key sequence in the data dict.
        Raises a KeyError naming the full path if the path doesn't have a value.
        '''
        output = self.data
        for i, key in enumerate(keys):
            if not isinstance(output, dict) or key not in output:
                raise KeyError(f"labels{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            output = output[key]
        return output

    def variable_name(self, key):
        nickname = self.context.states.get_register(key, "nickname")
        if len(nickname) > 0:
            variable_name = nickname
        else:
            variable_name = self.get("modbus_variables", key)
        return variable_name
