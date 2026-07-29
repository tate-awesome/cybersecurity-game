from customtkinter import CTkFrame, CTkEntry, CTkLabel, CTkButton
from abc import ABC, abstractmethod
from typing import Callable
from .....app_core.context import Context

class BaseForm(ABC, CTkFrame):
    def __init__(self, master: CTkFrame, context: Context, key: str, attack_noun: str):
        '''
        attack_noun is used like "start sniffer" "start DoS attack" "stopping MITM attack" "ARP Spoofer is running" "MITM attack is on"
        '''

        self.style = context.style
        self.context = context
        self.key = key
        self.attack_noun = attack_noun

        super().__init__(master, fg_color=self.style.color("widget"))

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.current_row = 0


    def add_header(self, text: str):
        self.header = CTkLabel(self, text=text, font=self.style.get_font())
        self.header.grid(row=self.current_row, column=0, columnspan="10", sticky="ew", pady=self.style.gaptop)
        self.current_row += 1