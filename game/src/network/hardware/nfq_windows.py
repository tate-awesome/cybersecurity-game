from .net_filter_queue import NetFilterQueueBaseClass
import pydivert

from scapy.all import IP, IPv6
import threading

class NetFilterQueue(NetFilterQueueBaseClass):
    '''
    Windows Version

    Uses a single WinDivert handle with a catch-all filter, branching on
    packet.is_inbound/is_outbound to run the PREROUTING/POSTROUTING-style
    callback - this is the pattern pydivert's own bundled README examples
    use throughout (one handle, one filter, direction read off the packet),
    not two separate handles opened with "inbound"/"outbound" filters. Two
    handles isn't documented anywhere as a supported way to split traffic,
    and running two independent recv/send loops made a crash in one
    direction's thread (see pump()) silently stop that whole direction
    without the other one noticing.

    Opened at Layer.NETWORK_FORWARD, not the default Layer.NETWORK.
    WinDivert's own docs draw a hard line between the two: NETWORK only
    ever sees packets to/from *this* machine's own sockets, while
    NETWORK_FORWARD is what sees packets merely transiting the machine
    between two other hosts - exactly what this class exists to intercept
    (the modbus master and slave are both other devices; this box is just
    sitting in the middle of their conversation). That's also why nothing
    was ever reaching prerouting_callback for real target traffic: at
    Layer.NETWORK, packets that aren't to/from this host don't arrive at
    all, no matter the filter.

    NETWORK_FORWARD only ever gets used by Windows in the first place if
    Windows is actually willing to route the packet, which - unlike
    Linux's `sysctl net.ipv4.ip_forward=1` - is off by default on non-server
    Windows and needs the IPEnableRouter registry value under
    HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters set to 1,
    followed by a reboot, before any of this can see third-party traffic.

    Unlike Linux, there's no PREROUTING/POSTROUTING pair here. netfilter is
    one linear chain of hooks - PREROUTING happens before the routing
    decision, POSTROUTING after it - so nfq_linux binds two separate
    NFQUEUE numbers and sees the same forwarded packet twice. WinDivert is
    built on the Windows Filtering Platform (WFP), which is a set of
    independent callout layers rather than one chain; NETWORK_FORWARD maps
    to WFP's single IP-forward callout, the equivalent of only Linux's
    FORWARD hook, with nothing on either side of it. The docs list exactly
    one event type for this layer (WINDIVERT_EVENT_NETWORK_PACKET) and
    scope the Outbound field's "which path does this get reinjected on"
    meaning specifically to Layer.NETWORK - there's no separate "before"
    and "after" to distinguish for a packet that's already mid-transit.
    So there is exactly one inspection point per forwarded packet here,
    not two, which is why prerouting_callback/postrouting_callback are
    collapsed into forwarding_callback below: whichever way is_inbound
    happens to read for a given leg, this is the only chance to modify
    the packet before it continues on its way, so it always has to run
    the full modify-capable path.
    '''
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        # Only meaningfully set while start_thread's pump loop is alive -
        # declared here so stop() can always safely check it.
        self.w: "pydivert.WinDivert | None" = None

    def start(self):
        if self.is_running():
            self.buffer.put("nfq", "NFQ is already running")
            return
        self.running = True
        self.stop_event = threading.Event()
        self.buffer.put("nfq", "Starting NFQ")

        # Run appropriate packet prerouter
        self.thread = threading.Thread(target=self.start_thread, daemon=True)
        self.thread.start()

    def stop(self):
        # Set first so pump()'s exception handler (fired by the close()
        # below) can tell this apart from a genuine WinDivert error.
        if self.stop_event is not None:
            self.stop_event.set()

        # WinDivertClose() interrupts any call currently blocked in recv()
        # on that handle from another thread - this is the Windows
        # equivalent of the stop pipe Linux registers alongside its NFQUEUE
        # fds in select.poll().
        w = self.w
        if w is not None and w.is_open:
            try:
                w.close()
            except Exception:
                # start_thread()'s own cleanup may win this race and close
                # the handle first (is_open isn't safe to check across
                # threads without a lock) - either way it ends up closed.
                pass
        super().stop()

    def start_thread(self):
        # Captured locally so stop() clearing self.stop_event once the
        # worker has exited can't race with the loop's own check of it.
        stop_event = self.stop_event

        self.buffer.put("nfq", "Starting WinDivert")

        self.w = pydivert.WinDivert("true", layer=pydivert.Layer.NETWORK_FORWARD)

        try:
            self.w.open()
        except Exception as e:
            self.buffer.put("nfq", f"Failed to open WinDivert (are you running as Administrator?): {e}")
            self.w = None
            self.running = False
            return

        self.pump(self.w, stop_event)

        if self.w.is_open:
            try:
                self.w.close()
            except Exception as e:
                print(f"[nfq] start_thread: error closing WinDivert handle: {e}")
        self.w = None
        self.buffer.put("nfq", "Stopped WinDivert")
        print("[nfq] start_thread: exiting")

    def pump(self, w: "pydivert.WinDivert", stop_event: threading.Event):
        while not stop_event.is_set():
            try:
                packet = w.recv()
            except Exception as e:
                # Raised by recv() once stop() closes the handle out from
                # under it - not a real error in that case.
                if not stop_event.is_set():
                    print(f"[nfq] pump: recv() error: {e}")
                    self._report_error(f"WinDivert error: {e}")
                return

            try:
                self.forwarding_callback(w, packet)
            except Exception as e:
                print(f"[nfq] pump: callback raised: {e}")
                self._report_error(f"Error processing packet: {e}")
                # A modify/logging failure must still forward the original
                # packet - dropping it here would silently black-hole the
                # victim's traffic.
                try:
                    w.send(packet, recalculate_checksum=False)
                except Exception as send_e:
                    print(f"[nfq] pump: fallback send() also failed: {send_e}")

    def _report_error(self, message: str):
        '''
        Reports a pump()/callback failure to the status buffer, falling
        back to a bare print() if the buffer itself is what's broken -
        otherwise a broken buffer.put() would raise again here, escape
        pump()'s own try/except, and silently kill this whole loop with
        no visible message at all.
        '''
        try:
            self.buffer.put("nfq", message)
        except Exception as e:
            print(f"[nfq] _report_error: buffer.put() itself failed: {e} (original: {message})")

    def accept_only(self, w: "pydivert.WinDivert", packet: "pydivert.Packet"):
        '''
        The WinDivert equivalent of nfq_linux's accept_only()/pkt.accept():
        forward the packet exactly as captured, with no dissection, no
        buffer.put(), no modify_mpkt() - just put it back on the wire.
        '''
        w.send(packet, recalculate_checksum=False)

    def forwarding_callback(self, w: "pydivert.WinDivert", packet: "pydivert.Packet"):
        '''
        The one inspection point NETWORK_FORWARD gives us per packet (see
        the class docstring for why there's no separate pre/post pair here)
        - so this always runs the full modify-capable path nfq_linux only
        runs at PREROUTING. The "in"/"out" tag is still taken from
        packet.is_inbound purely as a label for the buffer/UI; it does not
        gate whether modification is attempted.
        '''
        # This handle is opened at Layer.NETWORK_FORWARD only (see class
        # docstring), which per WinDivert's docs exclusively delivers
        # "network packets passing through the local machine" - packets
        # to/from this host's own sockets arrive at Layer.NETWORK instead
        # and never reach this handle at all. So every packet seen here is
        # necessarily the "received and forwarded" case, never "generated/
        # sent by this host" or "received-only, staying local" - there's no
        # per-packet check needed to know that, it's constant for this
        # whole handle.
        packet_type = "received_forwarded"

        # Direction will always be "out" because we're only in the forward layer
        # We'll set direction to "in" for our purposes to track pre/post modification
        direction = "in"

        spkt = self.get_spkt(packet)
        print(f"[nfq] forwarding_callback: packet_type={packet_type}, get_spkt -> {spkt.summary() if spkt is not None else None} (direction={direction})")
        if spkt is None:
            w.send(packet, recalculate_checksum=False)
            return

        enriched_mpkt = self.buffer.put("nfq", "WinDivert FORWARD IN", spkt, direction)
        print(f"    | buffer.put -> {'MetaPacket' if enriched_mpkt is not None else None}")
        if enriched_mpkt is None:
            w.send(packet, recalculate_checksum=False)
            return
        # TODO add logic and timeline flags if it really does get modded
        spkt, modified = self.modify_mpkt(enriched_mpkt)
        print(f"    | modify_mpkt -> modified={modified}")

        # Post modification (if there was one) we treat this as the halfway point and say the
        # packet is outbound

        direction = "out"
        if modified:
            self.buffer.put("nfq", "WinDivert MODIFIED IN", spkt, direction)
            # modify_mpkt() already deletes and rebuilds the IP/TCP
            # checksums and IP length via scapy (see net_filter_queue.py) -
            # the same trust-scapy's-rebuild model nfq_linux uses when it
            # hands the rebuilt bytes to pkt.set_payload(). Letting
            # WinDivert recalculate again on send() below is redundant on
            # every single packet (modified or not) and was slowing the
            # control loop down for no benefit.
            packet.raw = memoryview(bytearray(bytes(spkt)))
            print("    | posted modified outgoing packet")
        else:
            print("    | NOT modifying")
        self.buffer.put("nfq", "WinDivert FORWARD OUT", spkt, direction)
        print("    | posted outgoing packet")
        w.send(packet, recalculate_checksum=False)
        print("    | sent packet")

    def get_spkt(self, packet: "pydivert.Packet"):
        raw = bytes(packet.raw)

        if len(raw) < 1:
            return None

        # WinDivert's NETWORK layer only ever hands us IP packets, never
        # raw Ethernet frames.
        # IPv4
        if raw[0] >> 4 == 4:
            return IP(raw)

        # IPv6
        if raw[0] >> 4 == 6:
            return IPv6(raw)

        return None
