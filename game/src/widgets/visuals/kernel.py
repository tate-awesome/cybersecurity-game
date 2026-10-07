import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QFont, QFontMetricsF, QPainter, QPainterPath, QPen

from .base import Visual, VisualPalette, draw_glow


# key: (label, x, y, hook, kind) - positions normalized to the widget.
# kind: "wire" (offscreen entry/exit), "nic", "table", "conntrack", "route", "app"
NODES = {
    "wire_in":     ("",          -0.04, 0.62, None, "wire"),
    "nic_rx":      ("eth0 rx",   0.045, 0.62, None, "nic"),
    "pre_raw":     ("raw",       0.12,  0.62, "PREROUTING", "table"),
    "conntrack":   ("conntrack", 0.195, 0.62, "PREROUTING", "conntrack"),
    "pre_mangle":  ("mangle",    0.27,  0.62, "PREROUTING", "table"),
    "pre_nat":     ("nat",       0.335, 0.62, "PREROUTING", "table"),
    "route_in":    ("route",     0.40,  0.62, None, "route"),
    "in_mangle":   ("mangle",    0.40,  0.24, "INPUT", "table"),
    "in_filter":   ("filter",    0.47,  0.24, "INPUT", "table"),
    "app":         ("local app", 0.545, 0.24, None, "app"),
    "route_out":   ("route",     0.62,  0.24, None, "route"),
    "out_raw":     ("raw",       0.68,  0.24, "OUTPUT", "table"),
    "out_mangle":  ("mangle",    0.735, 0.24, "OUTPUT", "table"),
    "out_nat":     ("nat",       0.79,  0.24, "OUTPUT", "table"),
    "out_filter":  ("filter",    0.86,  0.24, "OUTPUT", "table"),
    "fwd_mangle":  ("mangle",    0.55,  0.62, "FORWARD", "table"),
    "fwd_filter":  ("filter",    0.66,  0.62, "FORWARD", "table"),
    "post_mangle": ("mangle",    0.86,  0.62, "POSTROUTING", "table"),
    "post_nat":    ("nat",       0.92,  0.62, "POSTROUTING", "table"),
    "nic_tx":      ("eth0 tx",   0.975, 0.62, None, "nic"),
    "wire_out":    ("",          1.04,  0.62, None, "wire"),
}

PREROUTING = ["wire_in", "nic_rx", "pre_raw", "conntrack", "pre_mangle", "pre_nat", "route_in"]
POSTROUTING = ["post_mangle", "post_nat", "nic_tx", "wire_out"]
PATHS = {
    "inbound":  PREROUTING + ["in_mangle", "in_filter", "app"],
    "forward":  PREROUTING + ["fwd_mangle", "fwd_filter"] + POSTROUTING,
    "outbound": ["app", "route_out", "out_raw", "out_mangle", "out_nat", "out_filter"] + POSTROUTING,
}

# (name, hue offset from the theme accent, spawn weight, replies from the app?)
PROTOCOLS = [
    ("TCP",        0.0,  0.35, True),
    ("UDP",        0.5,  0.25, False),
    ("ICMP",       0.25, 0.12, False),
    ("ModBus/TCP", 0.75, 0.28, True),
]


