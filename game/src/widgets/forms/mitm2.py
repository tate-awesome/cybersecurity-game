from customtkinter import CTkFrame, CTkLabel
from ...app_core.context import Context
from ...network.mod_table import ModTable
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from typing import cast

class Mitm2Form(CTkFrame):
    def __init__(self, master: CTkFrame, context: Context):
        # Assign local references
        self.context = context
        self.buffer = cast(DataBuffer, context.net.data_buffer)
        style = context.style
        
        # Create form
        super().__init__(master, fg_color=style.color("widget"))
        self.pack(side="top", fill="x", expand=False, padx=style.nogap, pady=style.gaptop)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        header = CTkLabel(self, text="MITM Readings", font=style.get_font())
        header.grid(row=0, column=0, columnspan="10", sticky="ew", pady=style.gaptop)
        self.header = header

        # Create value table entries
        self.outgoing_labels = {}
        self.frames = {}
        self.outgoing_labels = {}
        self.incoming_labels = {}
        self.delta_labels = {}
        self.names = {
            "": "",
            "x": "X",
            "y": "Y",
            "theta": "T",
            "speed": "S",
            "rudder": "R"
        }
        r = 1
        w = 90
        for name in ["", "x", "y", "theta", "speed", "rudder"]:
            label = CTkLabel(self, text=f"{self.names[name]}")
            label.grid(row=r, column=0, sticky="ew", pady=style.gaptop, padx=style.gap)
            self.outgoing_labels[name] = label

            incoming = CTkLabel(self, text="0", font=style.get_font("mono"))
            if name == "":
                incoming.configure(text="in")
            incoming.grid(row=r, column=1, pady=style.gaptop, padx=style.gap, sticky="ew")
            self.incoming_labels[name] = incoming

            delta = CTkLabel(self, text="0", width=w, font=style.get_font("mono"))
            if name == "":
                delta.configure(text="delta")
            delta.grid(row=r, column=2, pady=style.gaptop, sticky="ew")
            self.delta_labels[name] = delta

            outgoing = CTkLabel(self, text="0", width=w, font=style.get_font("mono"))
            if name == "":
                outgoing.configure(text="out")
            outgoing.grid(row=r, column=3, pady=style.gaptop, sticky="ew")
            self.outgoing_labels[name] = outgoing

            r = r+1
        self.update()

    def update(self):
        for name in self.names.keys():
            if name == "":
                continue
            in_value = self.buffer.get_latest_value(name,"in")
            out_value = self.buffer.get_latest_value(name,"out")
            delta_value = out_value - in_value
            self.incoming_labels[name].configure(text=f"{in_value:.3f}")
            self.delta_labels[name].configure(text=f"{delta_value:.3f}")
            self.outgoing_labels[name].configure(text=f"{out_value:.3f}")
        self.after(100, self.update)