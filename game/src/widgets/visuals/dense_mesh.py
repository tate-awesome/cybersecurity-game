from PySide6.QtCore import QLineF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import VisualPalette
from .network_mesh import NetworkMesh


class DenseMesh(NetworkMesh):
    '''
    NetworkMesh at a much higher density - several times the routers, each
    with a smaller subnet - where a packet isn't a dot but a pulse of
    thickness running along the link it's crossing, and a delivered one
    lights up the link into its host as it fades.

    Everything else (routing, connections, the startup build, the mouse,
    detail and quiet entrance) works as in NetworkMesh.
    '''

    KEY = "dense_mesh"
    ROUTER_DENSITY = 48
    ROUTER_COUNT = (20, 110)
    HOSTS_PER_ROUTER = (3, 6)
    TRAFFIC_RATE = 4.0
    CONNECTION_DENSITY = 1.2
    SPAWN_SLOW_SECONDS = 2
    PULSE_LENGTH = 34.0        # px of link a packet thickens
    PULSE_WIDTH = 3.4

    def paint_packets(self, painter: QPainter, palette: VisualPalette):
        pen = QPen(palette.color("accent", 0.95), self.PULSE_WIDTH)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pulses: list[QLineF] = []
        for packet in self.packets:
            if packet["linger"] > 0:
                continue  # hasn't set off yet - nothing on a link to thicken
            ax, ay = self.position(packet["path"][packet["hop"]])
            bx, by = self.position(packet["path"][packet["hop"] + 1])
            length = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
            half = self.PULSE_LENGTH / 2 / length
            t0, t1 = max(0.0, packet["t"] - half), min(1.0, packet["t"] + half)
            pulses.append(QLineF(ax + (bx - ax) * t0, ay + (by - ay) * t0, ax + (bx - ax) * t1, ay + (by - ay) * t1))
        painter.setPen(pen)
        painter.drawLines(pulses)

        # Delivered: the link into the host it reached glows, fading out
        for landed in self.landed:
            kind, index = landed["node"]
            if kind != "host":
                continue
            alpha = 1.0 - landed["age"] / self.LINGER_END
            glow = QPen(palette.color("accent", 0.8 * alpha), self.PULSE_WIDTH * 0.8)
            glow.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(glow)
            router = ("router", self.hosts[index]["router"])
            painter.drawLine(QLineF(*self.position(router), *self.position(landed["node"])))
