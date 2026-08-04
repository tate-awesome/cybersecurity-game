from scapy.all import rdpcap
from tkinter.filedialog import askopenfilename
import os, threading, time

from ..buffer import Buffer

class Loader:

    def __init__(self, buffer: Buffer):
        self.buffer = buffer
        self.running = False
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
    
    def load_pcap(self):
        '''
        Loads a pcap file into the buffer. Used by networkcontroller
        '''
        if self.running:
            # self.buffer.put("pcap", "Refused to load another pcap file at the same time.")
            return
        file_path = self.select_pcap_file()
        self.open_pcap_file(file_path)

    def select_pcap_file(self):

        # Open file dialog to select a pcap file
        self.buffer.put("pcap", "Opening PCAP file dialog...")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        presets_dir = os.path.join(BASE_DIR, "..", "..", "..", "assets", "captures")
        file_path = askopenfilename(
            initialdir=presets_dir,
            title="Select a pcap file",
            filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
        )
        if file_path == "":
            self.buffer.put("pcap", "No file selected")
            return file_path
        
        self.buffer.put("pcap", f"Selected file: {file_path}")
        return file_path


    def open_pcap_file(self, file_path):
        if not file_path or file_path == "":
            return
        self.running = True
        self.file_path = file_path
        self.buffer.put("pcap", f"Loading packets from {file_path}...")
        self.packets = rdpcap(file_path)
        self.worker_thread.start()

    def stop(self):
        if self.running:
            self.worker_thread.join(timeout=0.0)

    def reset_parameters(self):
        self.file_path = ""
        self.packets = []

    def worker(self):
        if self.packets is None or self.file_path is None:
            return
        index = 0
        while index < len(self.packets):
            if self.buffer.capacity() < 0.1:
                while self.buffer.capacity() < 0.9 and index < len(self.packets):
                    spkt = self.packets[index]
                    self.buffer.put("pcap", "Loaded packet", spkt)
                    index += 1

            time.sleep(0.01)
        self.buffer.put("pcap", f"Finished loading {len(self.packets)} packets from {self.file_path.split("/")[-1]}")
        self.reset_parameters()

            