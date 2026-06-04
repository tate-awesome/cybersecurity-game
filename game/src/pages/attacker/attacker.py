from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...widgets.console.packet_console import PacketConsole
from ...widgets.console.status_console import StatusConsole
from ...widgets.displays.build_displays import Displays
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
        nmap = NMap(style, left_p, context, net.do_nmap)
        arp = ARP(style, left_p, context, net.start_arp, net.arp_is_running, net.stop_arp)
        dos = DoS(style, left_p, context, net.start_dos, net.dos_is_running, net.stop_dos)
        sniff = Sniff(style, left_p, context, net.start_sniff, net.sniff_is_running, net.stop_sniff)
        mitm = MITM(style, left_p, context, net.start_mitm, net.mitm_is_running, net.stop_mitm)
        common.scroll_deadspace(style, left_p)

    # Console
        top, bottom = common.create_bifold(style, middle_p)
        packet_console = PacketConsole(style, top, context, net.data_buffer)
        status_console = StatusConsole(style, bottom, context, net.data_buffer)


    # Displays
        top, bottom = common.create_bifold(style, right_p)
        displays = Displays(style, top, context)
        # values = ValuesTable(style, top, context)
        network_visualizer = Visualizer(style, bottom, context)