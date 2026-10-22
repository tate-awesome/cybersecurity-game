import math

from .core.canvas import Canvas
from .core import transforms as t
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from ...app_core import Context
from ...network.buffer.meta_packet import MetaPacket
from ...network.buffer.channels.network_graph import MAX_NICKNAME_LENGTH
from scapy.all import conf, get_if_hwaddr

# Space between a chip's name and its edge, and its corners' radius
CHIP_PADDING = (6, 3)
CHIP_RADIUS = 6
# A chip's outline - heavier for a nicknamed host, like its text
CHIP_OUTLINE = 1
NICKNAME_CHIP_OUTLINE = 3
# Space between an IP label's text and the edge of its tab, and kept clear
# between a tab and the chip on the far side of its gap - so it's plain
# which chip a tab hangs off
LABEL_PADDING = 2
LABEL_GAP = 6
# An IP label is a tab off its chip: how far it tucks under the chip's
# edge, and its corners' radius
TAB_TUCK = 4
TAB_RADIUS = 4
# How steep an arrow has to be to count as leaving a chip's top or bottom
# (see the label sides in frame_callback) - flatter ones leave its sides
FLAT_ARROW = 0.2
# Space between the table's columns, past the widest of a chip and an IP label
COLUMN_GAP = 6
# How much of a chip past the pane's edge still shows (see Table)
PEEK = 14
# Space before an arrowhead
ARROW_GAP = 3
# The widest an IP gets - the table leaves room for one by every chip
WIDEST_IP = "255.255.255.255"


def _edge_distance(half_size: tuple[float, float], ux: float, uy: float) -> float:
    '''How far a chip's edge is from its middle along the unit direction (ux, uy).'''
    half_width, half_height = half_size
    return min(half_width / abs(ux) if ux else math.inf, half_height / abs(uy) if uy else math.inf)


