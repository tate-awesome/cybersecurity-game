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

def bind_reversible(widget, start_func: callable, stop_func: callable, func_name: str, start_on):
    button = widget.button
    entries = widget.entries
    status = widget.status

    def configure_on():
        button.configure(command=stop, text=f"Stop {func_name}")
        status.configure(text=f"{func_name} is on")
    def configure_off():
        button.configure(command=start, text=f"Start {func_name}")
        status.configure(text=f"{func_name} is off")
    
    def stop():
        button.configure(text=f"Stopping {func_name}...")
        stop_func()
        configure_off()

    def start():
        button.configure(text=f"Starting {func_name}...")
        start_func()
        configure_on()

    if start_on:
        configure_on()
    else:
        configure_off()

    if entries is None:
        return
    def event_callback(event=None):
        start()
    for entry in entries:
        entry.bind("<Return>", event_callback)

def bind_entries_autosave(entries: list[CTkEntry], save_slots: list[str]):
    for entry, slot_index in zip(entries, range(len(save_slots))):
        def autosave(event=None, e=entry, idx=slot_index):
            save_slots[idx] = e.get()
            print(e.get())
        entry.bind("<KeyRelease>", autosave)

def load_saved_entries(entries: list[CTkEntry], save_slots: list[str]):
    for i in range(len(entries)):
        entries[i].delete(0, "end")
        entries[i].insert(0, save_slots[i])

def bind_options_autosave(options: list[CTkOptionMenu], save_slots: list[str]):
    """
    Binds a callback to all CTkOptionMenus that saves the selected option to the
    corresponding save slot whenever an option is selected.
    """
    for option, idx in zip(options, range(len(save_slots))):
        def autosave(selected_value, i=idx):
            save_slots[i] = selected_value
            print(f"Saved option {i}: {save_slots[i]}")
        
        option.configure(command=autosave)

def load_saved_options(options: list[CTkOptionMenu], save_slots: list[str]):
    """
    Sets the selected option of each CTkOptionMenu to the corresponding string
    from the save slot.
    """
    for option, value in zip(options, save_slots):
        if value in option._values:  # make sure it's a valid option
            option.set(value)

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
        status.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Map Network", font=style.get_font(), command=None)
        button.grid(row=1, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

class ARP:
    def __init__(self, style: Style, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="ARP Spoofing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        label1 = CTkLabel(frame, text="Target IP:", font=style.get_font())
        label1.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label1 = label1

        entry1 = CTkEntry(frame, font=style.get_font())
        entry1.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.entry1 = entry1

        label2 = CTkLabel(frame, text="Host IP:", font=style.get_font())
        label2.grid(row=2, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label2 = label2

        entry2 = CTkEntry(frame, font=style.get_font())
        entry2.grid(row=2, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.entry2 = entry2

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=3, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Start ARP Spoof", font=style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

        self.entries = [entry1, entry2]


class Sniff:
    def __init__(self, style: Style, parent, options: list[str]):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="Traffic Sniffing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        label = CTkLabel(frame, text="Packet Handler:", font=style.get_font())
        label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label = label

        option = CTkOptionMenu(frame, font=style.get_font(), values=options)
        option.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.option = option

        button = CTkButton(frame, text="Start sniffing", font=style.get_font(), command=None)
        button.grid(row=2, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

        self.options = [option]

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