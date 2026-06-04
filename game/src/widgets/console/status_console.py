from customtkinter import *
from ...network.meta_packet import MetaStatus
from ...network.data_buffer import DataBuffer
from typing import cast

class StatusConsole:
    def __init__(self, style, parent, context, buffer: DataBuffer):
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

        # Reset print pointer on refresh
        self.buffer.reset_status_cursor()

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
        '''
        Prints new status lines to the text box, then sets a timer to call itself again after 100 ms.
        The buffer's getter returns all new lines since the last print, so we don't need to loop.
        Empty lines go after every cluster of statuses
        '''
        # Get new lines
        statuses = self.buffer.get_new_statuses()
        if len(statuses) == 0:
            # Don't print
            ...
        else:
            # Do print
            status_strings = [str(status) for status in statuses]
            text_block = "\n".join(status_strings) + "\n\n"
            
            # Add to text box
            self.text_box.configure(state="normal")
            self.text_box.insert("end", text_block)
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


    def configure_reversible_button(self, the_button: CTkButton, start_func: callable, stop_func: callable, inactive_name: str, active_name: str):
        def stop():
            stop_func()
            the_button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            the_button.configure(command=stop, text=active_name)
        the_button.configure(command=start, text=inactive_name)