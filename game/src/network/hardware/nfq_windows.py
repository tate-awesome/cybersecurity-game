from .net_filter_queue import NetFilterQueueBaseClass
import pydivert

from scapy.all import IP, IPv6
import threading

class NetFilterQueue(NetFilterQueueBaseClass):
    '''
    Windows Version
    '''
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        # Only meaningfully set while start_thread's pump threads are alive -
        # declared here so stop() can always safely check them.
        self.w_in: "pydivert.WinDivert | None" = None
        self.w_out: "pydivert.WinDivert | None" = None

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
        for w in (self.w_in, self.w_out):
            if w is not None and w.is_open:
                try:
                    w.close()
                except Exception:
                    pass
        super().stop()

    def start_thread(self):
        # Captured locally so stop() clearing self.stop_event once the
        # worker has exited can't race with the loop's own check of it.
        stop_event = self.stop_event

        self.buffer.put("nfq", "Starting WinDivert")

        # WinDivert filter language: "inbound"/"outbound" split traffic the
        # same way iptables' PREROUTING/POSTROUTING chains do on Linux.
        self.w_in = pydivert.WinDivert("inbound")
        self.w_out = pydivert.WinDivert("outbound")

        try:
            self.w_in.open()
            self.w_out.open()
        except Exception as e:
            self.buffer.put("nfq", f"Failed to open WinDivert (are you running as Administrator?): {e}")
            self.w_in = None
            self.w_out = None
            self.running = False
            return

        in_thread = threading.Thread(target=self.pump, args=(self.w_in, self.prerouting_callback, stop_event), daemon=True)
        out_thread = threading.Thread(target=self.pump, args=(self.w_out, self.postrouting_callback, stop_event), daemon=True)
        in_thread.start()
        out_thread.start()

        in_thread.join()
        out_thread.join()

        for w in (self.w_in, self.w_out):
            if w.is_open:
                try:
                    w.close()
                except Exception:
                    pass
        self.w_in = None
        self.w_out = None
        self.buffer.put("nfq", "Stopped WinDivert")

    def pump(self, w: "pydivert.WinDivert", callback, stop_event: threading.Event):
        while not stop_event.is_set():
            try:
                packet = w.recv()
            except Exception as e:
                # Raised by recv() once stop() closes the handle out from
                # under it - not a real error in that case.
                if not stop_event.is_set():
                    self.buffer.put("nfq", f"WinDivert error: {e}")
                return

            try:
                callback(w, packet)
            except Exception as e:
                self.buffer.put("nfq", f"Error processing packet: {e}")
                # A modify/logging failure must still forward the original
                # packet - dropping it here would silently black-hole the
                # victim's traffic.
                try:
                    w.send(packet)
                except Exception:
                    pass

    def prerouting_callback(self, w: "pydivert.WinDivert", packet: "pydivert.Packet"):
        spkt = self.get_spkt(packet)
        if spkt is None:
            w.send(packet)
            return

        enriched_mpkt = self.buffer.put("nfq", "PREROUTING NFQ", spkt, "in")
        if enriched_mpkt is None:
            w.send(packet)
            return
        # TODO add logic and timeline flags if it really does get modded
        spkt, modified = self.modify_mpkt(enriched_mpkt)
        if modified:
            self.buffer.put("nfq", "MODIFIED NFQ", spkt, "in")
            packet.raw = memoryview(bytearray(bytes(spkt)))

        w.send(packet)

    def postrouting_callback(self, w: "pydivert.WinDivert", packet: "pydivert.Packet"):
        spkt = self.get_spkt(packet)
        if spkt is None:
            w.send(packet)
            return

        self.buffer.put("nfq", "POSTROUTING NFQ", spkt, "out")

        w.send(packet)

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
