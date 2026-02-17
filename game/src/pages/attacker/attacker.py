from ...app_core.context import Context

from ...widgets.style import Style
from ...widgets import common, forms, popup
from ...widgets.map import Map
from ...drawing.viewport import ViewPort

from ...network.network_controller import HardwareNetwork


class AttackerV0:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = Style(context.ui_scale)
        # Defer to the existing net
        if context.net is None:
            context.net = HardwareNetwork()
        net = context.net



    # Menu bar
        menu = common.menu_bar(style, root, "Attacker Version 0")
        common.menu_bar_button(style, menu, "Quit", router.quit)
        common.menu_bar_button(style, menu, "Refresh", router.refresh)
        common.menu_bar_button(style, menu, "Toggle Theme", router.mode_toggle)
        common.menu_bar_button(style, menu, "Select Theme", router.select_theme)
        common.menu_bar_button(style, menu, "Help", lambda:popup.open(style,root,context.help_message()))

    # Page sections

        left_p, middle_p, right_p = common.trifold(style, root)

    # NMap Widget
        nmap = forms.NMap(style, left_p)
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
    
        forms.bind(do_nmap, nmap.button)
        if context.progress["nmap"]:
            nmap.status.configure(text="NMap Complete")
        else:
            nmap.status.configure(text="")

    # ARP Widget
        arp = forms.ARP(style, left_p)
        def start_arp():
            target_ip = str(arp.entry1.get())
            host_ip = str(arp.entry2.get())
            root.update_idletasks()
            net.start_arp(target_ip, host_ip)
        def stop_arp():
            root.update_idletasks()
            net.stop_arp()
        
        start_on = net.arp_is_running()
        forms.bind_reversible(arp, start_arp, stop_arp, "ARP Spoof", start_on)

        forms.load_saved_entries(arp.entries, context.inputs["arp"])
        forms.bind_entries_autosave(arp.entries, context.inputs["arp"])



    # Sniffing widget
        forms.sniff(style, left_p)

    # NFQ widget with modifiers
        forms.mitm(style, left_p)
    # Dos widget
        forms.dos(style, left_p)


    # Map
        from ...drawing import sprites
        self.positions = sprites.random_spline_path(20, 100)
        self.color = "blue"
        world_map = Map(style, right_p, self.draw_test_plane, 100)




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
    

