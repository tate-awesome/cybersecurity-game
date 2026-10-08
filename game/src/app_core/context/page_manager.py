
import json
import shutil
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
    like screenshots (assets/pages/workspaces/arp_ip/config.json ->
    "workspaces/arp_ip"). Everything else about a page - its link label,
    workspace metadata, what it links to - lives in its own config.
    '''

    SCHEMA_VERSION = 1
    FOLDER_CONFIG = "config.json"

    def __init__(self, context: "Context"):
        self.context: Context = context
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

        The "settings", "menu_bar", "layout_shape" and "layout_weights" keys are smart-unpacked: any
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
        return self.context.json.load(path, self.settings_roots())

    # Pane layouts
    PANE_GROUPS = {"h_panes": "horizontal", "v_panes": "vertical"}

    def layout_tree(self, shape: dict | None, weights: dict | None = None) -> dict | None:
        '''
        Combines a page config's "layout_shape" and "layout_weights" into
        the positional tree that WorkspacePage.build_panes, the layout
        editor and the autosave helpers below work with:
        {"id": ..., "orientation": ..., "children": [{"id": ..., "weight": ..., "panes": {...}} | {"id": ..., "weight": ..., "widget": "<panel type>"}]}

        "layout_shape" is one group: {"h_panes_1": [...]} (side by side)
        or {"v_panes_1": [...]} (stacked), listing its contents in order -
        a panel id string like "status_panel_1", or another group of the
        same form. Every id is its type plus a number, so the same panel
        type can appear any number of times as long as each copy's number
        differs. "layout_weights" is a flat {id: weight}: each pane's
        proportional share of the group it sits in (default 1). The top
        group fills the page, so it needs no weight.
        '''
        if not isinstance(shape, dict):
            return None
        groups = [(key, value) for key, value in shape.items() if self.pane_group(key)]
        if len(groups) != 1:
            print(f"layout_shape should have exactly one h_panes/v_panes group at its top, found {len(groups)}")
        if not groups:
            return None
        weights = weights if isinstance(weights, dict) else {}
        seen = set()
        tree = self.parse_layout_group(*groups[0], weights, seen)
        for unused in sorted(set(weights) - seen):
            if not unused.startswith("_"):
                print(f"layout_weights has {unused!r}, which isn't in layout_shape")
        return tree

    def pane_group(self, key: str) -> str | None:
        '''The orientation a key names if it's an h_panes/v_panes group id, else None.'''
        for prefix, orientation in self.PANE_GROUPS.items():
            if key.startswith(prefix):
                return orientation
        return None

    @staticmethod
    def panel_type(panel_id: str) -> str:
        '''The panel type a layout id names: "status_panel_2" -> "status_panel".'''
        base, _, number = panel_id.rpartition("_")
        return base if base and number.isdigit() else panel_id

    def parse_layout_group(self, group_id: str, contents, weights: dict, seen: set) -> dict:
        seen.add(group_id)
        children = []
        if not isinstance(contents, list):
            print(f"Layout group {group_id!r} should be a list, skipping its contents")
            contents = []
        for item in contents:
            if isinstance(item, str):
                child_id, value = item, None
            elif isinstance(item, dict) and len(item) == 1:
                child_id, value = next(iter(item.items()))
                if not self.pane_group(child_id):
                    print(f"Layout group {child_id!r} should start with h_panes or v_panes, skipping")
                    continue
            else:
                print(f"Layout item {item!r} in {group_id!r} should be a panel id or a one-key group, skipping")
                continue
            if child_id in seen:
                print(f"Layout id {child_id!r} is used more than once - give each copy its own number")
            seen.add(child_id)
            weight = weights.get(child_id, 1)
            if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
                print(f"layout_weights[{child_id!r}] should be a number above 0, using 1")
                weight = 1
            child = {"id": child_id, "weight": weight}
            if value is None:
                child["widget"] = self.panel_type(child_id)
            else:
                child["panes"] = self.parse_layout_group(child_id, value, weights, seen)
            children.append(child)
        return {"id": group_id, "orientation": self.pane_group(group_id), "children": children}

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
        Every page directly inside the given folder (e.g. "workspaces"),
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
            "layout_shape": settings / "layout_shape",
            "layout_weights": settings / "layout_weights",
        }

    def get_build_type(self, key: str) -> str | None:
        return self.build_types.get(key)

    # Page state (autosave)
    def prepare_page_config(self, key: str) -> dict:
        '''
        Loads the page's default config, then overlays anything a
        student previously autosaved for this exact page (see
        save_current_page) on top of its "settings" and "layout_weights" -
        only the input/register values and pane weights they changed from
        those defaults - before pushing the merged settings into
        context.states (which puts them on top of _packages/_default.json)
        so the page's widgets have the right values to read as they build
        themselves. Also adds "layout": the layout_tree built from the
        page's shape and those merged weights. Called by WorkspacePage,
        the only build type with "settings"/"layout_shape" to begin with.
        '''
        config = self.load_page_config(key)
        if not isinstance(config.get("settings"), dict):
            config["settings"] = {}
        if not isinstance(config.get("layout_weights"), dict):
            config["layout_weights"] = {}

        saved_path = self.context.paths.user_pages / key / "config.json"
        if saved_path.is_file():
            saved = self.context.json.load(saved_path)
            self.context.json.deep_merge(config["settings"], saved.get("settings"))
            saved_weights = saved.get("layout_weights")
            if isinstance(saved_weights, dict):
                # Matched by id, so a saved weight only lands on a pane that's still in the layout
                tree = self.layout_tree(config.get("layout_shape"))
                ids = self.layout_ids(tree) if tree else set()
                for pane_id, weight in saved_weights.items():
                    if pane_id in ids and isinstance(weight, (int, float)) and weight > 0:
                        config["layout_weights"][pane_id] = weight

        config["layout"] = self.layout_tree(config.get("layout_shape"), config["layout_weights"])
        self.context.states.load(config["settings"])
        return config

    def layout_ids(self, tree: dict) -> set[str]:
        '''Every pane id below the top group of a layout_tree.'''
        ids = set()
        for child in tree.get("children", []):
            ids.add(child["id"])
            if "panes" in child:
                ids |= self.layout_ids(child["panes"])
        return ids

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
        Panes tree as {id: size}, since dragging a sash doesn't itself
        touch context.states) as "layout_weights" only if their
        proportions differ from the default layout. If nothing differs,
        any old save is deleted instead. Called by ContextManager on page
        exit/app close (and by the Router before a refresh), while the
        page's widgets are still alive to read from. A no-op for anything
        but a "workspace" page, the only build type with
        "settings"/"layout_shape" worth saving.
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
            tree = self.layout_tree(default.get("layout_shape"), default.get("layout_weights"))
            if not self.pane_weights_match(tree, weights):
                saved["layout_weights"] = weights

        path = self.context.paths.user_pages / key / "config.json"
        if saved:
            self.context.json.save_to_file(saved, path)
        else:
            path.unlink(missing_ok=True)

    def pane_weights_match(self, default: dict | None, live: dict, tolerance: float = 0.02) -> bool:
        '''
        Whether live pane sizes (see Panes.get_weights - {id: pixel size})
        split every group in the same proportions as the default
        layout_tree's "weight"s, within tolerance (a fraction of the
        group's total) to absorb pixel rounding.
        '''
        if not isinstance(default, dict):
            return True
        children = default.get("children") or []
        if any(child["id"] not in live for child in children):
            return False
        default_total = sum(child["weight"] for child in children)
        live_total = sum(live[child["id"]] for child in children)
        if default_total <= 0 or live_total <= 0:
            return default_total == live_total
        for child in children:
            if abs(child["weight"] / default_total - live[child["id"]] / live_total) > tolerance:
                return False
            if not self.pane_weights_match(child.get("panes"), live, tolerance):
                return False
        return True

    def delete_saved_page(self, key: str):
        '''
        Deletes any autosaved page_data for the given page (see
        save_current_page), so the next time it's built -
        prepare_page_config finding nothing there to overlay -
        it falls back to its own config.json defaults instead of
        whatever was last saved for it. Used by ResetCurrentPageToDefaults
        and the workspace select page.
        '''
        path = self.context.paths.user_pages / key / "config.json"
        path.unlink(missing_ok=True)

    def delete_saved_page_part(self, key: str, part: str):
        '''
        Deletes one part ("settings" or "panes") of the given page's
        autosaved page_data (see save_current_page), keeping the other -
        and the whole file if nothing's left in it.
        '''
        path = self.context.paths.user_pages / key / "config.json"
        if not path.is_file():
            return
        saved = self.context.json.load(path)
        saved.pop(part, None)
        if saved:
            self.context.json.save_to_file(saved, path)
        else:
            path.unlink(missing_ok=True)

    def page_panel_keys(self, key: str | None) -> set[str] | None:
        '''
        Every panel key (see widgets.PANELS) the page's "panes" places,
        whichever form the tree is written in - a key of its own or a
        "widget" value. None if the page has no "panes" in its config (its
        panels, if any, are built in code), so callers can't know.
        '''
        if key is None:
            return None
        panes = self.load_page_config(key).get("panes")
        if not isinstance(panes, (dict, list)):
            return None
        found: set[str] = set()

        def walk(node):
            if isinstance(node, dict):
                for name, value in node.items():
                    found.add(name)
                    if name == "widget" and isinstance(value, str):
                        found.add(value)
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(panes)
        return found

    def has_saved_page(self, key: str) -> bool:
        '''Whether the given page has any autosaved page_data (see save_current_page).'''
        return (self.context.paths.user_pages / key / "config.json").is_file()

    def delete_all_saved_pages(self):
        '''
        Deletes every page's autosaved page_data - the whole
        user_data/page_data folder - leaving everything else in user_data
        (preferences like theme, labels and favorite page; captures) alone.
        '''
        shutil.rmtree(self.context.paths.user_pages, ignore_errors=True)
        self.context.paths.generate_path(self.context.paths.user_pages)

    # Creating and deleting pages
    def create_folder_page(self, key: str, config: dict):
        '''
        Writes a new folder page - assets/pages/<key>/config.json - and
        rediscovers pages so it can be navigated to. The Router still has
        to register it (see Router.register_discovered_pages).
        '''
        folder = self.context.paths.pages / key
        folder.mkdir(parents=True)
        (folder / self.FOLDER_CONFIG).write_text(self.context.json.format_config(config), encoding="utf-8")
        self.discover()

    def delete_folder_page(self, key: str):
        '''
        Permanently deletes a folder page: its whole folder under
        assets/pages, every student's autosaved data for it, and any other
        page's "prerequisites" entry naming it. Rediscovers pages afterward;
        the Router still has to drop it (see Router.register_discovered_pages).
        '''
        path = self.config_paths.get(key)
        if path is None or path.name != self.FOLDER_CONFIG:
            raise ValueError(f"{key!r} isn't a folder page")
        shutil.rmtree(path.parent)
        shutil.rmtree(self.context.paths.user_pages / key, ignore_errors=True)
        for other_path in self.config_paths.values():
            if not other_path.is_file():
                continue
            other = json.loads(other_path.read_text(encoding="utf-8"))
            if key in other.get("prerequisites", []):
                other["prerequisites"] = [item for item in other["prerequisites"] if item != key]
                other_path.write_text(self.context.json.format_config(other), encoding="utf-8")
        self.discover()
