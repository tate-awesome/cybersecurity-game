from customtkinter import CTkFrame
from .....app_core import Context
from ...base_form import BaseForm

SUBMARINE_VARIABLES = ["x", "y", "theta", "speed", "rudder"]
HVAC_VARIABLES = ["temperature"]
ATTRIBUTES = ["client_clean", "client_noisy", "server_clean", "server_noisy", "target"]


class ReadoutForm(BaseForm):
    '''
    One row per named defender_modbus variable (including its target),
    columns for all four client/server clean/noisy attributes plus target -
    like modbus_panel's MitmTable, but keyed by variable name/attribute
    instead of register/in-out. Rows show/hide by whichever variables
    belong to the AP's current mode (context.buffer.defender_status.
    submarine_mode), not a static settings toggle.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, attack_noun="Readout")

        for i in range(len(ATTRIBUTES) + 1):
            self.columnconfigure(i, weight=1)

        self.add_header("Live Modbus Readout")

        self.rows = {}
        self.add_label_row("defender_modbus_readout", ["name"] + ATTRIBUTES)

        for key in SUBMARINE_VARIABLES + HVAC_VARIABLES:
            labels = self.add_label_row("defender_modbus_readout", ["-"] * (len(ATTRIBUTES) + 1))
            row = {"name": labels[0]}
            for i, attribute in enumerate(ATTRIBUTES):
                row[attribute] = labels[i + 1]
            row["name"].configure(text=self.context.labels.get("modbus_variables", key))
            self.rows[key] = row

        self.context.animation_manager.add_callback(f"DefenderReadoutForm_{id(self)}", self.refresh)
        self.refresh()

    def format_number(self, value, decimals: int = 3) -> str:
        try:
            return f"{float(value):.{decimals}f}"
        except (TypeError, ValueError):
            return "-"

    def refresh(self):
        modbus = self.context.buffer.defender_modbus
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        active_variables = SUBMARINE_VARIABLES if submarine_mode else HVAC_VARIABLES

        for key, row in self.rows.items():
            visible = key in active_variables
            for widget in row.values():
                if visible and not widget.winfo_ismapped():
                    widget.grid()
                elif not visible and widget.winfo_ismapped():
                    widget.grid_remove()

            if not visible:
                continue

            for attribute in ATTRIBUTES:
                row[attribute].configure(text=self.format_number(modbus.get_single(key, attribute)))
