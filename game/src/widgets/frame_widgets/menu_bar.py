from ...app_core.context import Context
from customtkinter import *
from ..popup import message

class MenuBar(CTkFrame):
    '''
    The main Widget for the menu bar.
    Comes with a label and has a button maker.
    Inherits CTkFrame.
    '''

    def __init__(self, master: CTkFrame, context: Context, title_text: str = "Page"):
        self.context = context
        self.style = context.style

        super().__init__(master)
        self.pack(side="top", padx=self.style.gap, pady=self.style.gaptop, fill="x")

        game_label = CTkLabel(self, text=title_text, font=self.style.get_font(), padx=self.style.igap)
        game_label.pack(fill="y", side="left", padx=self.style.gap)

    def add_button(self, text, function=None):
        button = CTkButton(self, text=text, command=function, font=self.style.get_font())
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)

    def quit_button(self):
        self.add_button("Quit", self.context.router.quit)
    
    def refresh_button(self):
        self.add_button("Refresh", self.context.router.refresh)

    def back_button(self):
        self.add_button("Back to Title", self.context.router.go_back)
    
    def toggle_button(self):
        self.add_button("Toggle Theme", self.context.router.mode_toggle)
    
    def theme_button(self):
        self.add_button("Select Theme", self.context.router.select_theme)

    def pcap_button(self):
        self.add_button("Load PCAP File", self.context.net.loader.load_pcap)
    
    def preset_button(self):
        self.add_button("Load Preset", self.context.router.select_preset)
    
    def help_button(self):
        self.add_button("Help", lambda: message(self, self.context, self.context.help_message()))

    def all_buttons(self):
        self.quit_button()
        self.refresh_button()
        self.back_button()
        self.toggle_button()
        self.theme_button()
        self.pcap_button()
        self.preset_button()
        self.help_button()
        