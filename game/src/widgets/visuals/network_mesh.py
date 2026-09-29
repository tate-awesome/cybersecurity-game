import math
from collections import deque

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette, draw_glow


class NetworkMesh(Visual):
    '''
    A small internet: a network of networks in two layers.

    Backbone - core routers spread across the area, each linked to its
    nearest neighbors (plus whatever links it takes to keep the backbone
    connected), drifting slowly.
    Subnets - every router has its own cluster of hosts orbiting it,
    each host linked only to its own router.

    Packets are glowing dots that follow real hop-by-hop routes: host ->
    its router -> shortest backbone path -> destination router -> host.
    Most traffic is scattered one-off packets, but some host pairs open a
    "connection" for a few seconds and trade bursts of packets back and
    forth, the way a request/response session looks on the wire.

    Holding the left mouse button down makes the host nearest the cursor
    send a steady stream of packets out across the network. Holding the
    right button pulls every packet - in flight, waiting to leave, or just
    delivered - toward the host nearest the cursor.
    '''

    KEY = "network_mesh"
    ROUTER_SPEED = 6.0
    HOST_ORBIT_SPEED = 0.08  # radians per second
    PACKET_SPEED = 240.0     # pixels per second
    PING_SECONDS = 0.9
    PACKET_RADIUS = 6.0
    LINGER_START = 0.6          # seconds a new packet sits on its source, fading in, before it leaves
    LINGER_END = 0.9            # seconds a delivered packet sits on its destination, fading out
    WARMUP_SECONDS = 8.0
    # Router spreading (see build and repel_routers)
    PLACEMENT_CANDIDATES = 20   # spots tried per router; more = more even
    REPEL_RANGE = 0.85          # x spacing - closer than this, routers push apart
    REPEL_STRENGTH = 40.0       # pixels/s^2 of push at point-blank range
    SPEED_SETTLE = 0.5          # 1/s - how fast pushed routers return to ROUTER_SPEED
    HOLD_RATE = 8.0             # packets per second from the host under the cursor while the mouse is held
    PULL_SPEEDUP = 2.2          # pulled packets travel this many times faster
    # The network extends this fraction past every edge, so it reads as a
    # window onto a bigger internet rather than a diagram that fits the screen
    OVERSCAN = 0.15
    # Per megapixel of the overscanned area: routers, scattered packets per
    # second, and open connections. Traffic scales with area rather than
    # router count, so adding nodes doesn't also flood the screen.
    ROUTER_DENSITY = 16
    TRAFFIC_RATE = 2.0
    CONNECTION_DENSITY = 0.6

    def on_resize(self, first: bool):
        # Router count and subnet spacing depend on the area, so a big
        # change (e.g. first layout from a tiny initial size, or going
        # fullscreen) gets a fresh topology; small changes just stretch it.
        area_change = self.scale_x * self.scale_y
        if first or not hasattr(self, "routers") or not 0.6 < area_change < 1.6:
            self.build()
            return
        for router in self.routers:
            router["x"] *= self.scale_x
            router["y"] *= self.scale_y
        self.spacing *= math.sqrt(self.scale_x * self.scale_y)

    def area_megapixels(self) -> float:
        span = 1 + 2 * self.OVERSCAN
        return self.width * self.height * span * span / 1_000_000

    # Topology
    def build(self):
        area = self.area_megapixels() * 1_000_000
        router_count = max(8, min(40, int(self.area_megapixels() * self.ROUTER_DENSITY)))
        self.routers = []
        # Typical distance between neighboring routers if spread evenly
        self.spacing = math.sqrt(area / router_count)
        min_gap = self.spacing * 0.6
        low, high = -self.OVERSCAN, 1 + self.OVERSCAN
        for _ in range(router_count):
            # Best-candidate sampling: of several random spots, keep the one
            # farthest from every router placed so far. Evenly spread like
            # a Poisson-disk pattern, but never gives up and falls back to
            # a crowded spot the way plain rejection sampling can.
            best, best_distance = None, -1.0
            for _candidate in range(self.PLACEMENT_CANDIDATES):
                x = self.rng.uniform(low, high) * self.width
                y = self.rng.uniform(low, high) * self.height
                nearest = min((math.hypot(x - r["x"], y - r["y"]) for r in self.routers), default=math.inf)
                if nearest > best_distance:
                    best, best_distance = (x, y), nearest
            x, y = best
            heading = self.rng.uniform(0, math.tau)
            self.routers.append({
                "x": x, "y": y,
                "vx": math.cos(heading) * self.ROUTER_SPEED,
                "vy": math.sin(heading) * self.ROUTER_SPEED,
            })

        self.backbone = self.link_backbone()
        self.next_hop = self.route_all()

        # Longest a subnet link may get, for directions with no neighboring
        # router to stop it (the overscan edge of the network)
        self.max_reach = min_gap * 1.1
        self.hosts = []
        for index in range(router_count):
            count = self.rng.randint(5, 11)
            spin = self.rng.choice((-1, 1)) * self.HOST_ORBIT_SPEED * self.rng.uniform(0.5, 1.5)
            for i in range(count):
                host = {
                    "router": index,
                    "angle": math.tau * i / count + self.rng.uniform(-0.3, 0.3),
                    # How far out into its router's cell this host sits:
                    # mostly mid-range, with some hugging the router and
                    # some reaching nearly to the cell's edge
                    "reach": 0.15 + 0.75 * self.rng.random() ** 0.9,
                    "spin": spin,
                }
                host["target"] = host["radius"] = self.host_target(host)
                self.hosts.append(host)
        self.refresh_cursor = 0

        self.packets = []
        self.connections = []
        self.pings = []
        self.landed = []

        # Fast-forward to steady traffic, so a page opens on a network
        # that's already busy instead of one visibly filling up from empty
        for _ in range(int(self.WARMUP_SECONDS / 0.1)):
            self.update(0.1)

    def cell_edge(self, index: int, angle: float) -> float:
        '''
        Distance from router `index`, heading along `angle`, to the edge of
        its cell - the region closer to it than to any other router (its
        Voronoi cell). The edge in that direction is the nearest
        perpendicular bisector between it and a neighbor: for a neighbor
        at offset d, the ray reaches the bisector at |d|^2 / (2 u.d).
        '''
        router = self.routers[index]
        ux, uy = math.cos(angle), math.sin(angle)
        edge = self.max_reach
        for other_index, other in enumerate(self.routers):
            if other_index == index:
                continue
            dx, dy = other["x"] - router["x"], other["y"] - router["y"]
            toward = ux * dx + uy * dy
            if toward > 0:
                edge = min(edge, (dx * dx + dy * dy) / (2 * toward))
        return edge

    def host_target(self, host: dict) -> float:
        return max(10.0, host["reach"] * self.cell_edge(host["router"], host["angle"]))

    def link_backbone(self) -> set[tuple[int, int]]:
        '''Each router links to its 2 nearest, then a minimum spanning tree guarantees connectivity.'''
        n = len(self.routers)
        def distance(a, b):
            return math.hypot(self.routers[a]["x"] - self.routers[b]["x"], self.routers[a]["y"] - self.routers[b]["y"])

        links = set()
        for a in range(n):
            nearest = sorted((b for b in range(n) if b != a), key=lambda b: distance(a, b))[:2]
            for b in nearest:
                links.add((min(a, b), max(a, b)))

        # Prim's MST over the full graph - cheap at this size
        connected = {0}
        while len(connected) < n:
            a, b = min(
                ((a, b) for a in connected for b in range(n) if b not in connected),
                key=lambda pair: distance(*pair),
            )
            links.add((min(a, b), max(a, b)))
            connected.add(b)
        return links

    def route_all(self) -> dict[tuple[int, int], int]:
        '''next_hop[(here, destination)] -> neighboring router, by BFS hop count.'''
        n = len(self.routers)
        neighbors = {i: [] for i in range(n)}
        for a, b in self.backbone:
            neighbors[a].append(b)
            neighbors[b].append(a)
        table = {}
        for destination in range(n):
            # BFS outward from the destination; each node's parent is its next hop toward it
            parent = {destination: destination}
            queue = deque([destination])
            while queue:
                here = queue.popleft()
                for neighbor in neighbors[here]:
                    if neighbor not in parent:
                        parent[neighbor] = here
                        queue.append(neighbor)
            for here, hop in parent.items():
                table[(here, destination)] = hop
        return table

    def route(self, source_host: int, destination_host: int) -> list[tuple[str, int]]:
        '''Hop list of ("host"|"router", index) from one host to another.'''
        start = self.hosts[source_host]["router"]
        end = self.hosts[destination_host]["router"]
        path = [("host", source_host), ("router", start)]
        here = start
        while here != end:
            here = self.next_hop[(here, end)]
            path.append(("router", here))
        path.append(("host", destination_host))
        return path

    def route_from(self, node: tuple[str, int], destination_host: int) -> list[tuple[str, int]]:
        '''
        Hop list from any node - a host or a router partway through a
        route - to a host. Used to reroute packets already in flight.
        '''
        if node == ("host", destination_host):
            return [node]
        end = self.hosts[destination_host]["router"]
        kind, index = node
        path = [node]
        if kind == "host":
            here = self.hosts[index]["router"]
            path.append(("router", here))
        else:
            here = index
        while here != end:
            here = self.next_hop[(here, end)]
            path.append(("router", here))
        path.append(("host", destination_host))
        return path

    # Positions
    def position(self, node: tuple[str, int]) -> tuple[float, float]:
        kind, index = node
        if kind == "router":
            router = self.routers[index]
            return router["x"], router["y"]
        host = self.hosts[index]
        router = self.routers[host["router"]]
        return (router["x"] + math.cos(host["angle"]) * host["radius"],
                router["y"] + math.sin(host["angle"]) * host["radius"])

    # Simulation
    def update(self, dt: float):
        self.repel_routers(dt)
        low, high = -self.OVERSCAN, 1 + self.OVERSCAN
        for router in self.routers:
            router["x"] += router["vx"] * dt
            router["y"] += router["vy"] * dt
            # Point back inward (not just flip) so a router can't get stuck
            # flipping every frame just outside the edge
            if router["x"] < low * self.width:
                router["vx"] = abs(router["vx"])
            elif router["x"] > high * self.width:
                router["vx"] = -abs(router["vx"])
            if router["y"] < low * self.height:
                router["vy"] = abs(router["vy"])
            elif router["y"] > high * self.height:
                router["vy"] = -abs(router["vy"])
        # Hosts orbit and routers drift, so a host's room keeps changing.
        # Recompute a slice of the targets each frame (all of them about
        # every half second) and ease each link's length toward its target.
        slice_size = max(1, len(self.hosts) * 2 * max(dt, 1 / 60))
        for _ in range(int(math.ceil(slice_size))):
            host = self.hosts[self.refresh_cursor % len(self.hosts)]
            host["target"] = self.host_target(host)
            self.refresh_cursor += 1
        ease = 1.0 - math.exp(-1.5 * dt)
        for host in self.hosts:
            host["angle"] += host["spin"] * dt
            host["radius"] += (host["target"] - host["radius"]) * ease

        self.update_connections(dt)
        self.update_hold(dt)
        self.update_pull()

        # Scattered one-off traffic, mostly between subnets. Accumulated
        # rather than rolled per frame, since the rate can exceed the fps.
        self.traffic_due = getattr(self, "traffic_due", 0.0) + dt * self.area_megapixels() * self.TRAFFIC_RATE
        while self.traffic_due >= 1.0:
            self.traffic_due -= 1.0
            a = self.rng.randrange(len(self.hosts))
            self.send(a, self.pick_destination(a))

        alive = []
        for packet in self.packets:
            if packet["linger"] > 0:
                # Still sitting on its source host before setting off
                packet["linger"] -= dt
                alive.append(packet)
                continue
            speed = self.PACKET_SPEED * (self.PULL_SPEEDUP if packet.get("pulled") else 1.0)
            packet["t"] += speed * dt / max(1.0, self.hop_length(packet))
            while packet["t"] >= 1.0:
                packet["t"] -= 1.0
                packet["hop"] += 1
                if packet["hop"] >= len(packet["path"]) - 1:
                    break
            if packet["hop"] >= len(packet["path"]) - 1:
                self.pings.append({"node": packet["path"][-1], "age": 0.0})
                self.landed.append({"node": packet["path"][-1], "age": 0.0})
            else:
                alive.append(packet)
        self.packets = alive

        for landed in self.landed:
            landed["age"] += dt
        self.landed = [l for l in self.landed if l["age"] < self.LINGER_END]

        for ping in self.pings:
            ping["age"] += dt
        self.pings = [p for p in self.pings if p["age"] < self.PING_SECONDS]

    def repel_routers(self, dt: float):
        '''
        Antigravity: routers closer than REPEL_RANGE x spacing push each
        other apart, harder the closer they are, so drifting can't bunch
        subnets together. Each router's speed then eases back toward
        ROUTER_SPEED, so pushes turn into course changes rather than
        building up into ever-faster motion.
        '''
        reach = self.spacing * self.REPEL_RANGE
        routers = self.routers
        for i in range(len(routers)):
            a = routers[i]
            for j in range(i + 1, len(routers)):
                b = routers[j]
                dx, dy = b["x"] - a["x"], b["y"] - a["y"]
                if abs(dx) > reach or abs(dy) > reach:
                    continue
                distance = math.hypot(dx, dy)
                if distance >= reach or distance < 1e-6:
                    continue
                push = self.REPEL_STRENGTH * (1.0 - distance / reach) * dt / distance
                a["vx"] -= dx * push
                a["vy"] -= dy * push
                b["vx"] += dx * push
                b["vy"] += dy * push

        settle = 1.0 - math.exp(-self.SPEED_SETTLE * dt)
        for router in routers:
            speed = math.hypot(router["vx"], router["vy"])
            if speed > 1e-6:
                scale = 1.0 + (self.ROUTER_SPEED / speed - 1.0) * settle
                router["vx"] *= scale
                router["vy"] *= scale

    def update_connections(self, dt: float):
        # Keep a few sessions open at once
        limit = max(1, round(self.area_megapixels() * self.CONNECTION_DENSITY))
        if len(self.connections) < limit and self.rng.random() < dt * 0.8:
            a = self.rng.randrange(len(self.hosts))
            b = self.pick_destination(a)
            self.connections.append({
                "a": a, "b": b,
                "remaining": self.rng.uniform(3.0, 8.0),
                "burst": 0,            # packets left in the current burst
                "forward": True,       # current direction of the burst
                "gap": 0.0,            # seconds until the next packet
            })
        alive = []
        for connection in self.connections:
            connection["remaining"] -= dt
            connection["gap"] -= dt
            if connection["gap"] <= 0:
                if connection["burst"] <= 0:
                    # Turn around: a request, then a response, then another request...
                    connection["forward"] = not connection["forward"]
                    connection["burst"] = self.rng.randint(1, 4)
                    connection["gap"] = self.rng.uniform(0.6, 1.4)
                else:
                    a, b = connection["a"], connection["b"]
                    if connection["forward"]:
                        self.send(a, b)
                    else:
                        self.send(b, a)
                    connection["burst"] -= 1
                    connection["gap"] = self.rng.uniform(0.06, 0.12)
            if connection["remaining"] > 0:
                alive.append(connection)
        self.connections = alive

    def update_hold(self, dt: float):
        '''
        While the left mouse button is held over the network, the host
        nearest the cursor streams packets to random hosts, HOLD_RATE per
        second. The source is re-picked for each packet, so dragging while
        holding moves the stream along with the cursor.
        '''
        if not self.pressed or self.pointer is None:
            self.hold_due = 0.0
            return
        self.hold_due = getattr(self, "hold_due", 0.0) + dt * self.HOLD_RATE
        while self.hold_due >= 1.0:
            self.hold_due -= 1.0
            source = self.nearest_host(self.pointer)
            self.send(source, self.pick_destination(source))

    def update_pull(self):
        '''
        While the right button is held, every packet heads for the host
        nearest the cursor. A packet in flight finishes the link it's on,
        then follows the shortest route from there; one still waiting at
        its source leaves at once; one just delivered and fading on its
        host takes off again. Pulled packets move PULL_SPEEDUP x faster.
        Moving the cursor retargets everything to the new nearest host.
        '''
        if not self.pulling or self.pointer is None:
            return
        target = self.nearest_host(self.pointer)
        target_node = ("host", target)

        for packet in self.packets:
            path = packet["path"]
            if path[-1] == target_node:
                continue
            next_node = path[packet["hop"] + 1]
            packet["path"] = path[:packet["hop"] + 1] + self.route_from(next_node, target)
            packet["linger"] = 0.0
            packet["pulled"] = True

        staying = []
        for landed in self.landed:
            if landed["node"] == target_node:
                staying.append(landed)
            else:
                self.packets.append({
                    "path": self.route_from(landed["node"], target),
                    "hop": 0, "t": 0.0, "linger": 0.0, "pulled": True,
                })
        self.landed = staying

    def pick_destination(self, source: int) -> int:
        destination = self.rng.randrange(len(self.hosts) - 1)
        return destination + 1 if destination >= source else destination

    def nearest_host(self, point: tuple[float, float]) -> int:
        return min(range(len(self.hosts)), key=lambda index: math.dist(point, self.position(("host", index))))

    def send(self, source: int, destination: int):
        self.packets.append({"path": self.route(source, destination), "hop": 0, "t": 0.0, "linger": self.LINGER_START})

    def hop_length(self, packet: dict) -> float:
        ax, ay = self.position(packet["path"][packet["hop"]])
        bx, by = self.position(packet["path"][packet["hop"] + 1])
        return math.hypot(bx - ax, by - ay)

    # Drawing
    def paint(self, painter: QPainter, palette: VisualPalette):
        # Backbone links
        pen = QPen(palette.color("foreground", 0.28), 2.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        for a, b in self.backbone:
            painter.drawLine(QPointF(*self.position(("router", a))), QPointF(*self.position(("router", b))))

        # Subnet links
        painter.setPen(QPen(palette.color("foreground", 0.14), 1.0))
        for index, host in enumerate(self.hosts):
            painter.drawLine(QPointF(*self.position(("router", host["router"]))), QPointF(*self.position(("host", index))))

        # Arrival pings
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for ping in self.pings:
            progress = ping["age"] / self.PING_SECONDS
            radius = 4 + progress * (26 if ping["node"][0] == "router" else 16)
            painter.setPen(QPen(palette.color("accent", 0.5 * (1.0 - progress)), 1.5))
            painter.drawEllipse(QPointF(*self.position(ping["node"])), radius, radius)

        # Nodes
        painter.setPen(QPen(palette.color("foreground", 0.55), 1.6))
        painter.setBrush(palette.color("background", 1.0))
        for index in range(len(self.routers)):
            painter.drawEllipse(QPointF(*self.position(("router", index))), 7.0, 7.0)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(palette.color("foreground", 0.55))
        for index in range(len(self.routers)):
            painter.drawEllipse(QPointF(*self.position(("router", index))), 3.0, 3.0)
        painter.setBrush(palette.color("foreground", 0.45))
        for index in range(len(self.hosts)):
            painter.drawEllipse(QPointF(*self.position(("host", index))), 2.6, 2.6)

        # Packets
        for packet in self.packets:
            ax, ay = self.position(packet["path"][packet["hop"]])
            bx, by = self.position(packet["path"][packet["hop"] + 1])
            t = packet["t"]
            # Fades in while lingering on its source, full strength once moving
            alpha = 1.0 - max(0.0, packet["linger"]) / self.LINGER_START if self.LINGER_START > 0 else 1.0
            draw_glow(painter, QPointF(ax + (bx - ax) * t, ay + (by - ay) * t), self.PACKET_RADIUS, palette.color("accent", 0.95 * alpha))
        for landed in self.landed:
            # Delivered: sits on its destination host and fades out
            alpha = 1.0 - landed["age"] / self.LINGER_END
            draw_glow(painter, QPointF(*self.position(landed["node"])), self.PACKET_RADIUS, palette.color("accent", 0.95 * alpha))
