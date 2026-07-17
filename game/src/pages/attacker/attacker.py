from ...app_core.context import Context

# Better Widgets
from ...widgets import Panes, MenuBar
from ...widgets import HackingPanel, StatusConsole, PacketConsole, NetworkDiagram, BoatModel, VariableMonitor

# Widgets
from ...widgets import popup
from ...pages.page import Page

# Network
from ...network.network_controller import HardwareAttacker as HardwareNetwork

# Packet
from ...network.meta_packet import MetaPacket

class AttackerV0(Page):
    '''
    Page constructor for attacker/attackerv0. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)
        net = context.refresh_net(HardwareNetwork)

        menu_bar = MenuBar(self, context, "Attacker V0")
        menu_bar.page_buttons()

        trifold = Panes(self, context, "horizontal", 3, [4, 3, 2], True)

        left_p = trifold.pane(0)       
        middle_p = trifold.pane(1)
        right_p = trifold.pane(2)

    # Forms
        hacking_panel = HackingPanel(left_p, context)

    # Console
        console = Panes(middle_p, context, "vertical", 3, [3, 3, 3], False)
        packet_console = PacketConsole(console.pane(0), context)
        network_visualizer = NetworkDiagram(console.pane(1), context)
        status_console = StatusConsole(console.pane(2), context)


    # Displays
        display = Panes(right_p, context, "vertical", 2, [2, 2], False)
        system_model = BoatModel(display.pane(0), context)
        # display.bottom.configure(fg_color=context.style.color("panel"))
        # values = ValuesTable(style, top, context)
        monitor = VariableMonitor(display.pane(1), context, {
            "Speed": lambda: net.data_buffer.get_tracer_data("speed", "other"),
            "Rudder": lambda: net.data_buffer.get_tracer_data("rudder", "other"),
            "Heading": lambda: net.data_buffer.get_tracer_data("theta", "other"),
            "X Position": lambda: net.data_buffer.get_tracer_data("x", "other"),
            "Y Position": lambda: net.data_buffer.get_tracer_data("y", "other"),
        })