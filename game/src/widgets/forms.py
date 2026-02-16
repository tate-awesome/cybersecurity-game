from customtkinter import *
from .style import Style


def bind(callback: callable, button: CTkButton, entries: list[CTkEntry] = None):
    '''
    Bind the callback to pressing enter on the form or clicking the button
    '''
    button.configure(command=callback)
    if entries is None:
        return
    def event_callback(event=None):
        callback()
    for entry in entries:
        entry.bind("<Return>", event_callback)

class NMap:
    def __init__(self, style: Style, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="NMapping", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=1, column=0, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Map Network", font=style.get_font(), command=None)
        button.grid(row=1, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=0)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=0)

    return entry1, entry2, button

def arp(style: Style, parent):

    ip_frame = CTkFrame(parent)
    ip_frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
    ip_frame.columnconfigure(0, weight=0)
    ip_frame.columnconfigure(1, weight=1)
    ip_frame.columnconfigure(2, weight=0)

    ip_frame_header = CTkLabel(ip_frame, text="ARP Spoofing", font=style.get_font())
    ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))

    system_ip_label = CTkLabel(ip_frame, text="System IP:", font=style.get_font())
    system_ip_label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
    system_ip_input = CTkEntry(ip_frame, font=style.get_font())
    system_ip_input.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    controller_ip_label = CTkLabel(ip_frame, text="Controller IP:", font=style.get_font())
    controller_ip_label.grid(row=2, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
    controller_ip_input = CTkEntry(ip_frame, font=style.get_font())
    controller_ip_input.grid(row=2, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    network_sniffing_btn = CTkButton(ip_frame, text="Start ARP Spoof", font=style.get_font(), command=None)
    network_sniffing_btn.grid(row=3, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
    
def nmap(style: Style, parent):
    ip_frame = CTkFrame(parent)
    ip_frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
    ip_frame.columnconfigure(0, weight=0)
    ip_frame.columnconfigure(1, weight=1)
    ip_frame.columnconfigure(2, weight=0)

    ip_frame_header = CTkLabel(ip_frame, text="NMapping", font=style.get_font())
    ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))

    ip_label = CTkLabel(ip_frame, text="Your IP:", font=style.get_font())
    ip_label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)

    ip_input = CTkEntry(ip_frame, font=style.get_font())
    ip_input.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    network_sniffing_btn = CTkButton(ip_frame, text="Map Network", font=style.get_font(), command=None)
    network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=style.GAP, padx=style.GAP)

    return

def sniff(style: Style, parent):
    frame = CTkFrame(parent)
    frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=0)

    label = CTkLabel(frame, text="Traffic Sniffing", font=style.get_font())
    label.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))

    e_label = CTkLabel(frame, text="IP Address:", font=style.get_font())
    e_label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)

    entry = CTkEntry(frame, font=style.get_font())
    entry.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    e_label2 = CTkLabel(frame, text="IP Address:", font=style.get_font())
    e_label2.grid(row=2, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)

    entry2 = CTkEntry(frame, font=style.get_font())
    entry2.grid(row=2, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    button = CTkButton(frame, text="Start sniffing", font=style.get_font(), command=None)
    button.grid(row=3, column=2, sticky="e", pady=style.GAP, padx=style.GAP)

    return

def dos(style: Style, parent):
    ip_frame = CTkFrame(parent)
    ip_frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
    ip_frame.columnconfigure(0, weight=0)
    ip_frame.columnconfigure(1, weight=1)
    ip_frame.columnconfigure(2, weight=0)

    ip_frame_header = CTkLabel(ip_frame, text="Denial of Service", font=style.get_font())
    ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))

    ip_label = CTkLabel(ip_frame, text="Packets per second:", font=style.get_font())
    ip_label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)

    ip_input = CTkEntry(ip_frame, font=style.get_font())
    ip_input.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    network_sniffing_btn = CTkButton(ip_frame, text="Start DoS", font=style.get_font(), command=None)
    network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=style.GAP, padx=style.GAP)

    return

def mitm(style: Style, parent):
    ip_frame = CTkFrame(parent)
    ip_frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
    ip_frame.columnconfigure(0, weight=0)
    ip_frame.columnconfigure(1, weight=1)
    ip_frame.columnconfigure(2, weight=0)

    ip_frame_header = CTkLabel(ip_frame, text="Denial of Service", font=style.get_font())
    ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))

    ip_label = CTkLabel(ip_frame, text="Packets per second:", font=style.get_font())
    ip_label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)

    ip_input = CTkEntry(ip_frame, font=style.get_font())
    ip_input.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)

    network_sniffing_btn = CTkButton(ip_frame, text="Start DoS", font=style.get_font(), command=None)
    network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=style.GAP, padx=style.GAP)

    return