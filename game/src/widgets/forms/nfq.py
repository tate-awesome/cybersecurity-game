from customtkinter import *
from ..style import Style

def mult_offset(style: Style, parent, text_1, text_2, button_text):
    frame = CTkFrame(parent)
    frame.pack(fill=X)
    
    label1 = CTkLabel(frame, text=text_1, font=style.get_font())
    label1.grid(row=0, column=0, sticky="w", pady=5, padx=10)

    entry1 = CTkEntry(frame, width=50)
    entry1.grid(row=1, column=0)

    label2 = CTkLabel(frame, text=text_2, font=style.get_font())
    label2.grid(row=0, column=2, sticky="w", pady=5, padx=10)

    entry2 = CTkEntry(frame, width=50)
    entry2.grid(row=1, column=2)

    button = CTkButton(frame, text=button_text, font=style.get_font())
    button.grid(row=1, column=4)
    def con():
        print("button")
    button.configure(command=con)

    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=0)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=0)

    return entry1, entry2, button





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