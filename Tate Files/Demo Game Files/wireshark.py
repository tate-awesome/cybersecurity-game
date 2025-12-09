import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scapy.all import sniff, rdpcap, TCP, Raw
import threading

root = tk.Tk()
root.title("Modbus Packet Viewer")
root.geometry("1000x600")

tree = ttk.Treeview(root)
tree.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

modbus_only = tk.BooleanVar(value=True)

# ---- Packet Display ----
def insert_packet(packet):
    """Insert one packet and all its info into the tree."""
    try:
        parent = tree.insert("", "end", text=packet.summary(), open=False)
        for layer in packet.layers():
            layer_obj = packet.getlayer(layer)
            layer_node = tree.insert(parent, "end", text=str(layer), open=False)
            for field_name, field_value in getattr(layer_obj, "fields", {}).items():
                tree.insert(layer_node, "end", text=f"{field_name}: {field_value}")

        # Add raw payload if available
        if Raw in packet:
            raw_data = packet[Raw].load
            hex_dump = " ".join(f"{b:02X}" for b in raw_data)
            tree.insert(parent, "end", text=f"Raw Data: {hex_dump[:120]}{'...' if len(hex_dump)>120 else ''}")
    except Exception as e:
        print("Error inserting packet:", e)

# ---- Modbus Filter ----
def is_modbus_packet(packet):
    """Returns True if the packet likely contains Modbus data."""
    if TCP in packet:
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        if sport == 502 or dport == 502:
            return True
        if Raw in packet:
            data = packet[Raw].load
            # Typical Modbus TCP ADU starts with transaction + protocol ID (4 bytes)
            # Protocol ID = 0x0000 for Modbus
            if len(data) >= 6 and data[2:4] == b"\x00\x00":
                return True
    return False

# ---- Clear Tree ----
def clear_tree():
    for item in tree.get_children():
        tree.delete(item)

# ---- Sniffer ----
def handle_packet(packet):
    if modbus_only.get():
        if is_modbus_packet(packet):
            insert_packet(packet)
    else:
        insert_packet(packet)

def start_sniffing():
    sniff(prn=handle_packet, store=False)

def start_sniffer_thread():
    clear_tree()
    thread = threading.Thread(target=start_sniffing, daemon=True)
    thread.start()

# ---- Load PCAP ----
def load_pcap_file():
    clear_tree()
    file_path = filedialog.askopenfilename(
        title="Open PCAP or PCAPNG File",
        filetypes=[("Packet Capture Files", "*.pcap *.pcapng")]
    )
    if not file_path:
        return
    try:
        packets = rdpcap(file_path)
        count = 0
        for pkt in packets:
            if not modbus_only.get() or is_modbus_packet(pkt):
                insert_packet(pkt)
                count += 1
        messagebox.showinfo("Loaded", f"Displayed {count} Modbus packets from:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{e}")

# ---- Buttons ----
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=5)

start_button = tk.Button(button_frame, text="Start Live Capture", command=start_sniffer_thread)
start_button.pack(side=tk.LEFT, padx=10)

load_button = tk.Button(button_frame, text="Load PCAP/PCAPNG", command=load_pcap_file)
load_button.pack(side=tk.LEFT, padx=10)

filter_checkbox = tk.Checkbutton(button_frame, text="Modbus Only", variable=modbus_only)
filter_checkbox.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear View", command=clear_tree)
clear_button.pack(side=tk.LEFT, padx=10)

quit_button = tk.Button(button_frame, text="Quit", command=root.destroy)
quit_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
