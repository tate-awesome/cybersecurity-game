from PySide6.QtWidgets import QWidget
from ...app_core import Context

from .hvac_chart import HVACChart


class SniffedHVACChart(HVACChart):
    '''
    Sniffed counterpart to DefenderHVACChart: the same HVAC chart (see
    HVACChart), read from the ModBus traffic this computer sniffed or
    intercepted (context.buffer.hvac), like House. Sniffed traffic carries
    no setpoint, so its dashed line is instead the temperature this MITM
    vantage point forwarded on to the controller ("out") - next to the
    house's own reading ("in"), it shows any tampering in transit. The
    heater line is what the controller commanded ("in").
    '''

    SECOND_LINE_LABEL = "Controller Sees"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context)
        self.buffer = context.buffer.hvac
        self.start_animation()

    def histories(self):
        return (
            self.buffer.get_history("temperature", "in"),
            self.buffer.get_history("temperature", "out"),
            self.buffer.get_history("heater", "in"),
        )
