from ...app_core.context import Context

# Better Widgets
from ...widgets import *
# Widgets
from ...widgets import popup
from ...pages.page import Page

# Network
from ...network.network_controller import HardwareAttacker as HardwareNetwork

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

    # Forms
        hacking_side = Panes(trifold.pane(0), context, "vertical", 2, [2.3, 2], False)
        HackingPanel(hacking_side.pane(0), context)
        ModbusPanel(hacking_side.pane(1), context)

    # Console
        console = Panes(trifold.pane(1), context, "vertical", 3, [3, 3, 3], False)
        PacketConsole(console.pane(0), context)
        NetworkDiagram(console.pane(1), context)
        StatusConsole(console.pane(2), context)


    # Displays
        display = Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
        BoatModel(display.pane(0), context)
        # display.bottom.configure(fg_color=context.style.color("panel"))
        # values = ValuesTable(style, top, context)
        VariableMonitor(display.pane(1), context, {
            "Speed": lambda: net.buffer.modbus.get_history("hreg_3", "in"),
            "Rudder": lambda: net.buffer.modbus.get_history("hreg_4", "in"),
            "Heading": lambda: net.buffer.modbus.get_history("hreg_12", "in"),
            "X Position": lambda: net.buffer.modbus.get_history("hreg_10", "in"),
            "Y Position": lambda: net.buffer.modbus.get_history("hreg_11", "in"),
        })