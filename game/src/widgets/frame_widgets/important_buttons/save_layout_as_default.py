import json

from ....app_core import Context
from ...popup import confirm_dialog, message
from ._base_button import ImportantButton


class _SaveLayoutAsDefault(ImportantButton):
    '''
    Shared by the developer buttons that write the workspace's layout as
    it is on screen (see DockArea.layout_tree) into its own config.json, as
    the default every student starts from - asking first. Live sizes are
    pixels, so weights are written as whole percentages of their group.
    The autosave then matches the defaults, so it's dropped on its own
    (see PageManager.save_current_page).
    '''
    OPENS = "warning"  # it asks first
    MESSAGE = ""

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return context.pages.get_build_type(context.router.current_page) == "workspace"

    def on_click(self):
        if self.live() is None:
            message(self.window(), self.context, "This workspace has no panels to save.")
            return
        confirm_dialog(self.window(), self.context, self.MESSAGE, "Yes, save", "No, cancel", self.save)

    def live(self) -> dict | None:
        dock = getattr(self.context.router.current_frame, "dock", None)
        return dock.layout_tree() if dock is not None else None

    def save(self):
        pages = self.context.pages
        key = self.context.router.current_page
        path = pages.config_paths[key]
        config = json.loads(path.read_text(encoding="utf-8"))
        weights = config.get("layout_weights")
        weights = weights if isinstance(weights, dict) else {}
        error = self.write(config, weights, self.live())
        if error:
            message(self.window(), self.context, error)
            return
        path.write_text(self.context.json.format_config(config), encoding="utf-8")
        message(self.window(), self.context, f"Saved to {path}.")

    def write(self, config: dict, weights: dict, live: dict) -> str | None:
        '''Puts live into config (whose "layout_weights" is weights) - or says why it can't.'''
        raise NotImplementedError


class SaveLayoutShapeAsDefault(_SaveLayoutAsDefault):
    '''
    Makes the workspace's current arrangement of panels its default
    "layout_shape", with its current sizes as "layout_weights" - but a
    group that's still at its default weights keeps them as written
    (see PageManager.authored_weights).
    '''
    LABEL = "menu_bar_buttons_save_layout_shape_button"
    TOOLTIP = "menu_bar_tooltips_save_layout_shape_button"
    MESSAGE = ("Save this arrangement of panels as this workspace's default layout?\n"
               "It's written into the workspace's config.json, for everyone who opens it.")

    def write(self, config: dict, weights: dict, live: dict) -> str | None:
        pages = self.context.pages
        config["layout_shape"] = pages.layout_shape_of(live)
        config["layout_weights"] = pages.authored_weights(live, weights)
        return None


class SaveLayoutWeightsAsDefault(_SaveLayoutAsDefault):
    '''Makes the workspace's current pane sizes its default "layout_weights" - for its default arrangement of panels.'''
    LABEL = "menu_bar_buttons_save_layout_weights_button"
    TOOLTIP = "menu_bar_tooltips_save_layout_weights_button"
    MESSAGE = ("Save these pane sizes as this workspace's default layout weights?\n"
               "They're written into the workspace's config.json, for everyone who opens it.")

    def write(self, config: dict, weights: dict, live: dict) -> str | None:
        pages = self.context.pages
        default = pages.layout_tree(pages.load_page_config(self.context.router.current_page).get("layout_shape"))
        if default is None or pages.layout_shape_of(live) != pages.layout_shape_of(default):
            return ("This workspace's panels aren't in their default arrangement, so these sizes don't fit it.\n"
                    "Save the layout shape as the default instead (that saves its sizes too), or reset the layout first.")
        config["layout_weights"] = pages.authored_weights(live, weights)
        return None
