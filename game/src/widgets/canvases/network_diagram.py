import math

from .core.canvas import Canvas
from .core import transforms as t
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from ...app_core import Context
from ...network.buffer.meta_packet import MetaPacket
from scapy.all import conf, get_if_hwaddr

# Space between a chip's name and its edge, and its corners' radius
CHIP_PADDING = (6, 3)
CHIP_RADIUS = 6
# A chip's outline - heavier for a nicknamed host, like its text
CHIP_OUTLINE = 1
NICKNAME_CHIP_OUTLINE = 3
# Space between a chip and the IP label under it, and between a label's
# text and the edge of the box behind it
LABEL_GAP = 2
LABEL_PADDING = 2
# Space kept between hosts (chip and IP slot together) - around the one in
# the middle, and wherever they're pushed apart (see _separate)
HOST_GAP = 6
# The most rounds of pushing hosts apart a frame gets (see _separate)
SEPARATE_ROUNDS = 60
# Space before an arrowhead
ARROW_GAP = 3
# How many of a host's IPs are listed under it
MAX_IPS_SHOWN = 2
# The widest an IP gets - every host keeps room for one under its chip,
# showing or not, so nothing moves as IPs come and go
WIDEST_IP = "255.255.255.255"


def _edge_distance(half_size: tuple[float, float], ux: float, uy: float) -> float:
    '''How far a chip's edge is from its middle along the unit direction (ux, uy).'''
    half_width, half_height = half_size
    return min(half_width / abs(ux) if ux else math.inf, half_height / abs(uy) if uy else math.inf)


def _separate(centers: list[list[float]], half_sizes: list[tuple[float, float]],
              chip_halves: list[tuple[float, float]], pinned: set[int],
              bounds: tuple[float, float, float, float] | None) -> bool:
    '''
    Pushes overlapping hosts apart, in place. A host is its chip (at the
    top, chip_halves) and the IP slot under it, half_sizes across the
    whole: a chip may not overlap any part of another host, but two IP
    slots may overlap each other - they're only ever both in use when two
    neighbors show IPs at once, and keeping them apart too needs far more
    room than a small pane has. Each overlapping pair moves apart along
    whichever axis it overlaps least on, half the way each (all of it for
    the one not pinned), and none leaves bounds (left, top, right, bottom)
    if given. Rounds repeat until nothing overlaps (or SEPARATE_ROUNDS),
    since one push can make a new overlap. Starts from the same spots and
    sizes every frame, so it lands the same way every frame. Whether no two
    overlap by the end (closer than HOST_GAP is all right).
    '''
    def clamp(i):
        if i in pinned or bounds is None:
            return
        left, top, right, bottom = bounds
        half_width, half_height = half_sizes[i]
        # A box wider than the bounds centers in them rather than flipping past
        centers[i][0] = min(max(centers[i][0], left + half_width), right - half_width) \
            if right - left >= 2 * half_width else (left + right) / 2
        centers[i][1] = min(max(centers[i][1], top + half_height), bottom - half_height) \
            if bottom - top >= 2 * half_height else (top + bottom) / 2

    def whole(i):
        (x, y), (half_width, half_height) = centers[i], half_sizes[i]
        return x - half_width, y - half_height, x + half_width, y + half_height

    def chip(i):
        (x, y), (_, half_height), (chip_half_width, chip_half_height) = centers[i], half_sizes[i], chip_halves[i]
        return x - chip_half_width, y - half_height, x + chip_half_width, y - half_height + 2 * chip_half_height

    def overlaps(i, j):
        '''
        How far hosts i and j overlap on (x, y) - both above 0 when they do:
        either's chip against the other's whole, whichever overlaps more.
        '''
        worst = (-math.inf, -math.inf)
        for a, b in ((whole(i), chip(j)), (chip(i), whole(j))):
            over = (min(a[2], b[2]) - max(a[0], b[0]) + HOST_GAP, min(a[3], b[3]) - max(a[1], b[1]) + HOST_GAP)
            if min(over) > min(worst):
                worst = over
        return worst

    def push(i, j, axis, amount):
        '''Moves i and j apart by amount along axis - ties (the same spot) push j right/down.'''
        sign = 1 if centers[j][axis] >= centers[i][axis] else -1
        share_i = 0.0 if i in pinned else 1.0 if j in pinned else 0.5
        centers[i][axis] -= sign * amount * share_i
        centers[j][axis] += sign * amount * (1.0 - share_i)
        clamp(i)
        clamp(j)

    for i in range(len(centers)):
        clamp(i)
    for _ in range(SEPARATE_ROUNDS):
        moved = False
        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                if i in pinned and j in pinned:
                    continue
                over = overlaps(i, j)
                if over[0] <= 0 or over[1] <= 0:
                    continue
                # The axis they overlap least on first - and if the pane's
                # edge stops that, the other one
                axis = 0 if over[0] < over[1] else 1
                push(i, j, axis, over[axis])
                over = overlaps(i, j)
                if over[0] > 0 and over[1] > 0:
                    push(i, j, 1 - axis, over[1 - axis])
                moved = True
        if not moved:
            return True
    return all(min(overlaps(i, j)) <= HOST_GAP for i in range(len(centers)) for j in range(i + 1, len(centers)))


