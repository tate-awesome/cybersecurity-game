
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

from .json_backed_store import JsonBackedStore


class LocalizationManager(JsonBackedStore):
    def __init__(self, context: "Context"):
        super().__init__(
            context,
            preference_key="labels",
            default_dir=context.paths.labels,
            select_dir=context.paths.labels,
            dialog_title="Select a Localization File",
            error_label="labels",
        )

    def variable_name(self, key):
        nickname = self.context.states.get_register(key, "nickname")
        if len(nickname) > 0:
            variable_name = nickname
        else:
            variable_name = self.get("modbus_variables", key)
        return variable_name
