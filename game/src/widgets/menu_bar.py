from ..app_core.context import Context
from customtkinter import *
from .popup import message

class MenuBar:

    def __init__(self, parent, context: Context, title):
        router = context.router
        root = context.root
        style = context.style
        self.style = context.style
        self.frame = self.bar(root, "Attacker Version 0")
        self.button("Quit", router.quit)
        self.button("Refresh", router.refresh)
        self.button("Back to Title", router.go_back)
        self.button("Toggle Theme", router.mode_toggle)
        self.button("Select Theme", router.select_theme)
        cb = self.button("Customize", None)
        if context.net is not None:
            self.button("Load PCAP File", context.net.loader.load_pcap)
        self.button("Load Preset", router.select_preset)
        self.button("Help", lambda: message(root, context, context.help_message()))


    def bar(self, parent, title):
        med = self.style.get_font()
        menu_bar = CTkFrame(parent)
        menu_bar.pack(side="top", padx=self.style.gap, pady=self.style.gaptop, fill="x", anchor="n")
        game_label = CTkLabel(master = menu_bar, text=title, font=med, padx=self.style.igap)
        game_label.pack(fill=Y, side="left", padx=self.style.gap)
        return menu_bar


    def button(self, text, function=None):
        med = self.style.get_font()
        button = CTkButton(self.frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

        