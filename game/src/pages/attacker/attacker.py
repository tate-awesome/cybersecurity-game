from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...widgets.console.packet_console import PacketConsole
from ...widgets.console.status_console import StatusConsole
from ...widgets.displays.system_model import SystemModel
from ...widgets.displays.values_table import ValuesTable
from ...widgets.displays.visualizer import Visualizer

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

class AttackerV0:

    def __init__(self, context: Context):
        root = context.root
        style = Style(context)
        net = context.refresh_net(HardwareNetwork)

        menu_bar = MenuBar(style, root, "Attacker V0", context)

        left, middle_p, right_p = common.trifold(style, root)

        left_p = common.scrollable(style, left)        

    # Forms
        nmap = NMap(style, left_p, context)
        arp = ARP(style, left_p, context)
        dos = DoS(style, left_p, context)
        sniff = Sniff(style, left_p, context)
        mitm = MITM(style, left_p, context)
        mitm2 = MITM2(style, left_p, context)
        common.scroll_deadspace(style, left_p)

    # Console
        top, bottom = common.create_bifold(style, middle_p)
        packet_console = PacketConsole(style, top, context, net.data_buffer)
        status_console = StatusConsole(style, bottom, context, net.data_buffer)


    # Displays
        top, bottom = common.create_bifold(style, right_p)
        system_model = SystemModel(style, top, context)
        # values = ValuesTable(style, top, context)
        network_visualizer = Visualizer(style, bottom, context)