
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

from .json_backed_store import JsonBackedStore


class InputManager(JsonBackedStore):
    def __init__(self, context: "Context"):
        super().__init__(
            context,
            preference_key="settings",
            default_dir=context.paths.packages,
            select_dir=context.paths.settings,
            dialog_title="Select Settings",
            error_label="states",
        )

    def get_registers(self):
        return self.get("modbus_variables")

    def get_register(self, key: str, field: str):
        return self.get_registers()[key][field]

    def set_register(self, key: str, field: str, value):
        self.get_registers()[key][field] = value
