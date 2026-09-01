import json
import os
from pathlib import Path
from typing import Any
from .paths import Paths

class Json:
    def __init__(self, paths: Paths):
        self._ref_word = "_ref"
        self.paths = paths
        self.encountered_files = set()

    def load(self, path: Path, key_roots: dict[str, Path] | None = None):
        output = {}
        self.merge_from_file(output, path, key_roots)
        return output

    def merge_from_file(self, current_dict: dict, path: Path, key_roots: dict[str, Path] | None = None):
        '''
        Loads a dict from the given path, and deeply overwrites current_dict.
        If the loaded dict (or anything it in turn references) has a "_ref" key,
        its value - a single relative path, or a list of them - is resolved
        relative to the directory of the file it appears in, then merged in too.

        A "_ref" can also appear as an item inside a list (e.g.
        "buttons": [{"_ref": "menu_bar/admin.json"}]) - there, the
        referenced file must itself be a JSON array, and its elements are
        spliced into the surrounding list in place of the {"_ref": ...} item,
        rather than merged as a single nested item.

        key_roots optionally maps top-level keys of the loaded file (e.g.
        "settings", "menu_bar") to a fixed directory their own "_ref"s
        should resolve against, instead of the directory of the file they
        appear in - see deeper_merge. It only applies to the file's own
        top-level keys, not anything nested further down.
        '''
        self.encountered_files.clear()
        self._merge_from_file(current_dict, path, key_roots)

    def _load_file(self, path: Path) -> Any:
        '''
        Loads and returns the raw JSON at path, tracking it in encountered_files
        so the same file reached via two different relative chains (or a
        genuine reference cycle, e.g. packet_console_settings/_default.json
        <-> _packages/_default.json) is only ever loaded once per top-level
        load()/merge_from_file() call. Returns None if already seen or on error.
        '''
        path = Path(path).resolve()
        if path in self.encountered_files:
            print(f"Stopped circular json import from {path}")
            return None
        self.encountered_files.add(path)

        try:
            with open(path, encoding="utf-8") as json_file:
                return json.load(json_file)
        except Exception as e:
            print(f"Error during json merge from file ({path}): {e}")
            return None

    def _merge_from_file(self, current_dict: dict, path: Path, key_roots: dict[str, Path] | None = None):
        '''
        Loads the given path as a json file, then deeply overwrites the old dict
        using the new dict.
        example: current_dict["x"] = new_dict["x"] if new_dict["x"] is not dict

        "_ref" paths found inside resolve against path's own parent directory
        (see deeper_merge), not a fixed root - so a folder of files can
        reference its siblings without knowing where it's been placed.
        '''
        path = Path(path)
        data = self._load_file(path)
        if data is None:
            return
        self.deeper_merge(current_dict, data, Path(path).resolve().parent, key_roots)

    def deeper_merge(self, base_dict: dict, better_dict: dict | None, base_path: Path, key_roots: dict[str, Path] | None = None):
        '''
        better_dict ultimately comes from disk (a settings/preset file, or a
        preference value round-tripped through JSON) - it may not actually be
        a dict if the file was hand-edited or corrupted. Skip rather than crash.

        base_path is the directory any "_ref" entries in better_dict resolve
        against - the directory of the file better_dict was itself loaded from.

        key_roots optionally redirects specific top-level keys of better_dict
        (e.g. a page config's "settings"/"menu_bar"/"panes") to resolve their
        own "_ref"s against a fixed directory instead of base_path, so a page
        can reference shared settings/layout data by a stable key without
        knowing how deep its own folder sits under assets/pages. It's only
        consulted for better_dict's own keys - once recursed into, nested
        dicts resolve normally against wherever they were loaded from.
        '''
        if not isinstance(better_dict, dict):
            return
        for key, value in better_dict.items():
            key_base_path = base_path
            if key_roots and key in key_roots:
                key_base_path = key_roots[key]
            if key == self._ref_word:
                refs = value if isinstance(value, list) else [value]
                for ref in refs:
                    if not isinstance(ref, str):
                        print(f"Error resolving _ref in {base_path}: {ref!r} is not a relative path string")
                        continue
                    # If we already merged this file, skip it (see _merge_from_file)
                    self._merge_from_file(base_dict, base_path / ref)
            elif isinstance(value, dict):
                # Always recurse into a nested dict, even if base_dict has
                # nothing there yet - a plain overwrite would skip this
                # dict's own contents, silently missing any "_ref" nested
                # inside it instead of resolving it.
                if not isinstance(base_dict.get(key), dict):
                    base_dict[key] = {}
                self.deeper_merge(base_dict[key], value, key_base_path)
            elif isinstance(value, list):
                base_dict[key] = self.resolve_list(value, key_base_path)
            else:
                base_dict[key] = value

    def resolve_list(self, items: list, base_path: Path) -> list:
        '''
        Processes a JSON array for "_ref" splicing (see merge_from_file) and
        recurses into any dict/list elements it contains so refs nested
        further down (e.g. a pane-tree list of {"weight": ..., "panes": {"_ref": ...}})
        are resolved too.
        '''
        resolved = []
        for item in items:
            if isinstance(item, dict) and self._ref_word in item:
                refs = item[self._ref_word]
                refs = refs if isinstance(refs, list) else [refs]
                for ref in refs:
                    if not isinstance(ref, str):
                        print(f"Error resolving _ref in {base_path}: {ref!r} is not a relative path string")
                        continue
                    ref_path = base_path / ref
                    data = self._load_file(ref_path)
                    if data is None:
                        continue
                    if isinstance(data, list):
                        resolved.extend(self.resolve_list(data, Path(ref_path).resolve().parent))
                    else:
                        print(f"Error resolving list _ref in {base_path}: {ref_path} must contain a JSON array, got {type(data).__name__}")
            elif isinstance(item, dict):
                merged = {}
                self.deeper_merge(merged, item, base_path)
                resolved.append(merged)
            elif isinstance(item, list):
                resolved.append(self.resolve_list(item, base_path))
            else:
                resolved.append(item)
        return resolved

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
            self.paths.generate_path(file_path.parent)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Err: [{e}]. Other error occurred while saving json.")

