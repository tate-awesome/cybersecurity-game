from customtkinter import *
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from .filter_overlay import FilterOverlay

class PacketConsole:
    def __init__(self, style, parent, context, buffer: DataBuffer):
        self.context = context
        self.style = style
        self.buffer = buffer

        menu_frame = self.create_menu_bar(parent)
        #  self.create_filter_boxes(menu_frame)

        jump_button = self.create_menu_button(menu_frame, "Unlock Scrolling")
        self.configure_reversible_button(jump_button, self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")

        filter_button = self.create_menu_button(menu_frame, "Filters")
        filter_overlay = FilterOverlay(self.context, self.style, filter_button, buffer)

        self.text_box = self.create_text_box(parent)

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Start printing loop
        self.start_printing()
        

    def start_printing(self):
        print("start")
        self.run = True
        self.print_tick()
    
    def stop_printing(self):
        print("stop")
        self.run = False
        if self.after_id:
            self.text_box.after_cancel(self.after_id)
            self.after_id = None

    def print_tick(self):
        flag = True
        line_printed = False
        while flag:
            status = self.buffer.pop_packet(self.context.inputs["packet_filter_function"]["function"])
            if status is None:
                if line_printed:
                    self.text_box.configure(state="normal")
                    self.text_box.insert("end", "\n")
                    self.text_box.configure(state="disabled")
                flag = False
                continue
            # self.text_box.delete("1.0", "end")
            self.text_box.configure(state="normal")
            self.text_box.insert("end", status.get_info() + "\n")
            line_printed = True
            self.text_box.configure(state="disabled")
            if self.jump_to_bottom:
                self.text_box.see("end")
        if self.run:
            self.after_id = self.text_box.after(100, self.print_tick)

    # Text box
    def create_text_box(self, parent):
        textbox = CTkTextbox(parent, wrap="none", font=("Consolas", 16), state="disabled")
        textbox.pack(side="top", fill="both", expand=True, padx=self.style.gap, pady=self.style.gap)
        return textbox

    # Buttons
    def pause(self):
        self.stop_printing()

    def unpause(self):
        self.start_printing()
    
    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True

    # Menu Bar

    def create_menu_bar(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", pady=self.style.gaptop, padx=self.style.gap)

        header = CTkLabel(frame, text="Packet Stream", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    def configure_reversible_button(self, the_button: CTkButton, start_func: callable, stop_func: callable, inactive_name: str, active_name: str):
        def stop():
            stop_func()
            the_button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            the_button.configure(command=stop, text=active_name)
        the_button.configure(command=start, text=inactive_name)