import json
import os
from pathlib import Path
from .paths import Paths

class Json:
    def __init__(self, paths: Paths):
        self._ref_word = "_ref"
        self.paths = paths
        self.encountered_files = set()

    def merge_from_file(self, current_dict: dict, path: Path):
        '''
        Loads a dict from the given path, and deeply overwrites current_dict.
        If the loaded dict (or anything it in turn references) has a "_ref" key,
        its value - a single relative path, or a list of them - is resolved
        relative to the directory of the file it appears in, then merged in too.
        '''
        self.encountered_files.clear()
        self._merge_from_file(current_dict, path)

    def _merge_from_file(self, current_dict: dict, path: Path):
        '''
        Loads the given path as a json file, then deeply overwrites the old dict
        using the new dict.
        example: current_dict["x"] = new_dict["x"] if new_dict["x"] is not dict

        "_ref" paths found inside resolve against path's own parent directory
        (see deeper_merge), not a fixed root - so a folder of files can
        reference its siblings without knowing where it's been placed. Paths
        are resolved to absolute before the encountered_files check so the same
        file reached via two different relative chains is only merged once,
        and a genuine reference cycle (a file that transitively refers back to
        itself, e.g. packet_console_settings/_default.json <-> _packages/_default.json)
        terminates instead of recursing forever.
        '''
        path = Path(path).resolve()
        if path in self.encountered_files:
            return
        self.encountered_files.add(path)

        try:
            with open(path, encoding="utf-8") as json_file:
                data = json.load(json_file)
            self.deeper_merge(current_dict, data, path.parent)
        except Exception as e:
            print(f"Error during json merge from file ({path}): {e}")

    def deeper_merge(self, base_dict: dict, better_dict: dict | None, base_path: Path):
        '''
        better_dict ultimately comes from disk (a settings/preset file, or a
        preference value round-tripped through JSON) - it may not actually be
        a dict if the file was hand-edited or corrupted. Skip rather than crash.

        base_path is the directory any "_ref" entries in better_dict resolve
        against - the directory of the file better_dict was itself loaded from.
        '''
        if not isinstance(better_dict, dict):
            return
        for key, value in better_dict.items():
            if key == self._ref_word:
                refs = value if isinstance(value, list) else [value]
                for ref in refs:
                    if not isinstance(ref, str):
                        print(f"Error resolving _ref in {base_path}: {ref!r} is not a relative path string")
                        continue
                    # If we already merged this file, skip it (see _merge_from_file)
                    self._merge_from_file(base_dict, base_path / ref)
            elif (
                isinstance(value, dict)
                and isinstance(base_dict.get(key), dict)
            ):
                self.deeper_merge(base_dict[key], value, base_path)
            else:
                base_dict[key] = value

    def deep_merge(self, base_dict: dict, better_dict: dict | None):
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

    def save_to_file(self, data: dict, file_path: Path):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)
        except Exception as e:
            print(e)
