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

from .channels import StatusBuffer, PacketBuffer

class Buffer:
    def __init__(self, context, max_size = 5000):
        self.context = context
        self.max_size = max_size


        # Putting logic
        self.accept_puts = True
        self.put_lock = threading.Lock()
        self.put_queue = deque(maxlen=self.max_size)
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)

        # Buffers
        self.status = StatusBuffer(max_size=self.max_size)
        self.packets = PacketBuffer(max_size=self.max_size, context=self.context)

        self.start_worker()

    def reset(self):
        self.accept_puts = True
        self.put_queue.clear()

    def start_worker(self):
        if self.worker_thread.is_alive():
            return
        self.worker_thread.start()

    def stop_worker(self):
        self.worker_thread.join(timeout=1)
    
    def put(self, source: str, purpose: str, data: Packet | None=None):
        '''
        Put status messages and packets into appropriate buffers.

        source: the network action - "nmap", "arp", "dos", "sniff", "mitm", "pcap"

        purpose: a message about the packet, or a status message
        '''
        if not self.accept_puts:
            return
        if not isinstance(data, Packet) and data is not None:
            return
        with self.put_lock:
            self.put_queue.append((source, purpose, data))
    
    def worker(self):
        while True:
            items_to_put = []
            
            with self.put_lock:
                while self.put_queue:
                    items_to_put.append(self.put_queue.popleft())

            for p in items_to_put:
                self.worker_put(*p)

            time.sleep(0.01)

    def worker_put(self, source: str, purpose: str, data: Packet | None=None):
        '''
        source: the network action - "nmap", "arp", "dos", "sniff", "mitm", "pcap"

        purpose: a message about the packet, or a status message
        '''

        # Put status message in "status" buffer
        if data is None and isinstance(purpose, str) and isinstance(source, str):
            self.status.put(source, purpose)

        if isinstance(data, Packet) and isinstance(purpose, str) and isinstance(source, str):
            self.distribute_packet(source, purpose, data)
        return

    def distribute_packet(self, source: str, purpose: str, data: Packet):
        '''
        Puts packets into appropriate buffers.

        source: the network action - "nmap", "arp", "dos", "sniff", "mitm", "pcap"

        purpose: a message about the packet
        '''
        # self.packets.put(source, purpose, data, current_time)
        ...