import json

from .....app_core import Context
from ....popup import confirm_dialog, message
from .._base_button import ImportantButton
from .columns_overlay import is_column_available, tray_columns


class SavePacketColumnsAsDefault(ImportantButton):
    '''
    Developers: makes the packet console's current columns this workspace's
    defaults, in its own config.json - the tray's columns in their order
    ("packet_columns") and which fields students get
    ("packet_columns_available"), each written as just what differs from
    _packages/_default.json - asking first. The autosave then matches the
    defaults, so it drops them on its own (see PageManager.save_current_page).
    '''
    LABEL = "menu_bar_buttons_save_packet_columns_button"
    TOOLTIP = "menu_bar_tooltips_save_packet_columns_button"
    OPENS = "warning"  # it asks first

    @classmethod
    def is_available(cls, context: Context) -> bool:
        if context.pages.get_build_type(context.router.current_page) != "workspace":
            return False
        panels = context.pages.page_panel_keys(context.router.current_page)
        return panels is None or "packet_panel" in panels

    def on_click(self):
        confirm_dialog(self.window(), self.context,
                       "Save the packet console's current columns as this workspace's default?\n"
                       "They're written into the workspace's config.json, for everyone who opens it.",
                       "Yes, save", "No, cancel", self.save)

    def save(self):
        context = self.context
        path = context.pages.config_paths[context.router.current_page]
        config = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(config.get("settings"), dict):
            config["settings"] = {}
        settings = config["settings"]
        default = context.states.get_default()
        # Tidied: places numbered 1 up, and ints like _default.json's (older saves hold "1"/"0")
        tray = tray_columns(context)
        live = {
            "packet_columns": {key: tray.index(key) + 1 if key in tray else 0 for key in context.states.get("packet_columns")},
            "packet_columns_available": {key: 1 if is_column_available(context, key) else 0
                                         for key in context.states.get("packet_columns_available")},
        }
        for name, values in live.items():
            # Tidied in place too, so the autosave finds nothing left to save
            context.states.get(name).update(values)
            changed = context.json.diff(default.get(name, {}), values)
            if changed:
                settings[name] = changed
            else:
                settings.pop(name, None)
        path.write_text(context.json.format_config(config), encoding="utf-8")
        message(self.window(), context, f"Saved to {path}.")
