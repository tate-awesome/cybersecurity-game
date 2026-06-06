from ...app_core.context import Context

# Widgets
from ...widgets import common, popup
from ...widgets.frame_widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...widgets.console.packet_console import PacketConsole
from ...widgets.console.status_console import StatusConsole
from ...widgets.displays.system_model import SystemModel
from ...widgets.displays.values_table import ValuesTable
from ...widgets.displays.visualizer import Visualizer
from ...pages.page import Page

# Network
from ...network.network_controller import HardwareAttacker as HardwareNetwork

# Form widgets
from ...widgets.forms.nmap import NMap
from ...widgets.forms.arp import ARP
from ...widgets.forms.sniff import Sniff
from ...widgets.forms.mitm import MITM
from ...widgets.forms.dos import DoS
from ...widgets.forms.mitm2 import MITM2

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

        left, middle_p, right_p = common.trifold(self, context)

        left_p = common.scrollable(left, context)        

    # Forms
        nmap = NMap(left_p, context)
        arp = ARP(left_p, context)
        dos = DoS(left_p, context)
        sniff = Sniff(left_p, context)
        mitm = MITM(left_p, context)
        mitm2 = MITM2(left_p, context)
        common.scroll_deadspace(left_p, context)

    # Console
        top, bottom = common.create_bifold(middle_p, context)
        packet_console = PacketConsole(top, context)
        status_console = StatusConsole(bottom, context)


    # Displays
        top, bottom = common.create_bifold(right_p, context)
        system_model = SystemModel(top, context)
        # values = ValuesTable(style, top, context)
        network_visualizer = Visualizer(bottom, context)