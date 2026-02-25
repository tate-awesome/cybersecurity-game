from scapy.all import TCP, AsyncSniffer
from .. import modbus_util as mb
from ..data_buffer import DataBuffer


class Sniffer:
    def __init__(self, buffer: DataBuffer):
        self.sniffer = None
        self.buffer = buffer

    
    def is_running(self):
        return self.sniffer is not None
    

    def start(self):
        '''
        Starts a scapy sniffer that puts all packets into the buffer.
        This makes all packets available to the GUI and simplifies user options.
        '''
        if self.is_running():
            self.buffer.put("sniff", "status", "Sniffer is already running")
            return

        # callback_dict = {
        #     "show_all": self.show,
        #     "buffer_all": self.put_all_in_buffer,

        #     "show_modbus": self.show_modbus,
        #     "print_modbus": self.print_scannable,
        #     "buffer_modbus": self.put_modbus_in_buffer
        # }

        self.buffer.put("sniff", "status", "Starting Sniffer")
        def callback(pkt):
            self.buffer.put("sniff", "Sniffed Packet", pkt)
        self.sniffer = AsyncSniffer(
            prn=callback,
            store=False
        )
        self.sniffer.start()


    def stop(self):
        if self.sniffer is not None:
            self.sniffer.stop()
            self.sniffer = None
            self.buffer.put("sniff", "status", "Stopped Sniffer")
        else:
            self.buffer.put("sniff", "status", "Sniffer is not running")