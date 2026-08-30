
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
            config = self.context.json.load(config_path)
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
        '''
        path = self.context.paths.pages / key / "config.json"
        return self.context.json.load(path)

    def get_build_type(self, key: str) -> str | None:
        return self.build_types.get(key)
