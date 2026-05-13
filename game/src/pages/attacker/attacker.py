from ...widgets.displays.world_map import WorldMap
from ...widgets.displays.boat_focus import BoatFocus

from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...widgets.console.packet_console import PacketConsole
from ...widgets.console.status_console import StatusConsole

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

    # NFQ widget with modifiers
        mitm = MITM(style, left_p)

        def mitm_handler(mpkt: MetaPacket):
            mpkt.wireshark_line(True)

        def start_mitm():
            context.progress["mitm"] = True
            root.update_idletasks()
            net.buffer.add_callback("mitm_handler", mitm_handler)
            net.start_mitm()

        def stop_mitm():
            root.update_idletasks()
            net.stop_mitm()
            net.buffer.remove_callback("mitm_handler")

        start_on = net.mitm_is_running()
        mitm.bind_reversible(start_mitm, stop_mitm, "Attack", start_on)

        mitm.bind_input_alert()
        mitm.load_saved_input(net.table)
        mitm.bind_input_save(net.table)
        mitm.deactivate()

    # Spacer widget
        common.scroll_deadspace(style, left_p)

    # Console
        top, bottom = common.create_bifold(style, middle_p)
        packet_console = PacketConsole(style, top, context, net.data_buffer)
        status_console = StatusConsole(style, bottom, context, net.data_buffer)


    # Displays
        top, bottom = common.create_bifold(style, right_p)
        scroll = common.scrollable(style, top)
        world_map = WorldMap(style, scroll, context, net.data_buffer)
        boat_focus = BoatFocus(style, scroll, context)
        common.scroll_deadspace(style, scroll)


    

