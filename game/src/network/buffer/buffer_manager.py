'''
The manager of the grand buffer is where generators put() information.
Things get put into a queue to be processed by a worker thread.
The worker thread will then filter the information and put it into the appropriate buffers.
Each buffer will generate one packet's worth of information for its data structures.
When the UI requests information, the buffers' data will have already been processed.
Double buffering?

'''
import time
import threading
from collections import deque
from scapy.all import Packet

from .channels import (
    StatusBuffer, PacketBuffer, ModbusBuffer, MapBuffer, HouseBuffer, NetworkGraph,
    DefenderModbusBuffer, DefenderMapBuffer, DefenderStatusBuffer,
)
from .meta_packet import MetaPacket
from .channels.transaction_manager import TransactionManager
from .poll_unpacker import _PollUnpacker
from ..saved import Loader, Replay, FileStream

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context

class Buffer:
    def __init__(self, context: "Context", max_size = 5000):
        self.context = context
        self.max_size = max_size

        # Putting logic
        self.accept_puts = True
        self.put_lock = threading.Lock()
        self.put_queue = deque(maxlen=self.max_size)
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.stop_event = threading.Event()

        # Buffers
        self.transaction_manager = TransactionManager()
        self.status = StatusBuffer(max_size=self.max_size)
        self.packets = PacketBuffer(context, max_size=self.max_size)
        self.modbus = ModbusBuffer(self.context, max_size=self.max_size)
        self.submarine = MapBuffer(self.context, self.modbus, max_size=self.max_size)
        self.hvac = HouseBuffer(self.context, self.modbus, max_size=self.max_size)
        self.network = NetworkGraph(self.context, self.packets, max_size = self.max_size)
        self.file_stream = FileStream(self, context)
        self.loader = Loader(self, context)
        self.replay = Replay(self, context)

        # Defender-page channels: fed by the AP's polled /api/data JSON via
        # _PollUnpacker (see put_poll), not by MetaPacket like the channels
        # above - the AP reports already-decoded values over HTTP, there's no
        # wire packet to sniff.
        self.defender_modbus = DefenderModbusBuffer(max_size=self.max_size)
        self.defender_map = DefenderMapBuffer(max_size=self.max_size)
        self.defender_status = DefenderStatusBuffer()
        self._poll_unpacker = _PollUnpacker(self.defender_modbus, self.defender_map, self.defender_status)

        self.start_worker()

    def reset(self):
        self.accept_puts = True
        self.put_queue.clear()
        self.packets.reset()
        self.network.reset()
        self.status.reset_cursor()
        self.modbus.reset()
        self.submarine.reset()
        self.hvac.reset()
        self.defender_modbus.reset()
        self.defender_map.reset()
        self.defender_status.reset()
        self._poll_unpacker.reset()

    def put_poll(self, data: dict) -> None:
        '''
        Unpacks one /api/data poll blob from the defender page's AP into
        defender_modbus/defender_map/defender_status. The only way in - the
        unpacker itself is private to this class.
        '''
        self._poll_unpacker.unpack(data)

    def reset_modbus(self):
        self.modbus.reset()
        self.submarine.reset()
        self.hvac.reset()

    def start_worker(self):
        if self.worker_thread.is_alive():
            return
        self.worker_thread.start()

    def stop_worker(self):
        self.stop_event.set()
        self.worker_thread.join(timeout=1)

    def capacity(self) -> float:
        capacity = float(len(self.put_queue) / self.max_size)
        return capacity
    
    def put(self, source: str, purpose: str, data: Packet | None=None, direction: str | None=None) -> None | MetaPacket:
        '''
        Put status messages and packets into the worker queue.
        Returns an enriched MetaPacket for those who need it

        source: the network action - "nmap", "arp", "dos", "sniff", "nfq", "pcap"

        purpose: a message about the packet, or a status message

        direction: sent or received by the network action - "in" or "out"
        '''
        output = None
        # Return on weird data
        if not isinstance(data, Packet) and data is not None:
            return
        # Create and enrich MetaPacket
        if isinstance(data, Packet) and isinstance(purpose, str) and isinstance(source, str):
            mpkt = MetaPacket(data, self.packets.get_first_packet_time(data), 0,
                            source, purpose, direction)
            if mpkt.get("is_modbus"):
                self.transaction_manager.enrich(mpkt)
            output = mpkt

        if self.accept_puts:
            with self.put_lock:
                self.put_queue.append((source, purpose, output, direction))

        return output
    
    def worker(self):
        while not self.stop_event.is_set():
            items_to_put = []
            with self.put_lock:
                while self.put_queue:
                    items_to_put.append(self.put_queue.popleft())

            for p in items_to_put:
                # A single bad packet/status item must not be able to kill this thread -
                # every channel buffer's put() feeds through here, so an unhandled
                # exception would silently stop the whole live view from updating.
                try:
                    self.worker_put(*p)
                except Exception as e:
                    print(f"Error processing buffer item {p!r}: {e}")

            time.sleep(0.01)

    def worker_put(self, source: str, purpose: str, data: MetaPacket | None=None, src: str | None=None):
        '''
        source: the network action - "nmap", "arp", "dos", "sniff", "nfq", "pcap"

        purpose: a message about the packet, or a status message

        src: "out" or "in"
        '''

        # Put status message in "status" buffer
        if data is None and isinstance(purpose, str) and isinstance(source, str):
            self.status.put(source, purpose)

        if isinstance(data, MetaPacket):
            self.distribute_packet(data)
        return

    def distribute_packet(self, mpkt: MetaPacket):
        '''
        Puts packets into appropriate buffers.

        source: the network action - "nmap", "arp", "dos", "sniff", "nfq", "pcap"

        purpose: a message about the packet

        src: "out" or "in"
        '''
        # Put all packets in the "packets" buffer for use by the packet console
        # self.packets.put(source, purpose, data, current_time)


        self.packets.put(mpkt)
        self.network.put(mpkt)
        if mpkt.get("is_modbus"):
            self.modbus.put(mpkt)

        if mpkt.get("is_useful"):
            self.submarine.put(mpkt)
            self.hvac.put(mpkt)

        self.file_stream.put(mpkt)