class NetworkDiagramCanvas(Canvas):
    '''
    Canvas that displays hosts as nodes and packet flow as arrows between them.
    Live mode flashes arrows for recent traffic; paused mode shows the MAC/IP
    path of the single packet selected in the packet console.

    A packet to the broadcast MAC gets an arrow to every other host shown.
    The access point sits in the middle (see NetworkGraph.get_host_positions).

    Hosts are devices - MACs - each a chip with its name inside: its
    nickname in network_hosts (edited by EditNetworkHosts), or else the last
    3 bytes of its MAC (the device's own part - the first 3 only name its
    maker) - in bold, with a heavier outline, for a nickname, so the hosts
    only known by MAC fade into the background. Hidden ones are left out.

    Under each chip is a slot for the IPs of the packets shown right now
    that carry an IP source and destination. Each host is laid out as its
    chip and that slot together, sized for one IP whether one's showing or
    not, so nothing moves as packets come and go: on an ellipse that fills
    the pane, pushed apart wherever two overlap (see _separate), and kept
    in the pane. Laid out in pixels rather than world space - zooming and
    panning still apply on top. IP labels sit on a box of the background
    color, so arrows pass under them.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, ((-1.3, -1.3), (1.3, 1.3)))
        self.network = context.buffer.network
        self.packets = context.buffer.packets
        default_interface = conf.iface
        self.mac_address = get_if_hwaddr(default_interface)
        node_font = QFont("Consolas", 9)
        # Nicknamed hosts stand out - the ones only known by MAC fade back
        nickname_font = QFont(node_font)
        nickname_font.setBold(True)

        def chip_half_size(name, font):
            '''Half a chip's (width, height) - its name and the padding around it.'''
            width, height = self.draw.text_size(name, font)
            return width / 2 + CHIP_PADDING[0], height / 2 + CHIP_PADDING[1]

        def label_size(lines):
            '''The (width, height) of an IP label's box - its text and the padding around it.'''
            width, height = self.draw.text_size("\n".join(lines), node_font)
            return width + 2 * LABEL_PADDING, height + 2 * LABEL_PADDING

        slot_width, slot_height = label_size([WIDEST_IP])

        def host_half_size(chip_half):
            '''Half a host's whole (width, height): its chip, and the slot for an IP under it.'''
            return max(chip_half[0], slot_width / 2), chip_half[1] + (LABEL_GAP + slot_height) / 2

        def chip_center(host_center, chip_half, host_half):
            '''Where a host's chip sits in it - at the top, over the IP slot.'''
            x, y = host_center
            return x, y - host_half[1] + chip_half[1]

        def ring_radii(unit_points, host_halves):
            '''
            The ring's (x, y) radii in pixels: as big as the pane allows
            with every host inside it, but never so small that the ring's
            hosts run into the one in the middle.
            '''
            padding = self.camera.padding
            room_x = room_y = clear_x = clear_y = 0.0
            middle_half = next((host_halves[mac] for mac, point in unit_points.items() if point == (0.0, 0.0)),
                               (0.0, 0.0))
            for mac, point in unit_points.items():
                if point == (0.0, 0.0):
                    continue
                half_width, half_height = host_halves[mac]
                room_x, room_y = max(room_x, half_width), max(room_y, half_height)
                clear_x = max(clear_x, middle_half[0] + half_width + HOST_GAP)
                clear_y = max(clear_y, middle_half[1] + half_height + HOST_GAP)
            return (max(self.width() / 2 - padding - room_x, clear_x),
                    max(self.height() / 2 - padding - room_y, clear_y))

        def draw_chip(center, half_size, name, font, outline, color):
            # Fixed pixel size regardless of zoom, unlike Draw.circle()
            # (a world-space radius that would scale with it)
            cx, cy = center
            half_width, half_height = half_size
            box = (cx - half_width, cy - half_height, cx + half_width, cy + half_height)
            self.draw._draw_rounded_rect(box, CHIP_RADIUS, fill=context.style.color("field", opaque=True),
                                         outline=context.style.color(color), width=outline)
            self.draw._draw_text(cx, cy, name, font, context.style.color("field_text"))

        def draw_label(chip, chip_half, lines):
            '''An IP label centered under its chip, on a box of the background so arrows pass under it.'''
            (cx, cy), (_, chip_half_height) = chip, chip_half
            width, height = label_size(lines)
            top = cy + chip_half_height + LABEL_GAP
            self.draw._draw_rounded_rect((cx - width / 2, top, cx + width / 2, top + height), LABEL_PADDING,
                                         fill=context.style.color("widget"))
            self.draw._draw_text(cx, top + LABEL_PADDING, "\n".join(lines), node_font,
                                 context.style.color("field_text"), "n")

        def draw_arrow(chips, src, dst, color):
            '''An arrow from src's chip edge to just short of dst's, in canvas space.'''
            (x1, y1), src_half = chips[src]
            (x2, y2), dst_half = chips[dst]
            length = math.hypot(x2 - x1, y2 - y1)
            if length == 0:
                return
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            start = _edge_distance(src_half, ux, uy)
            end = length - _edge_distance(dst_half, ux, uy) - ARROW_GAP
            if end <= start:
                return  # the chips overlap - no room for an arrow
            self.draw._draw_line((x1 + ux * start, y1 + uy * start, x1 + ux * end, y1 + uy * end),
                                 context.style.color(color), 2, arrow_end=True)

        def frame_callback():
            self.draw.background(context.style.color("widget"))

            settings = context.states.get("network_hosts")
            def setting(mac, key):
                return settings.get(mac, {}).get(key)

            macs, host_ips = self.network.get_hosts()
            hidden = {mac for mac in macs if setting(mac, "hide") in (1, "1")}
            # Spots on a unit circle, the access point in the middle
            unit_points = self.network.get_host_positions(hidden)
            nicknames = {mac: setting(mac, "nickname") for mac in unit_points}
            names = {mac: nicknames[mac] or mac[-8:] for mac in unit_points}
            fonts = {mac: nickname_font if nicknames[mac] else node_font for mac in unit_points}
            chip_halves = {mac: chip_half_size(names[mac], fonts[mac]) for mac in unit_points}
            host_halves = {mac: host_half_size(chip_halves[mac]) for mac in unit_points}

            def receivers(src, dst):
                '''The shown hosts a packet goes to - every other one for a broadcast.'''
                if dst == MetaPacket.BROADCAST_MAC:
                    return [mac for mac in unit_points if mac != src]
                return [dst] if dst in unit_points and dst != src else []

            # The packets shown this frame: the one selected while paused, or
            # whatever arrived since the last frame while live
            mode = context.states.get("packet_console", "mode")
            if mode == "paused":
                mpkt = self.packets.get_selected()
                shown_packets = [mpkt] if mpkt is not None else []
            else:
                shown_packets = list(self.network.get_arrows_this_tick())

            # A host is labeled with an IP only while a packet shown carries
            # one both ways - the IPs in its bytes, not every IP it ever had
            packet_ips = {mac: [] for mac in unit_points}
            def add_ip(mac, ip):
                if mac in packet_ips and ip not in packet_ips[mac]:
                    packet_ips[mac].append(ip)
            for mpkt in shown_packets:
                ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                if ip_src not in (None, "-") and ip_dst not in (None, "-"):
                    add_ip(mpkt.get("mac_src"), ip_src)
                    for target in receivers(mpkt.get("mac_src"), mpkt.get("mac_dst")):
                        add_ip(target, ip_dst)

            # Each host (chip and IP slot together) on the ring, then pushed
            # apart wherever two overlap, staying in the pane - all but the
            # access point in the middle, which stays put. Before zooming,
            # so it's the same at any zoom. More than fit in the pane get
            # pushed apart past its edges instead (pan to see them), rather
            # than piling up against them.
            order = list(unit_points)
            radius_x, radius_y = ring_radii(unit_points, host_halves)
            middle_x, middle_y = self.width() / 2, self.height() / 2
            ring = [[middle_x + ux * radius_x, middle_y - uy * radius_y] for ux, uy in unit_points.values()]
            halves = [host_halves[mac] for mac in order]
            pinned = {i for i, mac in enumerate(order) if unit_points[mac] == (0.0, 0.0)}
            padding = self.camera.padding
            centers = [list(center) for center in ring]
            chip_sizes = [chip_halves[mac] for mac in order]
            pane = (padding, padding, self.width() - padding, self.height() - padding)
            if not _separate(centers, halves, chip_sizes, pinned, pane):
                centers = [list(center) for center in ring]
                _separate(centers, halves, chip_sizes, pinned, None)
            centers = t.zoom_and_pan(centers, self.camera.scale, tuple(self.camera.offset))
            # Each shown host's chip: its (canvas center, half size)
            chips = {mac: (chip_center(center, chip_halves[mac], host_halves[mac]), chip_halves[mac])
                     for mac, center in zip(order, centers)}

            # Arrows first, so the chips and labels sit on top of them
            for mpkt in shown_packets:
                mac_src = mpkt.get("mac_src")
                if mac_src not in chips:
                    continue
                has_ips = mpkt.get("ip_src") not in (None, "-") and mpkt.get("ip_dst") not in (None, "-")
                for target in receivers(mac_src, mpkt.get("mac_dst")):
                    draw_arrow(chips, mac_src, target, "accent")
                    if mode == "paused" and has_ips:
                        draw_arrow(chips, mac_src, target, "scrollbar_hover")

            for mac, (center, chip_half) in chips.items():
                color = "outgoing" if mac == self.mac_address else "incoming"
                outline = NICKNAME_CHIP_OUTLINE if nicknames[mac] else CHIP_OUTLINE
                draw_chip(center, chip_half, names[mac], fonts[mac], outline, color)

            for mac, (center, chip_half) in chips.items():
                # A router forwards packets for many outside IPs at once, so
                # only the first few, then how many more - past the one the
                # slot holds, they just run on below it
                ips = packet_ips[mac]
                if ips:
                    lines = ips[:MAX_IPS_SHOWN]
                    if len(ips) > MAX_IPS_SHOWN:
                        lines.append(f"+{len(ips) - MAX_IPS_SHOWN} more")
                    draw_label(center, chip_half, lines)

        self.set_frame_callback(frame_callback)
        self.start_animation()
