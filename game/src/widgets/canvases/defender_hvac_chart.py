from PySide6.QtWidgets import QWidget
from ...app_core import Context

from .hvac_chart import HVACChart


class DefenderHVACChart(HVACChart):
    '''
    Defender-page counterpart to House: the HVAC chart (see HVACChart) read
    from context.buffer.defender_modbus, ported from the old
    HVACView._build_graph/refresh's matplotlib figure so it can be selected
    as a modbus_model_panel model like WorldMap/House already are. Its
    dashed line is the AP's target setpoint.
    '''

    SECOND_LINE_LABEL = "Target Setpoint"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context)
        self.modbus = context.buffer.defender_modbus
        self.start_animation()

    def histories(self):
        return (
            self.modbus.get_history("temperature", "client_clean"),
            self.modbus.get_history("temperature", "target"),
            self.modbus.get_history("heater", "client_clean"),
        )

    def start_animation(self):
        super().start_animation()
        # This model being built/shown *is* "the HVAC model is active" -
        # see DefenderModbusBuffer.resume_hvac/pause_hvac. Lets the
        # temperature/target/heater history's relative-time clock advance
        # again after having been frozen while some other model was shown.
        self.modbus.resume_hvac(self)

    def stop_animation(self):
        super().stop_animation()
        self.modbus.pause_hvac(self)
