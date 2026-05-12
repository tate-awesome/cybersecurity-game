from ...widgets.displays.world_map import WorldMap

from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...widgets.console.console import Console

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
        console = Console(style, middle_p, context, net.data_buffer)


    # Map
        world_map = WorldMap(style, right_p, context, net.data_buffer)




    # Map callback
    def draw_test_plane(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
        import time
        from ...drawing import transformations as t

        path_duration = 30.0
        path_index = int(((time.time() % path_duration) / path_duration) * (len(self.positions)-2))
        bearing = t.get_bearing(self.positions[path_index], self.positions[path_index+1])
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.bbox()
            draw.grid_lines()
            draw.line(self.positions, self.color)
            last_position = self.positions[path_index]
            draw.boat(last_position, bearing)
    

