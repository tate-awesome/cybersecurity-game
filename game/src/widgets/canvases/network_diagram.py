import math

from .core.canvas import Canvas
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from ...app_core import Context
from ...network.buffer.meta_packet import MetaPacket
from scapy.all import conf, get_if_hwaddr

NODE_RADIUS = 6
# Space between a chip's name and its edge, and its corners' radius
CHIP_PADDING = (6, 3)
CHIP_RADIUS = 6
# Space between a node and its label, and before an arrowhead
LABEL_GAP = 4
ARROW_GAP = 3
# How many of a host's IPs are listed by it
MAX_IPS_SHOWN = 2
# Where a label goes for each of the 8 directions out from the middle,
# counterclockwise from east in 45 degree steps: the side or corner of the
# text that sits by the node
LABEL_ANCHORS = ("w", "sw", "s", "se", "e", "ne", "n", "nw")


def _snap_direction(dx: float, dy: float) -> tuple[int, int, str]:
    '''
    The nearest of the 8 flat and 45 degree directions to (dx, dy) in
    canvas space (y down), as a step of -1/0/1 each way and the label
    anchor for it. Straight up for no direction at all (the node in the middle).
    '''
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return 0, -1, "s"
    step = round(math.atan2(-dy, dx) / (math.pi / 4)) % 8
    angle = step * math.pi / 4
    return round(math.cos(angle)), -round(math.sin(angle)), LABEL_ANCHORS[step]


def _edge_distance(half_size: tuple[float, float], ux: float, uy: float) -> float:
    '''How far a node's edge is from its middle along the unit direction (ux, uy).'''
    half_width, half_height = half_size
    if half_width == half_height == NODE_RADIUS:
        return NODE_RADIUS
    return min(half_width / abs(ux) if ux else math.inf, half_height / abs(uy) if uy else math.inf)


