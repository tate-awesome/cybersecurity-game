
from pathlib import Path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context


class PageManager:
    '''
    Discovers every page config under assets/pages so the Router can
    dispatch data-driven pages by the "build_type" each one declares for
    itself, and so pages can link to each other by key.

    A page's key is its path relative to assets/pages, without ".json".
    A page is either a single file (assets/pages/start.json -> "start") or
    a folder holding a config.json, for pages that ship their own files
    like screenshots (assets/pages/lessons/arp_ip/config.json ->
    "lessons/arp_ip"). Everything else about a page - its link label,
    lesson metadata, what it links to - lives in its own config.
    '''

    SCHEMA_VERSION = 1
    FOLDER_CONFIG = "config.json"

    def __init__(self, context: "Context"):
        self.context: "Context" = context
        self.config_paths: dict[str, Path] = {}
        self.build_types: dict[str, str] = {}
        self.discover()

    # Startup
    def discover(self):
        '''
        Walks every page config under assets/pages, recording where each
        key's config lives and the "build_type" it declares. A page with no
        build_type is still linkable (see link_label) - it's built by a
        hand-written page class registered directly in the Router. Warns
        about any config whose "schema_version" this code doesn't know.
        '''
        self.config_paths = {}
        self.build_types = {}
        pages_root = self.context.paths.pages
        if not pages_root.is_dir():
            return
        for config_path in sorted(pages_root.rglob("*.json")):
            if config_path.name == self.FOLDER_CONFIG:
                key = config_path.parent.relative_to(pages_root).as_posix()
            elif (config_path.parent / self.FOLDER_CONFIG).is_file():
                # Some other file a folder page ships with, not a page itself
                continue
            else:
                key = config_path.relative_to(pages_root).with_suffix("").as_posix()
            self.config_paths[key] = config_path

            config = self.load_page_config(key)
            if config.get("schema_version") != self.SCHEMA_VERSION:
                print(f"Page {key!r} has schema_version {config.get('schema_version')!r}, expected {self.SCHEMA_VERSION}")
            build_type = config.get("build_type")
            if isinstance(build_type, str):
                self.build_types[key] = build_type

    # Reset
    def reload(self):
        self.discover()

    # Page config
    def load_page_config(self, key: str) -> dict:
        '''
        Loads and _ref-resolves the config for the page at the given key
        (see the class docstring). Returns {} for a key with no config,
        like a hand-written page nothing needs to link to.

        The "settings", "menu_bar" and "panes" keys are smart-unpacked: any
        "_ref" inside them resolves against their own known folder under
        assets/settings (see settings_roots), not the page's own folder.
        That lets a page config reference shared settings/layout data with a
        short, stable path regardless of how deeply its own folder is
        nested under assets/pages, and lets pages be moved or organized
        into subfolders freely without breaking those references.
        '''
        path = self.config_paths.get(key)
        if path is None:
            return {}
        config = self.context.json.load(path, self.settings_roots())
        if "panes" in config:
            config["panes"] = self.parse_panes(config["panes"])
        return config

    # Pane layouts
    PANE_GROUPS = {"h_panes": "horizontal", "v_panes": "vertical"}

    def parse_panes(self, layout: dict) -> dict | None:
        '''
        Converts an authored pane layout into the positional tree that
        WorkspacePage.build_panes, Panes.get_weights and the autosave
        helpers below work with:
        {"orientation": ..., "children": [{"weight": ..., "panes": {...}} | {"weight": ..., "widget": "<panel type>"}]}

        An authored layout is one group - a key starting with "h_panes"
        (side by side) or "v_panes" (stacked) - whose contents are, in
        order: "<panel type>": <weight> for a panel, or another group for
        a nested set of panes, which gives its own size as its "weight".
        Weights are proportional shares of the group they sit in. A group
        only needs the prefix, so sibling groups can be told apart by name
        ("v_panes_left", "v_panes_right"). Keys starting with "_" are notes.
        '''
        if not isinstance(layout, dict):
            return None
        groups = [(key, value) for key, value in layout.items() if self.pane_group(key)]
        if len(groups) != 1:
            print(f"Pane layout should have exactly one h_panes/v_panes group at its top, found {len(groups)}")
        if not groups:
            return None
        return self.parse_pane_group(*groups[0])

    def pane_group(self, key: str) -> str | None:
        '''The orientation a key names if it's an h_panes/v_panes group, else None.'''
        for prefix, orientation in self.PANE_GROUPS.items():
            if key.startswith(prefix):
                return orientation
        return None

    def parse_pane_group(self, key: str, group: dict) -> dict:
        children = []
        for child_key, value in group.items():
            if child_key == "weight" or child_key.startswith("_"):
                continue
            if self.pane_group(child_key):
                if not isinstance(value, dict):
                    print(f"Pane group {child_key!r} should be an object, skipping")
                    continue
                children.append({"weight": value.get("weight", 1), "panes": self.parse_pane_group(child_key, value)})
            else:
                children.append({"weight": value, "widget": child_key})
        return {"orientation": self.pane_group(key), "children": children}

    def link_label(self, key: str) -> str:
        '''
        The labels key a button linking to this page should show - the
        page's own "link_label" - so every link to a page reads the same.
        '''
        label = self.load_page_config(key).get("link_label")
        if not isinstance(label, str):
            print(f"Page {key!r} has no link_label")
            return "title_buttons__default"
        return label

    def pages_in(self, folder: str) -> dict[str, dict]:
        '''
        Every page directly inside the given folder (e.g. "lessons"),
        keyed by page key, each with its loaded config.
        '''
        prefix = f"{folder.strip('/')}/"
        return {
            key: self.load_page_config(key)
            for key in self.config_paths
            if key.startswith(prefix) and "/" not in key[len(prefix):]
        }

    def settings_roots(self) -> dict[str, Path]:
        settings = self.context.paths.settings
        return {
            "settings": settings,
            "menu_bar": settings / "menu_bar",
            "panes": settings / "panes",
        }

    def get_build_type(self, key: str) -> str | None:
        return self.build_types.get(key)

    # Page state (autosave)
    def prepare_page_config(self, key: str) -> dict:
        '''
        Loads the page's default config, then overlays anything a
        student previously autosaved for this exact page (see
        save_current_page) on top of its "settings" and "panes" - only
        the input/register values and pane weights they changed from
        those defaults - before pushing the merged settings into
        context.states (which puts them on top of _packages/_default.json)
        so the page's widgets have the right values to read as they build
        themselves. Called by WorkspacePage, the only build type with
        "settings"/"panes" to begin with.
        '''
        config = self.load_page_config(key)
        if not isinstance(config.get("settings"), dict):
            config["settings"] = {}

        saved_path = self.context.paths.user_pages / key / "config.json"
        if saved_path.is_file():
            saved = self.context.json.load(saved_path)
            self.context.json.deep_merge(config["settings"], saved.get("settings"))
            if isinstance(config.get("panes"), dict):
                self.merge_pane_weights(config["panes"], saved.get("panes"))

        self.context.states.load(config["settings"])
        return config

    def merge_pane_weights(self, default: dict | None, saved: dict | None):
        '''
        Overlays "weight" values from a previously-saved pane tree onto
        the page's own default pane tree, matched purely by position
        within each "children" list - a saved tree always comes from
        walking the live widgets built from this same default tree (see
        Panes.get_weights), so the two line up index for index without
        needing a "key" to match children by name. Everything else
        about the default tree (widget defs, nested structure) is left
        untouched. Mutates default in place.
        '''
        if not isinstance(default, dict) or not isinstance(saved, dict):
            return
        default_children = default.get("children")
        saved_children = saved.get("children")
        if not isinstance(default_children, list) or not isinstance(saved_children, list):
            return
        for default_child, saved_child in zip(default_children, saved_children):
            if not isinstance(default_child, dict) or not isinstance(saved_child, dict):
                continue
            weight = saved_child.get("weight")
            if isinstance(weight, (int, float)):
                default_child["weight"] = weight
            self.merge_pane_weights(default_child.get("panes"), saved_child.get("panes"))

    def save_current_page(self):
        '''
        Autosaves the page currently on screen to
        user_data/page_data/<key>/config.json - but only what differs
        from the page's own config.json defaults, so prepare_page_config
        can rebuild the full state by merging this diff back on top of
        them. Anything the student never touched stays out of the file,
        so later edits to the page's defaults still reach them.

        Saves the diff of context.states (kept live by the widgets that
        read/write it as the student works) against the default
        "settings", and the live pane weights (read straight off the
        Panes tree, since dragging a sash doesn't itself touch
        context.states) only if their proportions differ from the
        default "panes". If nothing differs, any old save is deleted
        instead. Called by ContextManager on page exit/app close (and by
        the Router before a refresh), while the page's widgets are still
        alive to read from. A no-op for anything but a "workspace" page,
        the only build type with "settings"/"panes" worth saving.
        '''
        key = self.context.router.current_page
        if key is None or self.get_build_type(key) != "workspace":
            return

        default = self.load_page_config(key)
        saved: dict = {}

        page_default = self.context.states.with_default(default.get("settings"))
        settings = self.context.json.diff(page_default, self.context.states.data)
        if settings:
            saved["settings"] = settings

        panes_root = getattr(self.context.router.current_frame, "panes_root", None)
        if panes_root is not None:
            weights = panes_root.get_weights()
            if not self.pane_weights_match(default.get("panes"), weights):
                saved["panes"] = weights

        path = self.context.paths.user_pages / key / "config.json"
        if saved:
            self.context.json.save_to_file(saved, path)
        else:
            path.unlink(missing_ok=True)

    def pane_weights_match(self, default: dict | None, live: dict | None, tolerance: float = 0.02) -> bool:
        '''
        Whether a live pane tree (see Panes.get_weights - pixel sizes)
        splits every level in the same proportions as the default pane
        tree's "weight"s, within tolerance (a fraction of the parent's
        total) to absorb pixel rounding. Matched by position, same as
        merge_pane_weights.
        '''
        if not isinstance(default, dict) or not isinstance(live, dict):
            return True
        default_children = default.get("children") or []
        live_children = live.get("children") or []
        if len(default_children) != len(live_children):
            return False
        default_total = sum(child.get("weight", 1) for child in default_children)
        live_total = sum(child.get("weight", 0) for child in live_children)
        if default_total <= 0 or live_total <= 0:
            return default_total == live_total
        for default_child, live_child in zip(default_children, live_children):
            default_share = default_child.get("weight", 1) / default_total
            live_share = live_child.get("weight", 0) / live_total
            if abs(default_share - live_share) > tolerance:
                return False
            if not self.pane_weights_match(default_child.get("panes"), live_child.get("panes"), tolerance):
                return False
        return True

    def delete_saved_page(self, key: str):
        '''
        Deletes any autosaved page_data for the given page (see
        save_current_page), so the next time it's built -
        prepare_page_config finding nothing there to overlay -
        it falls back to its own config.json defaults instead of
        whatever was last saved for it. Used by ContextManager.reset_data.
        '''
        path = self.context.paths.user_pages / key / "config.json"
        path.unlink(missing_ok=True)
