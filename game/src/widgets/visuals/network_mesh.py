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
    connected), each circling slowly around its own fixed spot.
    Subnets - every router has its own cluster of hosts orbiting it,
    each host linked only to its own router.

    Packets are glowing dots that follow real hop-by-hop routes: host ->
    its router -> shortest backbone path -> destination router -> host.
    Most traffic is scattered one-off packets, but some host pairs open a
    "connection" for a few seconds and trade bursts of packets back and
    forth, the way a request/response session looks on the wire.

    The first network of the app session spawns in slowly: one router a
    second, from the middle outward along the backbone, each one's hosts
    sliding out of it over the following second. Traffic only flows
    between nodes that have fully appeared. Later builds (a resize, the
    visuals demo) appear at once, already busy.

    {"packets": False} in paint_options stops traffic entirely (see
    update) - the routers and hosts keep moving, nothing is sent.

    Holding the left mouse button down makes the host nearest the cursor
    send a steady stream of packets out across the network. Holding the
    right button pulls every packet - in flight, waiting to leave, or just
    delivered - toward the host nearest the cursor.
    '''

    KEY = "network_mesh"
    # Routers circle their home spot: radius as a fraction of spacing, and
    # angular speed in radians per second (direction picked at random)
    ROUTER_ORBIT_RADIUS = (0.05, 0.12)
    ROUTER_ORBIT_SPEED = (0.1, 0.4)
    HOST_ORBIT_SPEED = 0.08  # radians per second
    PACKET_SPEED = 240.0     # pixels per second
    PING_SECONDS = 0.9
    PACKET_RADIUS = 6.0
    LINGER_START = 0.6          # seconds a new packet sits on its source, fading in, before it leaves
    LINGER_END = 0.9            # seconds a delivered packet sits on its destination, fading out
    WARMUP_SECONDS = 8.0
    PLACEMENT_CANDIDATES = 20   # spots tried per router; more = more even
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
    # Startup spawn-in (see build/update_spawn)
    SPAWN_DELAY = 0.4           # seconds before the first router appears
    ROUTER_INTERVAL = 1.0       # seconds between routers appearing
    HOST_WINDOW = 1.0           # a router's hosts appear over this many seconds after it
    GROW_SECONDS = 0.5          # how long each node takes to fade/slide in
    # Whether the app session's slow startup spawn has been claimed yet -
    # only the very first network built plays it
    startup_spawn_claimed = False

    def on_resize(self, first: bool):
        # Router count and subnet spacing depend on the area, so a big
        # change (e.g. first layout from a tiny initial size, or going
        # fullscreen) gets a fresh topology; small changes just stretch it.
        area_change = self.scale_x * self.scale_y
        if first or not hasattr(self, "routers") or not 0.6 < area_change < 1.6:
            self.build()
            return
        stretch = math.sqrt(self.scale_x * self.scale_y)
        for router in self.routers:
            router["cx"] *= self.scale_x
            router["cy"] *= self.scale_y
            router["orbit"] *= stretch
        self.spacing *= stretch
        self.move_routers(0.0)

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
                nearest = min((math.hypot(x - r["cx"], y - r["cy"]) for r in self.routers), default=math.inf)
                if nearest > best_distance:
                    best, best_distance = (x, y), nearest
            x, y = best
            self.routers.append({
                "cx": x, "cy": y,
                "orbit": self.rng.uniform(*self.ROUTER_ORBIT_RADIUS) * self.spacing,
                "angle": self.rng.uniform(0, math.tau),
                "spin": self.rng.choice((-1, 1)) * self.rng.uniform(*self.ROUTER_ORBIT_SPEED),
            })
        self.move_routers(0.0)

        self.backbone = self.link_backbone()

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

        if not NetworkMesh.startup_spawn_claimed:
            NetworkMesh.startup_spawn_claimed = True
            self.spawn_clock = 0.0
        # A rebuild partway through the spawn (e.g. the window's first real
        # layout) carries on from the same moment with the new topology
        self.spawning = getattr(self, "spawn_clock", None) is not None
        if self.spawning:
            self.schedule_spawn()
            self.visible_router_count = -1
            self.update_spawn(0.0)
            return

        for node in self.routers + self.hosts:
            node["born"] = -math.inf
        self.visible_hosts = list(range(len(self.hosts)))
        self.next_hop = self.route_all()
        # Fast-forward to steady traffic, so a page opens on a network
        # that's already busy instead of one visibly filling up from empty -
        # with traffic on even if this rebuild happened behind a workspace
        options, self.paint_options = self.paint_options, {}
        for _ in range(int(self.WARMUP_SECONDS / 0.1)):
            self.update(0.1)
        self.paint_options = options

    def schedule_spawn(self):
        '''
        Sets each node's "born" time on spawn_clock. Routers go in
        breadth-first order over the backbone from the one nearest the
        middle, so each new router links to one already there and the
        network grows outward as one piece. A router's hosts follow one by
        one, around the circle, within HOST_WINDOW after it.
        '''
        neighbors = {i: [] for i in range(len(self.routers))}
        for a, b in self.backbone:
            neighbors[a].append(b)
            neighbors[b].append(a)
        middle = (self.width / 2, self.height / 2)
        start = min(range(len(self.routers)), key=lambda i: math.dist(middle, (self.routers[i]["cx"], self.routers[i]["cy"])))
        order, queue, seen = [], deque([start]), {start}
        while queue:
            here = queue.popleft()
            order.append(here)
            # Nearest neighbors first, so growth spreads evenly
            for neighbor in sorted(neighbors[here], key=lambda n: math.dist(middle, (self.routers[n]["cx"], self.routers[n]["cy"]))):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        for rank, index in enumerate(order):
            self.routers[index]["born"] = self.SPAWN_DELAY + rank * self.ROUTER_INTERVAL
        for index, router in enumerate(self.routers):
            own = sorted((h for h in self.hosts if h["router"] == index), key=lambda h: h["angle"])
            for i, host in enumerate(own):
                host["born"] = router["born"] + (i + 1) / len(own) * self.HOST_WINDOW

    def update_spawn(self, dt: float):
        '''
        Advances the startup spawn: routes run over just the routers that
        have appeared, and traffic only uses hosts that have finished
        appearing. Ends the spawn once every node is fully grown.
        '''
        self.spawn_clock += dt
        visible = {i for i, router in enumerate(self.routers) if router["born"] <= self.spawn_clock}
        if len(visible) != self.visible_router_count:
            # A ping marks each router as it comes online (not on a rebuild)
            if self.visible_router_count >= 0:
                for index in visible:
                    if self.routers[index]["born"] > self.spawn_clock - dt:
                        self.pings.append({"node": ("router", index), "age": 0.0})
            self.visible_router_count = len(visible)
            self.next_hop = self.route_all(visible)
        self.visible_hosts = [i for i, host in enumerate(self.hosts) if self.growth(host) >= 1.0]
        if len(self.visible_hosts) == len(self.hosts):
            self.spawning = False
            self.spawn_clock = None

    def settle(self):
        if getattr(self, "spawning", False):
            self.spawn_clock = math.inf
            self.update_spawn(0.0)

    def growth(self, node: dict) -> float:
        '''0 before a node has spawned, rising to 1 once it has fully appeared.'''
        if not self.spawning:
            return 1.0
        return min(1.0, max(0.0, (self.spawn_clock - node["born"]) / self.GROW_SECONDS))

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

    def route_all(self, routers: set[int] | None = None) -> dict[tuple[int, int], int]:
        '''
        next_hop[(here, destination)] -> neighboring router, by BFS hop
        count - over just `routers` if given (the ones spawned so far).
        '''
        routers = set(range(len(self.routers))) if routers is None else routers
        neighbors = {i: [] for i in routers}
        for a, b in self.backbone:
            if a in routers and b in routers:
                neighbors[a].append(b)
                neighbors[b].append(a)
        table = {}
        for destination in routers:
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
        # A spawning host slides out of its router along its link
        radius = host["radius"] * (1.0 - (1.0 - self.growth(host)) ** 3)
        return (router["x"] + math.cos(host["angle"]) * radius,
                router["y"] + math.sin(host["angle"]) * radius)

    # Simulation
    def update(self, dt: float):
        if self.spawning:
            self.update_spawn(dt)
        self.move_routers(dt)
        # Hosts orbit and routers circle, so a host's room keeps changing.
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

        # {"packets": False} (a workspace's background) stops traffic
        # outright - the nodes keep drifting, but nothing is sent and
        # packets in flight hold still until it's back on a page with traffic
        if not self.paint_options.get("packets", True):
            return

        self.update_connections(dt)
        self.update_hold(dt)
        self.update_pull()

        # Scattered one-off traffic, mostly between subnets. Accumulated
        # rather than rolled per frame, since the rate can exceed the fps.
        # Scaled by how much of the network has spawned, so the first few
        # hosts aren't flooded with the whole network's traffic
        share = len(self.visible_hosts) / len(self.hosts)
        self.traffic_due = getattr(self, "traffic_due", 0.0) + dt * self.area_megapixels() * self.TRAFFIC_RATE * share
        while self.traffic_due >= 1.0:
            self.traffic_due -= 1.0
            if len(self.visible_hosts) < 2:
                continue
            a = self.rng.choice(self.visible_hosts)
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

    def move_routers(self, dt: float):
        for router in self.routers:
            router["angle"] += router["spin"] * dt
            router["x"] = router["cx"] + math.cos(router["angle"]) * router["orbit"]
            router["y"] = router["cy"] + math.sin(router["angle"]) * router["orbit"]

    def update_connections(self, dt: float):
        # Keep a few sessions open at once
        limit = max(1, round(self.area_megapixels() * self.CONNECTION_DENSITY))
        if self.spawning:
            limit = round(limit * len(self.visible_hosts) / len(self.hosts))
        if len(self.connections) < limit and len(self.visible_hosts) >= 2 and self.rng.random() < dt * 0.8:
            a = self.rng.choice(self.visible_hosts)
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
        if not self.pressed or self.pointer is None or len(self.visible_hosts) < 2:
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
        if not self.pulling or self.pointer is None or len(self.visible_hosts) < 2:
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
        '''Any other host that has finished spawning (callers make sure there's at least one).'''
        while True:
            destination = self.rng.choice(self.visible_hosts)
            if destination != source:
                return destination

    def nearest_host(self, point: tuple[float, float]) -> int:
        return min(self.visible_hosts, key=lambda index: math.dist(point, self.position(("host", index))))

    def send(self, source: int, destination: int):
        self.packets.append({"path": self.route(source, destination), "hop": 0, "t": 0.0, "linger": self.LINGER_START})

    def hop_length(self, packet: dict) -> float:
        ax, ay = self.position(packet["path"][packet["hop"]])
        bx, by = self.position(packet["path"][packet["hop"] + 1])
        return math.hypot(bx - ax, by - ay)

    # Drawing
    def paint(self, painter: QPainter, palette: VisualPalette):
        # {"packets": False} draws just the mesh - no pings or packets
        show_packets = self.paint_options.get("packets", True)

        # Backbone links
        pen = QPen(palette.color("foreground", 0.28), 2.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        for a, b in self.backbone:
            # While spawning, a link grows out from the router that was
            # there first toward the one just appearing
            if self.routers[a]["born"] > self.routers[b]["born"]:
                a, b = b, a
            grown = self.growth(self.routers[b])
            if grown <= 0.0:
                continue
            ax, ay = self.position(("router", a))
            bx, by = self.position(("router", b))
            painter.drawLine(QPointF(ax, ay), QPointF(ax + (bx - ax) * grown, ay + (by - ay) * grown))

        # Subnet links (a spawning host's link grows with it - see position)
        painter.setPen(QPen(palette.color("foreground", 0.14), 1.0))
        for index, host in enumerate(self.hosts):
            if self.growth(host) <= 0.0:
                continue
            painter.drawLine(QPointF(*self.position(("router", host["router"]))), QPointF(*self.position(("host", index))))

        # Arrival pings
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for ping in self.pings if show_packets else ():
            progress = ping["age"] / self.PING_SECONDS
            radius = 4 + progress * (26 if ping["node"][0] == "router" else 16)
            painter.setPen(QPen(palette.color("accent", 0.5 * (1.0 - progress)), 1.5))
            painter.drawEllipse(QPointF(*self.position(ping["node"])), radius, radius)

        # Nodes - spawning ones fade in, routers also swelling up to size
        painter.setPen(QPen(palette.color("foreground", 0.55), 1.6))
        painter.setBrush(palette.color("background", 1.0))
        for index, router in enumerate(self.routers):
            grown = self.growth(router)
            if grown > 0.0:
                painter.setOpacity(grown)
                size = 1.0 - (1.0 - grown) ** 3
                painter.drawEllipse(QPointF(*self.position(("router", index))), 7.0 * size, 7.0 * size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(palette.color("foreground", 0.55))
        for index, router in enumerate(self.routers):
            grown = self.growth(router)
            if grown > 0.0:
                painter.setOpacity(grown)
                size = 1.0 - (1.0 - grown) ** 3
                painter.drawEllipse(QPointF(*self.position(("router", index))), 3.0 * size, 3.0 * size)
        painter.setBrush(palette.color("foreground", 0.45))
        for index, host in enumerate(self.hosts):
            grown = self.growth(host)
            if grown > 0.0:
                painter.setOpacity(grown)
                painter.drawEllipse(QPointF(*self.position(("host", index))), 2.6, 2.6)
        painter.setOpacity(1.0)

        # Packets
        if not show_packets:
            return
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
