from .core.canvas import Canvas
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from ...app_core import Context
from ...network.buffer.meta_packet import MetaPacket
from scapy.all import conf, get_if_hwaddr

NODE_RADIUS = 6
# How many of a host's IPs are listed under it
MAX_IPS_SHOWN = 2

class NetworkDiagramCanvas(Canvas):
    '''
    Canvas that displays hosts as nodes and packet flow as arrows between them.
    Live mode flashes arrows for recent traffic; paused mode shows the MAC/IP
    path of the single packet selected in the packet console.

    A packet to the broadcast MAC gets an arrow to every other host shown.
    The access point sits in the middle (see NetworkGraph.get_host_positions).

    Follows network_hosts (edited by EditNetworkHosts): a host shows by its
    nicknames, and is left out if its MAC is hidden or every IP seen on it is.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, ((-1.3, -1.3), (1.3, 1.3)))
        self.network = context.buffer.network
        self.packets = context.buffer.packets
        default_interface = conf.iface
        self.mac_address = get_if_hwaddr(default_interface)
        node_font = QFont("Consolas", 9)

        def draw_host(name, ip_names, point, color):
            # Fixed pixel radius regardless of zoom, unlike Draw.circle()
            # (a world-space radius that would scale with it) - drawn
            # directly in canvas space instead.
            cx, cy = self.camera.world_to_canvas([point])[0]
            self.draw._draw_oval(
                (cx - NODE_RADIUS, cy - NODE_RADIUS, cx + NODE_RADIUS, cy + NODE_RADIUS),
                fill=context.style.color(color)
            )
            self.draw._draw_text(
                cx, cy - NODE_RADIUS - 8, name, node_font, context.style.color("field_text")
            )
            # Its IPs underneath - a router's MAC carries every outside IP
            # it forwards, so only the first few, then how many more
            if ip_names:
                shown = ", ".join(ip_names[:MAX_IPS_SHOWN])
                if len(ip_names) > MAX_IPS_SHOWN:
                    shown += f" +{len(ip_names) - MAX_IPS_SHOWN}"
                self.draw._draw_text(
                    cx, cy + NODE_RADIUS + 8, shown, node_font, context.style.color("field_text")
                )

        def frame_callback():
            self.draw.background(context.style.color("widget"))

            settings = context.states.get("network_hosts")
            def setting(kind, address, key):
                return settings[kind].get(address, {}).get(key)
            def is_hidden(kind, address):
                return setting(kind, address, "hide") in (1, "1")

            macs, ips, host_ips = self.network.get_hosts()
            hidden = set()
            for mac in macs:
                ips_on = host_ips.get(mac, [])
                if is_hidden("macs", mac) or (ips_on and all(is_hidden("ips", ip) for ip in ips_on)):
                    hidden.add(mac)

            positions = self.network.get_host_positions(hidden)

            def arrow_ends(src, dst):
                '''Where a packet's arrows go - every other shown host for a broadcast.'''
                if src not in positions:
                    return []
                if dst == MetaPacket.BROADCAST_MAC:
                    return [positions[mac] for mac in positions if mac != src]
                if dst in positions and dst != src:
                    return [positions[dst]]
                return []
            for mac, point in positions.items():
                name = setting("macs", mac, "nickname") or mac
                ip_names = [setting("ips", ip, "nickname") or ip for ip in host_ips.get(mac, []) if not is_hidden("ips", ip)]
                if mac == self.mac_address:
                    draw_host(name, ip_names, point, "outgoing")
                else:
                    draw_host(name, ip_names, point, "incoming")

            mode = context.states.get("packet_console", "mode")

            if mode == "paused":
                mpkt = self.packets.get_selected()
                if mpkt is None:
                    return

                mac_src, mac_dst = mpkt.get("mac_src"), mpkt.get("mac_dst")
                ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                for end in arrow_ends(mac_src, mac_dst):
                    self.draw.visible_arrow([positions[mac_src], end], context.style.color("accent"))
                    if ip_src != "-" and ip_dst != "-":
                        self.draw.visible_arrow([positions[mac_src], end], context.style.color("scrollbar_hover"))
            else:
                for mpkt, macs in self.network.get_arrows_this_tick().items():
                    src, dst = macs
                    for end in arrow_ends(src, dst):
                        self.draw.visible_arrow([positions[src], end], context.style.color("accent"))

        self.set_frame_callback(frame_callback)
        self.start_animation()
