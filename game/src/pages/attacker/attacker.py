from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort

# Network
from ...network.network_controller import HardwareNetwork

# Form widgets
from ...widgets.forms.nmap import NMap
from ...widgets.forms.arp import ARP
from ...widgets.forms.sniff import Sniff
from ...widgets.forms.mitm import MITM
from ...widgets.forms.dos import DOS

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

    # NMap Widget
        nmap = NMap(style, left_p)
        def do_nmap():
            context.progress["nmap"] = True
            nmap.status.configure(text="Pinging...")
            root.update_idletasks()

            ip, netmask = net.nmap.get_network()
            network = net.nmap.compute_network(ip, netmask)
            hosts = net.nmap.get_hosts(network)
            host_ips = net.nmap.get_host_ips(hosts)
            print(host_ips) # TODO push this to the GUI console

            nmap.status.configure(text="NMap Complete")
    
        nmap.bind(do_nmap, nmap.button)
        if context.progress["nmap"]:
            nmap.status.configure(text="NMap Complete")
        else:
            nmap.status.configure(text="")

    # ARP Widget
        arp = ARP(style, left_p)
        def start_arp():
            target_ip = str(arp.entry1.get())
            host_ip = str(arp.entry2.get())
            root.update_idletasks()
            net.start_arp(target_ip, host_ip)
        def stop_arp():
            root.update_idletasks()
            net.stop_arp()
        
        start_on = net.arp_is_running()
        arp.bind_reversible(start_arp, stop_arp, "ARP Spoof", start_on)

        arp.load_saved_input(context.inputs["arp"])
        arp.bind_input_autosave(context.inputs["arp"])

    # Sniffing Widget
        sniff = Sniff(style, left_p)

        def sniff_handler(mpkt: MetaPacket):
            if sniff.box1.get() == 1:
                mpkt.wireshark_line(True)
            if sniff.box2.get() == 1:
                mpkt.show()

        def start_sniff():
            root.update_idletasks()
            net.buffer.add_callback("sniff_handler", sniff_handler)
            net.start_sniff()

        def stop_sniff():
            root.update_idletasks()
            net.stop_sniff()
            net.buffer.remove_callback("sniff_handler")

        start_on = net.sniff_is_running()
        sniff.bind_reversible(start_sniff, stop_sniff, "Sniffing", start_on)

        sniff.load_saved_input(context.inputs["sniff"])
        sniff.bind_input_autosave(context.inputs["sniff"])

    # NFQ widget with modifiers
        mitm = MITM(style, left_p)

        def mitm_handler(mpkt: MetaPacket):
            mpkt.wireshark_line(True)

        def start_mitm():
            root.update_idletasks()
            net.buffer.add_callback("mitm_handler", mitm_handler)
            net.start_nfq()

        def stop_mitm():
            root.update_idletasks()
            net.stop_nfq()
            net.buffer.remove_callback("mitm_handler")

        start_on = net.nfq_is_running()
        mitm.bind_reversible(start_mitm, stop_mitm, "Attack", start_on)

        mitm.bind_input_alert()
        mitm.load_saved_input(net.table)
        mitm.bind_input_save(net.table)
    # Dos widget
        DOS(style, left_p)

    # Spacer widget
        common.scroll_deadspace(style, left_p)


    # Map
        def draw_full_map(canvas, draw_lock, scale: float, offset: tuple[float, float]):
            positions = net.buffer.get_all_positions("in")
            bearing = net.buffer.get_last_bearing("in")
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.grid_lines()
                if len(positions) < 1: return
                draw.line(positions, "white")
                if bearing is None: return
                last_position = positions[-1]
                draw.boat(last_position, bearing, "white", "black")
        map = Map(style, right_p, draw_full_map, 100, 20)




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
    

