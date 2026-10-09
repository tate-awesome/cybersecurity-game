from collections import Counter

from PySide6.QtCore import QLineF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import VisualPalette
from .network_mesh import NetworkMesh


class DenseMesh(NetworkMesh):
    '''
    NetworkMesh at a much higher density - many times the routers, each
    linked to more neighbors, with small subnets - in plain foreground
    color, where slow, sparse traffic shows only as thickness: a link
    thickens while packets cross it (more for more packets), and the link
    into a host that just received one stays thick for a moment. Each
    link's thickness glides between levels, easing in and out, rather
    than jumping as packets come and go.

    Everything else (routing, connections, the startup build, the mouse,
    detail and quiet entrance) works as in NetworkMesh.
    '''

    KEY = "dense_mesh"
    ROUTER_DENSITY = 144
    ROUTER_COUNT = (60, 330)
    NEAREST_LINKS = 4
    HOSTS_PER_ROUTER = (2, 5)
    PACKET_SPEED = 80.0
    TRAFFIC_RATE = 2.5
    CONNECTION_DENSITY = 0.8
    SPAWN_SLOW_SECONDS = 2
    SPAWN_ACCELERATION = 3
    BACKBONE_WIDTH = 1.4
    BACKBONE_CAP = Qt.PenCapStyle.FlatCap
    SUBNET_WIDTH = 0.8
    BUSY_WIDTH = 1.6          # px added per packet on a link (up to MAX_LOAD)
    MAX_LOAD = 3
    LOAD_RATE = 2.5           # packets' worth of thickness a link can gain or lose per second
    LOAD_STEPS = 12           # thickness steps drawn (each its own drawLines call)
    WARMUP_SECONDS = 4.0      # half the usual - keeps the build quick

    def update(self, dt: float):
        super().update(dt)
        # What each link's thickness is heading for: the packets on it, and
        # a host link that just delivered one
        target = Counter()
        for packet in self.packets:
            if packet["linger"] > 0:
                continue  # hasn't set off yet
            target[self.link(packet["path"][packet["hop"]], packet["path"][packet["hop"] + 1])] += 1
        for landed in self.landed:
            kind, index = landed["node"]
            if kind == "host":
                target[self.link(("router", self.hosts[index]["router"]), landed["node"])] += 1
        loads = getattr(self, "loads", {})
        step = self.LOAD_RATE * dt
        for link in set(loads) | set(target):
            goal = min(target.get(link, 0), self.MAX_LOAD)
            current = loads.get(link, 0.0)
            current += max(-step, min(step, goal - current))
            if current > 0.001 or goal:
                loads[link] = current
            else:
                loads.pop(link, None)
        self.loads = loads

    @staticmethod
    def link(a: tuple[str, int], b: tuple[str, int]) -> tuple:
        return (a, b) if a <= b else (b, a)

    def paint_packets(self, painter: QPainter, palette: VisualPalette):
        steps: dict[int, list[QLineF]] = {}
        for (a, b), load in getattr(self, "loads", {}).items():
            # Eased within each whole packet's worth, so every change in
            # thickness starts and ends gently (smoothstep per step)
            whole = int(load)
            part = load - whole
            shown = whole + part * part * (3 - 2 * part)
            level = round(shown / self.MAX_LOAD * self.LOAD_STEPS)
            if level > 0:
                steps.setdefault(level, []).append(QLineF(*self.position(a), *self.position(b)))
        for level, lines in sorted(steps.items()):
            load = level / self.LOAD_STEPS * self.MAX_LOAD
            pen = QPen(palette.color("foreground", 0.3 + 0.2 * load), self.SUBNET_WIDTH + self.BUSY_WIDTH * load)
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(pen)
            painter.drawLines(lines)
