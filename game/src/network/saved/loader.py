from scapy.all import rdpcap
from tkinter.filedialog import askopenfilename
import os, threading, time

from ..buffer import Buffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context

class Loader:

    def __init__(self, buffer: Buffer, context: "Context"):
        self.buffer = buffer
        self.context = context
        self._is_loading = False
        self._lock = threading.Lock()
        
        # FIX: Added an event flag to signal abortion to the background thread
        self.abort_event = threading.Event()
        
        self.file_path = ""
        self.packets = []

    def load_pcap(self):
        '''Loads a pcap file into the buffer.'''
        with self._lock:
            if self._is_loading:
                self.buffer.put("pcap", "Refused to load another pcap file at the same time.")
                return
            self._is_loading = True

        # Clear any previous abort signal before starting a fresh run
        self.abort_event.clear()

        try:
            file_path = self.select_pcap_file()
            if not file_path:
                with self._lock:
                    self._is_loading = False
                return
                
            self.open_pcap_file(file_path)
            
        except Exception as e:
            with self._lock:
                self._is_loading = False
            self.buffer.put("pcap", f"Error during file selection: {str(e)}")

    def select_pcap_file(self):
        self.buffer.put("pcap", "Opening PCAP file dialog...")
        directory = self.context.paths.pcaptures
        filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
        file_path = self.context.paths.select_path(directory, "Select a PCAP file", filetypes)
        if file_path is None:
            self.buffer.put("pcap", "No file selected")
            return ""
        
        self.buffer.put("pcap", f"Selected file: {file_path}")
        return file_path

    def open_pcap_file(self, file_path):
        self.file_path = file_path
        self.buffer.put("pcap", f"Reading packets from {file_path} into memory...")
        
        try:
            self.packets = rdpcap(file_path)
        except Exception as e:
            self.buffer.put("pcap", f"Failed to read PCAP: {str(e)}")
            with self._lock:
                self._is_loading = False
            return

        self.buffer.put("pcap", f"Loaded {len(self.packets)} packets into memory. Starting rate-limiter...")
        
        worker_thread = threading.Thread(target=self.worker, daemon=True)
        worker_thread.start()

    def abort(self):
        '''
        Call this method from your GUI button or controller to stop the process.
        '''
        with self._lock:
            if not self._is_loading:
                self.buffer.put("pcap", "No active PCAP loading process to abort.")
                return
            
            # Signal the worker thread to stop processing immediately
            self.abort_event.set()
            self.buffer.put("pcap", "Abort requested. Stopping loader thread...")

    def worker(self):
        if not self.packets or not self.file_path:
            with self._lock:
                self._is_loading = False
            return

        index = 0
        total_packets = len(self.packets)
        filename = os.path.basename(self.file_path)
        aborted_prematurely = False

        try:
            self.buffer.reset()

            # Rate limiter pumping loop
            while index < total_packets:
                # FIX: Check if abort was requested outside the inner processing loop
                if self.abort_event.is_set():
                    aborted_prematurely = True
                    break

                time.sleep(0.01)
                if self.buffer.capacity() < 0.1:
                    while self.buffer.capacity() < 0.9 and index < total_packets:
                        # FIX: Check if abort was requested INSIDE the processing loop
                        if self.abort_event.is_set():
                            aborted_prematurely = True
                            break

                        spkt = self.packets[index]
                        self.buffer.put("pcap", "Loaded packet", spkt)
                        index += 1

                    if aborted_prematurely:
                        break

            # Final message handling depending on exit conditions
            if aborted_prematurely:
                self.buffer.put("pcap", f"PCAP loading aborted. Processed {index}/{total_packets} packets.")
            else:
                self.buffer.put("pcap", f"Finished loading {total_packets} packets from {filename}")
        except Exception as e:
            # Without this, an uncaught exception here would leave _is_loading
            # stuck True forever, permanently blocking future loads.
            self.buffer.put("pcap", f"Error during PCAP loading: {e}")
        finally:
            # Cleanup and release locks
            self.reset_parameters()
            with self._lock:
                self._is_loading = False

    def reset_parameters(self):
        self.file_path = ""
        self.packets = []