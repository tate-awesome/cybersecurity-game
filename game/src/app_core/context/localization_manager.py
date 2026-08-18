
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
        If the path doesn't have a value, throws an error.
        '''
        output = self.labels        
        for key in keys:
            output = output[key]
        return output
    
    def set(self, *keys, value):
        '''
        Sets the given dict path to the given value
        '''
        current = self.labels

        for key in keys[:-1]:
            current = current[key]

        current[keys[-1]] = value