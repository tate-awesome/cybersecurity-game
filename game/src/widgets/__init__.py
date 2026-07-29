from .frame_widgets.menu_bar import MenuBar
from .frame_widgets.title_menu import TitleMenu
from .frame_widgets.panes import Panes
from .frame_widgets.scrollable import Scrollable
from .frame_widgets.overlay import Overlay

from .panels.hacking_panel._builder import Builder as HackingPanel
from .panels.status_console._builder import Builder as StatusConsole
from .panels.packet_console._builder import Builder as PacketConsole
from .panels.boat_model._builder import Builder as BoatModel
from .panels.network_diagram._builder import Builder as NetworkDiagram
from .panels.variable_monitor._builder import Builder as VariableMonitor

from .canvases.test_triangle import TriangleCanvas