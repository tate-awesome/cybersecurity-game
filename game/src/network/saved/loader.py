from tkinter import filedialog
from ..packet_buffer import PacketBuffer
from scapy.packet import Packet
from scapy.all import rdpcap
from .. import modbus_util as mb
from ..mod_table import ModTable

class Loader:


    def __init__(self, buffer: PacketBuffer, table: ModTable):
        self.file_path = self.select_pcap_file()
        self.buffer = buffer
        self.table = table


    def select_pcap_file(self):
        # Open file dialog to select a pcap file
        file_path = filedialog.askopenfilename(
            title="Select a pcap file",
            filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
        )
        if file_path:
            print(f"Selected file: {file_path}")
        else:
            print("No file selected")
        return file_path


    def open_pcap_file(self, handler: callable):
        self.packets = rdpcap(self.file_path)
        for spkt in self.packets:
            handler(spkt)


    # Handlers
    def buffer_and_accept(self, spkt: Packet):
        self.buffer.put(spkt, "in")

        if mb.is_commands(spkt):
            spkt = mb.modify_commands(spkt, self.table)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt, self.table)

        else:
            return
        mb.print_scannable(spkt)
        self.buffer.put(spkt, "out")

    def show_and_accept(self, spkt: Packet):
        spkt.show()