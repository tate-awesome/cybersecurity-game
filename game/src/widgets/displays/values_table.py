from customtkinter import *
from ..style import Style


class ValuesTable:
    
    def __init__(self, style: Style, parent, context):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = context.net.data_buffer

        frame = CTkFrame(parent, fg_color=style.color("panel"))
        frame.pack(fill="both",side="left", expand=False, padx=style.cgap, pady=style.cgap)


        self.labels = {}
        self.frames = {}
        self.outgoing_values = {}
        self.incoming_values = {}
        self.delta_values = {}
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
            label = CTkLabel(frame, text=f"{self.names[name]}", anchor="w")
            label.grid(row=r, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
            self.labels[name] = label

            incoming = CTkLabel(frame, text="0", font=style.get_font("mono"))
            if name == "":
                incoming.configure(text="in")
            incoming.grid(row=r, column=2, pady=style.gaptop, padx=style.gap, sticky="ew")
            self.incoming_values[name] = incoming

            delta = CTkLabel(frame, text="0", width=w, font=style.get_font("mono"))
            if name == "":
                delta.configure(text="delta")
            delta.grid(row=r, column=3, pady=style.gaptop, sticky="ew")
            self.delta_values[name] = delta


            outgoing = CTkLabel(frame, text="0", width=w, font=style.get_font("mono"))
            if name == "":
                outgoing.configure(text="out")
            outgoing.grid(row=r, column=4, pady=style.gaptop, sticky="ew")
            self.outgoing_values[name] = outgoing

            r = r+1
        self.update()

    def update(self):
        for name in self.names.keys():
            if name == "":
                continue
            in_value = self.buffer.get_latest_value(name,"in")
            out_value = self.buffer.get_latest_value(name,"out")
            delta_value = in_value - out_value
            self.incoming_values[name].configure(text=f"{in_value:.3f}")
            self.delta_values[name].configure(text=f"{delta_value:.3f}")
            self.outgoing_values[name].configure(text=f"{out_value:.3f}")
        self.parent.after(100, self.update)