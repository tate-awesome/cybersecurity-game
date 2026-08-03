from customtkinter import CTkTextbox
from ....network.meta_packet import MetaStatus
from ....app_core.context import Context
from typing import cast
from ... import MenuBar
from ..panel import Panel

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "Status Console")

        self.buffer = context.net.buffer.status

        self.text_box = self.create_text_box(self)

        # minimize_button = self.menu_bar.minimize_button(self.text_box, master)

        pause_button = self.menu_bar.reversible_button(self.pause, self.unpause, "Pause", "Resume")

        jump_button = self.menu_bar.reversible_button(self.unlock_scrolling, self.lock_scrolling, "Scroll Freely", "Jump to Live")

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Reset print pointer on refresh
        self.buffer.reset_cursor()

        # Start printing loop
        self.start_printing()
        

    def start_printing(self):
        self.run = True
        self.context.animation_manager.add_callback("status_console", self.print_tick)
    
    def stop_printing(self):
        self.run = False
        self.context.animation_manager.remove_callback("status_console")

    def print_tick(self):
        '''
        Prints new status lines to the text box, then sets a timer to call itself again after 100 ms.
        The buffer's getter returns all new lines since the last print, so we don't need to loop.
        Empty lines go after every cluster of statuses
        '''
        text_block = self.buffer.get_new_lines()
        
        # Add to text box
        self.text_box.configure(state="normal")
        self.text_box.insert("end", text_block)
        self.text_box.configure(state="disabled")

        if self.jump_to_bottom:
            self.text_box.see("end")

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