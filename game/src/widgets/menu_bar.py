from .style import Style
from customtkinter import *
from . import popup

class MenuBar:

    def __init__(self, style, parent, title, context):
        router = context.router
        root = context.root
        self.style = style
        self.frame = self.bar(style, root, "Attacker Version 0")
        self.button("Quit", router.quit)
        self.button("Refresh", router.refresh)
        self.button("Toggle Theme", router.mode_toggle)
        self.button("Select Theme", router.select_theme)
        self.button("Help", lambda:popup.open(style,root,context.help_message()))


    def bar(self, style: Style, parent, title):
        med = style.get_font()
        menu_bar = CTkFrame(parent)
        menu_bar.pack(side="top", padx=style.gap, pady=style.gaptop, fill="x", anchor="n")
        game_label = CTkLabel(master = menu_bar, text=title, font=med, padx=style.igap)
        game_label.pack(fill=Y, side="left", padx=style.gap)
        return menu_bar


    def button(self, text, function=None):
        med = self.style.get_font()
        button = CTkButton(self.frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

        