class Kernel(Visual):
    '''
    Packets flowing through a Linux kernel's netfilter hooks, the path
    iptables rules act on. Every table is its own node, grouped under the
    hook it belongs to:

      wire -> eth0 rx -> PREROUTING (raw, conntrack, mangle, nat)
           -> routing decision -+-> INPUT (mangle, filter) -> local app
                                +-> FORWARD (mangle, filter) -> POSTROUTING
      local app -> routing decision -> OUTPUT (raw, mangle, nat, filter)
                -> POSTROUTING (mangle, nat) -> eth0 tx -> wire

    Packets pause briefly at each node to be processed, colored by
    protocol. filter tables occasionally drop one (it falls away and
    fades), nat tables flash as they rewrite an address, and TCP/ModBus
    traffic that reaches the local app often gets a reply sent back out
    through OUTPUT.
    '''

    KEY = "kernel"
    DWELL = (0.05, 0.14)     # seconds of "processing" at each node
    DROP_CHANCE = 0.09
    REPLY_CHANCE = 0.6
    FALL_SECONDS = 0.9

    def on_resize(self, first: bool):
        self.font = QFont("Consolas")
        self.font.setStyleHint(QFont.StyleHint.Monospace)
        self.font.setPixelSize(max(9, min(13, int(self.width / 110))))
        self.hook_font = QFont(self.font)
        self.hook_font.setBold(True)
        metrics = QFontMetricsF(self.font)
        self.node_height = metrics.height() + 10
        self.node_widths = {key: metrics.horizontalAdvance(label) + 16 for key, (label, *_rest) in NODES.items()}
        if first or not hasattr(self, "packets"):
            self.packets = []
            self.falling = []
            self.flashes = []
            self.replies = []
            self.heat = dict.fromkeys(NODES, 0.0)
            self.spawn_clock = 0.0

    def point(self, key: str) -> QPointF:
        _, x, y, _, _ = NODES[key]
        return QPointF(x * self.width, y * self.height)

    # Simulation
    def update(self, dt: float):
        self.spawn_clock -= dt
        if self.spawn_clock <= 0:
            self.spawn_clock = self.rng.uniform(0.12, 0.4)
            self.spawn("inbound" if self.rng.random() < 0.55 else "forward")
        if self.rng.random() < dt * 0.6:
            self.spawn("outbound")  # unprompted local traffic (DNS lookups, keepalives...)

        for reply in self.replies:
            reply["delay"] -= dt
        for reply in [r for r in self.replies if r["delay"] <= 0]:
            self.spawn("outbound", reply["protocol"])
        self.replies = [r for r in self.replies if r["delay"] > 0]

        speed = self.width * 0.22
        alive = []
        for packet in self.packets:
            if self.advance(packet, dt, speed):
                alive.append(packet)
        self.packets = alive

        decay = math.exp(-4.0 * dt)
        for key in self.heat:
            self.heat[key] *= decay
        for item in self.falling:
            item["age"] += dt
        self.falling = [f for f in self.falling if f["age"] < self.FALL_SECONDS]
        for flash in self.flashes:
            flash["age"] += dt
        self.flashes = [f for f in self.flashes if f["age"] < 0.5]

    def spawn(self, path: str, protocol: int | None = None):
        if protocol is None:
            protocol = self.rng.choices(range(len(PROTOCOLS)), weights=[p[2] for p in PROTOCOLS])[0]
        self.packets.append({"path": PATHS[path], "hop": 0, "t": 0.0, "dwell": 0.0, "protocol": protocol})

    def advance(self, packet: dict, dt: float, speed: float) -> bool:
        '''Moves one packet along its path. Returns False once it's consumed, dropped, or gone.'''
        while dt > 0:
            if packet["dwell"] > 0:
                used = min(dt, packet["dwell"])
                packet["dwell"] -= used
                dt -= used
                continue
            path = packet["path"]
            a, b = self.point(path[packet["hop"]]), self.point(path[packet["hop"] + 1])
            length = max(1.0, math.hypot(b.x() - a.x(), b.y() - a.y()))
            remaining = (1.0 - packet["t"]) * length / speed
            if dt < remaining:
                packet["t"] += dt * speed / length
                return True
            dt -= remaining
            packet["hop"] += 1
            packet["t"] = 0.0
            if not self.arrive(packet, path[packet["hop"]]):
                return False
        return True

    def arrive(self, packet: dict, key: str) -> bool:
        '''Handles a packet reaching a node. Returns False if it stops here.'''
        _, _, _, _, kind = NODES[key]
        if kind == "wire":
            return False
        self.heat[key] = 1.0
        packet["dwell"] = self.rng.uniform(*self.DWELL)
        if key.endswith("filter") and self.rng.random() < self.DROP_CHANCE:
            self.falling.append({"x": self.point(key).x(), "y": self.point(key).y(), "age": 0.0, "protocol": packet["protocol"]})
            return False
        if key.endswith("nat"):
            self.flashes.append({"key": key, "age": 0.0, "protocol": packet["protocol"]})
        if kind == "app":
            if PROTOCOLS[packet["protocol"]][3] and self.rng.random() < self.REPLY_CHANCE:
                self.replies.append({"delay": self.rng.uniform(0.1, 0.5), "protocol": packet["protocol"]})
            return False
        return True

    # Drawing
    def paint(self, painter: QPainter, palette: VisualPalette):
        self.paint_hooks(painter, palette)
        self.paint_edges(painter, palette)
        # Packets under the (slightly see-through) nodes, so one being
        # processed glows through its node without covering the label
        self.paint_packets(painter, palette)
        self.paint_nodes(painter, palette)
        self.paint_legend(painter, palette)

    def node_rect(self, key: str) -> QRectF:
        center = self.point(key)
        width = self.node_widths[key]
        return QRectF(center.x() - width / 2, center.y() - self.node_height / 2, width, self.node_height)

    def paint_hooks(self, painter: QPainter, palette: VisualPalette):
        hooks: dict[str, QRectF] = {}
        for key, (_, _, _, hook, _) in NODES.items():
            if hook is not None:
                rect = self.node_rect(key)
                hooks[hook] = hooks[hook].united(rect) if hook in hooks else rect
        painter.setFont(self.hook_font)
        pad = 10.0
        for hook, rect in hooks.items():
            box = rect.adjusted(-pad, -pad - self.node_height * 0.9, pad, pad)
            painter.setPen(QPen(palette.color("foreground", 0.18), 1.0, Qt.PenStyle.DashLine))
            painter.setBrush(palette.color("foreground", 0.03))
            painter.drawRoundedRect(box, 8, 8)
            painter.setPen(palette.color("foreground", 0.5))
            painter.drawText(QPointF(box.left() + 8, box.top() + self.node_height * 0.75), hook)

    def paint_edges(self, painter: QPainter, palette: VisualPalette):
        pen = QPen(palette.color("foreground", 0.22), 1.6)
        painter.setPen(pen)
        drawn = set()
        for path in PATHS.values():
            for a, b in zip(path, path[1:]):
                if (a, b) not in drawn:
                    drawn.add((a, b))
                    painter.drawLine(self.point(a), self.point(b))

    def paint_nodes(self, painter: QPainter, palette: VisualPalette):
        painter.setFont(self.font)
        for key, (label, _, _, _, kind) in NODES.items():
            if kind == "wire":
                continue
            rect = self.node_rect(key)
            heat = self.heat[key]
            border = palette.faded(palette.accent if heat > 0.05 else palette.foreground, 0.35 + 0.6 * heat)
            painter.setPen(QPen(border, 1.4 + heat))
            painter.setBrush(palette.color("background", 0.7))
            if kind == "route":
                # Decision diamond
                c = rect.center()
                w, h = rect.width() / 2 + 6, rect.height() / 2 + 6
                diamond = QPainterPath(QPointF(c.x(), c.y() - h))
                diamond.lineTo(QPointF(c.x() + w, c.y()))
                diamond.lineTo(QPointF(c.x(), c.y() + h))
                diamond.lineTo(QPointF(c.x() - w, c.y()))
                diamond.closeSubpath()
                painter.drawPath(diamond)
            else:
                radius = self.node_height / 2 if kind in ("nic", "app") else 5
                painter.drawRoundedRect(rect, radius, radius)
            painter.setPen(palette.color("foreground", 0.85))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        for flash in self.flashes:
            progress = flash["age"] / 0.5
            rect = self.node_rect(flash["key"]).adjusted(-10 * progress, -10 * progress, 10 * progress, 10 * progress)
            painter.setPen(QPen(palette.hue(PROTOCOLS[flash["protocol"]][1], 0.8 * (1 - progress)), 2.0))
            painter.drawRoundedRect(rect, 7, 7)

    def paint_packets(self, painter: QPainter, palette: VisualPalette):
        for packet in self.packets:
            path = packet["path"]
            a, b = self.point(path[packet["hop"]]), self.point(path[packet["hop"] + 1])
            t = packet["t"]
            center = QPointF(a.x() + (b.x() - a.x()) * t, a.y() + (b.y() - a.y()) * t)
            draw_glow(painter, center, 9.0, palette.hue(PROTOCOLS[packet["protocol"]][1], 1.0))

        for item in self.falling:
            progress = item["age"] / self.FALL_SECONDS
            center = QPointF(item["x"], item["y"] + self.node_height * 0.6 + progress * progress * 70)
            draw_glow(painter, center, 9.0 * (1 - 0.5 * progress), palette.hue(PROTOCOLS[item["protocol"]][1], 1.0 - progress))

    def paint_legend(self, painter: QPainter, palette: VisualPalette):
        painter.setFont(self.font)
        metrics = QFontMetricsF(self.font)
        x = self.width * 0.045
        y = self.height * 0.88
        for name, hue, _, _ in PROTOCOLS:
            draw_glow(painter, QPointF(x, y), 8.0, palette.hue(hue, 1.0))
            painter.setPen(palette.color("foreground", 0.75))
            painter.drawText(QPointF(x + 12, y + metrics.ascent() / 2 - 1), name)
            x += 12 + metrics.horizontalAdvance(name) + 28
        painter.setPen(palette.color("foreground", 0.5))
        painter.drawText(QPointF(x + 10, y + metrics.ascent() / 2 - 1), "- falls away: dropped by filter    flash: nat rewrite")
