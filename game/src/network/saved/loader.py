from tkinter import filedialog
from scapy.packet import Packet
from scapy.all import rdpcap

from ..data_buffer import DataBuffer
from .. import modbus_util as mb
from ..mod_table import ModTable

class Loader:


    def __init__(self, buffer: DataBuffer):
        self.buffer = buffer

    
    def load_pcap(self):
        '''
        Loads a pcap file into the buffer. Used by networkcontroller
        '''
        file_path = self.select_pcap_file()
        self.open_pcap_file(file_path)
        


        


    def select_pcap_file(self):
        # Open file dialog to select a pcap file
        self.buffer.put("pcap", "Opening PCAP file dialog...")
        file_path = filedialog.askopenfilename(
            title="Select a pcap file",
            filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
        )
        if file_path:
            self.buffer.put("pcap", f"Selected file: {file_path}")
        else:
            self.buffer.put("pcap", "No file selected")
        return file_path


    def open_pcap_file(self, file_path):
        if not file_path:
            return
        self.buffer.put("pcap", f"Loading packets from {file_path}...")
        self.packets = rdpcap(file_path)
        for spkt in self.packets:
            self.buffer.put("pcap", "Loaded packet", spkt)

        self.buffer.put("pcap", f"Finished loading {len(self.packets)} packets from {file_path}")

