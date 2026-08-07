from ..buffer import Buffer
from ..mod_table import ModTable
from .net_filter_queue import NetFilterQueueBaseClass
import pydivert

from scapy.all import IP
import threading

class NetFilterQueue(NetFilterQueueBaseClass):
    '''
    Windows Version
    '''
    def __init__(self, buffer: Buffer, table: ModTable): 
        super().__init__(buffer, table)

    def start(self): 
        if self.is_running():
            self.buffer.put("nfq", "MITM attack is already running")
            return
        self.running = True
        self.stop_event = threading.Event()
        self.buffer.put("nfq", "Starting MITM attack")

        self.thread = threading.Thread(target=self.start_thread, daemon=True)
        self.thread.start()

    def start_thread(self):
        self.buffer.put("nfq", "Starting WinDivert")

        filt = (
            "true"
        )

        with pydivert.WinDivert(filt) as w:
            self.w = w

            while not self.stop_event.is_set():

                try:
                    packet = w.recv()

                    try:
                        spkt = IP(bytes(packet.raw))
                    except Exception:
                        w.send(packet)
                        continue

                    self.buffer.put("nfq", "Incoming mitm packet", spkt, "recv")
                    newspkt = self.modify_spkt(spkt)
                    self.buffer.put("nfq", "Outgoing mitm Packet", spkt, "recv")

                    if newspkt is not None:
                        packet.payload = bytes(newspkt)

                    w.send(packet)

                except Exception as e:
                    self.buffer.put(
                        "nfq",
                        f"WinDivert error: {e}"
                    )
                    self.buffer.put("nfq", "Problematic Packet", spkt)
                    pass

        self.buffer.put("nfq", "Stopped WinDivert")
