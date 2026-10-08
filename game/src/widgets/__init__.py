import inspect

from PySide6.QtWidgets import QWidget
from ..app_core import Context

from .frame_widgets.menu_bar import MenuBar
from .frame_widgets.title_menu import TitleMenu
from .frame_widgets.panes import Panes
from .frame_widgets.scrollable import Scrollable
from .frame_widgets.overlay import Overlay
from .frame_widgets.shift_wheel_slider import ShiftWheelSlider

from .panels.panel import Panel as GenericPanel
from .panels.network_action_panel._builder import Builder as HackingPanel
from .panels.status_console._builder import Builder as StatusConsole
from .panels.packet_console._builder import Builder as PacketConsole
from .panels.modbus_model._builder import Builder as ModbusModel
from .panels.network_diagram._builder import Builder as NetworkDiagram
from .panels.variable_monitor._builder import Builder as VariableMonitor
from .panels.modbus_panel._builder import Builder as ModbusPanel
from .panels.defender_modbus_panel._builder import Builder as DefenderModbusPanel
from .panels.defender_stripchart_panel._builder import Builder as DefenderStripchartPanel
from .panels.defender_console._builder import Builder as DefenderConsole
from .panels.defender_flag_panel._builder import Builder as DefenderFlagPanel

from .canvases.test_triangle import TriangleCanvas
from .visuals import VISUALS, VisualBackground

PANELS = {
    HackingPanel.KEY: HackingPanel,
    ModbusPanel.KEY: ModbusPanel,
    PacketConsole.KEY: PacketConsole,
    NetworkDiagram.KEY: NetworkDiagram,
    StatusConsole.KEY: StatusConsole,
    ModbusModel.KEY: ModbusModel,
    VariableMonitor.KEY: VariableMonitor,
    DefenderModbusPanel.KEY: DefenderModbusPanel,
    DefenderStripchartPanel.KEY: DefenderStripchartPanel,
    DefenderConsole.KEY: DefenderConsole,
    DefenderFlagPanel.KEY: DefenderFlagPanel,
}

def panel(key: str, master: QWidget, context: Context, panel_id: str | None = None):
    '''
    Generic panel builder. Make panels by key instead of class name.
    panel_id is the panel's id in the layout ("modbus_model_panel_2"),
    passed on to builders that take one - so per-copy settings (see
    ModbusModel and "model_panels") can tell the copies apart.
    '''
    if key not in PANELS:
        GenericPanel(master, context, f"err: no panel for this key: {key}")
        return
    builder = PANELS[key]
    if "panel_id" in inspect.signature(builder).parameters:
        builder(master, context, panel_id=panel_id)
    else:
        builder(master, context)
