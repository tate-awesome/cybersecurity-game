from scapy.all import TCP, AsyncSniffer
from ..buffer import Buffer


class Sniffer:
    def __init__(self, buffer: Buffer):
        self.buffer = buffer
        self.sniffer = AsyncSniffer(
            prn=self.callback,
            store=False
        )

    
    def is_running(self):
        return self.sniffer.running

    def start(self):
        '''
        Starts a scapy sniffer that puts all packets into the buffer.
        This makes all packets available to the GUI and simplifies user options.
        '''
        if self.is_running():
            self.buffer.put("sniff", "Sniffer is already running")
            return

        self.buffer.put("sniff", "Starting Sniffer")
        
        self.sniffer.start()

    def callback(self, pkt):
        try:
            self.buffer.put("sniff", "Sniffed Packet", pkt)
        except Exception as e:
            print(e)
            pkt.show()


    def stop(self):
        if self.sniffer.running:
            self.sniffer.stop()
            self.buffer.put("sniff", "Stopped Sniffer")
        else:
            self.buffer.put("sniff", "Sniffer is not running")