import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context


class LocalizationManager:
    def __init__(self, context: "Context"):
        self.context: Context = context
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
    def get(self, key: str) -> str:
        '''
        Returns the label for the given flat key (e.g. "menu_bar_buttons_quit").
        Raises a KeyError naming the key if there's no label for it.
        '''
        if key not in self.data:
            raise KeyError(f"labels[{key!r}] not found")
        return self.data[key]

    def group(self, prefix: str) -> dict[str, str]:
        '''
        Returns every label whose key starts with "<prefix>_", keyed by the
        rest of its key and kept in file order - e.g. group("packet_columns")
        -> {"time_word": "Time", ...}. For widgets that build one element per
        label in a group (table headers, columns) instead of looking up
        labels one at a time.
        '''
        start = f"{prefix}_"
        return {key[len(start):]: text for key, text in self.data.items() if key.startswith(start)}

    # Editing the default labels file
    def add_default_label(self, key: str, text: str, after_prefix: str):
        '''
        Adds a label to assets/labels/_default.json - right after the last
        label whose key starts with after_prefix, so it sits with its group -
        and to the labels in use now.
        '''
        labels = json.loads(self.default_path.read_text(encoding="utf-8"))
        group = [existing for existing in labels if existing.startswith(after_prefix)]
        output = {}
        for existing, value in labels.items():
            output[existing] = value
            if group and existing == group[-1]:
                output[key] = text
        output.setdefault(key, text)
        self.save_default_labels(output)
        self.data[key] = text

    def remove_default_labels(self, keys: list[str]):
        '''Removes labels from assets/labels/_default.json and from the labels in use now.'''
        labels = json.loads(self.default_path.read_text(encoding="utf-8"))
        self.save_default_labels({key: value for key, value in labels.items() if key not in keys})
        for key in keys:
            self.data.pop(key, None)

    def save_default_labels(self, labels: dict):
        self.default_path.write_text(json.dumps(labels, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")

    def variable_name(self, key):
        nickname = self.context.states.get_register(key, "nickname")
        if len(nickname) > 0:
            variable_name = nickname
        else:
            variable_name = self.get(f"modbus_variables_{key}")
        return variable_name
