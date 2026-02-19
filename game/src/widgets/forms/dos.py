from customtkinter import *
from ..style import Style

class DOS:
    def __init__(self, style: Style, parent: CTkBaseClass):
        ...

def dos(style: Style, parent):
    ip_frame = CTkFrame(parent)
    ip_frame.pack(side="top", fill="x", expand=False, padx=style.gap, pady=style.gaptop)
    ip_frame.columnconfigure(0, weight=0)
    ip_frame.columnconfigure(1, weight=1)
    ip_frame.columnconfigure(2, weight=0)

    ip_frame_header = CTkLabel(ip_frame, text="Denial of Service", font=style.get_font())
    ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=style.gaptop)

    ip_label = CTkLabel(ip_frame, text="Packets per second:", font=style.get_font())
    ip_label.grid(row=1, column=1, sticky="w", pady=style.gaptop, padx=style.gap)

    ip_input = CTkEntry(ip_frame, font=style.get_font())
    ip_input.grid(row=1, column=2, sticky="e", pady=style.gaptop, padx=style.gap)

    network_sniffing_btn = CTkButton(ip_frame, text="Start DoS", font=style.get_font(), command=None)
    network_sniffing_btn.grid(row=2, column=2, sticky="e", pady=style.gap, padx=style.gap)

    return