class Table:
    '''
    The cells hosts sit in, as many columns and rows as fit the pane, in the
    order they fill: the middle, then always the cell farthest from those
    before it (see spread_order), so the hosts are spread evenly however
    many there are. Then cells past the pane's edges, from the middle of
    each edge out, which are drawn pulled in so just PEEK of a chip shows
    (further-out ones stack on them).
    '''
    def __init__(self, width: float, height: float, padding: float, chip_size: tuple[float, float],
                 pitch: tuple[float, float], gap_height: float, count: int):
        chip_width, chip_height = chip_size
        pitch_x, pitch_y = pitch
        self.columns = max(1, int((width - 2 * padding + COLUMN_GAP) // pitch_x))
        self.rows = max(1, int((height - 2 * padding - gap_height) // pitch_y))
        # Centered in the pane, with a gap for IP labels above the top row and below the bottom one
        first_x = width / 2 - (self.columns - 1) * pitch_x / 2
        first_y = height / 2 - (self.rows * pitch_y + gap_height) / 2 + gap_height + chip_height / 2

        def spot(cell):
            column, row = cell
            x, y = first_x + column * pitch_x, first_y + row * pitch_y
            # Past the pane's edge, pulled in to just show
            if column < 0:
                x = PEEK - chip_width / 2
            elif column >= self.columns:
                x = width - PEEK + chip_width / 2
            if row < 0:
                y = PEEK - chip_height / 2
            elif row >= self.rows:
                y = height - PEEK + chip_height / 2
            return x, y

        middle = ((self.columns - 1) / 2, (self.rows - 1) / 2)
        def fill_order(cells):
            '''Nearest the middle first - and each followed by the one across the middle from it.'''
            def key(cell):
                dx, dy = (cell[0] - middle[0]) * pitch_x, (cell[1] - middle[1]) * pitch_y
                return round(math.hypot(dx, dy), 3), math.atan2(-dy, dx) % (2 * math.pi)
            cells_set = set(cells)
            ordered, placed = [], set()
            for cell in sorted(cells, key=key):
                if cell in placed:
                    continue
                across = (self.columns - 1 - cell[0], self.rows - 1 - cell[1])
                for each in (cell, across):
                    if each in cells_set and each not in placed:
                        ordered.append(each)
                        placed.add(each)
            return ordered

        def spread_order(cells):
            '''
            The middle first, then each time the cell farthest from every
            one before it - corners, then the middles of the edges, then
            the gaps between - so however many are filled, they're spread
            about evenly. Ties go to the one farthest from the cell just
            before (across from it), then fill_order's.
            '''
            def gap(a, b):
                return math.hypot((a[0] - b[0]) * pitch_x, (a[1] - b[1]) * pitch_y)
            remaining = fill_order(cells)
            rank = {cell: i for i, cell in enumerate(remaining)}
            ordered = [remaining.pop(0)]
            nearest = {cell: gap(cell, ordered[0]) for cell in remaining}
            while remaining:
                last = ordered[-1]
                cell = max(remaining, key=lambda cell: (round(nearest[cell], 3), round(gap(cell, last), 3),
                                                        -rank[cell]))
                remaining.remove(cell)
                ordered.append(cell)
                for other in remaining:
                    nearest[other] = min(nearest[other], gap(other, cell))
            return ordered

        self.cells = spread_order([(column, row) for column in range(self.columns) for row in range(self.rows)])
        # Cells this far in the list and on are past the pane's edges
        self.inside = len(self.cells)
        ring = 1
        while len(self.cells) < count:
            self.cells += fill_order([
                (column, row)
                for column in range(-ring, self.columns + ring) for row in range(-ring, self.rows + ring)
                if column in (-ring, self.columns - 1 + ring) or row in (-ring, self.rows - 1 + ring)])
            ring += 1
        self.spots = [spot(cell) for cell in self.cells]


class NetworkDiagramCanvas(Canvas):
    '''
    Canvas that displays hosts as nodes and packet flow as arrows between them.
    Live mode flashes arrows for recent traffic; paused mode shows the MAC/IP
    path of the single packet selected in the packet console.

    A packet to the broadcast MAC gets an arrow to every other host shown.

    Hosts are devices - MACs - each a chip with its name inside: its
    nickname in network_hosts (edited by EditNetworkHosts), or else the last
    3 bytes of its MAC (the device's own part - the first 3 only name its
    maker) - in bold, with a heavier outline, for a nickname, so the hosts
    only known by MAC fade into the background. Every chip is the same
    size, the longest a nickname can be (MAX_NICKNAME_LENGTH).

    The chips sit in a table (see Table), with a gap between the rows one
    IP label tall: the IP of the packets shown right now that carry an IP
    source and destination (the first, and how many more if there are
    several), as a tab hanging off its chip's top or bottom - whichever
    fewer arrows leave the chip from (see frame_callback).

    A host keeps its cell: new ones take the first free cell in the
    table's order, and the access point (NetworkGraph.get_access_point)
    the first of all, in the middle, kept for it until it's found. A
    hidden host leaves its cell empty - only a host from past the pane's
    edges (when the table's full) moves in to fill it - and gets it back
    when it's shown again if it's still free. Laid out in pixels rather
    than world space - zooming and panning still apply on top.
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

        # The cell each shown host is in (an index into the table's order),
        # and the one each hidden host was last in
        self.cell_of: dict[str, int] = {}
        self.last_cell: dict[str, int] = {}
        # The table, and what it was last worked out from (see place)
        self.table: Table | None = None
        self.table_args: tuple | None = None

        def label_size(text):
            '''The (width, height) of an IP label's box - its text and the padding around it.'''
            width, height = self.draw.text_size(text, node_font)
            return width + 2 * LABEL_PADDING, height + 2 * LABEL_PADDING

        text_width, text_height = self.draw.text_size("0" * MAX_NICKNAME_LENGTH, nickname_font)
        chip_size = (text_width + 2 * CHIP_PADDING[0], text_height + 2 * CHIP_PADDING[1])
        chip_half = (chip_size[0] / 2, chip_size[1] / 2)
        slot_width, slot_height = label_size(WIDEST_IP)
        # A tab sits flush on its own chip, with LABEL_GAP to spare before the next
        gap_height = slot_height + LABEL_GAP
        pitch = (max(chip_size[0], slot_width) + COLUMN_GAP, chip_size[1] + gap_height)

        def display_name(name):
            # A nickname saved before there was a limit gets cut to fit
            return name if len(name) <= MAX_NICKNAME_LENGTH else name[:MAX_NICKNAME_LENGTH - 1] + "…"

        def place(shown, access_point):
            '''
            Puts every shown host (in the order first seen) in a cell (see
            the class docstring) and returns the table. Hosts no longer
            shown give up theirs.
            '''
            shown_set = set(shown)
            for mac in list(self.cell_of):
                if mac not in shown_set:
                    self.last_cell[mac] = self.cell_of.pop(mac)
            # Only worked out again when the pane's size or the cells needed change
            table_args = (self.width(), self.height(), self.camera.padding, chip_size, pitch, gap_height,
                          max([len(shown) + 1] + [cell + 1 for cell in self.cell_of.values()]))
            if table_args != self.table_args:
                self.table_args = table_args
                self.table = Table(*table_args)
            table = self.table
            taken = {cell: mac for mac, cell in self.cell_of.items()}

            # The first cell is the access point's - anyone else there (in
            # it before the access point was known) gets a new one
            if access_point in shown_set and self.cell_of.get(access_point) != 0:
                if 0 in taken:
                    del self.cell_of[taken[0]]
                taken.pop(self.cell_of.pop(access_point, None), None)
                self.cell_of[access_point] = 0
                taken[0] = access_point

            def first_free():
                return next(cell for cell in range(1, len(table.cells)) if cell not in taken)
            for mac in shown:
                if mac in self.cell_of:
                    continue
                remembered = self.last_cell.pop(mac, None)
                cell = remembered if remembered not in (None, 0) and remembered not in taken \
                    and remembered < table.inside else first_free()
                self.cell_of[mac] = cell
                taken[cell] = mac

            # A cell left empty in the pane is only filled by a host from past its edges
            while True:
                empty = [cell for cell in range(1, table.inside) if cell not in taken]
                outside = sorted(cell for cell in taken if cell >= table.inside)
                if not empty or not outside:
                    break
                mac = taken.pop(outside[0])
                self.cell_of[mac] = empty[0]
                taken[empty[0]] = mac
            return table

        def draw_chip(center, name, font, outline, color):
            # Fixed pixel size regardless of zoom, unlike Draw.circle()
            # (a world-space radius that would scale with it)
            cx, cy = center
            box = (cx - chip_half[0], cy - chip_half[1], cx + chip_half[0], cy + chip_half[1])
            self.draw._draw_rounded_rect(box, CHIP_RADIUS, fill=context.style.color("field", opaque=True),
                                         outline=context.style.color(color), width=outline)
            self.draw._draw_text(cx, cy, name, font, context.style.color("field_text"))

        def draw_label(center, text, above, color):
            '''
            An IP label as a tab hanging off its chip's bottom (or top), in
            the gap there - drawn before the chip, which covers the part
            tucked under it, so the two read as one. Solid, so arrows pass under it.
            '''
            cx, cy = center
            width, height = label_size(text)
            edge = cy - chip_half[1] if above else cy + chip_half[1]
            if above:
                box = (cx - width / 2, edge - height, cx + width / 2, edge + TAB_TUCK)
                text_top = edge - height + LABEL_PADDING
            else:
                box = (cx - width / 2, edge - TAB_TUCK, cx + width / 2, edge + height)
                text_top = edge + LABEL_PADDING
            self.draw._draw_rounded_rect(box, TAB_RADIUS, fill=context.style.color("field", opaque=True),
                                         outline=context.style.color(color), width=CHIP_OUTLINE)
            self.draw._draw_text(cx, text_top, text, node_font, context.style.color("field_text"), "n")

        def draw_arrow(centers, src, dst, color):
            '''
            An arrow from src's chip edge to just short of dst's, in canvas
            space. Its direction (from src toward dst), or None if there's none.
            '''
            (x1, y1), (x2, y2) = centers[src], centers[dst]
            length = math.hypot(x2 - x1, y2 - y1)
            if length == 0:
                return None
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            start = _edge_distance(chip_half, ux, uy)
            end = length - _edge_distance(chip_half, ux, uy) - ARROW_GAP
            if end <= start:
                return None  # the chips overlap - no room for an arrow
            self.draw._draw_line((x1 + ux * start, y1 + uy * start, x1 + ux * end, y1 + uy * end),
                                 context.style.color(color), 2, arrow_end=True)
            return ux, uy

        def frame_callback():
            self.draw.background(context.style.color("widget"))

            settings = context.states.get("network_hosts")
            def setting(mac, key):
                return settings.get(mac, {}).get(key)

            macs, host_ips = self.network.get_hosts()
            # Forget hosts that are gone altogether (Clear Data)
            for mac in list(self.last_cell):
                if mac not in host_ips:
                    del self.last_cell[mac]
            shown = [mac for mac in macs if setting(mac, "hide") not in (1, "1")]
            table = place(shown, self.network.get_access_point())
            nicknames = {mac: setting(mac, "nickname") for mac in shown}

            def receivers(src, dst):
                '''The shown hosts a packet goes to - every other one for a broadcast.'''
                if dst == MetaPacket.BROADCAST_MAC:
                    return [mac for mac in shown if mac != src]
                return [dst] if dst in self.cell_of and dst != src else []

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
            packet_ips = {mac: [] for mac in shown}
            def add_ip(mac, ip):
                if mac in packet_ips and ip not in packet_ips[mac]:
                    packet_ips[mac].append(ip)
            for mpkt in shown_packets:
                ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                if ip_src not in (None, "-") and ip_dst not in (None, "-"):
                    add_ip(mpkt.get("mac_src"), ip_src)
                    for target in receivers(mpkt.get("mac_src"), mpkt.get("mac_dst")):
                        add_ip(target, ip_dst)

            # Each shown host's chip center, zoomed and panned like
            # everything else the camera shows
            order = list(self.cell_of)
            centers = dict(zip(order, t.zoom_and_pan([table.spots[self.cell_of[mac]] for mac in order],
                                                     self.camera.scale, tuple(self.camera.offset))))

            # Arrows first, so the labels and chips sit on top of them - and
            # how many leave each chip from its top and from its bottom
            arrow_ends = {mac: [0, 0] for mac in centers}
            def note_end(mac, uy):
                if abs(uy) > FLAT_ARROW:
                    arrow_ends[mac][0 if uy < 0 else 1] += 1
            for mpkt in shown_packets:
                mac_src = mpkt.get("mac_src")
                if mac_src not in centers:
                    continue
                has_ips = mpkt.get("ip_src") not in (None, "-") and mpkt.get("ip_dst") not in (None, "-")
                for target in receivers(mac_src, mpkt.get("mac_dst")):
                    direction = draw_arrow(centers, mac_src, target, "accent")
                    if mode == "paused" and has_ips:
                        draw_arrow(centers, mac_src, target, "scrollbar_hover")
                    if direction is not None:
                        note_end(mac_src, direction[1])
                        note_end(target, -direction[1])

            def color_of(mac):
                return "outgoing" if mac == self.mac_address else "incoming"

            # A label goes on the side of its chip fewer arrows leave from -
            # with as many either way, under it, unless there's a host in the
            # cell under it. Each gap between rows holds one label, so if the
            # side it wants is taken, the other; hosts claim them in the
            # table's order, the access point first.
            occupied = {table.cells[cell] for cell in self.cell_of.values()}
            used_gaps = set()
            for mac in sorted(centers, key=lambda mac: self.cell_of[mac]):
                # One line, all the gap between rows holds - a router forwards
                # packets for many outside IPs at once, so the first, then
                # how many more
                ips = packet_ips[mac]
                if not ips:
                    continue
                text = ips[0] + (f" +{len(ips) - 1}" if len(ips) > 1 else "")
                column, row = table.cells[self.cell_of[mac]]
                top_ends, bottom_ends = arrow_ends[mac]
                if top_ends == bottom_ends:
                    above_first = (column, row + 1) in occupied
                else:
                    above_first = top_ends < bottom_ends
                # The gap over row r is gap r; the one under it, gap r + 1
                sides = [(True, (column, row)), (False, (column, row + 1))]
                if not above_first:
                    sides.reverse()
                above, gap = next((side for side in sides if side[1] not in used_gaps), sides[0])
                used_gaps.add(gap)
                draw_label(centers[mac], text, above, color_of(mac))

            for mac, center in centers.items():
                nickname = nicknames.get(mac)
                draw_chip(center, display_name(nickname) if nickname else mac[-8:],
                          nickname_font if nickname else node_font,
                          NICKNAME_CHIP_OUTLINE if nickname else CHIP_OUTLINE, color_of(mac))

        self.set_frame_callback(frame_callback)
        self.start_animation()
