import tkinter as tk
from tkinter import ttk, filedialog
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether


class PcapViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Wireshark Demo")
        self.geometry("1100x700")

        self.packets = []

        self.create_menu()
        self.create_filter_bar()
        self.create_layout()

    # ------------------------
    # UI SETUP
    # ------------------------

    def create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open PCAP/PCAPNG", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        menubar.add_cascade(label="File", menu=file_menu)
        
        self.config(menu=menubar)

    def create_filter_bar(self):
        frame = tk.Frame(self)
        frame.pack(fill="x")

        tk.Label(frame, text="Filter: ").pack(side="left", padx=5)

        self.filter_entry = tk.Entry(frame)
        self.filter_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.filter_entry.bind("<Return>", self.apply_filter)

    def create_layout(self):
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(fill="both", expand=True)

        # Packet list
        columns = ("No", "Time", "Source", "Destination", "Protocol", "Length", "Info")
        self.tree = ttk.Treeview(paned, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        # Packet details
        self.detail_text = tk.Text(paned, height=15)

        paned.add(self.tree)
        paned.add(self.detail_text)

    # ------------------------
    # FILE LOADING
    # ------------------------

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("PCAP files", "*.pcap *.pcapng")]
        )

        if not filepath:
            return

        self.packets = rdpcap(filepath)
        self.populate_table(self.packets)

    # ------------------------
    # TABLE POPULATION
    # ------------------------

    def populate_table(self, packets):
        self.tree.delete(*self.tree.get_children())

        for i, pkt in enumerate(packets):
            time = f"{pkt.time:.6f}" if hasattr(pkt, "time") else "N/A"
            length = len(pkt)

            src = dst = proto = info = ""

            if pkt.haslayer(IP):
                src = pkt[IP].src
                dst = pkt[IP].dst
                proto = pkt[IP].proto

            if pkt.haslayer(TCP):
                proto = "TCP"
                info = f"{pkt[TCP].sport} → {pkt[TCP].dport}"
            elif pkt.haslayer(UDP):
                proto = "UDP"
                info = f"{pkt[UDP].sport} → {pkt[UDP].dport}"
            elif pkt.haslayer(Ether):
                proto = "Ethernet"
                src = pkt[Ether].src
                dst = pkt[Ether].dst

            self.tree.insert(
                "",
                "end",
                iid=str(i),
                values=(i + 1, time, src, dst, proto, length, info),
            )

    # ------------------------
    # FILTERING
    # ------------------------

    def apply_filter(self, event=None):
        query = self.filter_entry.get().lower()

        filtered = []

        for pkt in self.packets:
            summary = pkt.summary().lower()
            if query in summary:
                filtered.append(pkt)

        self.populate_table(filtered)

    # ------------------------
    # DETAIL VIEW
    # ------------------------

    def show_details(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        index = int(selected[0])
        pkt = self.packets[index]

        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, pkt.show(dump=True))


if __name__ == "__main__":
    app = PcapViewer()
    app.mainloop()