class NetworkDiagramCanvas(Canvas):
    '''
    Canvas that displays hosts as nodes and packet flow as arrows between them.
    Live mode flashes arrows for recent traffic; paused mode shows the MAC/IP
    path of the single packet selected in the packet console.

    A packet to the broadcast MAC gets an arrow to every other host shown.
    The access point sits in the middle (see NetworkGraph.get_host_positions).

    Hosts are devices - MACs. One shows the IPs of the packets shown right
    now that carry an IP source and destination, and no others.

    Follows network_hosts (edited by EditNetworkHosts): a host with a
    nickname is a chip with it inside (one without is labeled with the last
    3 bytes of its MAC), and a hidden one is left out.

    Each label points away from the middle, snapped to the nearest flat or
    45 degree direction, with its nearest side or corner by the node - so
    the labels around the ring stay out of the middle and off each other.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, ((-1.3, -1.3), (1.3, 1.3)))
        self.network = context.buffer.network
        self.packets = context.buffer.packets
        default_interface = conf.iface
        self.mac_address = get_if_hwaddr(default_interface)
        node_font = QFont("Consolas", 9)

        def node_half_size(nickname):
            '''Half a node's (width, height) - a dot, or a chip around its nickname.'''
            if not nickname:
                return NODE_RADIUS, NODE_RADIUS
            width, height = self.draw.text_size(nickname, node_font)
            return width / 2 + CHIP_PADDING[0], height / 2 + CHIP_PADDING[1]

        def draw_host(center, half_size, nickname, label_lines, color):
            # Fixed pixel size regardless of zoom, unlike Draw.circle()
            # (a world-space radius that would scale with it) - drawn
            # directly in canvas space instead.
            cx, cy = center
            half_width, half_height = half_size
            box = (cx - half_width, cy - half_height, cx + half_width, cy + half_height)
            if nickname:
                self.draw._draw_rounded_rect(box, CHIP_RADIUS, fill=context.style.color("field", opaque=True),
                                             outline=context.style.color(color), width=2)
                self.draw._draw_text(cx, cy, nickname, node_font, context.style.color("field_text"))
            else:
                self.draw._draw_oval(box, fill=context.style.color(color))
            if not label_lines:
                return
            middle_x, middle_y = self.camera.world_to_canvas([(0.0, 0.0)])[0]
            step_x, step_y, anchor = _snap_direction(cx - middle_x, cy - middle_y)
            # The label's side or corner sits just off the node's matching
            # side or corner
            self.draw._draw_text(cx + step_x * (half_width + LABEL_GAP), cy + step_y * (half_height + LABEL_GAP),
                                 "\n".join(label_lines), node_font, context.style.color("field_text"), anchor)

        def draw_arrow(nodes, src, dst, color):
            '''An arrow from src's edge to just short of dst's, in canvas space.'''
            (x1, y1), src_half = nodes[src]
            (x2, y2), dst_half = nodes[dst]
            length = math.hypot(x2 - x1, y2 - y1)
            if length == 0:
                return
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            start = _edge_distance(src_half, ux, uy)
            end = length - _edge_distance(dst_half, ux, uy) - ARROW_GAP
            if end <= start:
                return  # the nodes overlap - no room for an arrow
            self.draw._draw_line((x1 + ux * start, y1 + uy * start, x1 + ux * end, y1 + uy * end),
                                 context.style.color(color), 2, arrow_end=True)

        def frame_callback():
            self.draw.background(context.style.color("widget"))

            settings = context.states.get("network_hosts")
            def setting(mac, key):
                return settings.get(mac, {}).get(key)

            macs, host_ips = self.network.get_hosts()
            hidden = {mac for mac in macs if setting(mac, "hide") in (1, "1")}
            positions = self.network.get_host_positions(hidden)
            nicknames = {mac: setting(mac, "nickname") for mac in positions}
            # Each shown host's (canvas center, half size)
            nodes = {mac: (self.camera.world_to_canvas([point])[0], node_half_size(nicknames[mac]))
                     for mac, point in positions.items()}

            def receivers(src, dst):
                '''The shown hosts a packet goes to - every other one for a broadcast.'''
                if dst == MetaPacket.BROADCAST_MAC:
                    return [mac for mac in nodes if mac != src]
                return [dst] if dst in nodes and dst != src else []

            # The packets shown this frame: the one selected while paused, or
            # whatever arrived since the last frame while live
            mode = context.states.get("packet_console", "mode")
            if mode == "paused":
                mpkt = self.packets.get_selected()
                shown_packets = [mpkt] if mpkt is not None else []
            else:
                shown_packets = list(self.network.get_arrows_this_tick())

            # Arrows first, so the nodes sit on top of them. A host is
            # labeled with an IP only while a packet shown carries one both
            # ways - the IPs in its bytes, not every IP the host ever had.
            packet_ips = {mac: [] for mac in nodes}
            def add_ip(mac, ip):
                if mac in packet_ips and ip not in packet_ips[mac]:
                    packet_ips[mac].append(ip)
            for mpkt in shown_packets:
                mac_src, mac_dst = mpkt.get("mac_src"), mpkt.get("mac_dst")
                ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                has_ips = ip_src not in (None, "-") and ip_dst not in (None, "-")
                targets = receivers(mac_src, mac_dst)
                if mac_src in nodes:
                    for target in targets:
                        draw_arrow(nodes, mac_src, target, "accent")
                        if mode == "paused" and has_ips:
                            draw_arrow(nodes, mac_src, target, "scrollbar_hover")
                if has_ips:
                    add_ip(mac_src, ip_src)
                    for target in targets:
                        add_ip(target, ip_dst)

            for mac, (center, half_size) in nodes.items():
                nickname = nicknames[mac]
                # A chip already says who it is. Otherwise just a MAC's last
                # 3 bytes (the device's own part - the first 3 only name its
                # maker), to keep labels narrow
                label_lines = [] if nickname else [f"…{mac[-9:]}"]
                # A router forwards packets for many outside IPs at once,
                # so only the first few, then how many more
                ips = packet_ips[mac]
                label_lines += ips[:MAX_IPS_SHOWN]
                if len(ips) > MAX_IPS_SHOWN:
                    label_lines.append(f"+{len(ips) - MAX_IPS_SHOWN} more")
                color = "outgoing" if mac == self.mac_address else "incoming"
                draw_host(center, half_size, nickname, label_lines, color)

        self.set_frame_callback(frame_callback)
        self.start_animation()
