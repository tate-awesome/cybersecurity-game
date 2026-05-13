from customtkinter import *
from ...network.meta_packet import MetaStatus
from ...network.data_buffer import DataBuffer

class StatusConsole:
    def __init__(self, style, parent, context, buffer):
        self.context = context
        self.style = style
        self.buffer = buffer
         
        menu_frame = self.create_menu_bar(parent)
        #  self.create_filter_boxes(menu_frame)

        pause_button = self.create_menu_button(menu_frame, "Pause")
        self.configure_reversible_button(pause_button, self.pause, self.unpause, "Pause Printing", "Resume Printing")

        jump_button = self.create_menu_button(menu_frame, "Unlock Scrolling")
        self.configure_reversible_button(jump_button, self.unlock_scrolling, self.lock_scrolling, "Disable Jump to Live", "Jump to Live")

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
            status = self.buffer.pop_status()
            if status is None:
                if line_printed:
                    self.text_box.configure(state="normal")
                    self.text_box.insert("end", "\n")
                    self.text_box.configure(state="disabled")
                flag = False
                continue
            # self.text_box.delete("1.0", "end")
            self.text_box.configure(state="normal")
            self.text_box.insert("end", status.get_line() + "\n")
            line_printed = True
            self.text_box.configure(state="disabled")
            if self.jump_to_bottom:
                self.text_box.see("end")
        if self.run:
            self.after_id = self.text_box.after(100, self.print_tick)

    # Text box
    def create_text_box(self, parent):
        textbox = CTkTextbox(parent, wrap="none", font=self.style.get_font("mono"), state="disabled")
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

        header = CTkLabel(frame, text="Hacking Status", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    def create_filter_boxes(self, parent):
        box_slots = self.context.inputs["status_filters"]
        for box_name in box_slots:

            filter_box = CTkCheckBox(parent, text=box_name, font=self.style.get_font())
            filter_box.pack(side="left", pady=self.style.gap, padx=self.style.gap)
            # Load previous input
            value = box_slots[box_name]["state"]
            if value == "1": filter_box.select()
            else: filter_box.deselect()
            # Configure for autosave
            def autosave(slot=box_slots[box_name], b=filter_box):
                slot["state"] = str(b.get())
            def click_action():
                autosave()
                self.update_filters()
                
            filter_box.configure(command=click_action)


    def update_filters(self):
        ...

    def configure_reversible_button(self, the_button: CTkButton, start_func: callable, stop_func: callable, inactive_name: str, active_name: str):
        def stop():
            stop_func()
            the_button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            the_button.configure(command=stop, text=active_name)
        the_button.configure(command=start, text=inactive_name)