
from pathlib import Path
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .. import Context


class PageManager:
    '''
    Parses assets/pages/manifest.json - the single source of truth linking
    stable keys (the startup page, game modes, lessons) to page folders -
    and discovers every page's own config.json so the Router can dispatch
    data-driven pages by the "build_type" each one declares for itself.

    A page's key is its path relative to assets/pages (e.g. "attacker_lab",
    "title/select_mode"), which doubles as the folder its config.json lives
    in. The manifest only needs an entry for a page when something else
    needs to address it by a friendlier/stable name (see game_modes,
    lessons) - most pages need no manifest entry at all.
    '''

    def __init__(self, context: "Context"):
        self.context: "Context" = context
        self.manifest_path = self.context.paths.pages / "manifest.json"
        self.manifest: dict = {}
        self.build_types: dict[str, str] = {}
        manifest: dict = self.context.json.load(self.manifest_path)
        self.parse_manifest(manifest)

    # Startup
    def parse_manifest(self, manifest: dict):
        self.manifest = manifest
        self.build_types = self.discover_build_types()

    def discover_build_types(self) -> dict[str, str]:
        '''
        Walks every config.json under assets/pages and records its declared
        "build_type", keyed by its path relative to assets/pages - the same
        key used to navigate to it. A page with no (or an unrecognized)
        build_type is left out of the result; it's either page chrome not
        yet converted to a generic page, or a page still built by a
        hand-written page class registered directly in the Router.
        '''
        build_types: dict[str, str] = {}
        pages_root = self.context.paths.pages
        if not pages_root.is_dir():
            return build_types
        for config_path in pages_root.rglob("config.json"):
            key = config_path.parent.relative_to(pages_root).as_posix()
            config = self.context.json.load(config_path, self.settings_roots())
            build_type = config.get("build_type")
            if isinstance(build_type, str):
                build_types[key] = build_type
        return build_types

    # Reset
    def reload(self):
        manifest: dict = self.context.json.load(self.manifest_path)
        self.parse_manifest(manifest)

    # Control (readonly)
    def get(self, *keys: str) -> Any:
        '''
        Returns the value at the given key sequence in the manifest.
        Raises a KeyError naming the full path if the path doesn't have a value.
        '''
        output = self.manifest
        for i, key in enumerate(keys):
            if not isinstance(output, dict) or key not in output:
                raise KeyError(f"manifest{''.join(f'[{k!r}]' for k in keys[:i + 1])} not found (full path requested: {keys})")
            output = output[key]
        return output

    def startup_page(self) -> str:
        return self.get("startup_page")

    # Page config
    def load_page_config(self, key: str) -> dict:
        '''
        Loads and _ref-resolves the config.json for the page at the given
        key (its path relative to assets/pages, e.g. "attacker_lab").

        The "settings", "menu_bar" and "panes" keys are smart-unpacked: any
        "_ref" inside them resolves against their own known folder under
        assets/settings (see settings_roots), not the page's own folder.
        That lets a page config reference shared settings/layout data with a
        short, stable path regardless of how deeply its own folder is
        nested under assets/pages, and lets pages be moved or organized
        into subfolders freely without breaking those references.
        '''
        path = self.context.paths.pages / key / "config.json"
        return self.context.json.load(path, self.settings_roots())

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
        save_current_page) on top of its "settings" and "panes" - the
        input/register values their forms held, and the pane weights
        they'd dragged - before pushing the merged settings into
        context.states so the page's widgets have the right values to
        read as they build themselves. Called by WorkspacePage, the
        only build type with "settings"/"panes" to begin with.
        '''
        config = self.load_page_config(key)

        saved_path = self.context.paths.user_pages / key / "config.json"
        if saved_path.is_file():
            saved = self.context.json.load(saved_path)
            if isinstance(config.get("settings"), dict):
                self.context.json.deep_merge(config["settings"], saved.get("settings"))
            if isinstance(config.get("panes"), dict):
                self.merge_pane_weights(config["panes"], saved.get("panes"))

        self.context.states.load(config.get("settings", {}))
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
        Autosaves the page currently on screen: its context.states
        (kept live by the widgets that read/write it as the student
        works) and its pane weights (read straight off the live Panes
        tree, since dragging a sash doesn't itself touch context.states)
        - to assets/user_data/page_data/<key>/config.json, so
        prepare_page_config can restore them next time this page is
        shown. Called by the Router right before it tears down or
        rebuilds the current page (quit, go_back, refresh), while the
        page's widgets are still alive to read from. A no-op for
        anything but a "workspace" page, the only build type with
        "settings"/"panes" worth saving.
        '''
        key = self.context.router.current_page
        if key is None or self.get_build_type(key) != "workspace":
            return

        saved: dict = {"settings": self.context.states.data}

        panes_root = getattr(self.context.router.current_frame, "panes_root", None)
        if panes_root is not None:
            saved["panes"] = panes_root.get_weights()

        path = self.context.paths.user_pages / key / "config.json"
        self.context.json.save_to_file(saved, path)

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
