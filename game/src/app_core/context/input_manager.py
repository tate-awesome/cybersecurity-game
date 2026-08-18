
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

class InputManager:
    def __init__(self, context: "Context"):
        self.context = context
        self.states = self.get_preferred()

    def get_preferred(self):
        '''
        Loads settings from the preferences json file
        '''
        default = self.get_default()
        if self.context.preferences.has("settings"):
            self.context.json.deep_merge(default, self.context.preferences.get("settings"))
        return default

    def get_default(self):
        '''
        Loads settings from the default json file
        '''
        file_path = self.context.paths.packages / "_default.json"
        default = {}
        self.context.json.merge_from_file(default, file_path)
        return default

    def reset(self):
        self.states = self.get_default()

    def select(self):
        '''
        Opens a dialog for the user to select a context preset.
        Context presets populate fields and checkboxes.
        '''
        directory = self.context.paths.settings
        file_path = self.context.paths.select_path(directory, "Select Settings")
        self.context.json.merge_from_file(self.states, file_path)
        self.context.router.refresh()

    def get(self, *keys):
        '''
        Returns the value at the given key sequence in the states dict.
        If the path doesn't have a value, throws an error.
        '''
        output = self.states        
        for key in keys:
            output = output[key]
        return output

    def set(self, *keys, value):
        '''
        Sets the given dict path to the given value
        '''
        current = self.states

        for key in keys[:-1]:
            current = current[key]

        current[keys[-1]] = value
    

    def get_registers(self):
        return self.get("modbus_variables")

    def get_register(self, key: str, field: str):
        return self.get_registers()[key][field]

    def set_register(self, key: str, field: str, value):
        self.get_registers()[key][field] = value
        

    