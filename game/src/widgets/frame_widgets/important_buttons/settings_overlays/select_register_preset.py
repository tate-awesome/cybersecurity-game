from pathlib import Path
from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class SelectRegisterPreset(SettingsOverlayButton):
    '''
    Opens a list of register presets - every JSON file in
    assets/settings/register_presets, each a partial modbus_registers
    (e.g. {"hreg_3": {"show": 1, "nickname": "Speed", ...}}). Picking one
    resets every register to _default.json's values, then applies the
    preset - so registers it doesn't mention end up hidden. The ModBus
    forms and strip charts follow modbus_registers.
    '''
    LABEL = "menu_bar_buttons_register_preset_button"
    TOOLTIP = "menu_bar_tooltips_register_preset_button"

    def populate(self, overlay: Overlay):
        presets = self.section("register_presets")
        for path in sorted(self.context.paths.register_presets.glob("*.json")):
            presets.button(self.preset_name(path), lambda path=path: self.apply(overlay, path))

    def preset_name(self, path: Path) -> str:
        '''The preset's "register_presets_<file name>" label, or its file name if it has none.'''
        key = f"register_presets_{path.stem}"
        if key in self.context.labels.data:
            return self.context.labels.get(key)
        return path.stem.replace("_", " ").title()

    def apply(self, overlay: Overlay, path: Path):
        registers = self.context.states.get_registers()
        # Replaced in place - other widgets hold this same dict
        registers.clear()
        registers.update(self.context.states.get_default()["modbus_registers"])
        self.context.json.deep_merge(registers, self.context.json.load(path))
        overlay.close_chain()
