
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

class LocalizationManager:
    def __init__(self, context: "Context"):
            self.context = context
            self.labels = self.get_preferred()

    def get_preferred(self):
        '''
        Loads labels from the preferences json file
        '''
        default = self.get_default()
        if self.context.preferences.has("labels"):
            self.context.json.deep_merge(default, self.context.preferences.get("labels"))
        return default

    def get_default(self):
        '''
        Loads settings from the default json file
        '''
        data = {}
        file_path = self.context.paths.labels / "_default.json"
        self.context.json.merge_from_file(data, file_path)
        return data

    def select(self):
        '''
        Opens a dialog for the user to select a json file
        '''
        directory = self.context.paths.labels
        file_path = self.context.paths.select_path(directory, "Select a Localization File")
        self.context.json.merge_from_file(self.labels, file_path)
        self.context.router.refresh()

    def reset(self):
        self.labels = self.get_default()

    def get(self, *keys):
        '''
        Returns the value at the given key sequence in the labels dict.
        Raises a KeyError naming the full path if the path doesn't have a value.
        '''
        output = self.labels
        for i, key in enumerate(keys):
            if not isinstance(output, dict) or key not in output:
                raise KeyError(f"labels{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            output = output[key]
        return output

    def set(self, *keys, value):
        '''
        Sets the given dict path to the given value.
        Raises a KeyError naming the full path if an intermediate key doesn't have a value.
        '''
        current = self.labels

        for i, key in enumerate(keys[:-1]):
            if not isinstance(current, dict) or key not in current:
                raise KeyError(f"labels{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            current = current[key]

        current[keys[-1]] = value

    def variable_name(self, key):
        nickname = self.context.states.get_register(key, "nickname")
        if len(nickname) > 0:
            variable_name = nickname
        else:
            variable_name = self.get("modbus_variables", key)
        return variable_name