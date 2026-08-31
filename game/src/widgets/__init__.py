from customtkinter import CTkFrame
from ..app_core import Context

from .frame_widgets.menu_bar import MenuBar
from .frame_widgets.title_menu import TitleMenu
from .frame_widgets.panes import Panes
from .frame_widgets.scrollable import Scrollable
from .frame_widgets.overlay import Overlay
from .frame_widgets.checkbox_overlay import CheckboxOverlay

from .panels.panel import Panel as GenericPanel
from .panels.hacking_panel._builder import Builder as HackingPanel
from .panels.status_console._builder import Builder as StatusConsole
from .panels.packet_console._builder import Builder as PacketConsole
from .panels.boat_model._builder import Builder as BoatModel
from .panels.hvac_model._builder import Builder as HVACModel
from .panels.network_diagram._builder import Builder as NetworkDiagram
from .panels.variable_monitor._builder import Builder as VariableMonitor
from .panels.modbus_panel._builder import Builder as ModbusPanel

from .canvases.test_triangle import TriangleCanvas

PANELS = {
    HackingPanel.KEY: HackingPanel,
    ModbusPanel.KEY: ModbusPanel,
    PacketConsole.KEY: PacketConsole,
    NetworkDiagram.KEY: NetworkDiagram,
    StatusConsole.KEY: StatusConsole,
    BoatModel.KEY: BoatModel,
    HVACModel.KEY: HVACModel,
    VariableMonitor.KEY: VariableMonitor,
}

def panel(key: str, master: CTkFrame, context: Context, options: dict | None = None):
    '''
    Generic panel builder. Make panels by key instead of class name.
    options, if given, is forwarded as keyword arguments to the panel's
    builder (e.g. HackingPanel's available_forms) - a builder that doesn't
    accept them falls back to building without them rather than failing the
    whole page, since a pane-tree config may carry options meant for a
    builder that hasn't been wired up to use them yet.
    '''
    if key not in PANELS:
        GenericPanel(master, context, f"err: no panel for this key: {key}")
        return
    builder = PANELS[key]
    if not options:
        builder(master, context)
        return
    try:
        builder(master, context, **options)
    except TypeError as e:
        print(f"Panel {key!r} does not accept options {options!r} ({e}); building without them")
        builder(master, context)