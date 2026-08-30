
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .. import Context


class InputManager:
    def __init__(self, context: "Context"):
        self.context: "Context" = context
        self.data: dict = self.get_preferred()

    def get_preferred(self) -> dict:
        '''
        Loads the default file, then merges the saved preference on top.
        '''
        default = self.get_default()
        if self.context.preferences.has("settings"):
            self.context.json.deep_merge(default, self.context.preferences.get("settings"))
        return default

    def get_default(self) -> dict:
        '''
        Loads the default JSON file.
        '''
        file_path = self.context.paths.packages / "_default.json"
        return self.context.json.load(file_path)

    # Reset
    def reset(self):
        self.data = self.get_default()

    # Select
    def select(self):
        '''
        Opens a dialog for the user to select a JSON file to merge in.
        '''
        file_path = self.context.paths.select_path(self.context.paths.settings, "Select Settings")
        if file_path is None:
            return
        self.context.json.merge_from_file(self.data, file_path)
        self.context.router.refresh()

    # Control
    def get(self, *keys: str) -> Any:
        '''
        Returns the value at the given key sequence in the data dict.
        Raises a KeyError naming the full path if the path doesn't have a value.
        '''
        output = self.data
        for i, key in enumerate(keys):
            if not isinstance(output, dict) or key not in output:
                raise KeyError(f"states{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
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
                raise KeyError(f"states{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            current = current[key]

        current[keys[-1]] = value

    # Registers
    def get_registers(self):
        return self.get("modbus_variables")

    def get_register(self, key: str, field: str):
        return self.get_registers()[key][field]

    def set_register(self, key: str, field: str, value):
        self.get_registers()[key][field] = value

    # Save
    def save_inputs(self):
        page = self.context.router.current_page
        path = self.context.paths.user_pages / page
        path = path / "inputs.json"
        print(path)
        self.context.json.save_to_file(self.context.states.get(), path)
