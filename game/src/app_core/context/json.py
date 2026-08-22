import json
from .paths import Paths

class Json:
    def __init__(self, paths: Paths):
        self._package_word = "_files"
        self.paths = paths
        self.encountered_files = set()

    def merge_from_file(self, current_dict: dict, path: str):
        self.encountered_files.clear()
        self._merge_from_file(current_dict, path)

    def _merge_from_file(self, current_dict: dict, path: str):
        '''
        Loads the given path as a json file, then deeply overwrites the old dict
        using the new dict.
        example: current_dict["x"] = new_dict["x"] if new_dict["x"] is not dict

        If the new settings includes a "_files" key, it will unpack the given files shallowly
        '''
        path = str(path)
        if path in self.encountered_files:
            return
        self.encountered_files.add(path)

        try:
            with open(path, encoding="utf-8") as json_file:
                data = json.load(json_file)
            self.deeper_merge(current_dict, data)
        except Exception as e:
            print(f"Error during json merge from file: {e}")

    def deeper_merge(self, base_dict: dict, better_dict: dict):
        # better_dict ultimately comes from disk (a settings/preset file, or a
        # preference value round-tripped through JSON) - it may not actually be
        # a dict if the file was hand-edited or corrupted. Skip rather than crash.
        if not isinstance(better_dict, dict):
            return
        for key, value in better_dict.items():
            if key == self._package_word:
                files = better_dict.get(self._package_word)
                if isinstance(files, dict):
                    for folder, file in files.items():
                        file_path = self.paths.settings / folder / file
                        # If we already merged this file or package, skip it
                        self._merge_from_file(base_dict, file_path)
            elif (
                isinstance(value, dict)
                and isinstance(base_dict.get(key), dict)
            ):
                self.deeper_merge(base_dict[key], value)
            else:
                base_dict[key] = value

    def deep_merge(self, base_dict: dict, better_dict: dict):
        # See deeper_merge - better_dict may not be a dict if it came from a
        # corrupted or hand-edited preferences value.
        if not isinstance(better_dict, dict):
            return
        for key, value in better_dict.items():
            if (
                isinstance(value, dict)
                and isinstance(base_dict.get(key), dict)
            ):
                self.deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value

    def save_to_file(self, data: dict, file_path: str):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)
        except Exception as e:
            print(e)