from ...app_core.context import Context

# Better Widgets
from ...widgets import Trifold, MenuBar, Bifold, Scrollable
from ...widgets import ArpForm, NmapForm, DosForm, MitmForm, Mitm2Form, SniffForm
from ...widgets import NetworkVisualizer

# Widgets
from ...widgets import popup
from ...drawing.viewport import ViewPort
from ...widgets.console.packet_console import PacketConsole
from ...widgets.console.status_console import StatusConsole
from ...widgets.displays.system_model import SystemModel
from ...widgets.displays.values_table import ValuesTable
from ...widgets.displays.visualizer import Visualizer
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
        menu_bar.all_buttons()

        trifold = Trifold(self, context)

        left_p = Scrollable(trifold.left, context)       
        middle_p = trifold.middle
        right_p = trifold.right

    # Forms
        nmap = NmapForm(left_p, context)
        arp = ArpForm(left_p, context)
        dos = DosForm(left_p, context)
        sniff = SniffForm(left_p, context)
        mitm = MitmForm(left_p, context)
        mitm2 = Mitm2Form(left_p, context)
        left_p.add_deadspace()

    # Console
        console = Bifold(middle_p, context)
        packet_console = PacketConsole(console.top, context)
        status_console = StatusConsole(console.bottom, context)


    # Displays
        display = Bifold(right_p, context)
        system_model = SystemModel(display.top, context)
        # values = ValuesTable(style, top, context)
        bottom = Scrollable(display.bottom, context)
        network_visualizer = NetworkVisualizer(bottom, context)
        bottom.add_deadspace(1000)